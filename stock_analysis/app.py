import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from stock_info import 재무제표처리, 가치주, 우량주, 거래량
from backend import AI_report

# Set the page title
st.title("주식 정보 분석 대시보드")

# Create a text input for search
search_query = st.text_input("검색창")

# Create a select box for search results list
search_results = st.selectbox("검색 결과 리스트", ["Result 1", "Result 2", "Result 3"])

# Create tabs for different sections
tabs = ["회사 기본 정보", "AI 분석 보고서", "종목 토론실"]
tab1, tab2, tab3 = st.tabs(tabs)

# Content for "회사 기본 정보" tab
with tab1:
    data = 재무제표처리()
    st.header("회사 기본 정보")
    # 현금 흐름 항목 시각화
    st.subheader('Cash Flow Statement')
    fig, ax = plt.subplots(figsize=(14, 7))
    data['cashflow_items'].plot(kind='bar', ax=ax)
    ax.set_title(f'Cash Flow Statement')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount (in billions)')
    ax.legend(loc='upper left')
    st.pyplot(fig)

    st.subheader('Income Statement')
    fig, ax = plt.subplots(figsize=(14, 7))
    data['income_statement'].plot(kind='bar', ax=ax)
    ax.set_title(f'Income Statement')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount (in billions)')
    ax.legend(loc='upper left')
    st.pyplot(fig)

    st.subheader('Balance Sheet')
    fig, ax = plt.subplots(figsize=(14, 7))
    data['balance_sheet_items'].plot(kind='bar', ax=ax)
    ax.set_title(f'Balance Sheet')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount (in billions)')
    ax.legend(loc='upper left')
    st.pyplot(fig)

    # 가치주 비율 출력
    value_metrics = 가치주()

    # 데이터프레임 생성
    df_value_metrics = pd.DataFrame(list(value_metrics.items()), columns=['Metric', 'Value'])

    # 가치주 비율 출력
    st.subheader(f'Value Metrics')
    st.dataframe(df_value_metrics)

    # 우량주 비율 가져오기
    blue_chip_metrics = 우량주()

    # 데이터프레임 생성
    df_blue_chip_metrics = pd.DataFrame(list(blue_chip_metrics.items()), columns=['Metric', 'Value'])

    # 우량주 비율 출력
    st.subheader(f'Blue Chip Metrics')
    st.dataframe(df_blue_chip_metrics)

    # 거래량 시각화
    st.subheader(f'Volume Data')
    stock_data = 거래량()
    st.line_chart(stock_data['volume'])

    # 거래량 데이터프레임 표시
    st.subheader(f'Volume Data (Table)')
    st.dataframe(stock_data['volume'])

# Content for "AI 분석 보고서" tab
with tab2:
    st.header("AI 분석 보고서")
    if st.button("보고서 불러오기"):
        with st.spinner(text='In progress'):
            data = AI_report()
            st.success('Done')
        st.write(data)

# Content for "종목 토론실" tab
with tab3:
    st.header("종목 토론실")
    st.write("여기에 종목 토론실 내용을 추가하세요.")
