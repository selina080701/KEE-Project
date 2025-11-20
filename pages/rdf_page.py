# rdf_page.py

import streamlit as st
from streamlit_agraph import agraph, Config
from utils.data_loader import load_ttl
from utils.rdf_graph import create_rdf_graph
from rdflib import Graph
from streamlit_agraph import Node, Edge

def show_rdf_page():
    st.sidebar.info("You are on the RDF graph page.")
    st.header("James Bond Knowledge Graph")

    st.write('The RDF graph represents the relationships between various entities in the James Bond universe,' \
    'including movies, directors, and actors. Use the checkboxes below to customize the visualization of the graph.')

    # ---- Load data  ----
    df_ttl = load_ttl()
    graph_data = create_rdf_graph(df_ttl)

    # ---- User controls with checkboxes ----
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_all = st.checkbox('Display whole graph')
    with col2:
        show_movies = st.checkbox('Display movies', value=True)
    with col3:
        show_directors = st.checkbox('Display directors', value=True)
    with col4:
        show_actors = st.checkbox('Display Bond actors', value=True)

    # ---- Prepare graph rendering ----
    nodes, edges = [], []
    config = Config(height=600, width=760)

    if show_all:
        # Display the entire RDF graph
        g = Graph()
        g.parse(data=df_ttl, format='ttl')

        seen_nodes = set()
        for s, p, o in g:
            if s not in seen_nodes:
                nodes.append(Node(id=str(s)))
                seen_nodes.add(s)
            if o not in seen_nodes:
                nodes.append(Node(id=str(o)))
                seen_nodes.add(o)
            edges.append(Edge(
                source=str(s),
                label=str(p).split('/')[-1].split('#')[-1],
                target=str(o)
            ))

    else:
        # Display filtered graph based on user selections
        if show_movies:
            nodes += graph_data["movies"]
        if show_directors:
            nodes += graph_data["directors"]
        if show_actors:
            nodes += graph_data["actors"]
        if show_movies and show_directors:
            edges += graph_data["directed_by"]
        if show_movies and show_actors:
            edges += graph_data["starring"]

    # ---- Render Graph ----
    agraph(nodes=nodes, edges=edges, config=config)



