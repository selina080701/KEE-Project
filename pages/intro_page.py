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
    This application visualizes data about James Bond movies, directors and actors.

    - From an overview of a **full movie collection**,
    - to a **knowledge graph of relationships** and
    - a **timeline of films**,  
    - right up to a **global map of filming locations**.  

    Use the dropdown menu in the sidebar or the buttons below to select your preferred visualization.
    """)
    

"""
--> under construction:

    # ---- Call to Action Buttons ----
    st.markdown("#### Start Exploring:")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Go to Movie Collection"):
            st.session_state["page_select"] = "Movie Collection"
    with col2:
        if st.button("Go to RDF-Graph"):
            st.session_state["page_select"] = "RDF-Graph"
    with col3:
        if st.button("Go to Movie Chronology"):
            st.session_state["page_select"] = "Movie Chronology"
    with col4:
        if st.button("Go to Film Locations"):
            st.session_state["page_select"] = "Film Locations"

"""