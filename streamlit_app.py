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
            } else {
                console.error("사용자 정보를 가져올 수 없습니다.");
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
