# 余振中 (Yu Chen Chung)
# pages/image_preprocess_ui.py
import streamlit as st
import requests
from PIL import Image
import io
import os
from datetime import datetime
from pathlib import Path

def show():
    if "original_image" not in st.session_state:
        st.session_state["original_image"] = None

    if "processed_image" not in st.session_state:
        st.session_state["processed_image"] = None

    st.header("🖼️ 圖像前處理工具")

    uploaded_file = st.file_uploader("請上傳圖片", type=["jpg", "jpeg", "png"])
    mode = st.selectbox("請選擇處理模式", [
        "grayscale", "resize", "edge",
        "blur", "sharpen", "rotate", "flip_horizontal", "invert"
    ])

    # 處理圖片
    if uploaded_file and st.button("執行處理"):
        files = {'file': uploaded_file}
        data = {'mode': mode}

        try:
            res = requests.post("https://imageprep-api.onrender.com/process-image", files=files, data=data)
            if res.status_code == 200:
                st.session_state["original_image"] = Image.open(uploaded_file)
                st.session_state["processed_image"] = Image.open(io.BytesIO(res.content))
                st.session_state["mode_used"] = mode
            else:
                st.error(f"錯誤：{res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"請求失敗：{e}")

    # ✅ 修正顯示圖片比對條件
    if (
        "original_image" in st.session_state and st.session_state["original_image"] is not None and "processed_image" in st.session_state and st.session_state["processed_image"] is not None
    ):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("原始圖片")
            st.image(st.session_state["original_image"], use_container_width=True)
        with col2:
            st.subheader("處理後圖片")
            st.image(st.session_state["processed_image"], use_container_width=True)

    # 另存圖片按鈕
    if st.session_state["processed_image"] is not None and st.button("另存圖片到 [下載] 資料夾"):
        try:
            downloads_dir = str(Path.home() / "Downloads")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode = st.session_state.get("mode_used", "output")
            filename = f"{mode}_{timestamp}.jpg"
            filepath = os.path.join(downloads_dir, filename)

            st.session_state["processed_image"].save(filepath)
            st.success(f"圖片已儲存至：{filepath}")
        except Exception as e:
            st.error(f"儲存圖片失敗：{e}")

