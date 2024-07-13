import streamlit as st

def add_custom_css():
    css_style = """
    <style>
    [data-testid="manage-app-button"] {
        display: none;
    }
    </style>
    """
    st.markdown(css_style, unsafe_allow_html=True)

# 커스텀 CSS를 추가합니다.
add_custom_css()

# 헤더를 추가합니다.
st.header("한남2구역 Dashboard")
