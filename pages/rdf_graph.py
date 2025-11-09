import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from rdflib import Graph, Namespace
from rdflib.namespace import RDF
from utils.data_loader import load_ttl

def show_rdf_graph():

    # Define Namespaces
    EX = Namespace('http://example.org/jamesbond/')
    MO = Namespace('http://example.org/movieontology/')
    PERSON = Namespace('http://example.org/person/')

    st.header("James Bond Knowledge Graph")

    st.write('The RDF graph represents the relationships between various entities in the James Bond universe,' \
    'including movies, directors, and actors. Use the checkboxes below to customize the visualization of the graph.')
    st.sidebar.info("This is the RDF graph page.")
    config = Config(height=600, width=760)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        all = st.checkbox('Display whole graph')
    with col2:
        display_movies = st.checkbox('Display movies', value=True)
    with col3:
        display_directors = st.checkbox('Display directors', value=True)
    with col4:
        display_actors = st.checkbox('Display Bond actors', value=True)

    # Load graph
    g = Graph()
    ttl_data = load_ttl()
    g.parse(data=ttl_data, format='ttl')

    if all:
        nodes = []
        edges = []
        seen_nodes = []
        for s, p, o in g:
            if s not in seen_nodes:
                nodes.append(Node(id=str(s)))
                seen_nodes.append(s)
            if o not in seen_nodes:
                nodes.append(Node(id=str(o)))
                seen_nodes.append(o)
            edges.append(Edge(source=str(s),
                              label=str(p).split('/')[-1].split('#')[-1],
                              target=str(o)))
        agraph(nodes, edges, config=config)

    else:
        # Query for Movies (with title)
        movies = [
            Node(id=str(s),
                 label=str(title),
                 color='#FF6B6B',
                 shape='box',
                 size=25)
            for s, _, title in g.triples((None, EX.title, None))
        ]

        # Query for Directors
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

        # Query for Actors
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

        # Edges
        directed_by = [
            Edge(source=str(movie),
                 label='director',
                 target=str(director))
            for movie, _, director in g.triples((None, MO.director, None))
        ]

        starring = [
            Edge(source=str(movie),
                 label='starring',
                 target=str(actor),
                 color='#FFD93D')
            for movie, _, actor in g.triples((None, EX.starring, None))
        ]

        # Assemble graph
        nodes = []
        edges = []

        if display_movies:
            nodes += movies
        if display_directors:
            nodes += directors
        if display_actors:
            nodes += actors

        if display_movies and display_directors:
            edges += directed_by
        if display_movies and display_actors:
            edges += starring

        agraph(nodes=nodes, edges=edges, config=config)
