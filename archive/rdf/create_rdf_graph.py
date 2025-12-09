import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

def serialize_to_rdf(input_file, output_file):
    EX = Namespace("http://example.org/jamesbond/")
    PE = Namespace("http://example.org/person/")
    MO = Namespace("http://example.org/movieontology/")

    g = Graph()
    g.bind("ex", EX)
    g.bind("person", PE)
    g.bind("mo", MO)    

    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            # URI basierend auf Film-Titel (alternativ könnte man Jahr nutzen)
            movie_title_uri = row["Movie"].replace(" ", "_").replace(".", "")
            movie_uri = EX["movie_" + movie_title_uri]

            # Director URI
            director_name = row["Director"]
            director_uri = PE[director_name.replace(" ", "_")]
            
            # Bond Actor URI
            bond_actor_name = row["Bond"]
            bond_actor_uri = PE[bond_actor_name.replace(" ", "_")]
        
            # Movie Triples
            g.add((movie_uri, RDF.type, MO.Movie))
            g.add((movie_uri, EX.title, Literal(row["Movie"])))
            g.add((movie_uri, EX.year, Literal(int(row["Year"]), datatype=XSD.gYear)))
            g.add((movie_uri, EX.filmLength, Literal(int(row["Film_Length"]), datatype=XSD.integer)))
            g.add((movie_uri, EX.budgetAdjusted, Literal(int(row["Budget_Adj"]), datatype=XSD.integer)))
            g.add((movie_uri, EX.imdbRating, Literal(float(row["Avg_User_IMDB"]), datatype=XSD.decimal)))
            g.add((movie_uri, EX.rottenTomatoesRating, Literal(float(row["Avg_User_Rtn_Tom"]), datatype=XSD.decimal)))
            g.add((movie_uri, EX.sameAs, URIRef(row["wikidata_id"])))
            
            # Director Triples
            g.add((movie_uri, MO.director, director_uri))
            g.add((director_uri, RDF.type, MO.Director))
            g.add((director_uri, EX.name, Literal(director_name)))
            
            # Bond Actor Triples
            g.add((movie_uri, EX.starring, bond_actor_uri))
            g.add((bond_actor_uri, RDF.type, MO.Actor))
            g.add((bond_actor_uri, EX.name, Literal(bond_actor_name)))
            g.add((bond_actor_uri, EX.playsCharacter, Literal("James Bond")))

    turtle_output = g.serialize(format="turtle")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(turtle_output)
    print(f"{len(g)} Triples saved in {output_file}")

if __name__ == "__main__":
    serialize_to_rdf("./data/jamesbond_with_id.csv", "./rdf/jamesbond_rdf.ttl")