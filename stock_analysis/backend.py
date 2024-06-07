import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from stock_info import Stock


load_dotenv()
        
# 환경 변수 읽기
llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv('OPENAI_API_KEY'), temperature=0)


def AI_report(ticker):
    """
    분석에 필요한 정보를 제공해드립니다.
    세 개의 따옴표가 포함된 마크다운 보고서가 제공됩니다.
    재무 분석가로서 보고서에 담긴 수치를 자세히 살펴보고
    회사의 성장 추세와 재무 안정성을 평가하여 사용자들이 자유롭게 토론할 수 있도록 돕습니다.
    사람들이 공개 토론을 할 수 있도록 귀하의 의견을 제공하십시오.
    보고서를 한국어로 제출해주세요.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        I want you to act as a Financial Analyst.
        Want assistance provided by qualified individuals enabled with experience on understanding charts using technical analysis tools while interpreting macroeconomic environment prevailing across world consequently assisting customers acquire long term advantages requires clear verdicts therefore seeking same through informed predictions written down precisely! First statement contains following content- “Can you tell us what future stock market looks like based upon current conditions ?”.
        """),
        ("user", ''' 
        We provide the information necessary for analysis.
        Given markdown reports with triple quotes. 
        As a Financial Analyst, Take a closer look at the numbers in the report and evaluate the company's growth trends and financial stability to help users discuss freely.
        Provide your opinion to people so they can have an open discussion.
        Please provide the report in Korean.

        """
        {markdown}
        """
        ''')
    ])
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    return chain.invoke({
        "markdown": Stock(ticker).report_support()
    })
