# character_analysis.py

import pandas as pd
import streamlit as st
import plotly.express as px

"""
Helper functions for the characters page.
"""

# ---- Prepare character data with movie years and german titles ----
@st.cache_data
def prepare_character_data(df_char, df_years, df_german_titles):
    """Merge character data with movie years and German titles, create combined labels."""
    # Merge with years
    df = df_char.merge(
        df_years[['Year', 'Movie']],
        left_on='movie',
        right_on='Movie',
        how='left'
    )
    df = df.drop(columns=['Movie'])

    # Merge with German titles
    df = df.merge(
        df_german_titles[['Movie', 'Movie_de']],
        left_on='movie',
        right_on='Movie',
        how='left'
    )
    df = df.drop(columns=['Movie'])

    df = df.sort_values(by=['Year', 'movie'])
    df['movie_year'] = df.apply(lambda row: f"{row['Year']} - {row['movie']}", axis=1)
    return df


# ---- Get recurring characters ----
@st.cache_data
def get_recurring_characters(df, min_appearances):
    """Return list of characters with at least min_appearances."""
    char_counts = df['character'].value_counts()
    return char_counts[char_counts >= min_appearances].index.tolist()


# ---- Filter dataframe by character list ----
def filter_by_characters(df, characters):
    """Filter dataframe to only include specified characters."""
    return df[df['character'].isin(characters)]


# ---- Filter by exact character name ----
def filter_by_character_name(df, character_name):
    """Filter dataframe to exact character name match."""
    if character_name:
        return df[df['character'] == character_name]
    return df


# ---- Create scatterplot ----
@st.cache_data
def create_scatterplot(df_filtered):
    """Create a plotly scatterplot showing character appearances across movies."""
    if len(df_filtered) == 0:
        return None

    # Create pivot table
    pivot = df_filtered.pivot_table(
        index='character',
        columns='movie_year',
        values='actor',
        aggfunc='first',
        fill_value=""
    )
    pivot_binary = pivot.map(lambda x: 1 if x else 0)

    # Create scatter data
    scatter_df = pivot_binary.reset_index().melt(
        id_vars='character',
        var_name='movie_year',
        value_name='appears'
    )
    scatter_df = scatter_df[scatter_df['appears'] == 1]

    if len(scatter_df) == 0:
        return None

    # Merge to get german movie titles and actors for hover info
    scatter_df = scatter_df.merge(
            df_filtered[['character', 'movie_year', 'Movie_de', 'actor']],
            on=['character', 'movie_year'],
            how='left'
        )

    fig = px.scatter(
        scatter_df,
        x="character",
        y="movie_year",
        color="appears",
        color_discrete_sequence=["blue"],
        size=[2] * len(scatter_df),
        custom_data=['Movie_de', 'actor']
    )

    fig.update_traces(
        marker=dict(symbol="circle", opacity=0.9),
        hovertemplate='<b>%{customdata[0]}</b><br>%{x}<br>%{customdata[1]}<extra></extra>'
    )

    num_movies = scatter_df['movie_year'].nunique()
    dynamic_height = max(700, num_movies * 40)  # Adjust height based on number of movies: max 600px, 30px per movie

    fig.update_layout(
        xaxis=dict(side="top"),
        height=dynamic_height,
        xaxis_tickangle=-45,
        showlegend=False
    )
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(tickfont=dict(size=14), showgrid=False, dtick=1, title="")
    fig.update_xaxes(tickfont=dict(size=14), showgrid=True, title="")

    return fig


# ---- Prepare character details for display ----
@st.cache_data
def prepare_character_details(df, character_list):
    """Get character details for all characters in the list and format for display."""
    all_details = []

    for character in sorted(character_list):
        char_df = df[df['character'] == character].copy()
        char_df = char_df.sort_values('Year')

        if len(char_df) > 0:
            char_df["image"] = char_df["image_url"].apply(
                lambda url: f'<img src="{url}" width="100">' if pd.notna(url) else ""
            )
            # Combine English and German titles in one column
            char_df["movie_combined"] = char_df.apply(
                lambda row: f"{row['movie']}<br><i>{row['Movie_de']}</i>" if pd.notna(row['Movie_de']) else row['movie'],
                axis=1
            )
            display_df = char_df[['character', 'movie_combined', 'actor', 'Year', 'image']]
            display_df = display_df.rename(columns={'movie_combined': 'movie'})
            all_details.append(display_df)

    if all_details:
        return pd.concat(all_details, ignore_index=True)

    return None
