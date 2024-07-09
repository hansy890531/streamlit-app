import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

# Telegram Web App JavaScript를 로드하는 HTML 코드
telegram_script = """
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script>
    if (window.Telegram && window.Telegram.WebApp) {
        console.log("Telegram Web App script loaded successfully");
    } else {
        console.log("Failed to load Telegram Web App script");
    }
</script>
"""

# HTML 컴포넌트를 사용하여 스크립트 삽입
components.html(telegram_script, height=0)

# 나머지 Streamlit 앱 코드
st.title("Telegram Web App 통합")
st.write("Telegram Web App 스크립트가 로드되었습니다.")


js_code = """
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
        return JSON.stringify(userData);  // JSON 문자열로 변환하여 반환
    }
    return 'No user data available';
}
getUserData();
"""

# streamlit_js_eval을 사용하여 JavaScript 코드 실행 및 결과 받기
result = streamlit_js_eval(js_expressions=js_code, want_output=True, key='js_eval2')

def disp_result():
    if result:
        st.write("Telegram 사용자 정보: ", result)
    else:
        st.write("사용자 정보를 가져올 수 없습니다.")

# 버튼을 클릭할 때 JavaScript 결과를 표시
st.button("Telegram 사용자 정보 표시", on_click=disp_result)
