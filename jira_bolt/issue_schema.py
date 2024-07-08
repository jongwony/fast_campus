from typing import Literal, Optional

from pydantic import BaseModel, Field


class BugIssue(BaseModel):
    summary: str = Field(description="Jira 버그 이슈의 요약 필드입니다.")
    description: Optional[str] = Field(description="Jira 버그 이슈의 설명 필드 입니다.")
    stage: Literal['dev', 'testing', 'staging', 'production'] = Field(
        description="Jira 버그 이슈의 개발 환경입니다. 제공된 문서의 문맥을 추론하여"
         " 반드시 dev, testing, staging, production 중 하나를 선택하세요.",
    )

    def make_fields(self, reporter_id: str, assignee_id: str):
        return {
            'project': {'key': 'KAN'},
            'issuetype': {'name': '버그'},
            'summary': self.summary,
            'description': self.description,
            'customfield_10033': {'value': self.stage},
            'reporter': {'id': reporter_id},
            'assignee': {'id': assignee_id},
        }


class TaskIssue(BaseModel):
    summary: str = Field(description="Jira 작업 이슈의 요약 필드입니다.")
    description: Optional[str] = Field(description="Jira 작업 이슈의 설명 필드 입니다.")

    def make_fields(self, reporter_id: str, assignee_id: str):
        return {
            'project': {'key': 'KAN'},
            'issuetype': {'name': '작업'},
            'summary': self.summary,
            'description': self.description,
            'reporter': {'id': reporter_id},
            'assignee': {'id': assignee_id},
        }


class Issue(BaseModel):
    """
    Jira 이슈의 JSONSchema를 정의합니다.
    """
    # 프롬프트에 JSON이란 단어가 없으면 데이터 추출이 안되는 문제가 있습니다.
    issue_type: Literal['버그', '작업'] = Field(
        description="Jira 이슈의 타입입니다." 
            " 제공된 문서를 추론하여 반드시 버그와 작업 중 하나를 선택해주세요."
    )
