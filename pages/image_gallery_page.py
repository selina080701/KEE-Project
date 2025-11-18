# image_gallery_page.py

import streamlit as st
from utils.data_loader import load_vehicle_data, load_bond_girls_data, load_data, load_german_titles
from utils.image_gallery import (generate_vehicle_image_overview,
                                display_vehicle_image_overview_large,
                                generate_bond_girls_image_overview,
                                display_bond_girls_image_overview_large)

"""
The below functions are displayed in the image page.
"""

def show_image_gallery_page():
    st.sidebar.info("You are on the image gallery page.")

    # ---- Load all necessary data ----
    df_german_titles = load_german_titles()

    df_vehicles = load_vehicle_data()
    vehicles_overview = generate_vehicle_image_overview(df_vehicles, df_german_titles)

    df_bond_girls = load_bond_girls_data()
    df_movies = load_data()
    bond_girls_overview = generate_bond_girls_image_overview(df_bond_girls, df_movies, df_german_titles)

    st.write("### Image Gallery Overview")

    # ---- Tabs for different categories ----
    tab1, tab2, tab3 = st.tabs(["🚗 Vehicles", "💃 Bond Girls", "👹 Villains"])

    with tab1:
        st.write("#### Vehicle Gallery")
        
        # Filter by movie with dropdown box
        search = st.selectbox(
        "Filter by movie:",
        options=[""] + sorted(vehicles_overview['movie'].unique().tolist())
        )

        # show filtered DataFrame
        if search:
            filtered = vehicles_overview[
                vehicles_overview['movie'].str.contains(search, case=False, na=False)
            ]
        else:
            filtered = vehicles_overview

        # Display count of shown (filtered) vehicles
        st.metric(
        f"Displayed Vehicles of total {len(vehicles_overview)}:",
        f"{len(filtered)}",
        )

        display_vehicle_image_overview_large(filtered)
    
    with tab2:
        st.write("#### Bond Girls Gallery")

        # Filter by movie with dropdown box
        search = st.selectbox(
        "Filter by movie:",
        options=[""] + sorted(bond_girls_overview['movie'].unique().tolist())
        )

        # show filtered DataFrame
        if search:
            filtered = bond_girls_overview[
                bond_girls_overview['movie'].str.contains(search, case=False, na=False)
            ]
        else:
            filtered = bond_girls_overview

        # Display count of shown (filtered) vehicles
        st.metric(
        f"Total Number of Bond Girls:",
        f"{len(bond_girls_overview)}"
        )

        display_bond_girls_image_overview_large(filtered)
        
    with tab3:
        st.write("#### Villains Gallery")
        st.write("... will follow ...")