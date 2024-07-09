import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval


# JavaScript 코드 작성
js_code = """
function getUserId() {
    Telegram.WebApp.ready();
    let tg = window.Telegram.WebApp;
    if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
        console.log(tg.initDataUnsafe.user.id)
        return tg.initDataUnsafe.user.id;
    } else {
        return 'No user data available';
    }
}
getUserId();
"""

# streamlit_js_eval을 사용하여 JavaScript 코드 실행 및 결과 받기
result = streamlit_js_eval(js_expressions=js_code, want_output=True, key='js_eval')

def disp_result():
    to_display = f"JavaScript 결과는: {result}"
    st.write(to_display)

# 버튼을 클릭할 때 JavaScript 결과를 표시
st.button("JavaScript 결과 표시", on_click=disp_result)