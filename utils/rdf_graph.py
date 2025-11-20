# rdf_graph.py

import streamlit as st
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
from streamlit_agraph import Node, Edge

"""
The below functions are displayed in the rdf page.
"""

@st.cache_data
def create_rdf_graph(df_ttl):
    # ---- Define Namespaces ----
    EX = Namespace('http://example.org/jamesbond/')
    MO = Namespace('http://example.org/movieontology/')
    PERSON = Namespace('http://example.org/person/')

    # ---- Load RDF-graph ----
    g = Graph()
    g.parse(data=df_ttl, format='ttl')


    # ---- Movies ----
    movies = [
        Node(id=str(s),
                label=str(title),
                color='#FF6B6B',
                shape='box',
                size=25)
        for s, _, title in g.triples((None, EX.title, None))
    ]

    # ---- Directors ----
    director_query = '''
        PREFIX mo: <http://example.org/movieontology/>
        SELECT DISTINCT ?director
        WHERE {
            ?movie mo:director ?director.
        }
    '''
    directors = [
        Node(id=str(url[0]),
                label=str(url[0]).split('/')[-1].replace('_', ' '),
                color='#4ECDC4',
                shape='dot',
                size=20)
        for url in g.query(director_query)
    ]

    # ---- Actors ----
    actor_query = '''
        PREFIX ex: <http://example.org/jamesbond/>
        PREFIX mo: <http://example.org/movieontology/>
        SELECT DISTINCT ?actor
        WHERE {
            ?movie ex:starring ?actor.
            ?actor a mo:Actor.
        }
    '''
    actors = [
        Node(id=str(url[0]),
                label=str(url[0]).split('/')[-1].replace('_', ' '),
                color='#FFD93D',
                shape='star',
                size=22)
        for url in g.query(actor_query)
    ]

    # ---- Edges: Movie -> Director ----
    directed_by = [
        Edge(source=str(movie),
                label='director',
                target=str(director))
        for movie, _, director in g.triples((None, MO.director, None))
    ]

    # ---- Edges: Movie -> Actor ----
    starring = [
        Edge(source=str(movie),
                label='starring',
                target=str(actor),
                color='#FFD93D')
        for movie, _, actor in g.triples((None, EX.starring, None))
    ]

    return {
        "movies": movies,
        "directors": directors,
        "actors": actors,
        "directed_by": directed_by,
        "starring": starring
    }


@st.cache_data
def create_bond_info_graph(df_bond_ttl):
    EX = Namespace("http://example.org/jamesbond/")
    MOVIE = Namespace("https://triplydb.com/Triply/linkedmdb/vocab/")

    g = Graph()
    g.parse(data=df_bond_ttl, format="ttl")

    bond_info_nodes = []
    bond_info_edges = []

    country_nodes = {}
    gender_nodes = {}

    for actor in g.subjects(RDF.type, MOVIE.Actor):
        # Actor-Label
        label_value = g.value(actor, RDFS.label) or g.value(actor, EX.name)
        label = str(label_value) if label_value else str(actor).split("/")[-1]

        dob = g.value(actor, EX.dateOfBirth)
        dod = g.value(actor, EX.dateOfDeath)
        gender = g.value(actor, EX.gender)

        # Actor node
        bond_info_nodes.append(
            Node(
                id=str(actor),
                label=label,
                color="#FFD93D",
                shape="star",
                size=28,
            )
        )

        # all citizenship countries
        for citizenship in g.objects(actor, EX.citizenship):
            if citizenship not in country_nodes:
                country_label_val = g.value(citizenship, RDFS.label)
                country_label = (
                    str(country_label_val)
                    if country_label_val
                    else str(citizenship).split("/")[-1]
                )
                country_nodes[citizenship] = Node(
                    id=str(citizenship),
                    label=country_label,
                    color='#DBEBC2',
                    shape='dot',
                    size=20,
                )

            bond_info_edges.append(
                Edge(
                    source=str(actor),
                    label="citizenship",
                    target=str(citizenship),
                )
            )

        # Gender node
        if gender:
            if gender not in gender_nodes:
                gender_label_val = g.value(gender, RDFS.label)
                gender_label = (
                    str(gender_label_val)
                    if gender_label_val
                    else str(gender).split("/")[-1]
                )
                gender_nodes[gender] = Node(
                    id=str(gender),
                    label=gender_label,
                    color='#FF6B6B',
                    shape='diamond',
                    size=20,
                )

            bond_info_edges.append(
                Edge(
                    source=str(actor),
                    label="gender",
                    target=str(gender),
                )
            )

        # Dates nodes (Literal)
        def add_literal_node(prop_value, prop_label):
            if not prop_value:
                return
            node_id = f"{actor}_{prop_label}"
            bond_info_nodes.append(
                Node(
                    id=node_id,
                    label=str(prop_value),
                    shape="box",
                    size=18,
                )
            )
            bond_info_edges.append(
                Edge(
                    source=str(actor),
                    label=prop_label,
                    target=node_id,
                )
            )

        add_literal_node(dob, "dateOfBirth")
        add_literal_node(dod, "dateOfDeath")

    bond_info_nodes.extend(country_nodes.values())
    bond_info_nodes.extend(gender_nodes.values())

    return {
        "bond_info_nodes": bond_info_nodes,
        "bond_info_edges": bond_info_edges,
    }


@st.cache_data
def create_rdf_graph_characters(df_ttl):
    from rdflib.namespace import RDF, RDFS
    
    # ---- Define Namespaces ----
    MOVIE = Namespace("https://triplydb.com/Triply/linkedmdb/vocab/")

    # ---- Load RDF-graph ----
    g = Graph()
    g.parse(data=df_ttl, format='ttl')

    # ---- Characters ----
    character_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?character ?label
        WHERE {
            ?character a movie:FilmCharacter .
            ?character rdfs:label ?label .
        }
    '''
    characters = [
        Node(id=str(row[0]),
             label=str(row[1]),
             color='#FF6B6B',
             shape='box',
             size=25)
        for row in g.query(character_query)
    ]

    # ---- Actors ----
    actor_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?actor ?label
        WHERE {
            ?actor a movie:Actor .
            ?actor rdfs:label ?label .
        }
    '''
    actors = [
        Node(id=str(row[0]),
             label=str(row[1]),
             color='#4ECDC4',
             shape='dot',
             size=20)
        for row in g.query(actor_query)
    ]

    # ---- Edges: Actor -> Character ----
    portrayed_by = [
        Edge(source=str(actor),
             label='plays',
             target=str(character))
        for actor, _, character in g.triples((None, MOVIE.playsCharacter, None))
    ]

    return {
        "characters": characters,
        "actors": actors,
        "portrayed_by": portrayed_by
    }