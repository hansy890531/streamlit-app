import streamlit as st
from streamlit_javascript import st_javascript
import json

# 사용자 정보를 저장할 공간 생성
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# 텔레그램 웹앱 JavaScript 코드
telegram_js_code = """
    new Promise((resolve, reject) => {
        const tg = window.Telegram.WebApp;
        tg.ready();
        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
            let userData = {
                id: tg.initDataUnsafe.user.id,
                first_name: tg.initDataUnsafe.user.first_name,
                last_name: tg.initDataUnsafe.user.last_name,
                username: tg.initDataUnsafe.user.username,
                language_code: tg.initDataUnsafe.user.language_code
            };
            resolve(userData);
        } else {
            reject("사용자 정보를 가져올 수 없습니다.");
        }
    });
"""

# JavaScript 코드를 실행하고 결과를 받아옴
try:
    user_data = st_javascript(telegram_js_code)
    st.session_state.user_data = user_data
except Exception as e:
    st.error(f"오류 발생: {e}")

# 사용자 정보 표시
if st.session_state.user_data:
    st.write("사용자 정보:")
    st.json(st.session_state.user_data)
else:
    st.write("사용자 정보를 불러오는 중입니다...")
