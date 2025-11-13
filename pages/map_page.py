# map_page.py
 
import streamlit as st
import pandas as pd
from utils.data_loader import load_geo_locations


def show_map_page():
    st.sidebar.info("You are on the interactive map page.")
    st.header("Interactive Map")

    st.title("A View to a Kill – Filming Locations")
    st.write("## Prototype Interactive Map of Filming Locations")

    # ---- Load and display geolocation data ----
    geo_locations = load_geo_locations()
    df = pd.DataFrame(geo_locations)
    st.map(df)
    st.dataframe(df)