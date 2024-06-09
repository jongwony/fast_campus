"""
https://python.langchain.com/v0.2/docs/integrations/vectorstores/pinecone/
"""
import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders.csv_loader import CSVLoader

load_dotenv()

# initialize Pinecone client
index_name = "wine-pairing"
embedding = OpenAIEmbeddings(
    model='text-embedding-3-small',
    api_key=os.getenv('OPENAI_API_KEY'),
)
vectorstore = PineconeVectorStore(
    embedding=embedding,
    index_name=index_name,
    pinecone_api_key=os.getenv('PINECONE_API_KEY'),
)


def bootstrap_wines():
    loader = CSVLoader(file_path='winemag-data-130k-v2.csv')
    data = loader.load()
    return vectorstore.add_documents(data)


def wine_search(query):
    return vectorstore.similarity_search_with_relevance_scores(query)


if __name__ == '__main__':
    bootstrap_wines()