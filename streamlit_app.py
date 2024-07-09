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

# JavaScript 코드 작성
js_code = """
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
        window.parent.postMessage(userData, '*');  // 부모 창으로 데이터 전송
    } else {
        console.log('No user data available');
        window.parent.postMessage('No user data available', '*');
    }
}
getUserData();
"""

# streamlit_js_eval을 사용하여 JavaScript 코드 실행 및 결과 받기
result = streamlit_js_eval(js_expressions=js_code, want_output=True, key='js_eval2')

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

def disp_result():
    # 결과가 이미 표시될 것이므로 이 함수는 필요 없음
    pass

# 버튼을 클릭할 때 JavaScript 결과를 표시
st.button("Telegram 사용자 정보 표시", on_click=disp_result)
