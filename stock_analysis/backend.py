from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from stock_info import stock_analysis


def ai_stock_analysis(ticker):
    system = '''
    Want assistance provided by qualified individuals enabled with experience on understanding charts using technical analysis tools while interpreting macroeconomic environment prevailing across world consequently assisting customers acquire long term advantages requires clear verdicts therefore seeking same through informed predictions written down precisely!
    '''

    user = '''
    We provide the information necessary for analysis.
    Given markdown reports with triple quotes. 
    As a Financial Analyst, Take a closer look at the numbers in the report and evaluate the company's growth trends and financial stability to help users discuss freely.
    Provide your opinion to people so they can have an open discussion.
    Please provide the report in Korean.

    Stock Analysis Markdown: """
    ### {ticker} Financials
        
    #### Quarterly Income Statement
    {분기별_손익계산서}

    #### Quarterly Balance Sheet
    {분기별_대차대조표}

    #### Quarterly Cash Flow
    {분기별_현금흐름표}

    #### Profitability Ratios
    {수익성지표}
    """
    '''

    prompt = ChatPromptTemplate.from_messages([
        ('system', system),
        ('user', user),
    ])

    llm = ChatOpenAI(model='gpt-4-turbo', temperature=0.2)

    chain = prompt | llm
    info = stock_analysis(ticker)

    return chain.invoke({
        'ticker': ticker,
        '분기별_손익계산서': info['분기별_손익계산서'].to_markdown(),
        '분기별_대차대조표': info['분기별_대차대조표'].to_markdown(),
        '분기별_현금흐름표': info['분기별_현금흐름표'].to_markdown(),
        '수익성지표': info['수익성지표'].to_markdown(),
    })
