"""
confluence.get_all_spaces()
# PH정보 얻음(혹은 UI로 프로젝트 생성시 얻은 정보)
confluence.get_all_pages_from_space('PH')

confluence.get_space_content('PH')
"""
import os

import jmespath
from atlassian import Confluence
from dotenv import load_dotenv

load_dotenv()


class CustomConfluence(Confluence):
    def get_all_page_content(self, page_key='PH'):
        expr = '{id: id, title: title, type: type, status: status, body: body.storage.value, link: _links.webui}'
        for x in self.get_space_content(page_key)['page']['results']:
            content = jmespath.search(expr, x)
            # https://productivitysolutionsinc.atlassian.net/wiki + _links.webui
            content['link'] = 'https://productivitysolutionsinc.atlassian.net/wiki' + content['link']
            yield content


if __name__ == '__main__':
    client = CustomConfluence(
        url='https://productivitysolutionsinc.atlassian.net',
        username='fc.jongwony@gmail.com',
        password=os.getenv('ATLASSIAN_API_KEY'),
        cloud=True,
    )
    for x in client.get_all_page_content():
        print(x)
