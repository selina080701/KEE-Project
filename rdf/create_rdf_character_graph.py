import csv
import re
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

def clean_uri_component(text):
    """Clean text to make it URI-safe"""
    # Remove or replace invalid URI characters
    text = text.replace(" ", "_")
    text = text.replace(".", "")
    text = text.replace("'", "")
    text = text.replace('"', "")
    text = text.replace("|", "_")
    text = text.replace(":", "_")
    text = text.replace("/", "_")
    text = text.replace("\\", "_")
    text = text.replace("?", "")
    text = text.replace("#", "")
    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace(",", "")
    text = text.replace(";", "")
    text = text.replace("&", "and")
    text = text.replace("@", "at")
    text = text.replace("!", "")
    text = text.replace("*", "")
    text = text.replace("+", "plus")
    text = text.replace("=", "")
    text = text.replace("%", "percent")
    
    # Remove any remaining non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    
    # Remove leading/trailing underscores and collapse multiple underscores
    text = re.sub(r'_+', '_', text)
    text = text.strip('_')
    
    return text

def serialize_characters_to_rdf(input_file, output_file):
    # Namespaces basierend auf LinkedMDB
    MOVIE = Namespace("https://triplydb.com/Triply/linkedmdb/vocab/")
    
    g = Graph()
    g.bind("movie", MOVIE)
    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)

    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            # Skip unknown actors
            if row["actor"] == "Unknown":
                continue
                
            # Movie URI
            movie_title_uri = clean_uri_component(row["movie"])
            movie_uri = MOVIE["Film/" + movie_title_uri]
            
            # Character URI
            character_name = row["character"]
            character_name_uri = clean_uri_component(character_name)
            character_uri = MOVIE["FilmCharacter/" + character_name_uri]
            
            # Actor URI
            actor_name = row["actor"]
            actor_name_uri = clean_uri_component(actor_name)
            actor_uri = MOVIE["Actor/" + actor_name_uri]
            
            # Movie Triples (minimal)
            g.add((movie_uri, RDF.type, MOVIE.Film))
            g.add((movie_uri, RDFS.label, Literal(row["movie"])))
            
            # Character Triples
            g.add((character_uri, RDF.type, MOVIE.FilmCharacter))
            g.add((character_uri, RDFS.label, Literal(character_name)))
            g.add((character_uri, MOVIE.appearsIn, movie_uri))
            
            # Actor Triples
            g.add((actor_uri, RDF.type, MOVIE.Actor))
            g.add((actor_uri, RDFS.label, Literal(actor_name)))
            
            # HAUPTVERBINDUNG: Actor spielt Character
            g.add((actor_uri, MOVIE.playsCharacter, character_uri))

    turtle_output = g.serialize(format="turtle")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(turtle_output)
    print(f"{len(g)} Triples saved in {output_file}")

if __name__ == "__main__":
    serialize_characters_to_rdf("extract_knowledge/characters/all_movie_characters.csv", "rdf/jamesbond_characters_rdf.ttl")