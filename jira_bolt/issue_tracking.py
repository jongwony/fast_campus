from typing import Union

from atlassian import Jira

from issue_schema import TaskIssue, BugIssue


class CustomJira(Jira):
    fields = None

    def create_issue(self, update_history=False, update=None):
        """
        Python 3.12 부터는 override 라는 데코레이터가 있다
        https://docs.python.org/3/whatsnew/3.12.html#pep-698-override-decorator-for-static-typing
        """
        return super().create_issue(self.fields, update_history, update)

    def set_fields(self, issue: Union[BugIssue, TaskIssue], reporter_email: str, assignee_email: str):
        self.fields = issue.make_fields(
            self.get_user_id_from_email(reporter_email),
            self.get_user_id_from_email(assignee_email),
        )

    def get_user_id_from_email(self, email):
        response = self.get(
            self.resource_url('user/search'),
            params={'query': email},
        )
        try:
            return response[0]['accountId']
        except IndexError:
            return None


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()
    jira = CustomJira(
        url='https://productivitysolutionsinc.atlassian.net',
        username='fc.jongwony@gmail.com',
        password=os.getenv('ATLASSIAN_API_KEY'),
        cloud=True,
    )
    print(jira.get_user_id_from_email('fc.jongwony@gmail.com'))
