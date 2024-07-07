import streamlit as st
import json
from streamlit_javascript import st_javascript

# 페이지 설정
st.set_page_config(page_title="텔레그램 미니앱 테스트", layout="wide")

# 세션 상태 초기화
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# Telegram WebApp API를 사용하여 사용자 정보 가져오기
js_code = """
if (window.Telegram && window.Telegram.WebApp) {
    var tg = window.Telegram.WebApp;
    if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        var user = tg.initDataUnsafe.user;
        return {
            id: user.id,
            first_name: user.first_name,
            last_name: user.last_name,
            username: user.username,
            language_code: user.language_code
        };
    }
}
return null;
"""

user_data = st_javascript(js_code)

if user_data is not None:
    st.session_state.user_data = user_data
    st.experimental_rerun()

# 메인 애플리케이션
if st.session_state.user_data:
    username = st.session_state.user_data.get('username') or f"{st.session_state.user_data.get('first_name', '')} {st.session_state.user_data.get('last_name', '')}"
    telegram_id = st.session_state.user_data.get('id')
    
    st.title(f"{username}님! 안녕하세요")
    st.write(f"{username}님의 텔레그램 아이디는 {telegram_id}입니다!")
else:
    st.error("이 앱은 텔레그램 미니앱을 통해서만 접근할 수 있습니다.")
    st.info("사용자 데이터를 불러오는 중입니다. 잠시만 기다려주세요...")

# 디버깅을 위한 세션 상태 출력
st.write("Session State:", st.session_state)
