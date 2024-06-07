import pandas as pd
import yfinance as yf


class Stock:
    def __init__(self, ticker) -> None:
        # 주식 티커 설정
        self.ticker = ticker

        # 티커 데이터 가져오기
        self.stock = yf.Ticker(self.ticker)

    def 금융정보(self):
        return {
            'info': self.stock.info,
            'income_statement': self.stock.quarterly_income_stmt,
            'balance_sheet': self.stock.quarterly_balance_sheet,
            'cash_flow': self.stock.quarterly_cash_flow,
            'history': self.stock.history(period='1mo'),
        }

    def report_support(self):
        """
        금융 전문가의 분석을 보조할 지표들
        """
        def is_float(x):
            try:
                float(x)
                return True
            except ValueError:
                return False
            except TypeError:
                return False
        stock = self.stock
        info = pd.DataFrame.from_dict(stock.info, orient='index', columns=['Value'])
        info = info[info['Value'].apply(is_float)]

        return f'''
        ### Financials
        {info.to_markdown()}

        #### Quarterly Income Statement
        {stock.quarterly_income_stmt.loc[['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income']].to_markdown()}"""

        #### Quarterly Balance Sheet
        {stock.quarterly_balance_sheet.loc[['Total Assets', 'Total Liabilities Net Minority Interest', 'Stockholders Equity']].to_markdown()}"""

        #### Quarterly Cash Flow
        {stock.quarterly_cash_flow.loc[['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow']].to_markdown()}"""
        '''
