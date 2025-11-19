# characters_page.py

import streamlit as st
from utils.data_loader import load_character_actor_data, load_data, load_german_titles
from utils.character_analysis import (
    prepare_character_data,
    get_recurring_characters,
    filter_by_characters,
    filter_by_character_name,
    create_scatterplot,
    prepare_character_details
)

"""
The below functions are displayed in the characters page.
"""

def show_characters_page():
    st.sidebar.info("You are on the characters analysis page.")
    st.header("Recurring Character Analysis")

    # ---- Load and Prepare Data ----
    df_char = load_character_actor_data()
    df_years = load_data()
    df_german_titles = load_german_titles()
    df = prepare_character_data(df_char, df_years, df_german_titles)

    # ---- Filter Controls ----
    col1, col2 = st.columns([2, 1])

    with col1:
        min_appearances = st.slider(
            "Minimum appearances:",
            min_value=2,
            max_value=20,
            value=3
        )

    # Get recurring characters based on min_appearances
    recurring_chars = get_recurring_characters(df, min_appearances)

    with col2:
        char_options = [""] + sorted(recurring_chars)
        selected_character = st.selectbox(
            "Select a character:",
            char_options,
            index=0
        )

    # ---- Apply Filters ----
    df_filtered = filter_by_characters(df, recurring_chars)

    if selected_character:
        df_filtered = filter_by_character_name(df_filtered, selected_character)
        display_chars = [selected_character]
    else:
        display_chars = recurring_chars

    # ---- Validate Data ----
    if len(df_filtered) == 0:
        st.warning("No characters found with the current filters.")
        return

    # ---- View Mode Toggle ----
    view_mode = st.toggle("Switch between Scatterplot and Actor Details", value=False)

    st.write("---")

    # ---- Render View ----
    if view_mode:
        # Actor Details view
        st.subheader("Actor Details")
        display_df = prepare_character_details(df, display_chars)

        if display_df is not None:
            st.write(
                display_df.to_html(escape=False, index=False),
                unsafe_allow_html=True
            )
        else:
            st.warning("No details found for the selected characters.")
    else:
        # Scatterplot view
        fig = create_scatterplot(df_filtered)

        if fig:
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No data available for scatterplot.")
