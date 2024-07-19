
"""
https://python.langchain.com/v0.2/docs/integrations/vectorstores/pinecone/
"""
import os
from glob import glob

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters.html import HTMLSectionSplitter
from langchain_pinecone.vectorstores import PineconeVectorStore

from confluence import CustomConfluence


load_dotenv()

# initialize Pinecone client
index_name = "onboard-bolt"
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
    def __init__(self) -> None:
        self.client = CustomConfluence(
            url='https://productivitysolutionsinc.atlassian.net',
            username='fc.jongwony@gmail.com',
            password=os.getenv('ATLASSIAN_API_KEY'),
            cloud=True,
        ) 

    def _dump(self):
        """
        *강사용*
        confluence에서 docs 데이터를 가져와서 저장
        """
        for content in self.client.get_all_page_content('PH'):
            with open(os.path.join('docs', f'{content["title"]}.html'), 'w') as f:
                f.write(content['body'])

    def load(self):
        """
        *수강생용*
        docs 데이터를 confluence로 로드
        """
        for file in glob(os.path.join('docs', '*.html')):
            with open(file, 'r') as f:
                print(file)
                title = file.removeprefix('docs/').removesuffix('.html')
                self.client.create_page('PH', title, f.read()) 

    def bootstrap(self):
        """
        confluence에서 docs 데이터를 가져와서 vectorstore에 저장
        """
        headers_to_split_on = [
            ("h1", "header"),
            ("h2", "sub_header"),
        ]
        
        documents = []
        for content in self.client.get_all_page_content('PH'):
            html_splitter = HTMLSectionSplitter(
                headers_to_split_on,
                chunk_size=10,
                chunk_overlap=0,
            )
            html_header_splits = html_splitter.split_text(content['body'])
            # body 제거 후 metadata로 옮김
            _ = content.pop('body')
            for i, doc in enumerate(html_header_splits):
                content['insert_id'] = f'{content["id"]}_{i}'
                doc.metadata |= content
            documents += html_header_splits

        return documents


if __name__ == '__main__':
    # loader 코드는 1회만 실행합니다.
    loader = CustomLoader()
    # 아래 코드로 docs 디렉터리 데이터를 confluence로 로드합니다.
    # loader.load()

    # 로드된 데이터를 가져와서 vectorstore에 저장합니다.
    # docs = loader.bootstrap()
    # response = vectorstore.add_documents(
    #     documents=docs,
    #     ids=[doc.metadata['insert_id'] for doc in docs],
    # )

    ############################

    # vectorstore에 저장된 데이터를 검색합니다.

    # 방법 1. similarity_search 메서드 사용
    # vectorstore.similarity_search('육아 휴직 신청 방법을 알려주세요.', k=5)

    # 방법 2. as_retriever LCEL 사용
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    response = retriever.invoke('육아 휴직 신청 방법을 알려주세요.')
