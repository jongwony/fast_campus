"""
먼저 아래 코드를 실행해야 합니다.

sqlite3 Chinook.db
.read Chinook_Sqlite.sql
SELECT * FROM Artist LIMIT 10;
"""
import pandas as pd
from google.cloud import bigquery
from langchain_community.utilities import SQLDatabase

from dotenv import load_dotenv


load_dotenv()

uri = "sqlite:///Chinook.db"
db = SQLDatabase.from_uri(uri, sample_rows_in_table_info=3)
print(db.dialect)
print(db.get_usable_table_names())
print(db.run("SELECT * FROM Artist LIMIT 10;"))
print(db.dialect)
print(db.get_usable_table_names())
# print(db.get_context())

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"
job_config = bigquery.LoadJobConfig(
    # Specify a (partial) schema. All columns are always written to the
    # table. The schema is used to assist in data type definitions.
    autodetect=True,
    # Optionally, set the write disposition. BigQuery appends loaded rows
    # to an existing table by default, but with WRITE_TRUNCATE write
    # disposition it replaces the table with the loaded data.
    write_disposition="WRITE_TRUNCATE",
)

project_id = 'sigma-kayak-430300-a2'
dataset = 'chinook'
for table_name in db.get_usable_table_names():
    table_id = f"{project_id}.{dataset}.{table_name}"
    dataframe = pd.read_sql_table(table_name=table_name, con=uri)
    print(f"Loading {table_name} to {table_id}")
    job = client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )  # Make an API request.
    job.result()  # Wait for the job to complete.
