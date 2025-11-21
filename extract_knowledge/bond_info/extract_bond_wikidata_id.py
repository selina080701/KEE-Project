# extract_bond_wikidata_id.py
# with timeout=60, otherwise: ReadTimeoutError

import pandas as pd
import requests
import time


def load_unique_bond_actors(csv_path: str):
    """
    Load James Bond dataset and return sorted list
    of unique Bond actor names from the 'Bond' column.
    """
    df = pd.read_csv(csv_path, sep=";")
    actors = df["Bond"].unique()
    return sorted(actors)


def retrieve_wikidata_actor_uri(name: str) -> str | None:
    """
    Retrieve Wikidata URI for bond actor name. Search for resources
    with occupation film actor or television actor.
    """

    query = f"""
PREFIX wd:   <http://www.wikidata.org/entity/>
PREFIX wdt:  <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?actor WHERE {{
    {{
        ?actor wdt:P106 wd:Q10798782 .   # film actor
    }} 
    UNION 
    {{
        ?actor wdt:P106 wd:Q10800557 .   # television actor
    }}

  OPTIONAL {{ ?actor rdfs:label ?label . FILTER(LANG(?label) = "en") }}
  OPTIONAL {{ ?actor skos:altLabel ?altLabel . FILTER(LANG(?altLabel) = "en") }}

  FILTER(
    LCASE(STR(?label)) = LCASE("{name}") ||
    LCASE(STR(?altLabel)) = LCASE("{name}")
  )
}}
LIMIT 1
"""

    url = "https://query.wikidata.org/sparql"

    response = requests.get(
        url, params={"query": query, "format": "json"}, timeout=60
    )

    if response.status_code != 200:
        print(f"HTTP {response.status_code} for actor: {name}")
        return None

    results = response.json().get("results", {}).get("bindings", [])
    if not results:
        print(f"No match for actor: {name}")
        return None

    return results[0]["actor"]["value"]


def build_actor_id_csv(input_file: str, output_file: str, delay_seconds: float = 2.0):
    """
    Load Bond movie CSV, query Wikidata for each unique actor name,
    and write a new CSV with columns: Bond;wikidata_id;wikidata_url
    """
    actors = load_unique_bond_actors(input_file)
    print("Unique actors:", actors)

    rows = []
    for name in actors:
        print(f"Querying Wikidata for actor: {name} ...")
        time.sleep(delay_seconds)
        uri = retrieve_wikidata_actor_uri(name)

        if uri:
            qid = uri.rsplit("/", 1)[-1]
            rows.append({"Bond": name, "wikidata_id": qid,"wikidata_url": uri})
        else:
            # Keep the actor in the CSV even if we did not find a match
            rows.append({"Bond": name,"wikidata_id": "","wikidata_url": ""})

    out_df = pd.DataFrame(rows, columns=["Bond", "wikidata_id", "wikidata_url"])
    out_df.to_csv(output_file, index=False, sep=";")
    print(f"Saved actor ID mapping to {output_file}")


if __name__ == "__main__":
    build_actor_id_csv("../../data/jamesbond_with_id.csv","bond_with_ids.csv")
