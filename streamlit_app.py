import streamlit as st
from streamlit_js_eval import streamlit_js_eval

# JavaScript 코드를 문자열로 정의
js_code = """
document.head.insertAdjacentHTML("beforeEnd", <script src="https://telegram.org/js/telegram-web-app.js"></script>);
"""


get_user_data_js_code = """
<script>
    function getUserData() {
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
"""


# Streamlit 앱의 내용
st.title("Telegram Web App Integration with Streamlit")
st.write("This is an example of integrating Telegram Web App JS with Streamlit.")
st.wriite("야심찬 신작입니다.")

# 유저 정보를 표시할 HTML 영역 추가
st.markdown('<div id="user-info" style="white-space: pre-wrap; border: 1px solid #ddd; padding: 10px; border-radius: 5px;"></div>', unsafe_allow_html=True)


# JavaScript 코드 실행
import_telegram = streamlit_js_eval(js_expressions=js_code, want_output=False, key='import_telegram')
get_user_data = streamlit_js_eval(js_expression=get_user_data_js_code, want_output = False, key='get_user_data')
