# character_analysis.py

import pandas as pd
import streamlit as st
import plotly.express as px

"""
The below functions are displayed in the characters page.
"""

# ---- Merge character data with movie years ----
@st.cache_data
def merge_with_years(df_char, df_years):
    df = df_char.merge(
        df_years[['Year', 'Movie']],
        left_on='movie',
        right_on='Movie',
        how='left'
    )
    df = df.drop(columns=['Movie'])
    df = df.sort_values(by=['Year', 'movie'])
    df['movie_year'] = df.apply(lambda row: f"{row['Year']} - {row['movie']}", axis=1)
    return df


# ---- Filter recurring characters ----
@st.cache_data
def filter_recurring_characters(df, min_appearances):
    char_counts = df['character'].value_counts()
    recurring_chars = char_counts[char_counts >= min_appearances].index.tolist()
    df_filtered = df[df['character'].isin(recurring_chars)]
    return df_filtered, recurring_chars


# ---- Filter by search term: character or actor ----
@st.cache_data
def filter_by_search(df, search_term):
    if search_term:
        mask = (
            df['character'].str.contains(search_term, case=False, na=False) |
            df['actor'].str.contains(search_term, case=False, na=False)
        )
        return df[mask]
    return df


# ---- Create pivot table for visualization ----
@st.cache_data
def create_pivot_table(df_filtered):
    pivot = df_filtered.pivot_table(
        index='character',
        columns='movie_year',
        values='actor',
        aggfunc='first',
        fill_value=""
    )
    pivot_binary = pivot.applymap(lambda x: 1 if x else 0)
    return pivot, pivot_binary


# ---- Create scatterplot data ----
@st.cache_data
def create_scatter_data(pivot_binary):
    scatter_df = pivot_binary.reset_index().melt(
        id_vars='character',
        var_name='movie_year',
        value_name='appears'
    )
    scatter_df = scatter_df[scatter_df['appears'] == 1]
    return scatter_df


# ---- Get character details for selected character ----
@st.cache_data
def get_character_details(df, character_name):
    char_df = df[df['character'] == character_name].copy()
    char_df = char_df.sort_values('Year')
    return char_df


# ---- Convert image URL to HTML img tag ----
@st.cache_data
def make_image_html(url):
    return f'<img src="{url}" width="100">' if pd.notna(url) else ""


# ---- Prepare complete character dataset ----
@st.cache_data
def prepare_character_data(df_char, df_years):
    """Merge character data with movie years and create combined labels."""
    return merge_with_years(df_char, df_years)


# ---- Apply all filters to character data ----
@st.cache_data
def apply_filters(df, min_appearances, search_term):
    """Apply recurring character filter and search filter in one go."""
    df_filtered, recurring_chars = filter_recurring_characters(df, min_appearances)
    df_filtered = filter_by_search(df_filtered, search_term)
    
    # Update recurring_chars after search
    if search_term:
        recurring_chars = df_filtered['character'].unique().tolist()
    
    return df_filtered, recurring_chars


# ---- Create scatterplot figure ----
@st.cache_data
def create_scatterplot(pivot_binary):
    """Create a plotly scatterplot from binary pivot data."""
    scatter_df = create_scatter_data(pivot_binary)
    
    if len(scatter_df) == 0:
        return None
    
    fig = px.scatter(
        scatter_df,
        x="character",
        y="movie_year",
        color="appears",
        color_discrete_sequence=["blue"],
        size=[2] * len(scatter_df),
    )
    
    fig.update_traces(marker=dict(symbol="circle", opacity=0.9))
    
    fig.update_layout(
        xaxis=dict(side="top"),
        height=max(1000, len(pivot_binary) * 50),
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    fig.update_coloraxes(showscale=False)
    
    fig.update_yaxes(
        tickfont=dict(size=14),
        showgrid=False,
        dtick=1,
        title=""
    )
    
    fig.update_xaxes(
        tickfont=dict(size=14),
        showgrid=True,
        title=""
    )
    
    return fig


# ---- Prepare all character details for filtered characters ----
@st.cache_data
def prepare_all_characters_display(df, character_list):
    """Get character details for all characters in the list and format for display."""
    all_details = []
    
    for character in sorted(character_list):
        char_df = get_character_details(df, character)
        
        if len(char_df) > 0:
            char_df["image"] = char_df["image_url"].apply(make_image_html)
            char_df["character"] = character  # Add character name to each row
            display_df = char_df[['character', 'movie', 'actor', 'Year', 'image']]
            all_details.append(display_df)
    
    if all_details:
        return pd.concat(all_details, ignore_index=True)
    
    return None