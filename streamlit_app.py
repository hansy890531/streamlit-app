import streamlit as st
import json
from streamlit.components.v1 import html

# 사용자 정보를 저장할 공간 생성
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# JavaScript 코드 삽입
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

                // 사용자 정보를 Streamlit에 전달
                window.parent.postMessage({
                    type: "userData",
                    data: userData
                }, "*");
            } else {
                console.error("사용자 정보를 가져올 수 없습니다.");
            }
        }

        window.addEventListener("message", (event) => {
            if (event.data.type === "userData") {
                const userData = event.data.data;
                console.log("Received user data:", userData);
                // Streamlit에 사용자 정보 전달
                Streamlit.setComponentValue(JSON.stringify(userData));
            }
        });
    </script>
</head>
<body>
    <h1>Welcome to the Telegram Web App</h1>
    <pre id="user-info"></pre>
</body>
</html>
"""

# HTML 코드 삽입
html(html_code, height=300)

# 사용자 정보 수신 및 세션 상태 업데이트
user_data_raw = st.experimental_get_query_params().get("streamlit:componentValue")
if user_data_raw:
    try:
        user_data = json.loads(user_data_raw[0])
        st.session_state.user_data = user_data
    except json.JSONDecodeError:
        st.error("사용자 데이터를 파싱하는 중 오류가 발생했습니다.")

# 사용자 정보 표시
if st.session_state.user_data:
    st.write("사용자 정보:")
    st.json(st.session_state.user_data)
else:
    st.write("사용자 정보를 불러오는 중입니다...")
