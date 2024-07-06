import streamlit as st
import json
from streamlit.components.v1 import html

# 페이지 설정
st.set_page_config(page_title="텔레그램 미니앱 테스트", layout="wide")

# 세션 상태 초기화
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# Telegram WebApp API 스크립트 추가
html("""
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script>
        window.onload = function() {
            let tg = window.Telegram.WebApp;
            if (tg.initDataUnsafe.user) {
                let userData = {
                    id: tg.initDataUnsafe.user.id,
                    first_name: tg.initDataUnsafe.user.first_name,
                    last_name: tg.initDataUnsafe.user.last_name,
                    username: tg.initDataUnsafe.user.username
                };
                
                // Streamlit에 사용자 정보 전달
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: JSON.stringify(userData)
                }, "*");
            } else {
                console.error("사용자 정보를 가져올 수 없습니다.");
            }
        }
    </script>
""", height=0)

# 사용자 정보 받기
user_data_raw = st.experimental_get_query_params().get("streamlit:componentValue")
if user_data_raw:
    try:
        user_data = json.loads(user_data_raw[0])
        st.session_state.user_data = user_data
    except json.JSONDecodeError:
        st.error("사용자 데이터 파싱 실패")

# 메인 애플리케이션
if st.session_state.user_data:
    username = st.session_state.user_data.get('username') or f"{st.session_state.user_data.get('first_name', '')} {st.session_state.user_data.get('last_name', '')}"
    telegram_id = st.session_state.user_data.get('id')
    
    st.title(f"{username}님! 안녕하세요")
    st.write(f"{username}님의 텔레그램 아이디는 {telegram_id}입니다!")
else:
    st.error("이 앱은 텔레그램 미니앱을 통해서만 접근할 수 있습니다.")

# 디버깅을 위한 세션 상태 출력
st.write("Session State:", st.session_state)
