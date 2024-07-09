# app.py
import streamlit as st
import asyncio
from telegram import Bot
from telegram.ext import Application
from config import TELEGRAM_BOT_TOKEN, WEBAPP_URL
from utils import get_user_info, verify_webapp_data
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(page_title="Secure Telegram WebApp Integration", page_icon="🔐")

# Telegram Bot 초기화
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def get_chat_member(user_id, chat_id):
    try:
        return await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    except Exception as e:
        st.error(f"Error getting chat member: {e}")
        return None

# Streamlit 앱 메인 함수
def main():
    st.title("🔐 Secure Telegram WebApp Integration")

    # 클라이언트 측 스크립트
    client_script = """
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script>
    let tgData = {};
    function initTelegramWebApp() {
        if (window.Telegram && window.Telegram.WebApp) {
            tgData = window.Telegram.WebApp.initData || "";
            document.getElementById('tg-data').value = tgData;
            window.parent.postMessage({
                type: 'streamlit:set_widget_value',
                key: 'tg_data',
                value: tgData
            }, '*');
            console.log("Telegram WebApp initialized:", tgData);
        } else {
            console.error("Telegram WebApp is not available");
        }
    }
    window.addEventListener('load', function() {
        setTimeout(initTelegramWebApp, 1000);
    });
    </script>
    <input type="hidden" id="tg-data">
    """
    components.html(client_script, height=0)

    # Streamlit 위젯을 통해 Telegram 데이터 받기
    if 'tg_data' not in st.session_state:
        st.session_state.tg_data = ""
    
    tg_data = st.session_state.tg_data

    if tg_data:
        # 데이터 검증
        if verify_webapp_data(tg_data, TELEGRAM_BOT_TOKEN):
            user_info = get_user_info(tg_data)
            if user_info:
                st.success("✅ User authenticated successfully!")
                st.json(user_info)

                # 비동기로 추가 사용자 정보 가져오기
                chat_member = asyncio.run(get_chat_member(user_info['id'], user_info['id']))
                if chat_member:
                    st.subheader("Additional User Info:")
                    st.json({
                        "status": chat_member.status,
                        "user": {
                            "first_name": chat_member.user.first_name,
                            "last_name": chat_member.user.last_name,
                            "username": chat_member.user.username
                        }
                    })
            else:
                st.warning("⚠️ No user information available in the WebApp data.")
        else:
            st.error("🚫 Invalid or tampered WebApp data!")
    else:
        st.info("Waiting for Telegram WebApp data...")

    st.markdown("---")
    st.subheader("🔍 Debug Information")
    st.text(f"WebApp URL: {WEBAPP_URL}")
    st.text("Check the browser console for more detailed logs.")

if __name__ == "__main__":
    main()
