
"""
https://python.langchain.com/v0.2/docs/how_to/extraction_parse/
"""
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from retrieval import vectorstore


load_dotenv()

model = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)


def onboard():
    with open("system_prompt.md") as f:
        system_prompt = f.read()

    def format_documents(docs):
        format_doc = '\n\n---\n\n'.join([
            f'Title: {doc.metadata["title"]}\n'
            f'Sub Title: {doc.metadata.get("sub_header", "")}\n' 
            f'Page Content: """{doc.page_content}"""\n'
            f'Source Link: {doc.metadata["link"]}'
            for doc in docs
        ])
        return format_doc

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    prompt = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('user', 'Please provide an answer to the question and a link to the document source.\n'
                 'question: """{query}"""')

    ])
    parser = StrOutputParser()

    return {
        'documents': retriever | format_documents,
        'query': RunnablePassthrough()
    } | prompt | model | parser


if __name__ == "__main__":
    response = onboard().invoke('육아 휴직 신청 방법을 알려주세요.')
