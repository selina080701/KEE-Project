# image_gallery.py
import pandas as pd
import streamlit as st

# ---- Generate Vehicle Image Overview ----
@st.cache_data
def generate_vehicle_image_overview(df_vehicles):
    df_vehicles = df_vehicles[['image_url',
                               'vehicle',
                               'movie',
                               'sequence']].copy()
    return df_vehicles


# ---- Display Vehicle Image Overview as Cards (medium-sized) ----
@st.cache_data
def display_vehicle_image_overview_large(df_vehicles):
    for idx, row in df_vehicles.iterrows():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if pd.notna(row['image_url']) and row['image_url'] and str(row['image_url']).strip():
                try:
                    st.image(row['image_url'],
                             width='content')
                except Exception as e:
                    st.error(f"Error loading image: {e}")
                    st.write("No image")
            else:
                st.write("No image")
        
        with col2:
            st.write(f"**Vehicle:** {row['vehicle']}")
            st.write(f"**Movie:** {row['movie']}")
            st.write(f"**Sequence:** {row['sequence']}")
        
        st.divider()
