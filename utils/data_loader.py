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

# ---- Load Characters and Actors TTL-dataset with caching ----
@st.cache_data
def load_characters_ttl():
    with open('rdf/jamesbond_characters_rdf.ttl', 'r', encoding='utf-8') as file:
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


# ---- Load geocoded locations with caching ----
@st.cache_data
def load_geo_locations():
    try:
        df_locations = pd.read_csv('extract_knowledge/geocoded_locations/all_movies_geocoded.csv', sep=',', encoding='utf-8')
        return df_locations
    except FileNotFoundError:
        st.warning("Geocoded Locations-Datei nicht gefunden.")
        return pd.DataFrame(columns=['name', 'lat', 'lon'])
    
# ---- Load character-actor pairs with caching ----
@st.cache_data
def load_character_actor_data():
    try:
        df_characters = pd.read_csv('extract_knowledge/characters/all_movie_characters.csv', sep=';', encoding='utf-8')
        return df_characters
    except FileNotFoundError:
        st.warning("Character-Actor Datei nicht gefunden.")
        return pd.DataFrame(columns=['character', 'actor', 'movie'])
    
