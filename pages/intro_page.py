# intro_page.py

import streamlit as st

def show_intro_page():
    st.sidebar.info("You are on the introduction page.")

    # ---- James Bond Banner ----
    st.image("utils/banner.png", width=300)

    # ---- Title ----
    st.title("Welcome to the James Bond Universe")
    st.subheader("Dive into the world of 007 - Explore Movies, Actors & More")

    # ---- Tabs for Key Features and Key Findings ----
    tab1, tab2 = st.tabs(["Key Features", "Key Finding & Obstacles"])

    with tab1:
        st.markdown("""
        This application visualizes data about James Bond movies:

        - :clapper: From an overview of a **full movie collection**,
        - :link: to a **knowledge graph of relationships**,
        - :busts_in_silhouette: a **recurring characters analysis** and
        - :camera: an **image gallery** of vehicles, bond-girls & villains,
        - :earth_africa: right up to a **global map of filming locations**.


        Start your journey by navigating through the sidebar – We wish you lots of fun!\n
        Selina Steiner & Tamara Nyffeler\n
        :copyright: 2025

        ---
        *Created for the \"Knowledge Engineering and Extraction\" module at FHGR (MSc in Data Visualization)*
        """)

        with st.expander("ℹ️ Data Sources", expanded=False):
            st.markdown("""
            - [Kaggle - James Bond Dataset](https://www.kaggle.com/datasets/dreb87/jamesbond)
            - [James Bond Wiki](https://jamesbond.fandom.com/wiki/James_Bond_Wiki)
            - [Wikipedia - List of James Bond villains](https://en.wikipedia.org/wiki/List_of_James_Bond_villains)
            - [Wikidata](https://www.wikidata.org/)
            - [YouTube](https://www.youtube.com/)
            - [007 Logo Intro Page](https://www.pngegg.com/en/png-ecmnv)
            """)              

    with tab2:
        st.markdown("""
        #### Knowledge Extraction with Structured Data
        - ✅ The Kaggle dataset provided a solid foundation for the movies' structured data, requiring only minor
          cleaning and manual additions (e.g. adding missing directors and the latest movie "No Time to Die").

        - ✅ The SPARQL queries used to retrieve James Bond actors' information from Wikidata were – due to being
          limited to 6 actors – quite straightforward and efficient.

        #### Knowledge Extraction with Unstructured Data
        - ✅ The James Bond Fandom Wiki served as the primary source for all unstructured data, providing information on characters, Bond girls, vehicles, and filming locations.

        - ⚠️ **Exception:** Villain data was sourced from Wikipedia, as the Fandom Wiki lacked a 
          section clearly designating characters as villains.

        - ⚠️ **Inconsistency:** SpaCy NER was used to extract location names from unstructured text. However, some
          duplicate location names (e.g., "San Francisco" and "San Francisco City") remain in the geocoded data due
          to inconsistent formatting across different movie pages.

        - ⚠️ **Limitation:** Vehicle data is limited to movies with a "Major Vehicles" section on their Fandom page.
          Newer movies lack this section and consequently have no vehicle data available.

        - ‼️ **Major Challenge I:** Extracting image URLs (for movie posters, characters, and vehicles) proved to be
          the most significant technical challenge. The solution involved making direct requests to the Fandom API
          and parsing the JSON response. Initial attempts to extract URLs from the scraped movie pages were unreliable
          and often returned errors or invalid links.

        - ‼️ **Major Challenge II:** Embedding and displaying image URLs as thumbnails in Streamlit presented another
          initial obstacle. The solution required cleaning the URLs by removing "/revision/" and "/latest/" path
          segments to obtain direct, stable links to the images.

        #### Knowledge Engineering
        - ✅ **Data fusion**: The harmonization of structured and unstructured data into a unified RDF knowledge graph was done by merging all datasets to a single json-file before converting it to ttl.
        - ✅ Ontology reasoning successfully validated that relationships between entities were correctly implemented
          and effectively demonstrated the inverse properties.
        - ⚠️ **Challenge:** data transformationm, e.g. specifying image URLs as datatype=XSD.anyURI and not string.
        """)
