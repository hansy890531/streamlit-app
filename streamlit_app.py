import streamlit as st
import os

# 현재 파일의 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# html 파일 경로
html_file_path = os.path.join(current_dir, 'main.html')

# html 파일 읽기
with open(html_file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# iframe으로 html 삽입
st.components.v1.html(html_content, height=600)
