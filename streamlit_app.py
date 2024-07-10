import streamlit as st
from streamlit_javascript import st_javascript

# Streamlit 앱의 내용
st.title("Telegram Web App Integration with Streamlit")
st.write("This is an example of integrating Telegram Web App JS with Streamlit.")
st.write("야심찬 신작입니다.")

# JavaScript 코드 삽입 및 실행
js_code = """
// Head 태그에 스크립트 삽입
document.head.insertAdjacentHTML("beforeEnd", '<script src="https://telegram.org/js/telegram-web-app.js"></script>');

function getUserId() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const tg = window.Telegram.WebApp;
            if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
                resolve(tg.initDataUnsafe.user.id);
            } else {
                resolve("No user data available.");
            }
        }, 1000); // 스크립트 로드를 기다리기 위해 1초 지연
    });
}

getUserId();
"""

# JavaScript 코드 실행 및 결과 반환
user_id = st_javascript(js_code)

# user_id 값을 확인하여 적절한 메시지 표시
if user_id is None:
    st.write("JavaScript execution returned None.")
elif user_id == "No user data available.":
    st.write(user_id)
else:
    st.write(f"User ID: {user_id}")

# 간단한 수학 연산 예제
result = st_javascript('2 + 3')
st.write(f"2 + 3 = {result}")
