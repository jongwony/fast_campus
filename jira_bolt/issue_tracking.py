import os

from atlassian import Jira
from dotenv import load_dotenv

load_dotenv()

jira = Jira(
    url='https://productivitysolutionsinc.atlassian.net',
    username='fc.jongwony@gmail.com',
    password=os.getenv('ATLASSIAN_API_KEY'),
    cloud=True,
)

jira.projects()
jira.get_issue_types()
# jira.issue_create
jira.issue_fields('KAN-1')
# jira.create_issue()