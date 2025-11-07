#!/usr/bin/env python3

from rdflib import Graph, Namespace
from rdflib.namespace import RDF

# Namespaces definieren
EX = Namespace('http://example.org/jamesbond/')
MO = Namespace('http://example.org/movieontology/')
PERSON = Namespace('http://example.org/person/')

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

st.write('jamesbond_rdf_output.ttl')
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

# Graph laden
g = Graph()
g.parse(open('jamesbond_rdf_output.ttl', 'rt'), format='ttl')

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
        edges.append(Edge(source=str(s), label=str(p).split('/')[-1].split('#')[-1], target=str(o)))
    agraph(nodes, edges, config=config)
else:
    # Query für Movies (mit title statt name)
    movies = [Node(id=str(s), 
                   label=str(title), 
                   color='#FF6B6B',
                   shape='box',
                   size=25)
              for s, _, title in g.triples((None, EX.title, None))]

    # Query für Directors
    director_query = '''
    PREFIX mo: <http://example.org/movieontology/>
    SELECT DISTINCT ?director
    WHERE {
      ?movie mo:director ?director.
    }'''
    
    directors = [Node(id=str(url[0]),
                     label=str(url[0]).split('/')[-1].replace('_', ' '),
                     color='#4ECDC4',
                     shape='dot',
                     size=20)
                for url in g.query(director_query)]

    # Query für Bond Actors
    actor_query = '''
    PREFIX ex: <http://example.org/jamesbond/>
    PREFIX mo: <http://example.org/movieontology/>
    SELECT DISTINCT ?actor
    WHERE {
      ?movie ex:starring ?actor.
      ?actor a mo:Actor.
    }'''
    
    actors = [Node(id=str(url[0]),
                  label=str(url[0]).split('/')[-1].replace('_', ' '),
                  color='#FFD93D',
                  shape='star',
                  size=22)
             for url in g.query(actor_query)]

    # Edges: Movie -> Director
    directed_by = [Edge(source=str(movie), 
                       label='director', 
                       target=str(director))
                  for movie, _, director in g.triples((None, MO.director, None))]

    # Edges: Movie -> Actor
    starring = [Edge(source=str(movie), 
                    label='starring', 
                    target=str(actor),
                    color='#FFD93D')
               for movie, _, actor in g.triples((None, EX.starring, None))]

    # Nodes zusammenstellen
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