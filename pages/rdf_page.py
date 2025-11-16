# rdf_page.py

import streamlit as st
from streamlit_agraph import agraph, Config
from utils.data_loader import load_ttl, load_characters_ttl
from utils.rdf_graph import create_rdf_graph_general, create_rdf_graph_characters
from rdflib import Graph, URIRef
from streamlit_agraph import Node, Edge
from rdflib.namespace import Namespace

def show_rdf_page():
    st.sidebar.info("You are on the RDF graph page.")
    st.header("James Bond Knowledge Graph")

    st.write('The RDF graph represents the relationships between various entities in the James Bond universe,' \
    'including movies, directors, and actors. Use the search or checkboxes below to customize the visualization of the graph.')

    # ---- Load data  ----
    df_ttl = load_ttl()
    df_characters_ttl = load_characters_ttl()
    graph_data_general = create_rdf_graph_general(df_ttl)
    graph_data_characters = create_rdf_graph_characters(df_characters_ttl)

    # ---- Display mode switch ----
    view_mode = st.toggle("Switch between Full-View and Character-View", value=False)
    st.write("---")
    
    if view_mode:
        st.subheader("Character-Centric RDF Graph")
        current_ttl = df_characters_ttl
        graph_data = graph_data_characters
        
        # Search functionality for character view
        col_search1, col_search2 = st.columns(2)
        with col_search1:
            # Get all character names for autocomplete
            character_names = sorted([node.label for node in graph_data["characters"]])
            search_character = st.selectbox(
                "Search for a character:",
                options=[""] + character_names,
                key="character_search"
            )
        
        with col_search2:
            # Get all actor names for autocomplete
            actor_names = sorted([node.label for node in graph_data["actors"]])
            search_actor = st.selectbox(
                "Search for an actor:",
                options=[""] + actor_names,
                key="actor_search"
            )
        
        st.write("---")
        
        # User controls for character view
        col1, col2, col3 = st.columns(3)
        with col1:
            show_all = st.checkbox('Display whole graph')
        with col2:
            show_characters = st.checkbox('Display characters', value=True)
        with col3:
            show_actors = st.checkbox('Display actors', value=True)
        
    else:
        st.subheader("General RDF Graph")
        current_ttl = df_ttl
        graph_data = graph_data_general
        
        # Search functionality for general view
        col_search1, col_search2 = st.columns(2)
        with col_search1:
            # Get all movie names for autocomplete
            movie_names = sorted([node.label for node in graph_data["movies"]])
            search_movie = st.selectbox(
                "Search for a movie:",
                options=[""] + movie_names,
                key="movie_search"
            )
        
        with col_search2:
            # Get all actor names for autocomplete
            actor_names = sorted([node.label for node in graph_data["actors"]])
            search_actor = st.selectbox(
                "Search for a Bond actor:",
                options=[""] + actor_names,
                key="bond_actor_search"
            )
        
        st.write("---")
        
        # User controls for general view
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
    nodes = []
    edges = []
    seen_node_ids = set()
    config = Config(height=600, width=760, directed=True, nodeHighlightBehavior=True, highlightColor="#F7A7A6")

    # ---- Handle search queries ----
    search_active = False
    
    if view_mode:
        # Character view search
        if search_character or search_actor:
            search_active = True
            g = Graph()
            g.parse(data=current_ttl, format='ttl')
            MOVIE = Namespace("https://triplydb.com/Triply/linkedmdb/vocab/")
            
            # Find the selected nodes
            if search_character:
                for node in graph_data["characters"]:
                    if node.label == search_character:
                        nodes.append(node)
                        seen_node_ids.add(node.id)
                        
                        # Find connected actors
                        for actor_uri, _, char_uri in g.triples((None, MOVIE.playsCharacter, URIRef(node.id))):
                            for actor_node in graph_data["actors"]:
                                if actor_node.id == str(actor_uri) and actor_node.id not in seen_node_ids:
                                    nodes.append(actor_node)
                                    seen_node_ids.add(actor_node.id)
                            edges.append(Edge(source=str(actor_uri), label="plays", target=str(char_uri)))
            
            if search_actor:
                for node in graph_data["actors"]:
                    if node.label == search_actor:
                        nodes.append(node)
                        seen_node_ids.add(node.id)
                        
                        # Find connected characters
                        for actor_uri, _, char_uri in g.triples((URIRef(node.id), MOVIE.playsCharacter, None)):
                            for char_node in graph_data["characters"]:
                                if char_node.id == str(char_uri) and char_node.id not in seen_node_ids:
                                    nodes.append(char_node)
                                    seen_node_ids.add(char_node.id)
                            edges.append(Edge(source=str(actor_uri), label="plays", target=str(char_uri)))
    
    else:
        # General view search
        if search_movie or search_actor:
            search_active = True
            g = Graph()
            g.parse(data=current_ttl, format='ttl')
            EX = Namespace('http://example.org/jamesbond/')
            MO = Namespace('http://example.org/movieontology/')
            
            if search_movie:
                for node in graph_data["movies"]:
                    if node.label == search_movie:
                        nodes.append(node)
                        seen_node_ids.add(node.id)
                        
                        # Find connected directors and actors
                        for movie_uri, _, director_uri in g.triples((URIRef(node.id), MO.director, None)):
                            for dir_node in graph_data["directors"]:
                                if dir_node.id == str(director_uri) and dir_node.id not in seen_node_ids:
                                    nodes.append(dir_node)
                                    seen_node_ids.add(dir_node.id)
                            edges.append(Edge(source=str(movie_uri), label="director", target=str(director_uri)))
                        
                        for movie_uri, _, actor_uri in g.triples((URIRef(node.id), EX.starring, None)):
                            for actor_node in graph_data["actors"]:
                                if actor_node.id == str(actor_uri) and actor_node.id not in seen_node_ids:
                                    nodes.append(actor_node)
                                    seen_node_ids.add(actor_node.id)
                            edges.append(Edge(source=str(movie_uri), label="starring", target=str(actor_uri)))
            
            if search_actor:
                for node in graph_data["actors"]:
                    if node.label == search_actor:
                        nodes.append(node)
                        seen_node_ids.add(node.id)
                        
                        # Find connected movies
                        for movie_uri, _, actor_uri in g.triples((None, EX.starring, URIRef(node.id))):
                            for movie_node in graph_data["movies"]:
                                if movie_node.id == str(movie_uri) and movie_node.id not in seen_node_ids:
                                    nodes.append(movie_node)
                                    seen_node_ids.add(movie_node.id)
                            edges.append(Edge(source=str(movie_uri), label="starring", target=str(actor_uri)))

    # ---- If no search, use checkboxes ----
    if not search_active:
        if show_all:
            # Display the entire RDF graph
            g = Graph()
            g.parse(data=current_ttl, format='ttl')

            for s, p, o in g:
                # Add subject node
                if str(s) not in seen_node_ids:
                    nodes.append(Node(id=str(s)))
                    seen_node_ids.add(str(s))
                
                # Add object node (only if it's a URI, not a Literal)
                if isinstance(o, URIRef) and str(o) not in seen_node_ids:
                    nodes.append(Node(id=str(o)))
                    seen_node_ids.add(str(o))
                
                # Add edge (only if object is a URI)
                if isinstance(o, URIRef):
                    edges.append(Edge(
                        source=str(s),
                        label=str(p).split('/')[-1].split('#')[-1],
                        target=str(o)
                    ))
        else:
            # Display filtered graph based on user selections and view mode
            if view_mode:
                # Character view logic
                if show_characters:
                    for node in graph_data["characters"]:
                        if node.id not in seen_node_ids:
                            nodes.append(node)
                            seen_node_ids.add(node.id)
                
                if show_actors:
                    for node in graph_data["actors"]:
                        if node.id not in seen_node_ids:
                            nodes.append(node)
                            seen_node_ids.add(node.id)
                
                if show_characters and show_actors:
                    edges += graph_data["portrayed_by"]
            else:
                # General view logic
                if show_movies:
                    for node in graph_data["movies"]:
                        if node.id not in seen_node_ids:
                            nodes.append(node)
                            seen_node_ids.add(node.id)
                
                if show_directors:
                    for node in graph_data["directors"]:
                        if node.id not in seen_node_ids:
                            nodes.append(node)
                            seen_node_ids.add(node.id)
                
                if show_actors:
                    for node in graph_data["actors"]:
                        if node.id not in seen_node_ids:
                            nodes.append(node)
                            seen_node_ids.add(node.id)
                
                if show_movies and show_directors:
                    edges += graph_data["directed_by"]
                
                if show_movies and show_actors:
                    edges += graph_data["starring"]

    # ---- Render Graph ----
    if nodes:
        if search_active:
            st.info(f"Showing {len(nodes)} nodes and {len(edges)} connections for your search.")
        agraph(nodes=nodes, edges=edges, config=config)
    else:
        st.warning("Please select at least one entity type to display or use the search function.")