# intro_page.py

import streamlit as st
from utils.data_loader import load_data, load_poster_urls
from utils.movie_overview import get_movie_overview, display_movie_overview_large, display_movie_overview_thumbnails

def show_movie_page():
    st.sidebar.info("You are on the movie overview page.")
    
    # ---- Load data and create overview ----
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


    # ---- Display mode switch ----
    view_mode = st.toggle("Switch between Poster-View and Table-View", value=False)

    st.write("---")
    if view_mode:
        display_movie_overview_thumbnails(filtered) # activate table view
    else:
        display_movie_overview_large(filtered)  # activate card view
