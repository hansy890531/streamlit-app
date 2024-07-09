import streamlit as st
import streamlit.components.v1 as components
import json

# Streamlit 페이지 설정
st.set_page_config(page_title="Telegram WebApp User Info", page_icon="🚀")

# Telegram WebApp 스크립트 로드 및 사용자 정보 가져오기
telegram_script = """
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script>
    function getUserInfo() {
        if (window.Telegram && window.Telegram.WebApp) {
            var userInfo = window.Telegram.WebApp.initDataUnsafe.user;
            if (userInfo) {
                document.getElementById('user-info').textContent = JSON.stringify(userInfo);
            } else {
                document.getElementById('user-info').textContent = "User information not available";
            }
        } else {
            document.getElementById('user-info').textContent = "Telegram WebApp is not initialized";
        }
    }
</script>
<div id="user-info"></div>
<script>
    getUserInfo();
</script>
"""

# Streamlit 앱 구조
def main():
    st.title("Telegram WebApp User Information")

    st.write("이 앱은 Telegram WebApp을 통해 접속한 사용자의 정보를 표시합니다.")

    # Telegram WebApp 스크립트 로드
    components.html(telegram_script, height=100)

    # 사용자 정보 표시
    st.subheader("사용자 정보")
    user_info_placeholder = st.empty()

    # JavaScript에서 가져온 사용자 정보를 파싱하고 표시
    st.markdown("""
    <script>
    const userInfoElement = document.getElementById('user-info');
    if (userInfoElement) {
        const userInfo = JSON.parse(userInfoElement.textContent);
        window.parent.postMessage({type: 'streamlit:set_widget_value', key: 'user_info', value: JSON.stringify(userInfo)}, '*');
    }
    </script>
    """, unsafe_allow_html=True)

    # Streamlit 세션 상태를 사용하여 JavaScript에서 전달받은 사용자 정보 업데이트
    if 'user_info' not in st.session_state:
        st.session_state.user_info = '{}'

    user_info = json.loads(st.session_state.user_info)
    if user_info:
        user_info_placeholder.json(user_info)
    else:
        user_info_placeholder.warning("사용자 정보를 불러올 수 없습니다. Telegram WebApp을 통해 접속했는지 확인해주세요.")

    st.info("주의: 이 정보는 클라이언트 측에서 제공되며, 보안상 중요한 작업에는 서버 측 검증이 필요합니다.")

if __name__ == "__main__":
    main()
