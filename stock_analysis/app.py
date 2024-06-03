import streamlit as st

from stock_info import stock_analysis
from backend import ai_stock_analysis
from search import stock_search
from comment import create_connection, create_table, insert_comment, get_all_comments

@st.cache_data
def cache_ai_stock_analysis(ticker):
    return ai_stock_analysis(ticker).content


# 메인 페이지 설정
st.title('주식 정보 및 분석 대시보드')

# 사이드바 검색 기능
query = st.text_input("기호 또는 회사 이름을 입력하세요:")
results = stock_search(query)

# 드롭다운 메뉴로 검색 결과 표시
if results['hits']:
    # 사용자가 선택할 수 있는 드롭다운 생성
    options = [f"{result['Symbol']} - {result['Security Name']}" for result in results['hits']]
    selected_option = st.selectbox("검색 결과에서 선택하세요:", options)

    # 선택된 옵션을 저장
    st.session_state['selected_symbol'] = selected_option
else:
    st.write("검색 결과가 없습니다.")

정보탭, 보고서탭, 토론탭 = st.tabs(['주식 정보', 'AI 분석 보고서', '종목토론방'])

# 선택된 Symbol을 기반으로 추가 로직 수행 (예시)
if 'selected_symbol' in st.session_state:
    symbol, company = st.session_state['selected_symbol'].split(' - ', 1)
    try:
        report = stock_analysis(symbol)
    except KeyError:
        st.error(f'{company}에 대한 정보를 찾을 수 없습니다.')
    else:
        # 로직 조건 분기
        정보탭.title('손익계산서')
        정보탭.line_chart(report['분기별_손익계산서'].drop('Basic EPS').T)

        정보탭.title('EPS')
        정보탭.line_chart(report['분기별_손익계산서'].loc['Basic EPS'].T)

        정보탭.title('대차대조표')
        정보탭.line_chart(report['분기별_대차대조표'].T)

        정보탭.title('현금흐름표')
        정보탭.line_chart(report['분기별_현금흐름표'].T)

        # 투자 추천 섹션
        보고서탭.header(company)
        if 보고서탭.button('AI 분석 보고서 가져오기'):
            보고서탭.markdown(cache_ai_stock_analysis(symbol))


# SQLite 데이터베이스 연결 및 테이블 생성
conn = create_connection()
create_table(conn)

# 댓글 입력 섹션
토론탭.subheader('댓글을 입력하세요')
comment = 토론탭.text_input('댓글')

if 토론탭.button('댓글 남기기'):
    if comment:
        insert_comment(conn, f"{symbol} - {comment}")
        토론탭.success('댓글이 성공적으로 저장되었습니다.')
    else:
        토론탭.error('댓글을 입력하세요.')

# 저장된 댓글 표시 섹션
토론탭.subheader('저장된 댓글')
comments = get_all_comments(conn)
for comment in sorted(comments, reverse=True):
    시간, 댓글 = comment
    토론탭.write(f"{시간}: {댓글}")

# SQLite 데이터베이스 연결 종료
# conn.close()