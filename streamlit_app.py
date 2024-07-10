import streamlit as st
import streamlit.components.v1 as components

# Streamlit 앱의 내용
st.title("Telegram Web App Integration with Streamlit")
st.write("This is an example of integrating Telegram Web App JS with Streamlit.")
st.write("야심찬 신작입니다.")

# HTML 및 JavaScript 코드 삽입
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Web App</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script>
        function sendUserIdToStreamlit() {
            const tg = window.Telegram.WebApp;
            if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
                const userId = tg.initDataUnsafe.user.id;
                const streamlitMessage = { "user_id": userId };
                window.parent.postMessage(streamlitMessage, "*");
            } else {
                const streamlitMessage = { "user_id": "No user data available." };
                window.parent.postMessage(streamlitMessage, "*");
            }
        }
        window.onload = function() {
            sendUserIdToStreamlit();
        }
    </script>
</head>
<body>
    <h1>Welcome to the Telegram Web App</h1>
    <pre id="user-info">Loading...</pre>
</body>
</html>
"""

# Streamlit 앱에 HTML 삽입
components.html(html_code, height=400)

# JavaScript에서 보낸 메시지를 수신하기 위한 콜백 함수 정의
def handle_js_message():
    message = st.session_state.get("js_message")
    if message and "user_id" in message:
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

# 페이지 새로고침 버튼 추가
if st.button("Reload Page"):
    js_code_reload = """
    <script>
    window.parent.postMessage({type: "reload"}, "*");
    </script>
    """
    components.html(js_code_reload, height=0)
