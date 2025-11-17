# characters_page.py

import streamlit as st
from utils.data_loader import load_character_actor_data, load_data
from utils.character_analysis import (prepare_character_data, filter_by_search, filter_recurring_characters,create_pivot_table,
                                      create_scatterplot, prepare_all_characters_display)
 
def show_characters_page():
    st.sidebar.info("You are on the characters analysis page.")
    st.header("Recurring Character Analysis")
    
    # ---- Load and Prepare Data ----
    df_char = load_character_actor_data()
    df_years = load_data()
    df = prepare_character_data(df_char, df_years)
    
    # ---- Filter Controls ----
    col1, col2 = st.columns([2, 1])
    
    with col1:
        min_appearances = st.slider(
            "Minimum appearances:", 
            min_value=2, 
            max_value=20, 
            value=3
        )
    
    # Erst nach min_appearances filtern
    df_filtered_by_appearances, recurring_chars = filter_recurring_characters(df, min_appearances)
    
    with col2:
        # Selectbox mit gefilterten Charakteren
        char_options = [""] + sorted(recurring_chars)
        search_term = st.selectbox(
            "Select a character:", 
            char_options,
            index=0
        )
    
    # ---- Apply Search Filter ----
    df_filtered = filter_by_search(df_filtered_by_appearances, search_term)
    
    # Update recurring_chars after search
    if search_term:
        recurring_chars = df_filtered['character'].unique().tolist()
    
    # ---- Validate Data ----
    if len(df_filtered) == 0:
        st.warning("No characters found with the current filters.")
        return
    
    # ---- View Mode Toggle ----
    view_mode = st.toggle("Switch between Scatterplot and Actor Details", value=False)
    
    st.write("---")
    
    # ---- Render View based on Toggle ----
    if view_mode:
        # Actor Details view - zeigt alle gefilterten Charaktere
        if recurring_chars:
            st.subheader("Actor Details")
            
            display_df = prepare_all_characters_display(df, recurring_chars)
            
            if display_df is not None:
                st.write(
                    display_df.to_html(escape=False, index=False),
                    unsafe_allow_html=True
                )
            else:
                st.warning("No details found for the selected characters.")
    else:
        # Scatterplot view
        pivot, pivot_binary = create_pivot_table(df_filtered)
        fig = create_scatterplot(pivot_binary)
        
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for scatterplot.")