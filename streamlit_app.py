import streamlit as st
import streamlit.components.v1 as components
import json

# Streamlit 페이지 설정
st.set_page_config(page_title="Telegram WebApp User Info", page_icon="🚀")

# Telegram WebApp 스크립트 및 사용자 정보 가져오기 함수
telegram_script = """
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script>
    function getUserInfo() {
        if (window.Telegram && window.Telegram.WebApp) {
            var userInfo = window.Telegram.WebApp.initDataUnsafe.user;
            if (userInfo) {
                document.getElementById('user-info').textContent = JSON.stringify(userInfo);
                window.parent.postMessage({
                    type: 'streamlit:set_widget_value', 
                    key: 'user_info', 
                    value: JSON.stringify(userInfo)
                }, '*');
            } else {
                document.getElementById('user-info').textContent = "User information not available";
            }
        } else {
            document.getElementById('user-info').textContent = "Telegram WebApp is not initialized";
        }
    }

    // Streamlit 앱이 로드된 후 스크립트 실행
    window.addEventListener('load', function() {
        setTimeout(getUserInfo, 1000); // 1초 지연 후 실행
    });
</script>
<div id="user-info"></div>
"""

# Streamlit 앱 구조
def main():
    st.title("Telegram WebApp User Information")

    st.write("이 앱은 Telegram WebApp을 통해 접속한 사용자의 정보를 표시합니다.")

    # 사용자 정보 표시를 위한 플레이스홀더
    user_info_placeholder = st.empty()

    # Telegram WebApp 스크립트 로드 (페이지 하단에 배치)
    st.markdown("---")
    st.subheader("데이터 로딩 중...")
    components.html(telegram_script, height=100)

    # Streamlit 세션 상태를 사용하여 JavaScript에서 전달받은 사용자 정보 업데이트
    if 'user_info' not in st.session_state:
        st.session_state.user_info = '{}'

    # 사용자 정보 표시
    st.subheader("사용자 정보")
    user_info = json.loads(st.session_state.user_info)
    if user_info:
        user_info_placeholder.json(user_info)
    else:
        user_info_placeholder.warning("사용자 정보를 불러오는 중입니다. 잠시만 기다려주세요...")

    st.info("주의: 이 정보는 클라이언트 측에서 제공되며, 보안상 중요한 작업에는 서버 측 검증이 필요합니다.")

if __name__ == "__main__":
    main()
