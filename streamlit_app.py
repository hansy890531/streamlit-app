import streamlit as st
import streamlit.components.v1 as components

# Telegram WebApp 초기화 및 사용자 정보 가져오기 스크립트
telegram_js = """
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script type="text/javascript">
    Telegram.WebApp.ready();

    // Telegram 사용자 정보 가져오기
    const user = Telegram.WebApp.initDataUnsafe.user;
    document.addEventListener('DOMContentLoaded', (event) => {
        if (user) {
            document.body.insertAdjacentHTML('beforeend', `<p>Telegram 사용자 이름: ${user.first_name} ${user.last_name}</p>`);
            document.body.insertAdjacentHTML('beforeend', `<p>Telegram 사용자 ID: ${user.id}</p>`);
            document.body.insertAdjacentHTML('beforeend', `<p>Telegram 사용자 사용자명: ${user.username}</p>`);
        } else {
            document.body.insertAdjacentHTML('beforeend', `<p>사용자 정보를 가져올 수 없습니다.</p>`);
        }
    });
</script>
"""

# Streamlit 마크다운을 사용하여 JavaScript 코드를 포함
components.html(telegram_js)

st.write("안녕하세요")
