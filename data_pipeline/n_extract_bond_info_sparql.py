import pandas as pd
import requests
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
from pathlib import Path

"""
This file queries Wikidata SPARQL endpoint to extract detailed information
about Bond actors using their Wikidata Q-IDs (extracted with m_extract_bond_wikidata_id_sparql.py)
    -> Input: bond_with_ids.csv (folder extract_knowledge/bond_info)
    -> Output: bond_info.ttl in Turtle format
"""

base_dir = Path(__file__).parent.parent
INPUT_CSV = base_dir / "extract_knowledge/bond_info/bond_with_ids.csv"
OUTPUT_TTL = base_dir / "extract_knowledge/bond_info/bond_info.ttl"


def load_actor_qids(csv_path: str):
    """
    Read Q-IDs from the 'wikidata_id' column.
    """
    df = pd.read_csv(csv_path, sep=";")
    return df["wikidata_id"].dropna().tolist()


def build_sparql_query(qids):
    values_lines = [f"wd:{qid}" for qid in qids]
    values_block = "VALUES ?actor {\n" + "\n".join(values_lines) + "\n  }"

    query = f"""
PREFIX wd:   <http://www.wikidata.org/entity/>
PREFIX wdt:  <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?actor ?actor_label ?gender ?gender_label ?country ?country_label ?dob ?dod
WHERE {{
{values_block}

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


def fetch_bindings(query: str):
    url = "https://query.wikidata.org/sparql"
    r = requests.get(url, params={"query": query, "format": "json"}, timeout=30)
    r.raise_for_status()
    return r.json()["results"]["bindings"]


def serialize_bindings_to_rdf(bindings, output_file: str):
    EX = Namespace("http://example.org/jamesbond/")
    PE = Namespace("http://example.org/person/")
    MOVIE = Namespace("https://triplydb.com/Triply/linkedmdb/vocab/")
    CT = Namespace("http://example.org/country/")
    GD = Namespace("http://example.org/gender/")

    g = Graph()
    g.bind("ex", EX)
    g.bind("person", PE)
    g.bind("movie", MOVIE)
    g.bind("country", CT)
    g.bind("gender", GD)

    for b in bindings:
        actor_uri = b["actor"]["value"]
        qid = actor_uri.rsplit("/", 1)[-1]
        actor_local = PE[qid]

        # Actor-Typ
        g.add((actor_local, RDF.type, MOVIE.Actor))

        # Name (Literal)
        if "actor_label" in b:
            g.add((actor_local, RDFS.label, Literal(b["actor_label"]["value"])))

        # sameAs Wikidata
        g.add((actor_local, EX.sameAs, URIRef(actor_uri)))

        # Gender (Ressource)
        if "gender" in b and b["gender"]["value"]:
            gender_qid = b["gender"]["value"].rsplit("/", 1)[-1]
            gender_res = GD[gender_qid]
            g.add((actor_local, EX.gender, gender_res))
            # Label an Gender-Resource hängen
            if "gender_label" in b:
                g.add((gender_res, RDFS.label, Literal(b["gender_label"]["value"])))

        # Citizenship (Ressource)
        if "country" in b and b["country"]["value"]:
            country_qid = b["country"]["value"].rsplit("/", 1)[-1]
            country_res = CT[country_qid]
            g.add((actor_local, EX.citizenship, country_res))
            if "country_label" in b:
                g.add((country_res, RDFS.label, Literal(b["country_label"]["value"])))

        # Dates (Literal)
        if "dob" in b:
            dob = b["dob"]["value"].split("T")[0]
            g.add((actor_local, EX.dateOfBirth, Literal(dob, datatype=XSD.date)))

        if "dod" in b:
            dod = b["dod"]["value"].split("T")[0]
            g.add((actor_local, EX.dateOfDeath, Literal(dod, datatype=XSD.date)))

    g.serialize(destination=output_file, format="turtle")
    print(f"{len(g)} triples saved in {output_file}")


if __name__ == "__main__":
    qids = load_actor_qids(INPUT_CSV)
    print("Actor Q-IDs:", qids)

    query = build_sparql_query(qids)
    bindings = fetch_bindings(query)

    serialize_bindings_to_rdf(bindings, OUTPUT_TTL)
