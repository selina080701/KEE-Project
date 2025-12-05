# app.py

import streamlit as st
from utils.page_config import PAGE_CONFIG

# ---- Page Configuration and Sidebar Logo ----
st.set_page_config(page_title="James Bond Visualizations", layout="wide", initial_sidebar_state="expanded")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)
st.logo("utils/logo.png", size="large")

# ---- Sidebar with Dropdown ----
st.sidebar.title("Page Navigation")

page_select = st.sidebar.radio(
    "What would you like to explore?",
    list(PAGE_CONFIG.keys()))

# ---- Page routing ----
if page_select in PAGE_CONFIG:
    PAGE_CONFIG[page_select]()
