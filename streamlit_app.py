import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV data
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


# Box layout CSS for displaying the total user count
box_layout_css = """
    <style>
        .stat-box {
            # background-color: #F0F2F6;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            margin: 10px 0;
            max-width: 50%;
        }
    </style>
"""

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

st.markdown(box_layout_css, unsafe_allow_html=True)
if (selected_date != '[전체내용]') and (selected_user == '[전체내용]'):
    # Display total user count in a box
    unique_users_count = data['사용자 이름'].nunique()
    st.markdown(f'<div class="stat-box"><h2>{unique_users_count}</h2><p>대화에 참여한 사람 수</p></div>', unsafe_allow_html=True)

    # Display a bar chart for messages per user
    messages_per_user = data['사용자 이름'].value_counts().sort_values(ascending=False)
    top_10_messages_per_user = messages_per_user.head(10)
    # chart = st.bar_chart(data=top_10_messages_per_user)
    # Convert the pandas Series to a Plotly bar chart
    fig = px.bar(top_10_messages_per_user, 
                x=top_10_messages_per_user.index, 
                y=top_10_messages_per_user.values, 
                labels={'x': '사용자', 'y': '대화수'}, 
                title="대화 상위 10명",
                text=top_10_messages_per_user.values) 
    # 막대의 텍스트 위치 조정
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    # Display the Plotly chart
    st.plotly_chart(fig)

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
