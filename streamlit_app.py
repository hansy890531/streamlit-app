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
"""

# JavaScript 코드 실행
# geteUserData function의 return 값을 user_id 변수에 담습니다.
user_id = streamlit_js_eval(js_expressions=js_code, want_output=True, key='get_user_id')
st.write(user_id)

# 간단한 수학 연산 예제
st.header("간단 수학 연산")
result = streamlit_js_eval(js_expressions='2+3', want_output=True, key='do_sum')
st.write(result) # 5
