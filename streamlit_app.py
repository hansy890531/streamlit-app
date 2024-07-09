import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

# Telegram Web App JavaScript를 로드하는 HTML 코드
telegram_script = """
<!DOCTYPE html>
<html>
<head>
    <title>Telegram WebApp</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <h1>Telegram WebApp</h1>
    <script>
        // Telegram Web App 준비
        function getUserData() {
            Telegram.WebApp.ready();
            let tg = window.Telegram.WebApp;
            if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
                let userData = {
                    id: tg.initDataUnsafe.user.id,
                    first_name: tg.initDataUnsafe.user.first_name,
                    last_name: tg.initDataUnsafe.user.last_name,
                    username: tg.initDataUnsafe.user.username,
                    language_code: tg.initDataUnsafe.user.language_code
                };
                console.log(userData);
                window.parent.parent.postMessage(userData, '*');  // 부모 창으로 데이터 전송
            } else {
                console.log('No user data available');
                window.parent.parent.postMessage('No user data available', '*');
            }
        }
        window.onload = getUserData;
    </script>
</body>
</html>
"""

# HTML 컴포넌트를 사용하여 Telegram Web App 스크립트 삽입
components.html(telegram_script, height=300)

# JavaScript 결과를 받을 HTML 및 JavaScript 코드 삽입
html_code_for_result = """
<script>
window.addEventListener("message", (event) => {
    const userData = event.data;
    const userInfoElement = document.getElementById("user-info");
    if (typeof userData === 'string') {
        userInfoElement.textContent = userData;
    } else {
        userInfoElement.textContent = JSON.stringify(userData, null, 2);
    }
});
</script>
<div id="user-info">사용자 정보가 여기에 표시됩니다.</div>
"""
components.html(html_code_for_result, height=200)

# Streamlit에서 결과를 표시하는 함수
def disp_result():
    # 결과가 이미 표시될 것이므로 이 함수는 필요 없음
    pass

# 버튼을 클릭할 때 JavaScript 결과를 표시
st.button("Telegram 사용자 정보 표시", on_click=disp_result)
