import streamlit as st
from streamlit.components.v1 import html

# Streamlit 앱의 내용
st.title("Telegram Web App Integration with Streamlit")

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
html(html_code, height=400)

# JavaScript에서 보낸 메시지를 수신하기 위한 HTML 코드
js_message_handler = """
<script>
window.addEventListener("message", (event) => {
    const data = event.data;
    if (data && data.user_id !== undefined) {
        Streamlit.setComponentValue(data);
    }
});
</script>
"""

# 메시지 수신을 위한 HTML 삽입
html(js_message_handler, height=0)

# Streamlit의 이벤트로부터 user_id 값을 받아 처리
user_id = st.experimental_get_query_params().get("user_id", [None])[0]

# user_id 값을 확인하여 적절한 메시지 표시
if user_id is None:
    st.write("JavaScript execution returned None.")
elif user_id == "No user data available.":
    st.write(user_id)
else:
    st.write(f"User ID: {user_id}")
