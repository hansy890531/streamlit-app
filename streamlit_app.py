import streamlit as st
from streamlit.components.v1 import html
from streamlit_javascript import st_javascript

# Streamlit 앱의 내용
st.title("Telegram Web App Integration with Streamlit")
st.write("이 예제는 Streamlit과 Telegram Web App JS를 통합하는 방법을 보여줍니다.")

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
            function getUserId() {
                return new Promise((resolve) => {
                    setTimeout(() => {
                        const tg = window.Telegram.WebApp;
                        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
                            resolve(tg.initDataUnsafe.user.id);
                        } else {
                            resolve("No user data available.");
                        }
                    }, 1000); // 스크립트가 로드될 시간을 기다리기 위해 1초 대기
                });
            }

            getUserId().then(userId => {
                document.getElementById("user-info").innerText = 'User ID: ' + userId;
                window.parent.postMessage({ user_id: userId }, "*");
            });
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

# JavaScript 코드 실행 및 결과 반환
user_id = st_javascript(js_code="")

# user_id 값을 확인하여 적절한 메시지 표시
if user_id is None:
    st.write("JavaScript execution returned None.")
elif user_id == "No user data available.":
    st.write(user_id)
else:
    st.write(f"User ID: {user_id}")
