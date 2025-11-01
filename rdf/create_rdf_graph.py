import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

def serialize_to_rdf(input_file, output_file):
    EX = Namespace("http://example.org/movie/")
    PE = Namespace("http://example.org/person/")
    MO = Namespace("http://example.org/movieontology/")

    g = Graph()
    g.bind("ex", EX)
    g.bind("person", PE)
    g.bind("mo", MO)    

    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            movie_uri = EX["movie_" + row["rank"]]

            director_name = row["directors"]
            director_uri = PE[director_name.replace(" ", "_")]
        
            g.add((movie_uri, RDF.type, MO.Movie))
            g.add((movie_uri, EX.name, Literal(row["name"])))
            g.add((movie_uri, EX.datePublished, Literal(row["year"], datatype=XSD.gYear)))
            g.add((movie_uri, MO.director, director_uri))
            g.add((director_uri, RDF.type, MO.Director))
            g.add((director_uri, EX.name, Literal(director_name)))
            g.add((movie_uri, EX.budget, Literal(int(row["budget"]), datatype=XSD.integer)))
            g.add((movie_uri, EX.rating, Literal(float(row["rating"]), datatype=XSD.decimal)))

            # Genres may have multiple values separated by commas
            genres = row["genre"].split(",")
            for genre in genres:
                g.add((movie_uri, EX.genre, Literal(genre.strip())))

            g.add((movie_uri, EX.sameAs, URIRef(row["wikidata_id"])))

    turtle_output = g.serialize(format="turtle")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(turtle_output)
    print(f"{len(g)} Triples saved in {output_file}")

if __name__ == "__main__":
    serialize_to_rdf("./data/imdb_top_10_test.csv", "./rdf/movies_rdf_output.ttl")
