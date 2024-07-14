import streamlit as st
from get_telegram_id import TelegramLoginWidgetComponent
from get_telegram_id.helpers import YamlConfig

# Load configuration
config = YamlConfig('config.yaml').config

# Initialize the Telegram Login Widget
telegram_login = TelegramLoginWidgetComponent(
    bot_username=config['bot_username'],
    secret_key=config['secret_key'],
    button_style=config.get('button_style', 'large'),
    userpic=config.get('userpic', True),
    corner_radius=config.get('corner_radius'),
    request_access=config.get('request_access', True),
    expiry_days=config.get('expiry_days', 30),
)

st.title("Streamlit App with Telegram Login")

# Display the Telegram login button
telegram_login.button

# Check if user is logged in
user_data = telegram_login.get_session
if user_data.get('id'):
    st.success(f"Welcome, {user_data.get('first_name')}!")
    st.write(f"Your Telegram ID is: {user_data.get('id')}")
    
    # Add a logout button
    if st.button("Logout"):
        telegram_login.clear_session()
        st.experimental_rerun()
else:
    st.info("Please log in using Telegram to access the app.")

# Your app's main content goes here
st.header("Main Content")
st.write("This is the main content of your Streamlit app. It can be accessed after logging in.")

# You can add more Streamlit components and logic here
