import streamlit as st
from streamlit_javascript import st_javascript

# HTML 코드 정의
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Web App</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script>
        window.onload = function() {
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
                window.parent.postMessage({ user_id: userData.id }, "*");
            } else {
                console.error("사용자 정보를 가져올 수 없습니다.");
                window.parent.postMessage({ user_id: "No user data available." }, "*");
            }
        }
    </script>
</head>
<body>
    <h1>Welcome to the Telegram Web App</h1>
    <pre id="user-info"></pre>
</body>
</html>
"""

# Streamlit 앱에 HTML 삽입
components.html(html_code, height=400)

# JavaScript에서 보낸 메시지를 수신하기 위한 콜백 함수 정의
def handle_js_message(message):
    if "user_id" in message:
        st.write(f"User ID: {message['user_id']}")
    else:
        st.write("No user data available.")

# JavaScript에서 메시지를 수신
st_js_message = """
<script>
window.addEventListener("message", (event) => {
    const data = event.data;
    if (data && data.user_id !== undefined) {
        Streamlit.setComponentValue(data);
    }
});
</script>
"""

# HTML 삽입을 통해 JS 메시지 수신 설정
components.html(st_js_message, height=0)
st.experimental_set_query_params(js_message=handle_js_message)

# 페이지 새로고침 버튼 추가
if st.button("Reload Page"):
    js_code_reload = """
    <script>
    window.parent.postMessage({type: "reload"}, "*");
    </script>
    """
    components.html(js_code_reload, height=0)
