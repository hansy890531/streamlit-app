import streamlit as st
import streamlit.components.v1 as components

# Declare the custom component
telegram_web_app = components.declare_component("telegram_web_app", path="./frontend")

# Main Streamlit app
def main():
    st.title("Telegram Web App with Streamlit")
    
    # Placeholder for the user data
    user_data = telegram_web_app(user_data=None)
    
    # Display user data if available
    if user_data:
        st.write("User Data from Telegram Web App:")
        st.json(user_data)
    else:
        st.write("Waiting for user data from Telegram Web App...")

if __name__ == "__main__":
    main()
