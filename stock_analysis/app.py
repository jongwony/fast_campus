import streamlit as st

from stock_info import Stock
from backend import AI_report
from search import stock_search

# Set the page title
st.title("주식 정보 분석 대시보드")


class SearchResult:
    def __init__(self, item):
        self.item = item

    @property
    def symbol(self):
        return self.item['Symbol']
    
    @property
    def name(self):
        return self.item['Name']

    def __str__(self):
        return f"{self.symbol}: {self.name}"


# Create a text input for search
search_query = st.text_input("검색창")
hits = stock_search(search_query)['hits']
search_results = [SearchResult(hit) for hit in hits]

# Create a select box for search results list

selected = st.selectbox("검색 결과 리스트", search_results)

# Create tabs for different sections
tabs = ["회사 기본 정보", "AI 분석 보고서", "종목 토론실"]
tab1, tab2, tab3 = st.tabs(tabs)

# Content for "회사 기본 정보" tab
with tab1:
    stock = Stock(selected.symbol)
    st.header("회사 기본 정보")
    # 거래량 시각화
    st.subheader(f'거래량')
    stock_data = stock.금융정보()
    st.line_chart(stock_data['history']['Volume'])

    st.header("재무제표")
    cols = st.columns(3)
    cols[0].subheader("매출액")
    cols[0].line_chart(stock_data['income_statement'].loc['Total Revenue'])
    cols[1].subheader("순이익")
    cols[1].line_chart(stock_data['income_statement'].loc['Net Income'])
    cols[2].subheader("영업이익")
    cols[2].line_chart(stock_data['income_statement'].loc['Operating Income'])

    cols = st.columns(3)
    cols[0].subheader("자산")
    cols[0].line_chart(stock_data['balance_sheet'].loc['Total Assets'])
    cols[1].subheader("부채")
    cols[1].line_chart(stock_data['balance_sheet'].loc['Total Liabilities Net Minority Interest'])
    cols[2].subheader("자본")
    cols[2].line_chart(stock_data['balance_sheet'].loc['Stockholders Equity'])

    cols = st.columns(4)
    cols[0].subheader("영업 현금흐름")
    cols[0].line_chart(stock_data['cash_flow'].loc['Operating Cash Flow'])
    cols[1].subheader("투자 현금흐름")
    cols[1].line_chart(stock_data['cash_flow'].loc['Investing Cash Flow'])
    cols[2].subheader("재무 현금흐름")
    cols[2].line_chart(stock_data['cash_flow'].loc['Financing Cash Flow'])
    cols[3].subheader("순 현금흐름")
    cols[3].line_chart(stock_data['cash_flow'].loc['Free Cash Flow'])

# Content for "AI 분석 보고서" tab
with tab2:
    st.header("AI 분석 보고서")
    if st.button("보고서 불러오기"):
        with st.spinner(text='In progress'):
            data = AI_report(selected.symbol)
            st.success('Done')
        st.write(data)

# Content for "종목 토론실" tab
with tab3:
    st.header("종목 토론실")
    st.write("여기에 종목 토론실 내용을 추가하세요.")
