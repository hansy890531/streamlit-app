import streamlit as st

st.set_page_config(page_title="텔레그램 미니앱 테스트", layout="wide")

st.title("텔레그램 미니앱 테스트")

st.markdown(
    """
    <div id="user-info"></div>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script>
        function getUserData() {
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
                document.getElementById("user-info").innerText = JSON.stringify(userData, null, 2);
            } else {
                console.error("사용자 정보를 가져올 수 없습니다.");
                document.getElementById("user-info").innerText = "사용자 정보를 가져올 수 없습니다.";
            }
        }

        // 페이지 로드 시 사용자 데이터 가져오기
        window.onload = getUserData;
    </script>
    """,
    unsafe_allow_html=True
)

st.write("위의 'user-info' div에 사용자 정보가 표시됩니다.")
st.write("개발자 도구의 콘솔에서 로그를 확인하세요.")

# 디버깅을 위한 세션 상태 출력
st.write("Session State:", st.session_state)
