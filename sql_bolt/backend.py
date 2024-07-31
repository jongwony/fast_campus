import os
from typing import List, Set
from operator import itemgetter

import pandas as pd
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.sql_database.prompt import SQL_PROMPTS
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
data_catalog_df: pd.DataFrame = loader.v1

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


def generate(tables: Set[str]):
    queries = []
    for table in tables:
        table_schema, table_name, table_description = table
        columns = get_data_catalog_columns_map(table_schema, table_name)
        ddl = generate_create_table_query(
            table_schema,
            table_name,
            columns,
            table_comment=table_description,
        )
        queries.append(ddl)
    return '\n\n'.join(queries)


def sql_chain():
    """
    https://python.langchain.com/v0.2/docs/how_to/prompts_composition/
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": 16})

    # prompt를 직접 커스텀하여 사용할 수 있습니다.
    with open("user_prompt.md") as f:
        user_prompt = f.read()
    prompt = ChatPromptTemplate.from_messages([
        ("placeholder", "{history}"),
        ("human", user_prompt),
    ])

    # # ChatPromptTemplate과 PromptTemplate을 합성하여 사용하는 방법입니다.
    # prompt = ChatPromptTemplate.from_messages([
    #     ("placeholder", "{history}"),
    # ]) + HumanMessagePromptTemplate(
    #     prompt=[SQL_PROMPTS['googlesql']]
    # )

    parser = StrOutputParser()

    def conversations(x):
        history = '\n'.join(
            k[1] for k in x['history']
            if isinstance(k[1], str)
        )
        question = x['question']
        return f'{history}\n{question}'

    def top_k(x):
        return 10

    return {
        'top_k': top_k,
        'table_info': conversations | retriever | group_by_table | generate,
        'input': RunnablePassthrough() | itemgetter('question'),
        'history': RunnablePassthrough() | itemgetter('history'),
    } | prompt | model | parser


if __name__ == '__main__':
    # template = SQL_PROMPTS['googlesql']
    # template.get_prompts()[0].pretty_print()

    # template.invoke(
    #     top_k=10,
    #     table_info=generate_create_table_query(...),
    #     question='음악 장르별 판매량을 조회하려고 합니다',
    # )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 16})
    rag_response = retriever.invoke('음악 장르별 판매량을 조회하려고 합니다')

    # mytable 테스트
    mytable = get_data_catalog_columns_map('chinook', 'mytable')

    # retrieve된 문서를 테이블별로 그룹핑 테스트
    groups = group_by_table(rag_response)

    # 테이블별 DDL 생성 테스트
    table_info = generate(groups)

    # SQL 체인 테스트
    response = sql_chain().invoke({
        'history': [
            ('human', '음악 장르별로 판매량 데이터를 조회하려고 합니다.'),
        ],
        'question': '위의 내용을 바탕으로 쿼리를 작성해 주세요',
    })

    # response = sql_chain().invoke({
    #     'history': [],
    #     'question': '음악 장르별로 판매량 데이터를 조회하려고 합니다.',
    # })
