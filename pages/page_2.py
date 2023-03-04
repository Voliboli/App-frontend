import streamlit as st
import st_pages as stp

stp.show_pages(
    [
        stp.Page("app.py", "Home", "🏠"),
        stp.Page("pages/page_1.py", "Upload & Visualize", "📄"),
        stp.Page("pages/page_2.py", "Select & Analyze", "🏆")
    ]
)

st.set_page_config(page_title="Select & Analyze", page_icon="🏐")