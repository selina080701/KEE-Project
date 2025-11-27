# n_extract_bond_info_sparql.py

import pandas as pd
import requests
import json
from pathlib import Path

"""
This file queries Wikidata SPARQL endpoint to extract detailed information
about Bond actors using their Wikidata Q-IDs (extracted with m_extract_bond_wikidata_id_sparql.py)
    -> Input: bond_with_ids.csv (folder extract_knowledge/bond_info)
    -> Output: bond_info.json in JSON format
"""

base_dir = Path(__file__).parent.parent
INPUT_CSV = base_dir / "extract_knowledge/bond_info/bond_with_ids.csv"
OUTPUT_JSON = base_dir / "extract_knowledge/bond_info/bond_info.json"


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


def bindings_to_actor_dict(bindings):
    """
    Transform SPARQL bindings into a dict keyed by actor QID.
    """
    actors = {}

    for b in bindings:
        actor_uri = b["actor"]["value"]
        actor_qid = actor_uri.rsplit("/", 1)[-1]

        actor_entry = actors.setdefault(
            actor_qid,
            {
                "actor_uri": actor_uri,
                "label": None,
                "birth_date": None,
                "death_date": None,
                "genders": [],
                "citizenships": [],
            },
        )

        # Label
        if "actor_label" in b and b["actor_label"]["value"]:
            actor_entry["label"] = b["actor_label"]["value"]

        # Birth date
        if "dob" in b and b["dob"]["value"]:
            actor_entry["birth_date"] = b["dob"]["value"].split("T")[0]

        # Death date
        if "dod" in b and b["dod"]["value"]:
            actor_entry["death_date"] = b["dod"]["value"].split("T")[0]

        # Gender
        if "gender" in b and b["gender"]["value"]:
            gender_uri = b["gender"]["value"]
            gender_label = b.get("gender_label", {}).get("value")
            gender_obj = {"uri": gender_uri, "label": gender_label}

            if gender_obj not in actor_entry["genders"]:
                actor_entry["genders"].append(gender_obj)

        # Citizenship
        if "country" in b and b["country"]["value"]:
            country_uri = b["country"]["value"]
            country_label = b.get("country_label", {}).get("value")
            country_obj = {"uri": country_uri, "label": country_label}

            if country_obj not in actor_entry["citizenships"]:
                actor_entry["citizenships"].append(country_obj)

    return actors


def save_actors_to_json(actors_dict, output_file: str):
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(actors_dict, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(actors_dict)} actors to {output_file}")


if __name__ == "__main__":
    qids = load_actor_qids(INPUT_CSV)
    print("Actor Q-IDs:", qids)

    query = build_sparql_query(qids)
    bindings = fetch_bindings(query)

    actors = bindings_to_actor_dict(bindings)
    save_actors_to_json(actors, OUTPUT_JSON)
