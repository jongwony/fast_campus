import os

from atlassian import Jira
from dotenv import load_dotenv

load_dotenv()


class CustomJira(Jira):
    """
    self.get_all_custom_fields() 로 custom field id 를 찾아서 사용할 수 있음
    """
    fields = None

    def __init__(self):
        super().__init__(
            url='https://productivitysolutionsinc.atlassian.net',
            username='fc.jongwony@gmail.com',
            password=os.getenv('ATLASSIAN_API_KEY'),
            cloud=True,
        )

    def create_issue(self):
        """
        Python 3.12 부터는 override 라는 데코레이터가 있다
        https://docs.python.org/3/whatsnew/3.12.html#pep-698-override-decorator-for-static-typing
        """
        return super().create_issue(self.fields)

    def set_fields(self, fields: dict):
        self.fields = fields

    def task_fields(self, summary: str, description: str):
        return {
            'project': {'key': 'KAN'},
            'issuetype': {'name': '작업'},
            'summary': summary,
            'description': description,
        }

    def bug_fields(self, summary: str, description: str, stage: str):
        return {
            'project': {'key': 'KAN'},
            'issuetype': {'name': '버그'},
            'summary': summary,
            'description': description,
            'customfield_10033': {'value': stage},
        }


if __name__ == '__main__':
    jira = CustomJira()
    # jira.get_all_custom_fields()
    # fields = jira.task_fields('테스트', '테스트')
    fields = jira.bug_fields('테스트', '테스트', 'dev')
    jira.set_fields(fields)
    response = jira.create_issue()
    print(response)