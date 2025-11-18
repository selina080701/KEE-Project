# image_gallery.py
import pandas as pd
import streamlit as st

# ---- Generate Vehicle Image Overview ----
@st.cache_data
def generate_vehicle_image_overview(df_vehicles, df_german_titles):
    df_vehicles = df_vehicles[['image_url',
                               'vehicle',
                               'movie',
                               'sequence']].copy()

    # Merge to german movie titles
    df_vehicles = df_vehicles.merge(
        df_german_titles[['Movie', 'Movie_de']],
        left_on='movie',
        right_on='Movie',
        how='left'
    )
    # Drop duplicate Movie column and rename Movie_de to title_de
    df_vehicles = df_vehicles.drop(columns=['Movie'])
    df_vehicles = df_vehicles.rename(columns={'Movie_de': 'title_de'})

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
            st.write(f"**Movie:** {row['movie']}" + (f" ({row['title_de']})" if pd.notna(row['title_de']) else ""))
            st.write(f"**Sequence:** {row['sequence']}")
        
        st.divider()


# ---- Generate Bond Girls Image Overview ----
@st.cache_data
def generate_bond_girls_image_overview(df_bond_girls, df_movies, df_german_titles):
    df_bond_girls = df_bond_girls[['image_url',
                                   'bond_girl',
                                   'actress',
                               'movie']].copy()
    
    # Merge to df_movie to get the year
    df_bond_girls = df_bond_girls.merge(
        df_movies[['Movie', 'Year']],
        left_on='movie',
        right_on='Movie',
        how='left'
    )
    # Drop duplicate Movie column from first merge
    df_bond_girls = df_bond_girls.drop(columns=['Movie'])

    # Merge to german movie titles
    df_bond_girls = df_bond_girls.merge(
        df_german_titles[['Movie', 'Movie_de']],
        left_on='movie',
        right_on='Movie',
        how='left'
    )
    # Drop duplicate Movie column and rename Movie_de to title_de
    df_bond_girls = df_bond_girls.drop(columns=['Movie'])
    df_bond_girls = df_bond_girls.rename(columns={'Movie_de': 'title_de'})

    # order by year
    df_bond_girls = df_bond_girls.sort_values(by='Year')

    return df_bond_girls


# ---- Display Bond Girls Image Overview as Cards (medium-sized) ----
@st.cache_data
def display_bond_girls_image_overview_large(df_bond_girls):
    for idx, row in df_bond_girls.iterrows():
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
            st.write(f"**Year:** {row['Year']}")
            st.write(f"**Bond Girl:** {row['bond_girl']}")
            st.write(f"**Actress:** {row['actress']}")
            st.write(f"**Movie:** {row['movie']}" + (f" ({row['title_de']})" if pd.notna(row['title_de']) else ""))


        
        st.divider()
