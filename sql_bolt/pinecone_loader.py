import os

from dotenv import load_dotenv
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore

load_dotenv()

# initialize Pinecone client
index_name = "sql-bolt"
embedding = OpenAIEmbeddings(
    model='text-embedding-3-small',
    api_key=os.getenv('OPENAI_API_KEY'),
)
vectorstore = PineconeVectorStore(
    embedding=embedding,
    index_name=index_name,
    pinecone_api_key=os.getenv('PINECONE_API_KEY'),
)


class CustomLoader:
    v2_query = """
    WITH
    TableDescription AS (
    SELECT
        table_schema,
        table_name,
        option_value table_description
    FROM
        chinook.INFORMATION_SCHEMA.TABLE_OPTIONS
    WHERE
        option_name = 'description'),
    ColumnDescription AS (  
    SELECT
        table_schema,
        table_name,
        column_name,
        data_type,
        description
    FROM
        chinook.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS)
    SELECT
    *
    FROM
    TableDescription
    JOIN
    ColumnDescription
    USING
    (table_schema,
        table_name)
    """
    v1_table_id = 'sigma-kayak-430300-a2.chinook._v1_metadata'

    def __init__(self) -> None:
        self.bq_client = bigquery.Client()
        self.v2 = None
        self.v1 = None
        self.delete_set = None
        self.upsert_set = None

    def load_v2(self):
        query_job = self.bq_client.query(self.v2_query)  # API request
        rows = query_job.result()  # Waits for query to finish
        df = rows.to_dataframe()
        df['id'] = df[['table_schema', 'table_name', 'column_name']].apply('.'.join, axis=1)
        df['table_description'] = df['table_description'].str.strip('"')
        self.v2 = df

    def check_v1(self):
        try:
            self.bq_client.get_table(self.v1_table_id)  # Make an API request.
        except NotFound:
            return False
        else:
            return True

    def fetch_v1(self):
        query = f"SELECT * FROM {self.v1_table_id}"
        query_job = self.bq_client.query(query)  # API request
        rows = query_job.result()  # Waits for query to finish
        self.v1 = rows.to_dataframe()

    def operation(self):
        if self.v1 is not None:
            self.delete_set = set(self.v1['id']) - set(self.v2['id'])
        else:
            self.delete_set = set()
        self.upsert_set = set(self.v2['id'])

    def delete_pinecone(self):
        return vectorstore.delete(ids=list(self.delete_set))

    def upsert_pinecone(self):
        metadatas = self.v2.to_dict(orient='records')
        texts = [
            '\n'.join(f'{k}: {v}' for k, v in d.items())
            for d in metadatas
        ]
        return vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=list(self.upsert_set),
        )

    def overwrite_v2(self):
        """
        migration.py의 load_job을 참고하여 v2 테이블에 데이터를 덮어씁니다.
        """
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            write_disposition="WRITE_TRUNCATE",
        )
        job = self.bq_client.load_table_from_dataframe(
            self.v2,
            self.v1_table_id,
            job_config=job_config
        )
        return job.result()


if __name__ == '__main__':
    loader = CustomLoader()
    loader.load_v2()
    if loader.check_v1():
        loader.fetch_v1()
    
    loader.operation()
    loader.delete_pinecone()
    loader.upsert_pinecone()
    loader.overwrite_v2()
