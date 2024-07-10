"""
https://python.langchain.com/v0.2/docs/how_to/extraction_parse/
"""
import os
from operator import itemgetter

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, chain

from issue_schema import Issue, TaskIssue, BugIssue

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)


def jira_issue_type_():
    return RunnableLambda(lambda x: {
        'conversations': x,
        'issue_type': model.with_structured_output(Issue).invoke(x)['issue_type'],
    })


def jira_issue_type():
    """
    This function is equivalent to the jira_issue_type_ function.
    """
    return {
        'conversations': RunnablePassthrough(),
        # Issue 클래스가 pydantic인 경우 dictionary로 변환하여 itemgetter로 값을 가져올 수 있습니다.
        # Issue 클래스가 pydantic v1 인 경우 class로 변환하여 attrgetter로 값을 가져올 수 있습니다.
        'issue_type': model.with_structured_output(Issue) | itemgetter('issue_type'),
    }


@chain
def jira_field(inputs):
    issue_type_map = {'작업': TaskIssue, '버그': BugIssue}
    pydantic_object = issue_type_map[inputs['issue_type']]

    with open("system_prompt.md") as f:
        system_prompt = f.read()

    parser = PydanticOutputParser(pydantic_object=pydantic_object)
    prompt = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('user', 'A conversation consists of multiple conversations, '
         'with one conversation having the following format:\n'
         'Username: """Messages""":\n\n'
         'Conversations: ```{conversations}```'),
    ]).partial(format_instructions=parser.get_format_instructions())

    return prompt | model | parser


def structured_jira_issue(conversations: str):
    full_chain = jira_issue_type() | jira_field
    return full_chain.invoke(conversations)


def get_graph():
    """
    pip install grandalf
    """
    return (jira_issue_type() | jira_field).get_graph().print_ascii()


if __name__ == "__main__":
    conversations = '''
    Secretary: """An error occurred in the API: *Error Message:*
Error code: 429 - {'error': {'message': 'Request too large for gpt-4o in organization org-2FUZOO7oAvSs9x0QCG0pH2Cc on tokens per min (TPM): Limit 30000, Requested 600223. The input or output tokens must be reduced in order to run successfully. Visit <https://platform.openai.com/account/rate-limits> to learn more.', 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}} *Status Code:* 429 *Request ID:* req_0c3413bab17c202ec850c2df6cad68d5 *Error Code:* rate_limit_exceeded For more details, please check the logs or contact support."""
    최종원 Jongwon Choi: """리퀘스트가 너무 크다고 하네요. 토큰 정보를 줄여야 한다고 합니다. 사용자에게 이런 경우 새로운 스레드를 만들어서 다시 시도하라고 알려주는 것이 좋을 것 같습니다."""
    최종원 Jongwon Choi: """테스트 서버에서 발생했습니다. 제가 작업할게요."""
    '''
    # response = model.with_structured_output(Issue).invoke(conversations)
    response = structured_jira_issue(conversations)