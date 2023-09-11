import streamlit as st
import pandas as pd

# Load the CSV data
# data = pd.read_csv('./parsed_chat_박흥순_0817.csv')
data = pd.read_excel('./parsed_chat_홍경태.xlsx')
data['날짜'] = pd.to_datetime(data['날짜'], format='%Y년 %m월 %d일').dt.date
data['메시지'] = data['메시지'].replace("\n\n", "\n", regex=True).replace("\n", "<br>", regex=True)

# Set page configuration
st.set_page_config(
    page_title='Chat Viewer', 
    layout='wide',
    initial_sidebar_state='auto',
)

# Set theme
st.markdown("""
    <style>
    body {
        color: #000;
        background-color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .chat-message {
        font-size: 16px;
        font-family: Arial;
        color: black;
        background-color: lightgray;  # Background color of the chat bubble
        border-radius: 10px;  # Rounded border
        padding: 10px;
        margin: 10px;
        max-width: 50%;
        word-wrap: break-word;
    }
    body {
        background-color: white;  # Background color of the page
    }
    </style>
    """, unsafe_allow_html=True)
# Get a list of unique user names
user_names = data['사용자 이름'].unique()

# Add an "All" option to the list of user names
user_names = list(user_names)
user_names.insert(0, '[전체내용]')

# Use a sidebar to allow the user to select a user name
selected_user = st.sidebar.selectbox("Select a user", user_names)

# Get a list of unique dates
unique_dates = data['날짜'].unique()
unique_dates = sorted(list(unique_dates), reverse=True)  # Sort the dates in descending order

# Add an "All" option to the list of dates
unique_dates.insert(0, '[전체내용]')

# Use a sidebar to allow the user to select a date
selected_date = st.sidebar.selectbox("Select a date", unique_dates, index=1)  # Set the default selected date to the most recent date

# Filter the data based on the selected user name and date
if selected_user != '[전체내용]':
    data = data[(data['사용자 이름'] == selected_user)]

if selected_date != '[전체내용]':
    data = data[data['날짜'] == selected_date]

# Display the messages
for i, row in data.iterrows():
    st.markdown(f"**{row['사용자 이름']} ({row['날짜']})({row['시간']})**\n<div class='chat-message'>{row['메시지']}</div>", unsafe_allow_html=True)

# Remove "Made with Streamlit"
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
