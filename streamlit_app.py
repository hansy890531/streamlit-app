import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

# HTML 코드 작성 및 components.html 사용
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Telegram WebApp</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <h1>Telegram WebApp</h1>
</body>
</html>
"""
components.html(html_code)

# JavaScript 코드 작성 및 실행
js_ready_code = """
function onTelegramReady() {
    Telegram.WebApp.ready();
}
window.onload = onTelegramReady;
"""
streamlit_js_eval(js_expressions=js_ready_code, want_output=False, key='js_eval1')

# 사용자 정보를 가져오는 JavaScript 코드
js_user_data_code = """
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
        console.log(userData);
        return JSON.stringify(userData);
    }
    return 'No user data available';
}
getUserData();
"""

# streamlit_js_eval을 사용하여 JavaScript 코드 실행 및 결과 받기
result = streamlit_js_eval(js_expressions=js_user_data_code, want_output=True, key='js_eval2')

def disp_result():
    if result:
        st.write("Telegram 사용자 정보: ", result)
    else:
        st.write("사용자 정보를 가져올 수 없습니다.")

# 버튼을 클릭할 때 JavaScript 결과를 표시
st.button("Telegram 사용자 정보 표시", on_click=disp_result)
