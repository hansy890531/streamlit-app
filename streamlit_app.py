import streamlit as st
import json

# 사용자 정보를 저장할 공간 생성
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# JavaScript 코드 삽입
html_code = """
    <div id="div"></div>
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
        };
    </script>
"""

# HTML 코드 삽입
st.markdown(html_code, unsafe_allow_html=True)

# JavaScript로부터 메시지 수신 및 세션 상태 업데이트
if st.session_state.user_data is None:
    # JavaScript로부터 데이터 수신 설정
    st.markdown("""
    <script>
        window.addEventListener("message", (event) => {
            if (event.data.type === "userData") {
                const userData = event.data.data;
                console.log("Received user data:", userData);
                // Streamlit에 사용자 정보 전달
                const streamlitMessage = {
                    type: "streamlit:message",
                    data: JSON.stringify(userData)
                };
                parent.postMessage(streamlitMessage, "*");
            }
        });
    </script>
    """, unsafe_allow_html=True)

# 사용자 정보 수신 및 세션 상태 업데이트
user_data_raw = st.experimental_get_query_params().get("streamlit:message")
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
