# app.py
import streamlit as st
import os

# Set page config
st.set_page_config(page_title="Telegram Web App", page_icon="🚀", layout="wide")

# Read HTML file
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, 'main.html')

try:
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Insert HTML content
    st.components.v1.html(html_content, height=600, scrolling=True)
except FileNotFoundError:
    st.error("HTML file not found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Add Streamlit elements if needed
st.write("This is a Streamlit app embedding a Telegram Web App.")
