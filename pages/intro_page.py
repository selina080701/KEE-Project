# intro_page.py

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.data_loader import load_data, load_poster_urls
from utils.overview import get_movie_overview, display_movie_overview

def show_intro():
    st.markdown(
        """
        This application visualizes data about James Bond movies, directors, and actors.
        Please choose a visualization from the dropdown menu.
        """
    )
    st.sidebar.info("This is the introduction page.")
    
    # Load data
    df = load_data()
    df_posters = load_poster_urls()

    # Create Movie Overview with Posters
    movie_overview = get_movie_overview(df, df_posters)

    # Header
    st.write("### Movie Collection Overview")
    st.metric("Total Movies", len(movie_overview))

    # Search functionality
    search = st.text_input("Search movies:", placeholder="Type to filter...")
  
    if search:
        filtered = movie_overview[movie_overview['Movie'].str.contains(search, case=False, na=False)]
    else:
        filtered = movie_overview

    # Display count of shown (filtered) movies
    st.caption(f"Showing {len(filtered)} of {len(movie_overview)} movies")

    # Display movie overview as cards
    display_movie_overview(filtered)


