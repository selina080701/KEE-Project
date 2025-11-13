# map_page.py
 
import streamlit as st
import pandas as pd
from utils.data_loader import load_geo_locations


def show_map_page():
    st.sidebar.info("You are on the interactive map page.")
    st.header("Filming Locations")
    geo_locations = load_geo_locations()

    # ---- Search by movie title ----
    movie_search = st.text_input("Filter by movie title:", placeholder="Type a movie to filter...")
    name_search = st.text_input("Filter by location name:", placeholder="Type a location to filter...")
    filtered = geo_locations.copy()

    if movie_search:
        filtered = filtered[filtered['movie'].str.contains(movie_search, case=False, na=False)]
    
    if name_search:
        filtered = filtered[filtered['name'].str.contains(name_search, case=False, na=False)]


    # ---- Load and display geolocation data ----
    df = pd.DataFrame(filtered)
    st.map(df)
    st.dataframe(df)