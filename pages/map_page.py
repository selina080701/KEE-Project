# map_page.py
 
import streamlit as st
import pandas as pd
from utils.data_loader import load_geo_locations


def show_map_page():
    st.sidebar.info("You are on the interactive map page.")
    st.header("Filming Locations")
    geo_locations = load_geo_locations()

    # ---- Search by movie title ----
    movie_search = st.selectbox("Filter by movie title:", options=geo_locations['movie'].unique(), index=None, placeholder="Select a movie to filter...")
    name_search = st.selectbox("Filter by location name:", options=geo_locations['name'].unique(), index=None, placeholder="Select a location to filter...")
    filtered = geo_locations.copy()
    filtered['movie_combined'] = filtered['movie'] + ' (' + filtered['Movie_de'] + ')'

    if movie_search:
        filtered = filtered[filtered['movie_combined'].str.contains(movie_search, case=False, na=False)]
    
    if name_search:
        filtered = filtered[filtered['name'].str.contains(name_search, case=False, na=False)]


    # ---- Load data -----
    df = pd.DataFrame(filtered[['movie_combined', 'name', 'lat', 'lon']])
    df = df.rename(columns={'movie_combined': 'movie'})

    # ---- Show map and dataframe below ----
    st.map(df)
    st.dataframe(df)