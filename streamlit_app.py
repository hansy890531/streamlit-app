import streamlit as st
from streamlit_js_eval import streamlit_js_eval

# Telegram 웹앱 JavaScript 파일을 head에 삽입하는 코드
js_code_import = """
document.head.insertAdjacentHTML("beforeEnd", '<script src="https://telegram.org/js/telegram-web-app.js"></script>');
"""

get_user_data_js_code = """
const tg = window.Telegram.WebApp;
if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
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

# user_id 값을 확인하여 적절한 메시지 표시
if user_id is None:
    st.write("JavaScript execution returned None.")
elif user_id == "No user data available.":
    st.write(user_id)
else:
    st.write(f"User ID: {user_id}")
