# rdf_graph.py

import streamlit as st
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
from streamlit_agraph import Node, Edge

"""
The below functions are displayed in the rdf page.
"""

@st.cache_data
def get_movies_with_titles(df_ttl):
    """
    Extract movies with both English and German titles from RDF graph.
    Returns a list of tuples: (movie_uri, english_title, german_title, combined_title)
    """
    from rdflib.namespace import RDF, RDFS

    MOVIE = Namespace("https://triplydb.com/Triply/linkedmdb/vocab/")

    g = Graph()
    g.parse(data=df_ttl, format='ttl')

    movie_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?movie ?title_en ?title_de
        WHERE {
            ?movie a movie:Film .
            ?movie rdfs:label ?title_en .
            FILTER(lang(?title_en) = "en")
            OPTIONAL {
                ?movie rdfs:label ?title_de .
                FILTER(lang(?title_de) = "de")
            }
        }
        ORDER BY ?title_en
    '''

    movies = []
    for row in g.query(movie_query):
        movie_uri = str(row[0])
        title_en = str(row[1]) if row[1] else ""
        title_de = str(row[2]) if row[2] else title_en
        combined_title = f"{title_en} - {title_de}"
        movies.append((movie_uri, title_en, title_de, combined_title))

    return movies


@st.cache_data
def create_rdf_graph(df_ttl):
    # ---- Define Namespaces ----
    MOVIE = Namespace("https://triplydb.com/Triply/linkedmdb/vocab/")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    DBO = Namespace("http://dbpedia.org/ontology/")
    TIME = Namespace("http://www.w3.org/2006/time#")
    SCHEMA = Namespace("http://schema.org/")
    BOND = Namespace("http://example.org/bond/")
    GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

    # ---- Load RDF-graph ----
    g = Graph()
    g.parse(data=df_ttl, format='ttl')

    # ---- Movies ----
    movie_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX schema: <http://schema.org/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX time: <http://www.w3.org/2006/time#>
        PREFIX bond: <http://example.org/bond/>
        SELECT DISTINCT ?movie ?label_en ?label_de ?year ?imdb ?rtm
        WHERE {
            ?movie a movie:Film .
            ?movie schema:name ?label_en .
            OPTIONAL {
                ?movie rdfs:label ?label_de .
                FILTER(lang(?label_de) = "de")
            }
            OPTIONAL { ?movie time:year ?year }
            OPTIONAL { ?movie bond:imdbRating ?imdb }
            OPTIONAL { ?movie bond:rtmRating ?rtm }
        }
    '''

    movies = []
    movie_attributes = []  # Store attribute nodes separately
    movie_attribute_edges = []  # Store edges to attributes

    for row in g.query(movie_query):
        movie_uri = str(row[0])
        label_en = str(row[1])
        label_de = str(row[2]) if row[2] else None
        year = str(row[3])[:4] if row[3] else None
        imdb = f"{float(row[4]):.1f}" if row[4] else None
        rtm = f"{float(row[5]):.1f}" if row[5] else None

        # Create movie node with simple label (English title only)
        movies.append(
            Node(id=movie_uri,
                 label=label_en,
                 color="#797DCF",
                 shape='ellipse',
                 size=25)
        )

        # Create attribute nodes for year, German title, and ratings
        # German title node (if different)
        if label_de and label_de != label_en:
            de_node_id = f"{movie_uri}_de_title"
            movie_attributes.append(
                Node(id=de_node_id,
                     label=f"DE: {label_de}",
                     color='#FFCCCC',
                     shape='box',
                     size=15)
            )
            movie_attribute_edges.append(
                Edge(source=movie_uri,
                     label='germanTitle',
                     target=de_node_id)
            )

        # Year node
        if year:
            year_node_id = f"{movie_uri}_year"
            movie_attributes.append(
                Node(id=year_node_id,
                     label=year,
                     color='#FFCCCC',
                     shape='box',
                     size=12)
            )
            movie_attribute_edges.append(
                Edge(source=movie_uri,
                     label='year',
                     target=year_node_id)
            )

        # IMDb rating node
        if imdb:
            imdb_node_id = f"{movie_uri}_imdb"
            movie_attributes.append(
                Node(id=imdb_node_id,
                     label=f"IMDb: {imdb}",
                     color='#FFCCCC',
                     shape='box',
                     size=12)
            )
            movie_attribute_edges.append(
                Edge(source=movie_uri,
                     label='imdbRating',
                     target=imdb_node_id)
            )

        # Rotten Tomatoes rating node
        if rtm:
            rtm_node_id = f"{movie_uri}_rtm"
            movie_attributes.append(
                Node(id=rtm_node_id,
                     label=f"RT: {rtm}",
                     color='#FFCCCC',
                     shape='box',
                     size=12)
            )
            movie_attribute_edges.append(
                Edge(source=movie_uri,
                     label='rtmRating',
                     target=rtm_node_id)
            )

    # ---- Directors ----
    director_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX bond: <http://example.org/bond/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?director ?name
        WHERE {
            ?director a movie:Director .
            ?director foaf:name ?name .
        }
    '''
    directors = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color="#7CCCC7",
                shape='ellipse',
                size=20)
        for row in g.query(director_query)
    ]

    # ---- Producers ----
    producer_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?producer ?name
        WHERE {
            ?producer a movie:Producer .
            ?producer foaf:name ?name .
        }
    '''
    producers = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color='#7CCCC7',
                shape='ellipse',
                size=18)
        for row in g.query(producer_query)
    ]

    # ---- Actors ----
    actor_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?actor ?name
        WHERE {
            ?actor a movie:Actor .
            ?actor foaf:name ?name .
        }
    '''
    actors = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color='#FFD93D',
                shape='star',
                size=22)
        for row in g.query(actor_query)
    ]

    # ---- Bond Actors: Attribute + hasJamesBond ----
    bond_actor_attr_nodes = []
    bond_actor_attr_edges = []
    bond_actor_edges = []

    # Attribute für alle BondActor-Knoten
    for actor in g.subjects(RDF.type, BOND.BondActor):
        actor_uri = str(actor)

        # birthDate
        for dob in g.objects(actor, DBO.birthDate):
            node_id = f"{actor_uri}_birthDate"
            bond_actor_attr_nodes.append(
                Node(
                    id=node_id,
                    label=str(dob),
                    color='#91D9F7',
                    shape="box",
                    size=16,
                )
            )
            bond_actor_attr_edges.append(
                Edge(
                    source=actor_uri,
                    label="birthDate",
                    target=node_id,
                )
            )

        # deathDate
        for dod in g.objects(actor, DBO.deathDate):
            node_id = f"{actor_uri}_deathDate"
            bond_actor_attr_nodes.append(
                Node(
                    id=node_id,
                    label=str(dod),
                    color='#0B6E99',
                    shape="box",
                    size=16,
                )
            )
            bond_actor_attr_edges.append(
                Edge(
                    source=actor_uri,
                    label="deathDate",
                    target=node_id,
                )
            )

        # citizenship (Länder-Knoten wiederverwenden, daher ID = URI)
        for country in g.objects(actor, DBO.citizenship):
            country_uri = str(country)
            country_label = g.value(country, RDFS.label) or country_uri.split("/")[-1]
            bond_actor_attr_nodes.append(
                Node(
                    id=country_uri,
                    label=str(country_label),
                    color='#DBEBC2',
                    shape="dot",
                    size=20,
                )
            )
            bond_actor_attr_edges.append(
                Edge(
                    source=actor_uri,
                    label="citizenship",
                    target=country_uri,
                )
            )

        # gender
        for gender in g.objects(actor, FOAF.gender):
            gender_uri = str(gender)
            gender_label = g.value(gender, RDFS.label) or gender_uri.split("/")[-1]
            bond_actor_attr_nodes.append(
                Node(
                    id=gender_uri,
                    label=str(gender_label),
                    color='#FF6B6B',
                    shape='diamond',
                    size=20,
                )
            )
            bond_actor_attr_edges.append(
                Edge(
                    source=actor_uri,
                    label="gender",
                    target=gender_uri,
                )
            )

    # Kanten Film -> BondActor (hasJamesBond)
    for movie, _, actor in g.triples((None, BOND.hasJamesBond, None)):
        bond_actor_edges.append(
            Edge(
                source=str(movie),
                label="hasJamesBond",
                target=str(actor),
            )
        )

    # ---- Film Characters (other characters - not bond girls or villains) ----
    character_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?character ?name
        WHERE {
            ?character a movie:FilmCharacter .
            ?character foaf:name ?name .
        }
    '''
    characters = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color="#7CCCC7",
                shape='ellipse',
                size=20)
        for row in g.query(character_query)
    ]

    # ---- Bond Girls ----
    bondgirl_query = '''
        PREFIX bond: <http://example.org/bond/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?bondgirl ?name
        WHERE {
            ?bondgirl a bond:BondGirl .
            ?bondgirl foaf:name ?name .
        }
    '''
    bondgirls = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color='#7CCCC7',
                shape='ellipse',
                size=20)
        for row in g.query(bondgirl_query)
    ]

    # ---- Villains ----
    villain_query = '''
        PREFIX bond: <http://example.org/bond/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?villain ?name
        WHERE {
            ?villain a bond:Villain .
            ?villain foaf:name ?name .
        }
    '''
    villains = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color="#7CCCC7",
                shape='ellipse',
                size=22)
        for row in g.query(villain_query)
    ]

    # ---- Locations ----
    location_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?location ?label
        WHERE {
            ?location a movie:FilmLocation .
            ?location rdfs:label ?label .
        }
    '''
    locations = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color='#90EE90',
                shape='dot',
                size=18)
        for row in g.query(location_query)
    ]

    # ---- Vehicles ----
    vehicle_query = '''
        PREFIX bond: <http://example.org/bond/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?vehicle ?label
        WHERE {
            ?vehicle a bond:Vehicle .
            ?vehicle rdfs:label ?label .
        }
    '''
    vehicles = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color='#7CCCC7',
                shape='ellipse',
                size=18)
        for row in g.query(vehicle_query)
    ]

    # ---- Theme Songs ----
    song_query = '''
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?song ?label
        WHERE {
            ?song a dbo:Song .
            ?song rdfs:label ?label .
        }
    '''
    songs = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color='#7CCCC7',
                shape='ellipse',
                size=18)
        for row in g.query(song_query)
    ]

    # ---- Music Contributors ----
    music_contributor_query = '''
        PREFIX movie: <https://triplydb.com/Triply/linkedmdb/vocab/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?contributor ?name
        WHERE {
            ?contributor a movie:MusicContributor .
            ?contributor foaf:name ?name .
        }
    '''
    music_contributors = [
        Node(id=str(row[0]),
                label=str(row[1]),
                color='#7CCCC7',
                shape='ellipse',
                size=18)
        for row in g.query(music_contributor_query)
    ]

    # ---- Edges: Movie -> Director ----
    director_edges = [
        Edge(source=str(movie),
                label='hasDirector',
                target=str(director))
        for movie, _, director in g.triples((None, BOND.hasDirector, None))
    ]

    # ---- Edges: Movie -> Producer ----
    producer_edges = [
        Edge(source=str(movie),
                label='hasProducer',
                target=str(producer))
        for movie, _, producer in g.triples((None, BOND.hasProducer, None))
    ]

    # ---- Edges: Movie -> BondGirl (hasBondGirl) ----
    bondgirl_edges = [
        Edge(source=str(movie),
                label='hasBondGirl',
                target=str(bondgirl))
        for movie, _, bondgirl in g.triples((None, BOND.hasBondGirl, None))
    ]

    # ---- Edges: Movie -> Villain (hasAntagonist) ----
    villain_edges = [
        Edge(source=str(movie),
                label='hasAntagonist',
                target=str(villain))
        for movie, _, villain in g.triples((None, BOND.hasAntagonist, None))
    ]

    # ---- Edges: Movie -> Character (hasCharacter) ----
    character_edges = [
        Edge(source=str(movie),
                label='hasCharacter',
                target=str(character))
        for movie, _, character in g.triples((None, BOND.hasCharacter, None))
    ]

    # ---- Edges: Character -> Actor (portrayedBy) ----
    portrayed_edges = [
        Edge(source=str(character),
                label='portrayedBy',
                target=str(actor))
        for character, _, actor in g.triples((None, BOND.portrayedBy, None))
    ]

    # ---- Edges: Actor -> Movie (actedIn) ----
    acted_in_edges = [
        Edge(source=str(actor),
                label='actedIn',
                target=str(movie))
        for actor, _, movie in g.triples((None, BOND.actedIn, None))
    ]

    # ---- Edges: Character -> Movie (isCharacterIn) ----
    character_in_edges = [
        Edge(source=str(character),
                label='isCharacterIn',
                target=str(movie))
        for character, _, movie in g.triples((None, BOND.isCharacterIn, None))
    ]

    # ---- Edges: Movie -> Location ----
    location_edges = [
        Edge(source=str(movie),
                label='hasLocation',
                target=str(location))
        for movie, _, location in g.triples((None, BOND.hasLocation, None))
    ]

    # ---- Edges: Movie -> Vehicle ----
    vehicle_edges = [
        Edge(source=str(movie),
                label='hasVehicle',
                target=str(vehicle))
        for movie, _, vehicle in g.triples((None, BOND.hasVehicle, None))
    ]

    # ---- Edges: Movie -> ThemeSong ----
    song_edges = [
        Edge(source=str(movie),
                label='hasThemeSong',
                target=str(song))
        for movie, _, song in g.triples((None, BOND.hasThemeSong, None))
    ]

    # ---- Edges: Song -> MusicContributor ----
    performer_edges = [
        Edge(source=str(song),
                label='isPerformedBy',
                target=str(contributor))
        for song, _, contributor in g.triples((None, BOND.isPerformedBy, None))
    ]

    return {
        "movies": movies,
        "movie_attributes": movie_attributes,
        "directors": directors,
        "producers": producers,
        "actors": actors,
        "characters": characters,
        "bondgirls": bondgirls,
        "villains": villains,
        "locations": locations,
        "vehicles": vehicles,
        "songs": songs,
        "music_contributors": music_contributors,
        "director_edges": director_edges,
        "producer_edges": producer_edges,
        "bondgirl_edges": bondgirl_edges,
        "villain_edges": villain_edges,
        "character_edges": character_edges,
        "movie_attribute_edges": movie_attribute_edges,
        "portrayed_edges": portrayed_edges,
        "acted_in_edges": acted_in_edges,
        "character_in_edges": character_in_edges,
        "location_edges": location_edges,
        "vehicle_edges": vehicle_edges,
        "song_edges": song_edges,
        "performer_edges": performer_edges,
        "bond_actor_attr_nodes": bond_actor_attr_nodes,
        "bond_actor_attr_edges": bond_actor_attr_edges,
        "bond_actor_edges": bond_actor_edges,
    }
