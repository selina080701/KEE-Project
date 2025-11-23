# rdf_page.py

import streamlit as st
from streamlit_agraph import agraph, Config
from utils.data_loader import load_ttl, load_bond_info_ttl
from utils.rdf_graph import create_rdf_graph, create_bond_info_graph, get_movies_with_titles

def show_rdf_page():
    st.sidebar.info("You are on the RDF graph page.")
    st.header("James Bond Knowledge Graph")

    st.write('The RDF graph represents the relationships between various entities in the James Bond universe, '
    'including movies, directors, actors, bond girls, villains, locations, vehicles, songs, and music contributors. '
    'Use the checkboxes below to customize the visualization of the graph.')

    # ---- Load data  ----
    df_ttl = load_ttl()
    graph_data = create_rdf_graph(df_ttl)

    # Load Bond actor info (separate RDF graph)
    bond_ttl = load_bond_info_ttl()
    bond_info_data = create_bond_info_graph(bond_ttl)

    # Radio buttons for mutually exclusive view selection
    view_option = st.radio(
        " ",
        options=[
            "Movie overview",
            "Bond girls",
            "Villains",
            "Characters",
            "Theme songs",
            "Locations",
            "Vehicles"
        ],
        index=0,  # Default to "Movie overview"
        horizontal=True
    )

    # Movie filter dropdown
    selected_movie_uri = None
    selected_movie = None

    # Show filter for views that support movie filtering
    filterable_views = ["Movie overview", "Bond girls", "Villains", "Characters", "Theme songs", "Locations", "Vehicles"]

    if view_option in filterable_views:
        st.write("---")
        movies_list = get_movies_with_titles(df_ttl)
        movie_options = [movie[3] for movie in movies_list]  # movie[3] is combined_title

        selected_movies = st.multiselect(
            "Filter by Movie(s):",
            options=movie_options,
            default=["Casino Royale - James Bond 007: Casino Royale", "Diamonds Are Forever - James Bond 007 – Diamantenfieber"]
        )

        # Get the movie URIs for selected movies
        selected_movie_uris = []
        if selected_movies:
            for movie in movies_list:
                if movie[3] in selected_movies:
                    selected_movie_uris.append(movie[0])

    # Separate Bond actor info checkbox
    st.write("---")
    show_bond_info = st.checkbox('Display Bond actor information (separate graph)', value=False)

    # ---- Prepare graph rendering ----
    nodes, edges = [], []
    config = Config(height=600, width=760)

    # ---- Separate Bond actor info graph ----
    if show_bond_info:
        nodes = bond_info_data["bond_info_nodes"]
        edges = bond_info_data["bond_info_edges"]
        agraph(nodes=nodes, edges=edges, config=config)
        return

    # ---- Build graph based on selected view ----
    node_list = []

    if view_option == "Movie overview":
        # View 1: Movie Overview - movies, directors, producers, songs, performers, bond girls, villains, and movie attributes
        if selected_movie_uris:
            # Filter to show only selected movies and their related entities
            for movie in graph_data["movies"]:
                if movie.id in selected_movie_uris:
                    node_list.append(movie)

            # Get movie attributes, directors, producers, etc. for selected movies
            for movie_uri in selected_movie_uris:
                # Get movie attributes (year, German title, ratings)
                for edge in graph_data["movie_attribute_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for attr in graph_data["movie_attributes"]:
                            if attr.id == edge.to:
                                node_list.append(attr)

                # Get directors for this movie
                for edge in graph_data["director_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for director in graph_data["directors"]:
                            if director.id == edge.to:
                                node_list.append(director)

                # Get producers for this movie
                for edge in graph_data["producer_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for producer in graph_data["producers"]:
                            if producer.id == edge.to:
                                node_list.append(producer)

                # Get bond girls in this movie using hasBondGirl edges
                bondgirls_in_movie = set()
                for edge in graph_data["bondgirl_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for bg in graph_data["bondgirls"]:
                            if bg.id == edge.to:
                                node_list.append(bg)
                                bondgirls_in_movie.add(bg.id)

                # Get villains in this movie using hasAntagonist edges
                villains_in_movie = set()
                for edge in graph_data["villain_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for v in graph_data["villains"]:
                            if v.id == edge.to:
                                node_list.append(v)
                                villains_in_movie.add(v.id)

                # Get all characters in this movie (bond girls and villains)
                all_characters_in_movie = bondgirls_in_movie | villains_in_movie

                # Get actors using Casting instances (movie-specific character-actor relationships)
                for casting in graph_data["castings"]:
                    if casting['film'] == movie_uri and casting['character'] in all_characters_in_movie:
                        # Add actor
                        for actor in graph_data["actors"]:
                            if actor.id == casting['actor']:
                                node_list.append(actor)
                                break

                        # Add portrayedBy edge from character to actor
                        for edge in graph_data["portrayed_edges"]:
                            if edge.source == casting['character'] and edge.to == casting['actor']:
                                edges.append(edge)
                                break

                # Get theme song for this movie
                for edge in graph_data["song_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for song in graph_data["songs"]:
                            if song.id == edge.to:
                                node_list.append(song)
                                # Get performers for this song
                                for perf_edge in graph_data["performer_edges"]:
                                    if perf_edge.source == song.id:
                                        edges.append(perf_edge)
                                        for contributor in graph_data["music_contributors"]:
                                            if contributor.id == perf_edge.to:
                                                node_list.append(contributor)
        else:
            # Show all
            node_list += graph_data["movies"]
            node_list += graph_data["movie_attributes"]
            node_list += graph_data["directors"]
            node_list += graph_data["producers"]
            node_list += graph_data["bondgirls"]
            node_list += graph_data["songs"]
            node_list += graph_data["music_contributors"]
            node_list += graph_data["villains"]

            edges += graph_data["movie_attribute_edges"]
            edges += graph_data["director_edges"]
            edges += graph_data["producer_edges"]
            edges += graph_data["bondgirl_edges"]
            edges += graph_data["villain_edges"]
            edges += graph_data["song_edges"]
            edges += graph_data["performer_edges"]

    elif view_option == "Bond girls":
        # View 2: Bond Girls - movies, bond girls, and actresses (actors who portray them)
        if selected_movie_uris:
            # Filter to show only selected movies
            for movie in graph_data["movies"]:
                if movie.id in selected_movie_uris:
                    node_list.append(movie)

            # Get bond girls and actors for each selected movie
            for movie_uri in selected_movie_uris:
                # Get bond girls in this movie using hasBondGirl edges
                bondgirls_in_movie = set()
                for edge in graph_data["bondgirl_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for bg in graph_data["bondgirls"]:
                            if bg.id == edge.to:
                                node_list.append(bg)
                                bondgirls_in_movie.add(bg.id)

                # Get actors using Casting instances (movie-specific character-actor relationships)
                for casting in graph_data["castings"]:
                    if casting['film'] == movie_uri and casting['character'] in bondgirls_in_movie:
                        # Add actor
                        for actor in graph_data["actors"]:
                            if actor.id == casting['actor']:
                                node_list.append(actor)
                                break

                        # Add portrayedBy edge from character to actor
                        for edge in graph_data["portrayed_edges"]:
                            if edge.source == casting['character'] and edge.to == casting['actor']:
                                edges.append(edge)
                                break
        else:
            # Show all
            node_list += graph_data["movies"]
            node_list += graph_data["bondgirls"]

            # Add only actors who portray bond girls
            bondgirl_ids = set(bondgirl.id for bondgirl in graph_data["bondgirls"])
            bondgirl_actor_ids = set()

            for edge in graph_data["portrayed_edges"]:
                # Check if source is a bond girl (portrayed_edges go from character to actor)
                if edge.source in bondgirl_ids:
                    bondgirl_actor_ids.add(edge.to)

            # Add those specific actors
            for actor in graph_data["actors"]:
                if actor.id in bondgirl_actor_ids:
                    node_list.append(actor)

            # Add only edges related to bond girls
            edges += graph_data["bondgirl_edges"]
            edges += [e for e in graph_data["portrayed_edges"] if e.source in bondgirl_ids]

    elif view_option == "Villains":
        # View 3: Villains - movies, villains, and actors (who portray them)
        if selected_movie_uris:
            # Filter to show only selected movies
            for movie in graph_data["movies"]:
                if movie.id in selected_movie_uris:
                    node_list.append(movie)

            # Get villains and actors for each selected movie
            for movie_uri in selected_movie_uris:
                # Get villains in this movie using hasAntagonist edges
                villains_in_movie = set()
                for edge in graph_data["villain_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for v in graph_data["villains"]:
                            if v.id == edge.to:
                                node_list.append(v)
                                villains_in_movie.add(v.id)

                # Get actors using Casting instances (movie-specific character-actor relationships)
                for casting in graph_data["castings"]:
                    if casting['film'] == movie_uri and casting['character'] in villains_in_movie:
                        # Add actor
                        for actor in graph_data["actors"]:
                            if actor.id == casting['actor']:
                                node_list.append(actor)
                                break

                        # Add portrayedBy edge from character to actor
                        for edge in graph_data["portrayed_edges"]:
                            if edge.source == casting['character'] and edge.to == casting['actor']:
                                edges.append(edge)
                                break
        else:
            # Show all
            node_list += graph_data["movies"]
            node_list += graph_data["villains"]

            # Add only actors who portray villains
            villain_ids = set(villain.id for villain in graph_data["villains"])
            villain_actor_ids = set()

            for edge in graph_data["portrayed_edges"]:
                # Check if source is a villain (portrayed_edges go from character to actor)
                if edge.source in villain_ids:
                    villain_actor_ids.add(edge.to)

            # Add those specific actors
            for actor in graph_data["actors"]:
                if actor.id in villain_actor_ids:
                    node_list.append(actor)

            # Add only edges related to villains
            edges += graph_data["villain_edges"]
            edges += [e for e in graph_data["portrayed_edges"] if e.source in villain_ids]

    elif view_option == "Characters":
        # View 4: Characters - movies, all characters (bond girls, villains, and other characters), and actors who portray them

        # If a specific movie is selected, filter to show only that movie
        if selected_movie_uris:
            # Add only the selected movies
            for movie in graph_data["movies"]:
                if movie.id in selected_movie_uris:
                    node_list.append(movie)

            # Get characters and actors for each selected movie
            for movie_uri in selected_movie_uris:
                # Get bond girls in this movie using hasBondGirl edges
                bondgirls_in_movie = set()
                for edge in graph_data["bondgirl_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for bg in graph_data["bondgirls"]:
                            if bg.id == edge.to:
                                node_list.append(bg)
                                bondgirls_in_movie.add(bg.id)

                # Get villains in this movie using hasAntagonist edges
                villains_in_movie = set()
                for edge in graph_data["villain_edges"]:
                    if edge.source == movie_uri:
                        edges.append(edge)
                        for v in graph_data["villains"]:
                            if v.id == edge.to:
                                node_list.append(v)
                                villains_in_movie.add(v.id)

                # Get other characters in this movie using appearsIn edges
                other_characters_in_movie = set()
                for edge in graph_data["appears_in_edges"]:
                    if edge.to == movie_uri:
                        # Only add if it's not a bond girl or villain
                        if edge.source not in bondgirls_in_movie and edge.source not in villains_in_movie:
                            for c in graph_data["characters"]:
                                if c.id == edge.source:
                                    node_list.append(c)
                                    other_characters_in_movie.add(c.id)
                                    edges.append(edge)

                # Get all characters in this movie
                all_characters_in_movie = bondgirls_in_movie | villains_in_movie | other_characters_in_movie

                # Get actors using Casting instances (movie-specific character-actor relationships)
                for casting in graph_data["castings"]:
                    if casting['film'] == movie_uri and casting['character'] in all_characters_in_movie:
                        # Add actor
                        for actor in graph_data["actors"]:
                            if actor.id == casting['actor']:
                                node_list.append(actor)
                                break

                        # Add portrayedBy edge from character to actor
                        for edge in graph_data["portrayed_edges"]:
                            if edge.source == casting['character'] and edge.to == casting['actor']:
                                edges.append(edge)
                                break

        else:
            # Show all movies and characters
            node_list += graph_data["movies"]
            node_list += graph_data["bondgirls"]  # Pink stars
            node_list += graph_data["villains"]   # Dark red triangles
            node_list += graph_data["characters"] # Orange dots (other characters)

            # Add only actors who portray any character (bond girls, villains, or other characters)
            all_character_ids = set()
            all_character_ids.update(bg.id for bg in graph_data["bondgirls"])
            all_character_ids.update(v.id for v in graph_data["villains"])
            all_character_ids.update(c.id for c in graph_data["characters"])

            character_actor_ids = set()
            for edge in graph_data["portrayed_edges"]:
                # portrayed_edges go from character to actor
                if edge.source in all_character_ids:
                    character_actor_ids.add(edge.to)

            # Add those specific actors
            for actor in graph_data["actors"]:
                if actor.id in character_actor_ids:
                    node_list.append(actor)

            # Add only edges related to characters
            edges += [e for e in graph_data["appears_in_edges"] if e.source in all_character_ids]
            edges += [e for e in graph_data["portrayed_edges"] if e.source in all_character_ids]

    elif view_option == "Theme songs":
        # View 5: Theme Songs - movies, songs, and performers
        if selected_movie_uris:
            # Filter to show only selected movie
            for movie in graph_data["movies"]:
                if movie.id in selected_movie_uris:
                    node_list.append(movie)
                    break

            # Get theme song for this movie
            for edge in graph_data["song_edges"]:
                if edge.source in selected_movie_uris:
                    edges.append(edge)
                    for song in graph_data["songs"]:
                        if song.id == edge.to:
                            node_list.append(song)
                            # Get performers for this song
                            for perf_edge in graph_data["performer_edges"]:
                                if perf_edge.source == song.id:
                                    edges.append(perf_edge)
                                    for contributor in graph_data["music_contributors"]:
                                        if contributor.id == perf_edge.to:
                                            node_list.append(contributor)
        else:
            # Show all
            node_list += graph_data["movies"]
            node_list += graph_data["songs"]
            node_list += graph_data["music_contributors"]

            edges += graph_data["song_edges"]
            edges += graph_data["performer_edges"]

    elif view_option == "Locations":
        # View 6: Locations - movies and locations
        if selected_movie_uris:
            # Filter to show only selected movie
            for movie in graph_data["movies"]:
                if movie.id in selected_movie_uris:
                    node_list.append(movie)
                    break

            # Get locations for this movie
            for edge in graph_data["location_edges"]:
                if edge.source in selected_movie_uris:
                    edges.append(edge)
                    for location in graph_data["locations"]:
                        if location.id == edge.to:
                            node_list.append(location)
        else:
            # Show all
            node_list += graph_data["movies"]
            node_list += graph_data["locations"]

            edges += graph_data["location_edges"]

    elif view_option == "Vehicles":
        # View 7: Vehicles - movies and vehicles
        if selected_movie_uris:
            # Filter to show only selected movie
            for movie in graph_data["movies"]:
                if movie.id in selected_movie_uris:
                    node_list.append(movie)
                    break

            # Get vehicles for this movie
            for edge in graph_data["vehicle_edges"]:
                if edge.source in selected_movie_uris:
                    edges.append(edge)
                    for vehicle in graph_data["vehicles"]:
                        if vehicle.id == edge.to:
                            node_list.append(vehicle)
        else:
            # Show all
            node_list += graph_data["movies"]
            node_list += graph_data["vehicles"]

            edges += graph_data["vehicle_edges"]

    # Remove duplicates by using a dictionary with node ID as key
    seen_node_ids = {}
    for node in node_list:
        if node.id not in seen_node_ids:
            seen_node_ids[node.id] = node
    nodes = list(seen_node_ids.values())

    # ---- Render Graph ----
    agraph(nodes=nodes, edges=edges, config=config)



