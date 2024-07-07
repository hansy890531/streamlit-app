import streamlit as st
from streamlit_javascript import st_javascript
import json

# 페이지 설정
st.set_page_config(page_title="텔레그램 미니앱 테스트", layout="wide")

# HTML 및 JavaScript 코드
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Web App</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <h1>Welcome to the Telegram Web App</h1>
    <pre id="user-info"></pre>
</body>
</html>
"""

js_code = """
function getUserData() {
    let tg = window.Telegram.WebApp;
    if (tg.initDataUnsafe.user) {
        let userData = {
            id: tg.initDataUnsafe.user.id,
            first_name: tg.initDataUnsafe.user.first_name,
            last_name: tg.initDataUnsafe.user.last_name,
            username: tg.initDataUnsafe.user.username,
            language_code: tg.initDataUnsafe.user.language_code
        };
        console.log(userData);
        document.getElementById("user-info").innerText = JSON.stringify(userData, null, 2);
        return JSON.stringify(userData);
    } else {
        console.error("사용자 정보를 가져올 수 없습니다.");
        return null;
    }
}
getUserData();
"""

# HTML 삽입
st.components.v1.html(html_code, height=300)

# JavaScript 실행 및 결과 가져오기
user_data_str = st_javascript(js_code)
st.write("Raw return value:", user_data_str)

try:
    user_data = json.loads(user_data_str)
    st.write("Parsed user data:", user_data)
    if user_data is not None:
        st.session_state.user_data = user_data
except json.JSONDecodeError:
    st.error("Failed to parse user data")

# 메인 애플리케이션
if 'user_data' in st.session_state and st.session_state.user_data is not None:
    username = st.session_state.user_data.get('username') or f"{st.session_state.user_data.get('first_name', '')} {st.session_state.user_data.get('last_name', '')}"
    telegram_id = st.session_state.user_data.get('id')
    
    st.title(f"{username}님! 안녕하세요")
    st.write(f"{username}님의 텔레그램 아이디는 {telegram_id}입니다!")
else:
    st.error("이 앱은 텔레그램 미니앱을 통해서만 접근할 수 있습니다.")
    st.info("사용자 데이터를 불러오는 중입니다. 잠시만 기다려주세요...")

# 디버깅을 위한 세션 상태 출력
st.write("Session State:", st.session_state)
