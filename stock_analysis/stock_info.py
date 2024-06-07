import yfinance as yf
import matplotlib.pyplot as plt


# 주식 티커 설정
ticker = 'AAPL'

# 티커 데이터 가져오기
stock = yf.Ticker(ticker)


def 재무제표():
    # 재무제표 데이터 가져오기
    income_statement = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    return {
        'income_statement': income_statement,
        'balance_sheet': balance_sheet,
        'cash_flow': cash_flow,
    }


def 재무제표처리():
    # 주요 항목 선택
    income_statement = stock.financials.loc[['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income']].T
    balance_sheet_items = stock.balance_sheet.loc[['Total Assets', 'Total Liabilities Net Minority Interest', 'Stockholders Equity']].T
    cashflow_items = stock.cashflow.loc[['Operating Cash Flow', 'Cash Flow From Continuing Operating Activities',
                                  'Investing Cash Flow', 'Cash Flow From Continuing Investing Activities',
                                  'Financing Cash Flow', 'Cash Flow From Continuing Financing Activities']].T
    return {
        'income_statement': income_statement,
        'balance_sheet_items': balance_sheet_items,
        'cashflow_items': cashflow_items,
    }


def 재무제표시각화():
    # 재무제표 데이터 가져오기
    재무제표데이터 = 재무제표처리()
    income_statement = 재무제표데이터['income_statement']
    balance_sheet_items = 재무제표데이터['balance_sheet_items']
    cashflow_items = 재무제표데이터['cashflow_items']

    # 수익 및 이익 항목 시각화
    plt.figure(figsize=(14, 7))
    income_statement.plot(kind='bar')
    plt.title(f'{ticker} Income Statement')
    plt.xlabel('Date')
    plt.ylabel('Amount (in billions)')
    plt.legend(loc='upper left')
    plt.show()

    # 자산 및 부채 항목 시각화
    plt.figure(figsize=(14, 7))
    balance_sheet_items.plot(kind='bar')
    plt.title(f'{ticker} Balance Sheet')
    plt.xlabel('Date')
    plt.ylabel('Amount (in billions)')
    plt.legend(loc='upper left')
    plt.show()

    # 현금 흐름 항목 시각화
    plt.figure(figsize=(14, 7))
    cashflow_items.plot(kind='bar')
    plt.title(f'{ticker} Cash Flow Statement')
    plt.xlabel('Date')
    plt.ylabel('Amount (in billions)')
    plt.legend(loc='upper left')
    plt.show()


def 가치주():
    # P/E 비율
    pe_ratio = stock.info['forwardPE']

    # P/B 비율
    pb_ratio = stock.info['priceToBook']

    # PEG 비율
    peg_ratio = stock.info['pegRatio']

    # EV/EBITDA 비율
    ev_ebitda_ratio = stock.info['enterpriseToEbitda']

    # 배당 수익률
    dividend_yield = stock.info['dividendYield']
    return {
        'pe_ratio': pe_ratio,
        'pb_ratio': pb_ratio,
        'peg_ratio': peg_ratio,
        'ev_ebitda_ratio': ev_ebitda_ratio,
        'dividend_yield': dividend_yield,
    }


def 우량주():
    # ROE
    roe = stock.info['returnOnEquity']

    # ROA
    roa = stock.info['returnOnAssets']

    # 부채비율
    debt_to_equity = stock.info['debtToEquity']

    # 이자 및 세전이익
    interest_coverage = stock.info['ebitda']

    # 매출 성장률
    revenue_growth = stock.info['revenueGrowth']

    # 배당 지급률
    dividend_payout_ratio = stock.info['payoutRatio']

    # 현금 흐름 (Operating Cash Flow)
    operating_cash_flow = stock.info['operatingCashflow']
    return {
        'roe': roe,
        'roa': roa,
        'debt_to_equity': debt_to_equity,
        'interest_coverage': interest_coverage,
        'revenue_growth': revenue_growth,
        'dividend_payout_ratio': dividend_payout_ratio,
        'operating_cash_flow': operating_cash_flow,
    }


def 거래량():
    hist = stock.history(period='1mo')
    return {
        'volume': hist['Volume'],
        'open': hist['Open'],
        'high': hist['High'],
        'low': hist['Low'],
        'close': hist['Close'],
    }
