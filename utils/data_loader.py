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

# ---- Load german movie title ----
@st.cache_data
def load_german_titles():
    """
    Load German movie titles and align column names with the main dataset.
    """
    df_titles = pd.read_csv('extract_knowledge/movie_title_german/movie_title_en_de.csv', encoding='utf-8')
    # Assuming columns: title_en, title_de
    df_titles = df_titles.rename(columns={
        "title_en": "Movie",
        "title_de": "Movie_de"
    })
    return df_titles

# ---- Load main TTL-dataset with caching ----
@st.cache_data
def load_ttl():
    with open('rdf/jamesbond_rdf.ttl', 'r', encoding='utf-8') as file:
        ttl_data = file.read()
    return ttl_data

# ---- Load Bond info TTL (separate RDF graph) ----
@st.cache_data
def load_bond_info_ttl():
    """
    Load the RDF data containing detailed Bond actor information.
    """
    with open("extract_knowledge/actor_info/bond_actor_info.ttl", "r", encoding="utf-8") as file:
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
        st.warning("Poster File not found.")
        return pd.DataFrame(columns=['title', 'poster_url'])

# ---- Load geocoded locations with caching ----
@st.cache_data
def load_geo_locations():
    try:
        df_locations = pd.read_csv('extract_knowledge/geocoded_locations/all_movies_geocoded.csv', sep=',', encoding='utf-8')

        # Merge with German titles
        df_titles = load_german_titles()
        df_locations = df_locations.merge(
            df_titles,
            left_on='movie',
            right_on='Movie',
            how='left'
        )
        df_locations = df_locations.drop(columns=['Movie'])
        return df_locations
    except FileNotFoundError:
        st.warning("Geocoded Locations File not found.")
        return pd.DataFrame(columns=['name', 'movie', 'Movie_de', 'lat', 'lon'])
    
# ---- Load character-actor pairs with caching ----
@st.cache_data
def load_character_actor_data():
    try:
        df_characters = pd.read_csv('extract_knowledge/characters/all_movie_characters_with_image.csv', sep=';', encoding='utf-8')
        return df_characters
    except FileNotFoundError:
        st.warning("Character-Actor File not found.")
        return pd.DataFrame(columns=['character', 'actor', 'movie', 'image_url', 'search_title'])
    
# ---- Load vehicle data with caching ----
@st.cache_data
def load_vehicle_data():
    try:
        df_vehicles = pd.read_csv('extract_knowledge/vehicles/all_movie_vehicles_with_image.csv', sep=';', encoding='utf-8')
        return df_vehicles
    except FileNotFoundError:
        st.warning("Vehicle File not found.")
        return pd.DataFrame(columns=['vehicle', 'sequence', 'movie', 'image_url'])
    
# ---- Load bond girls data with caching ----
@st.cache_data
def load_bond_girls_data():
    try:
        df_bond_girls = pd.read_csv('extract_knowledge/bond_girls/bond_girls_with_images.csv', sep=';', encoding='utf-8')
        return df_bond_girls
    except FileNotFoundError:
        st.warning("Bond Girls File not found.")
        return pd.DataFrame(columns=['bond_girl', 'actress', 'movie', 'image_url', 'search_title'])
    
# ---- Load song data with caching ----
@st.cache_data
def load_song_data():
    try:
        df_songs = pd.read_csv('extract_knowledge/songs/all_movie_songs.csv', sep=';', encoding='utf-8')
        return df_songs
    except FileNotFoundError:
        st.warning("Song File not found.")
        return pd.DataFrame(columns=['movie', 'song', 'performer', 'composer', 'youtube_link'])

# ---- Load villains data with caching ----
@st.cache_data
def load_villains_data():
    try:
        df_villains = pd.read_csv('extract_knowledge/villains/villains_with_images.csv', sep=';', encoding='utf-8')
        return df_villains
    except FileNotFoundError:
        st.warning("Villains File not found.")
        return pd.DataFrame(columns=['Film', 'Villain', 'Portrayed by', 'Objective', 'Outcome', 'Status', 'Image URL' ])