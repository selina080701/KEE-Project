import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.overview import get_movie_overview


def show_intro():
    st.markdown(
        """
        This application visualizes data about James Bond movies, directors, and actors.
        Please chose a visualization from the dropdown menu.
        """
    )
    st.sidebar.info("This is the introduction page.")
    
    df = load_data()
    st.write("### Movie Collection Overview")
    movie_overview = get_movie_overview(df)
    st.metric("Total Movies", len(movie_overview))

    search = st.text_input("Search movies:", placeholder="Type to filter...")
    
    if search:
        filtered = movie_overview[movie_overview['Movie'].str.contains(search, case=False)]
    else:
        filtered = movie_overview
    
    st.dataframe(
        filtered,
        use_container_width=True,
        height=400,
        hide_index=True
    )

    st.caption(f"Showing {len(filtered)} of {len(movie_overview)} movies")


 