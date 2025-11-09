import streamlit as st
from pages.intro import show_intro
from pages.rdf_graph import show_rdf_graph
from pages.timeline import show_timeline
from pages.map import show_interactive_map

# ---- Page Configuration ----
st.set_page_config(page_title="James Bond Visualizations", layout="wide")

# ---- Header ----
st.title("Welcome to the James Bond Universe")

# ---- Sidebar with Dropdown ----
st.sidebar.title("Visualizations")

page = st.sidebar.selectbox(
    "What would you like to explore?",
    ("Intro", "RDF-Graph", "Timeline", "Interactive Map")
)

# ---- Page routing ----
if page == "Intro":
    show_intro()
elif page == "RDF-Graph":
    show_rdf_graph()
elif page == "Timeline":
    show_timeline()
elif page == "Interactive Map":
    show_interactive_map()
