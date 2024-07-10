import streamlit as st
from streamlit_js_eval import streamlit_js_eval

# Telegram 웹앱 JavaScript 파일을 head에 삽입하고 사용자 데이터를 가져오는 코드
js_code = """
document.head.insertAdjacentHTML("beforeEnd", '<script src="https://telegram.org/js/telegram-web-app.js"></script>');
function getUserData() {
    const tg = window.Telegram.WebApp;
    if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        console.log(tg.initDataUnsafe.user.id)
        return tg.initDataUnsafe.user.id;
    } else {
        return "No user data available.";
    }
}
setTimeout(() => window.Streamlit.setComponentValue(getUserData()), 1000);  // 1초 대기 후 실행
"""

# Streamlit 앱의 내용
st.title("Telegram Web App Integration with Streamlit")
st.write("This is an example of integrating Telegram Web App JS with Streamlit.")
st.write("야심찬 신작입니다.")

# JavaScript 코드 실행
user_id = streamlit_js_eval(js_expressions=js_code, want_output=True, key='get_user_id')

# user_id 값을 확인하여 적절한 메시지 표시
if user_id is None:
    st.write("JavaScript execution returned None.")
elif user_id == "No user data available.":
    st.write(user_id)
else:
    st.write(f"User ID: {user_id}")

# 간단한 수학 연산 예제
result = streamlit_js_eval(js_expressions='2+3', want_output=True, key='do_sum')
st.write(result)
