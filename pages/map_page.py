# map_page.py
 
import streamlit as st
import pandas as pd
from utils.data_loader import load_geo_locations



def show_interactive_map():
    st.header("Interactive Map)")
    st.sidebar.info("This is the interactive map page.")

    st.title("Prototype: A View to a Kill – Filming Locations")

    geo_locations = load_geo_locations()
    df = pd.DataFrame(geo_locations)
    st.map(df)
    st.dataframe(df)