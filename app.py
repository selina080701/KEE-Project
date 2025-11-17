# app.py

import streamlit as st
from pages.intro_page import show_intro_page
from pages.movie_page import show_movie_page
from pages.rdf_page import show_rdf_page
from pages.characters_page import show_characters_page
from pages.map_page import show_map_page

# ---- Page Configuration and Sidebar Logo ----
st.set_page_config(page_title="James Bond Visualizations", layout="wide", initial_sidebar_state="expanded")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)
st.logo("utils/logo.png", size="large")

# ---- Sidebar with Dropdown ----
st.sidebar.title("Page Navigation")

pages = ["Introduction", "Movie Collection", "RDF-Graph", "Recurring Characters", "Film Locations"]

page_select = st.sidebar.selectbox(
    "What would you like to explore?",
    pages)

# ---- Page routing ----
if page_select == "Introduction":
    show_intro_page()
elif page_select == "Movie Collection":
    show_movie_page()
elif page_select == "RDF-Graph":
    show_rdf_page()
elif page_select == "Recurring Characters":
    show_characters_page()
elif page_select == "Film Locations":
    show_map_page()
