import streamlit as st
from src.ui import render_app

st.set_page_config(
    page_title="StudyFlow AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_app()