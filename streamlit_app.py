import streamlit as st
from streamlit_javascript import st_javascript

# HTML 구조를 사용하여 head와 body에 스크립트를 삽입
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
    <pre id="user-info">Loading...</pre>
    <script>
        function getUserId() {
            return new Promise((resolve, reject) => {
                const tg = window.Telegram.WebApp;
                if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
                    resolve(tg.initDataUnsafe.user.id);
                } else {
                    resolve("No user data available.");
                }
            });
        }
        window.onload = async function() {
            const userId = await getUserId();
            document.getElementById('user-info').innerText = 'User ID: ' + userId;
            window.parent.postMessage({ user_id: userId }, "*");
        }
    </script>
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

components.html(st_js_message, height=0)
st.experimental_set_query_params(js_message=handle_js_message)
