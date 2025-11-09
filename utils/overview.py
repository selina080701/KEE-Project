import pandas as pd
import streamlit as st

"""
The below functions are displayed in the intro page.
"""

# ---- Get an overview of the James Bond Movies ----
@st.cache_data
def get_movie_overview(df):
    overview = df[['Year', 'Movie', 'Bond', 'Director', 'Avg_User_IMDB', 'Avg_User_Rtn_Tom']]
    return overview