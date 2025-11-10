# data_loader.py
 
import pandas as pd
import streamlit as st

"""
Helper function to load datasets with caching.
"""

# ---- Load main CSV-dataset with caching ----
@st.cache_data
def load_data():
    df = pd.read_csv('data/jamesbond_with_id.csv', 
                     sep=';', encoding='utf-8')
    return df


# ---- Load main TTL-dataset with caching ----
@st.cache_data
def load_ttl():
    with open('rdf/jamesbond_rdf.ttl', 'r', encoding='utf-8') as file:
        ttl_data = file.read()
    return ttl_data

# ---- Load poster URLs with caching ----
@st.cache_data
def load_poster_urls():
    try:
        df_posters = pd.read_csv('extract_knowledge/movie_posters/movie_poster_url.csv')
        
        # Remove '/revision/latest' parameter from URLs (it may cause issues with image loading)
        df_posters['poster_url'] = df_posters['poster_url'].apply(
            lambda x: x.split('/revision/latest')[0] if pd.notna(x) and '/revision/latest' in str(x) else x
        )
        
        return df_posters
    except FileNotFoundError:
        st.warning("Poster-Datei nicht gefunden.")
        return pd.DataFrame(columns=['title', 'poster_url'])
