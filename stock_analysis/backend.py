import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from stock_info import 재무제표, 가치주, 우량주, 거래량


load_dotenv()
        
# 환경 변수 읽기
llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def AI_report():
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        I want you to act as a Financial Analyst.
        Want assistance provided by qualified individuals enabled with experience on understanding charts using technical analysis tools while interpreting macroeconomic environment prevailing across world consequently assisting customers acquire long term advantages requires clear verdicts therefore seeking same through informed predictions written down precisely! First statement contains following content- “Can you tell us what future stock market looks like based upon current conditions ?”.
        """),
        ("user", ''' 
        Here is the information required for analysis enclosed in triple quotation marks. As a financial analysis expert, please examine these indicators closely and conduct an open discussion to assess the company's growth or value.
        Balance Sheet: """{재무제표}"""
        Value Stock: """{가치주}"""
        Blue Chip Stock: """{우량주}"""
        Volume: """{거래량}"""

        {input}

        한글로 답변해 주세요.
        ''')
    ])
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    return chain.invoke({
        "input": "엔비디아 주간 차트를 분석해주세요.",
        "재무제표": 재무제표(),
        "가치주": 가치주(),
        "우량주": 우량주(),
        "거래량": 거래량(),
    })
