import os
from typing import List, Set
from operator import itemgetter

from langchain_openai.chat_models.base import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain.chains.sql_database.prompt import SQL_PROMPTS
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.documents.base import Document
from dotenv import load_dotenv

from pinecone_loader import CustomLoader, vectorstore
from schema import generate_create_table_query

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

"""
마지막 저장된 빅쿼리 데이터 카탈로그를 전역변수로 저장
"""
loader = CustomLoader()
loader.fetch_v1()
data_catalog_df = loader.v1

data_catalog_table = data_catalog_df.set_index(
    ['table_schema', 'table_name']
)['table_description'].to_dict()


def get_data_catalog_columns_map(table_schema, table_name):
    return data_catalog_df[
        (data_catalog_df['table_schema'] == table_schema)
        & (data_catalog_df['table_name'] == table_name)
    ].to_dict(orient='records')


def group_by_table(docs: List[Document]) -> Set:
    return set((
        doc.metadata['table_schema'],
        doc.metadata['table_name'],
        doc.metadata['table_description'],
    ) for doc in docs)


def generate(table: set[tuple]) -> str:
    queries = []
    for table_schema, table_name, table_description in table:
        ddl = generate_create_table_query(
            table_schema,
            table_name,
            get_data_catalog_columns_map(table_schema, table_name),
            table_description=table_description,
        )
        queries.append(ddl)
    return '\n\n'.join(queries)


def sql_chain():
    """
    https://python.langchain.com/v0.2/docs/how_to/prompts_composition/
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": 16})

    with open('system_prompt.md') as f, open('user_prompt.md') as g:
        system_prompt = f.read()
        user_prompt = g.read()
    prompt = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('placeholder', '{history}'),
        ('human', user_prompt),
    ])

    # # ChatPromptTemplate과 PromptTemplate을 합성하여 사용하는 방법입니다.
    # prompt = ChatPromptTemplate.from_messages([
    #     ("placeholder", "{history}"),
    # ]) + HumanMessagePromptTemplate(
    #     prompt=[SQL_PROMPTS['googlesql']]
    # )

    parser = StrOutputParser()

    def conversations(d: dict) -> str:
        history = '\n'.join(msg for _, msg in d['history'] if isinstance(msg, str))
        question = d['question']
        return f'{history}\n{question}'

    def top_k(x) -> int:
        return 10

    return {
        'top_k': top_k,
        'table_info': conversations | retriever | group_by_table | generate,
        'input': RunnablePassthrough() | itemgetter('question'),
        'history': RunnablePassthrough() | itemgetter('history'),
    } | prompt | model | parser


if __name__ == '__main__':
    template = SQL_PROMPTS['googlesql']
    template.get_prompts()[0].pretty_print()

    # template.invoke(
    #     top_k=10,
    #     table_info=generate_create_table_query(...),
    #     question='음악 장르별 판매량을 조회하려고 합니다',
    # )

    # retrieve된 문서를 테이블별로 그룹핑 테스트
    # retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
    # response = retriever.invoke('음악 장르별 판매량을 조회해 주세요')
    # grouped = group_by_table(response)

    # SQL 체인 테스트
    # response = sql_chain().invoke({
    #     'history': [],
    #     'question': '음악 장르별로 판매량 데이터를 조회하려고 합니다.',
    # })
    response = sql_chain().invoke(
        {
            'question': '@Secretary 위 데이터를 조회해 주세요',
            'history': [('human', '음악 장르별 판매량을 조회해 주세요')],
        }
    )
