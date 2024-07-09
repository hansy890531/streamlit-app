import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import streamlit.components.v1 as components

# HTML 코드 작성 및 렌더링
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Telegram WebApp</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <h1>Telegram WebApp</h1>
    <script>
        Telegram.WebApp.ready();
    </script>
</body>
</html>
"""
components.html(html_code)

# JavaScript 코드 작성
js_code = """
function getUserData() {
    let tg = window.Telegram.WebApp;
    if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
        let userData = {
            id: tg.initDataUnsafe.user.id,
            first_name: tg.initDataUnsafe.user.first_name,
            last_name: tg.initDataUnsafe.user.last_name,
            username: tg.initDataUnsafe.user.username,
            language_code: tg.initDataUnsafe.user.language_code
        };
    return userData;
"""

# streamlit_js_eval을 사용하여 JavaScript 코드 실행 및 결과 받기
result = streamlit_js_eval(js_expressions=js_code, want_output=True, key='telegram_user')

def disp_result():
    st.write("Telegram 사용자 정보: ", result)

# 버튼을 클릭할 때 JavaScript 결과를 표시
st.button("Telegram 사용자 정보 표시", on_click=disp_result)
