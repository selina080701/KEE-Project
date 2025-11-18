# image_gallery_page.py

import streamlit as st
from utils.data_loader import load_vehicle_data
from utils.image_gallery import generate_vehicle_image_overview, display_vehicle_image_overview_large

"""
The below functions are displayed in the image page.
"""

def show_image_gallery_page():
    st.sidebar.info("You are on the image gallery page.")

    df_vehicles = load_vehicle_data()
    vehicles_overview = generate_vehicle_image_overview(df_vehicles)

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
        st.write("... will follow ...")
        
    with tab3:
        st.write("#### Villains Gallery")
        st.write("... will follow ...")