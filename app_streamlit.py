# 余振中 (Yu Chen Chung)
# app_streamlit.py
import streamlit as st
from pages import image_preprocess_ui

st.set_page_config(page_title="AI 多功能工具平台", layout="wide")

st.sidebar.title("🛠️ AI 小工具選單")
option = st.sidebar.selectbox("請選擇功能", [
    "圖像前處理",
    # 未來可擴充其他功能模組
])

if option == "圖像前處理":
    image_preprocess_ui.show()
