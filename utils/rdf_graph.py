# rdf_graph.py

import streamlit as st
from rdflib import Graph, Namespace
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