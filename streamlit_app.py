import streamlit as st
from streamlit_js_eval import streamlit_js_eval

# JavaScript 코드를 문자열로 정의
js_code_import = """
document.head.insertAdjacentHTML("beforeEnd", '<script src="https://telegram.org/js/telegram-web-app.js"></script>');
"""

get_user_data_js_code = """
const tg = window.Telegram.WebApp;
if (tg.initDataUnsafe.user) {
    return tg.initDataUnsafe.user.id;
} else {
    return "No user data available.";
}
"""

# Streamlit 앱의 내용
st.title("Telegram Web App Integration with Streamlit")
st.write("This is an example of integrating Telegram Web App JS with Streamlit.")
st.write("야심찬 신작입니다.")

# JavaScript 코드 실행
import_telegram = streamlit_js_eval(js_expressions=js_code_import, want_output=False, key='import_telegram')
user_id = streamlit_js_eval(js_expressions=get_user_data_js_code, want_output=True, key='get_user_id')

# 사용자 ID를 화면에 표시
st.write(f"User ID: {user_id}")
