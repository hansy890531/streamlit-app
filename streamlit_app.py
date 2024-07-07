import streamlit as st

st.set_page_config(page_title="텔레그램 미니앱 테스트", layout="wide")

st.title("텔레그램 미니앱 테스트")

st.markdown(
    """
    <div id="user-info">사용자 정보 로딩 중...</div>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script>
        console.log("Script 시작");
        function getUserData() {
            console.log("getUserData 함수 시작");
            let tg = window.Telegram.WebApp;
            console.log("Telegram WebApp 객체:", tg);
            if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
                console.log("사용자 정보 존재");
                let userData = {
                    id: tg.initDataUnsafe.user.id,
                    first_name: tg.initDataUnsafe.user.first_name,
                    last_name: tg.initDataUnsafe.user.last_name,
                    username: tg.initDataUnsafe.user.username,
                    language_code: tg.initDataUnsafe.user.language_code
                };
                console.log("사용자 데이터:", userData);
                document.getElementById("user-info").innerText = JSON.stringify(userData, null, 2);
            } else {
                console.error("사용자 정보를 가져올 수 없습니다.");
                document.getElementById("user-info").innerText = "사용자 정보를 가져올 수 없습니다.";
            }
        }

        // 페이지 로드 시 사용자 데이터 가져오기
        console.log("window.onload 설정");
        window.onload = function() {
            console.log("window.onload 실행");
            getUserData();
        };

        // 즉시 실행 함수를 사용하여 스크립트 로드 직후 실행
        (function() {
            console.log("즉시 실행 함수 시작");
            getUserData();
        })();

        // WebApp ready 이벤트 리스너 추가
        window.Telegram.WebApp.onEvent('viewportChanged', function() {
            console.log("viewportChanged 이벤트 발생");
            getUserData();
        });
    </script>
    """,
    unsafe_allow_html=True
)

st.write("위의 'user-info' div에 사용자 정보가 표시됩니다.")
st.write("개발자 도구의 콘솔에서 로그를 확인하세요.")

# 디버깅을 위한 세션 상태 출력
st.write("Session State:", st.session_state)
