import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="텔레그램 사용자 정보")

st.title("텔레그램 사용자 정보")

# 텔레그램 WebApp API 스크립트 로드
telegram_script = """
<script src="https://telegram.org/js/telegram-web-app.js"></script>
"""
st.components.v1.html(telegram_script, height=0)

# 텔레그램 WebApp 초기화 및 사용자 정보 가져오기
user_info = streamlit_js_eval(
    """
    if (window.Telegram && window.Telegram.WebApp) {
        const webApp = window.Telegram.WebApp;
        webApp.ready();
        if (webApp.initDataUnsafe && webApp.initDataUnsafe.user) {
            return {
                id: webApp.initDataUnsafe.user.id,
                first_name: webApp.initDataUnsafe.user.first_name,
                last_name: webApp.initDataUnsafe.user.last_name,
                username: webApp.initDataUnsafe.user.username,
                language_code: webApp.initDataUnsafe.user.language_code
            };
        }
    }
    return null;
    """,
    want_output=True,
    key="telegram_user_info"
)

if user_info:
    st.success("텔레그램 웹앱으로 접속했습니다!")
    st.write("사용자 정보:")
    st.json(user_info)
else:
    st.warning("이 앱은 텔레그램 웹앱으로 접속해야 합니다.")

# 테마 설정 (옵션)
theme_params = streamlit_js_eval(
    """
    if (window.Telegram && window.Telegram.WebApp) {
        return window.Telegram.WebApp.themeParams;
    }
    return null;
    """,
    want_output=True,
    key="telegram_theme"
)

if theme_params:
    st.write("테마 정보:")
    st.json(theme_params)

# 뒤로가기 버튼 (옵션)
if st.button("뒤로가기"):
    streamlit_js_eval(
        """
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.close();
        }
        """
    )
