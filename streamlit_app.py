import streamlit as st
import streamlit.components.v1 as components

# Streamlit 앱의 내용
st.title("Telegram Web App Integration with Streamlit")
st.write("This is an example of integrating Telegram Web App JS with Streamlit.")
st.write("야심찬 신작입니다.")

# JavaScript 및 HTML 코드 삽입
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const tg = window.Telegram.WebApp;
            if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
                const user_id = tg.initDataUnsafe.user.id;
                document.getElementById('output').innerText = 'User ID: ' + user_id;
            } else {
                document.getElementById('output').innerText = 'No user data available.';
            }
        });
    </script>
</head>
<body>
    <div id="output">Loading...</div>
</body>
</html>
"""

components.html(html_code, height=200)
