# extract_bond_actors_rdf_simple.py

import csv
import requests
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

INPUT_CSV = "../../data/jamesbond_with_id.csv"
OUTPUT_TTL = "bond_info.ttl"


def load_unique_bond_actors(csv_path: str):
    """
    Load James Bond dataset and return a list
    of unique Bond actor names from the 'Bond' column.
    """
    actors = set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            name = row.get("Bond")
            if name and name.strip():
                actors.add(name.strip())
    return sorted(actors)


def build_sparql_query(actor_names):
    """
    Build SPARQL SELECT query.
    """
    if not actor_names:
        raise ValueError("Actor list is empty.")

    # VALUES block with English labels
    values_lines = []
    for name in actor_names:
        safe_name = name.replace('"', '\\"')
        values_lines.append(f'    "{safe_name}"@en')

    values_block = "  VALUES ?actor_name_en {\n" + "\n".join(values_lines) + "\n  }"

    query = f"""
PREFIX wd:   <http://www.wikidata.org/entity/>
PREFIX wdt:  <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?actor ?actor_label ?gender_label ?country_label ?dob ?dod
WHERE {{
{values_block}

  ?actor rdfs:label ?actor_name_en .
  FILTER(LANG(?actor_name_en) = "en")

  OPTIONAL {{
    ?actor rdfs:label ?actor_label .
    FILTER(LANG(?actor_label) = "en")
  }}
  OPTIONAL {{
    ?actor wdt:P21 ?gender .
    ?gender rdfs:label ?gender_label .
    FILTER(LANG(?gender_label) = "en")
  }}
  OPTIONAL {{
    ?actor wdt:P27 ?country .
    ?country rdfs:label ?country_label .
    FILTER(LANG(?country_label) = "en")
  }}
  OPTIONAL {{ ?actor wdt:P569 ?dob . }}
  OPTIONAL {{ ?actor wdt:P570 ?dod . }}
}}
ORDER BY ?actor_label ?country_label
"""
    return query


def fetch_actor_bindings(query):
    """
    Send the SPARQL query to Wikidata and return the list of bindings.
    """
    url = "https://query.wikidata.org/sparql"
    response = requests.get(url, params={"query": query, "format": "json"}, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["results"]["bindings"]


def build_actor_info(bindings):
    """
    Convert SPARQL bindings into a simple dictionary.
    """
    actors = {}

    for b in bindings:
        # Use actor_label as key; if missing, skip row
        if "actor_label" not in b:
            continue

        label = b["actor_label"]["value"]
        actor_entry = actors.setdefault(
            label,
            {
                "wikidata_uri": b["actor"]["value"],
                "gender": None,
                "countries": set(),
                "dob": None,
                "dod": None,
            },
        )

        if "gender_label" in b:
            actor_entry["gender"] = b["gender_label"]["value"]

        if "country_label" in b:
            actor_entry["countries"].add(b["country_label"]["value"])

        if "dob" in b:
            dob_val = b["dob"]["value"].split("T")[0]
            actor_entry["dob"] = dob_val

        if "dod" in b:
            dod_val = b["dod"]["value"].split("T")[0]
            actor_entry["dod"] = dod_val

    return actors


def serialize_actors_to_rdf(actor_info, output_file):
    """
    Serialize actor info into a Turtle RDF graph using a style
    similar to your existing movie and character RDF.
    """
    EX = Namespace("http://example.org/jamesbond/")
    PE = Namespace("http://example.org/person/")
    MOVIE = Namespace("https://triplydb.com/Triply/linkedmdb/vocab/")

    g = Graph()
    g.bind("ex", EX)
    g.bind("person", PE)
    g.bind("movie", MOVIE)

    for actor_label, info in actor_info.items():
        # Create a local URI for the actor (similar pattern as your colleague)
        actor_uri_local = PE[actor_label.replace(" ", "_")]

        # Type: movie:Actor
        g.add((actor_uri_local, RDF.type, MOVIE.Actor))

        # Human-readable name
        g.add((actor_uri_local, EX.name, Literal(actor_label)))

        # Link to Wikidata entity
        wikidata_uri = info.get("wikidata_uri")
        if wikidata_uri:
            g.add((actor_uri_local, EX.sameAs, URIRef(wikidata_uri)))

        # Gender (as plain text)
        gender = info.get("gender")
        if gender:
            g.add((actor_uri_local, EX.gender, Literal(gender)))

        # Citizenship(s)
        for country in sorted(info.get("countries", [])):
            g.add((actor_uri_local, EX.citizenship, Literal(country)))

        # Date of birth
        dob = info.get("dob")
        if dob:
            g.add((actor_uri_local, EX.dateOfBirth, Literal(dob, datatype=XSD.date)))

        # Date of death
        dod = info.get("dod")
        if dod:
            g.add((actor_uri_local, EX.dateOfDeath, Literal(dod, datatype=XSD.date)))

    turtle_output = g.serialize(format="turtle")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(turtle_output)

    print(f"{len(g)} triples saved in {output_file}")


if __name__ == "__main__":
    # load actors from csv
    actor_names = load_unique_bond_actors(INPUT_CSV)
    print("Actors:", actor_names)

    # get actors info
    sparql_query = build_sparql_query(actor_names)
    bindings = fetch_actor_bindings(sparql_query)

    print("Building actor info dictionary...")
    actor_info = build_actor_info(bindings)

    print("Serializing actors to RDF (Turtle)...")
    serialize_actors_to_rdf(actor_info, OUTPUT_TTL)

    print("Done.")
