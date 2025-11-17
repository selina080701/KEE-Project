# movie_overview.py

import pandas as pd
import streamlit as st

"""
The below functions are displayed in the movie page.
"""

# ---- Get an overview of the James Bond Movies ----
@st.cache_data
def get_movie_overview(df, df_posters, df_german_titles):
    overview = df[['Year', 'Movie', 'Bond', 'Director', 'Avg_User_IMDB', 'Avg_User_Rtn_Tom']].copy()
    df_posters = df_posters.copy()
    df_posters['title'] = df_posters['title'].str.replace(' (film)', '', regex=False)

    # Merge German titles based on the English movie title
    overview = overview.merge(
        df_german_titles[['Movie', 'Movie_de']],
        on='Movie',
        how='left'
    )

    # Merge poster URLs based on movie title
    overview = overview.merge(
        df_posters[['title', 'poster_url']], 
        left_on='Movie', 
        right_on='title', 
        how='left'
    )

    # Drop the duplicate title column
    overview = overview.drop(columns=['title'])

    # Reorder columns to have poster_url first, then sort by Year and rename Poster column
    cols = ['poster_url', 'Year', 'Movie', 'Movie_de', 'Bond', 'Director', 'Avg_User_IMDB', 'Avg_User_Rtn_Tom']
    overview = overview[cols].sort_values(by='Year').reset_index(drop=True)
    overview = overview.rename(columns={'poster_url': 'Poster'})

    return overview


# ---- Display Movie Overview as Cards (medium-sized) ----
@st.cache_data
def display_movie_overview_large(overview_df):
    for idx, row in overview_df.iterrows():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if pd.notna(row['Poster']) and row['Poster'] and str(row['Poster']).strip():
                try:
                    st.image(row['Poster'],
                             width='content')
                except Exception as e:
                    st.error(f"Error loading image: {e}")
                    st.write("No poster")
            else:
                st.write("No poster")
        
        with col2:
            st.subheader(f"{row['Movie']} ({row['Year']})")
            st.markdown(
                f"<span style='font-size:18px; font-weight:bold;'>{row['Movie_de']}</span>",
                unsafe_allow_html=True
            )
            st.write(f"**Bond:** {row['Bond']}")
            st.write(f"**Director:** {row['Director']}")
            st.write(f"**IMDB:** {row['Avg_User_IMDB']:.1f} ⭐ | **RT:** {row['Avg_User_Rtn_Tom']:.1f} 🍅")
        st.divider()


# ---- Display DataFrame with image thumbnails ----
@st.cache_data
def display_movie_overview_thumbnails(overview_df):
    st.dataframe(
        overview_df,
        column_config={
            "Poster": st.column_config.ImageColumn(
                "Poster",
                help="double-click to enlarge",
                width="small"  # Options: "small", "medium", "large"
            ),
            "Year": st.column_config.NumberColumn(
                "Year",
                format="%d"
            ),
            "Movie_de": st.column_config.TextColumn(
                "Movie (DE)"
            ),
            "Avg_User_IMDB": st.column_config.NumberColumn(
                "IMDB Rating",
                format="%.1f ⭐"
            ),
            "Avg_User_Rtn_Tom": st.column_config.NumberColumn(
                "Rotten Tomatoes",
                format="%.1f 🍅"
            )
        },
        hide_index=True,
        use_container_width=True
    )