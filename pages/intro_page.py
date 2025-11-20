# intro_page.py

import streamlit as st

def show_intro_page():
    st.sidebar.info("You are on the introduction page.")
    
    # ---- James Bond Banner ----
    st.image("utils/banner.png", width=300)

    # ---- Title ----
    st.title("Welcome to the James Bond Universe")
    st.subheader("Dive into the world of 007 - Explore Movies, Actors & More")
    
    # ---- Description on Main Page ----
    st.markdown("""  
    This application visualizes data about James Bond movies:

    - :clapper: From an overview of a **full movie collection**,
    - :link: to a **knowledge graph of relationships**,
    - :busts_in_silhouette: a **recurring characters analysis** and
    - :camera: an **image gallery** of vehicles, bond-girls & villains,
    - :earth_africa: right up to a **global map of filming locations**.  


    Start your journey by navigating through the sidebar – We wish you lots of fun!
                
    Selina Steiner & Tamara Nyffeler
                
    :copyright: 2025  

    ---       
    *Created for the \"Knowledge Engineering and Extraction\" module at FHGR (MSc in Data Visualization)*
    """)

    with st.expander("ℹ️ Data Sources", expanded=False):
        st.markdown("""
        - [Kaggle - James Bond Dataset](https://www.kaggle.com/datasets/dreb87/jamesbond)
        - [James Bond Wiki](https://jamesbond.fandom.com/wiki/James_Bond_Wiki)
        - [Wikipedia - List of James Bond villains](https://en.wikipedia.org/wiki/List_of_James_Bond_villains)
        - [Wikidata](https://www.wikidata.org/)
        - [YouTube](https://www.youtube.com/)
        """)