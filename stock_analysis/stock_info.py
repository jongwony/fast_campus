import pandas as pd
import yfinance as yf


def stock_analysis(ticker):
    # Apple의 주식 기호 'AAPL'로 Ticker 객체 생성
    aapl = yf.Ticker(ticker)

    # 재무제표 가져오기
    # balance_sheet = aapl.balance_sheet  # 대차대조표
    # cash_flow = aapl.cashflow  # 현금흐름표

    # 연간 또는 분기별 재무제표
    # quarterly_financials = aapl.quarterly_financials  # 분기별 손익계산서
    # quarterly_balance_sheet = aapl.quarterly_balance_sheet  # 분기별 대차대조표

    분기별_손익계산서 = aapl.quarterly_income_stmt.loc[['Net Income', 'Total Revenue', 'Basic EPS']]
    # 키를 빨리 찾는 방법
    # q_bal = aapl.quarterly_balance_sheet
    # 'Total Assets'
    # q_bal[q_bal.index.str.contains('Asset')]
    # 'Total Liabilities Net Minority Interest'
    # q_bal[q_bal.index.str.contains('Liab')]
    # 'Common Stock Equity'
    # q_bal[q_bal.index.str.contains('Equity')]
    분기별_대차대조표 = aapl.quarterly_balance_sheet.loc[['Total Assets', 'Total Liabilities Net Minority Interest', 'Common Stock Equity']]
    분기별_현금흐름표 = aapl.quarterly_cash_flow.loc[['Free Cash Flow', 'Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'Changes In Cash']]

    # 정보 가져오기
    info = aapl.info

    # 수익성 지표 출력
    # eps = info.get('trailingEps', 'N/A')  # 주당순이익
    # pe_ratio = info.get('trailingPE', 'N/A')  # 주가수익비율
    # pb_ratio = info.get('priceToBook', 'N/A')  # 주가순자산비율
    # ps_ratio = info.get('priceToSalesTrailing12Months', 'N/A')  # 주가매출비율
    # dividend_yield = info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A'  # 배당수익률
    수익성지표 = pd.DataFrame.from_dict(
        {k: info[k] for k in info if k in ['trailingEps', 'trailingPE', 'priceToBook', 'priceToSalesTrailing12Months', 'dividendYield']},
        orient='index', columns=['Value'],
    )

    # return markdown
    return {
        '분기별_손익계산서': 분기별_손익계산서,
        '분기별_대차대조표': 분기별_대차대조표,
        '분기별_현금흐름표': 분기별_현금흐름표,
        '수익성지표': 수익성지표,
    }

