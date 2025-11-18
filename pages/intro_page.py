# intro_page.py

import streamlit as st

def show_intro_page():
    st.sidebar.info("You are on the introduction page.")
    
    # ---- James Bond Banner ----
    st.image("utils/banner.png", width=300)

    # ---- Title ----
    st.title("Welcome to the James Bond Universe")
    st.subheader("Dive into the world of 007 - Explore Movies, Directors & Actors")
    
    # ---- Description on Main Page ----
    st.markdown("""  
    This application visualizes data about James Bond movies:

    - From an overview of a **full movie collection**,
    - to a **knowledge graph of relationships**,
    - a **recurring characters analysis** and
    - a **image gallery** of vehicles, bond-girls & villains,
    - right up to a **global map of filming locations**.  


    Start your journey by navigating through the sidebar – We wish you lots of fun!
                
    Selina Steiner & Tamara Nyffeler
                
    :copyright: 2025  

    ---       
    *Created for the \"Knowledge Engineering and Extraction\" module at FHGR (MSc in Data Visualization)*
    """)
    