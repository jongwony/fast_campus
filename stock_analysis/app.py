import streamlit as st

from stock_info import stock_analysis
from backend import ai_stock_analysis
from search import stock_search

@st.cache_data
def cache_ai_stock_analysis(ticker):
    return ai_stock_analysis(ticker).content


# 메인 페이지 설정
st.title('주식 정보 및 분석 대시보드')

# 사이드바 검색 기능
query = st.sidebar.text_input("검색 결과")
results = stock_search(query)

# 드롭다운 메뉴로 검색 결과 표시
if results['hits']:
    # 사용자가 선택할 수 있는 드롭다운 생성
    options = [f"{result['Symbol']} - {result['Security Name']}" for result in results['hits']]
    selected_option = st.sidebar.selectbox("검색 결과에서 선택하세요:", options)

    # 선택된 옵션을 저장
    st.session_state['selected_symbol'] = selected_option
else:
    st.write("검색 결과가 없습니다.")

# 선택된 Symbol을 기반으로 추가 로직 수행 (예시)
if 'selected_symbol' in st.session_state:
    symbol, company = st.session_state['selected_symbol'].split(' - ', 1)
    try:
        report = stock_analysis(symbol)
    except KeyError:
        st.error(f'{company}에 대한 정보를 찾을 수 없습니다.')
    else:
        # 로직 조건 분기
        st.sidebar.title('손익계산서')
        st.sidebar.line_chart(report['분기별_손익계산서'].drop('Basic EPS').T)

        st.sidebar.title('EPS')
        st.sidebar.line_chart(report['분기별_손익계산서'].loc['Basic EPS'].T)

        st.sidebar.title('대차대조표')
        st.sidebar.line_chart(report['분기별_대차대조표'].T)

        st.sidebar.title('현금흐름표')
        st.sidebar.line_chart(report['분기별_현금흐름표'].T)

        # 투자 추천 섹션
        st.header(company)
        if st.button('AI 분석 보고서 가져오기'):
            st.markdown(cache_ai_stock_analysis(symbol))

    # 종목토론방
    st.header('종목토론방')
    # TODO: 종목토론방 구현
