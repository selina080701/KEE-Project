import pandas as pd
import streamlit as st

"""
Helper function to load datasets with caching.
"""

# ---- Load dataset with caching ----
@st.cache_data
def load_data():
    df = pd.read_csv('data/jamesbond_clean.csv', 
                     sep=';', encoding='utf-8')
    return df

@st.cache_data
def load_ttl():
    with open('rdf/jamesbond_rdf.ttl', 'r', encoding='utf-8') as file:
        ttl_data = file.read()
    return ttl_data