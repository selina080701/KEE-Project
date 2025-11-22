# o_extract_movie_title_german.py

import pandas as pd
import requests
from pathlib import Path

"""
This file extracts the German movie titles from Wikidata using SPARQL queries.
It reads a CSV file with James Bond movies and their Wikidata IDs, fetches the German titles,
and saves the results in a new CSV file.
"""

base_dir = Path(__file__).resolve().parent.parent
INPUT_CSV = base_dir / "data/jamesbond_with_id.csv"
OUTPUT_CSV = base_dir / "extract_knowledge/movie_title_german/movie_title_en_de.csv"

def load_movies(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
    df["qid"] = df["wikidata_id"].str.rsplit("/", n=1).str[-1]
    return df


def fetch_german_titles(qids):
    """
    Get german titles for given Q-IDs and return
    as DataFrame with columns ['qid', 'title_de'].
    """

    # SPARQL Query
    values = " ".join(f"wd:{qid}" for qid in qids)

    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?item ?title_de WHERE {{
      VALUES ?item {{ {values} }}
      ?item rdfs:label ?title_de .
      FILTER(LANG(?title_de) = "de")
    }}
    """

    url = "https://query.wikidata.org/sparql"
    r = requests.get(url, params={"query": query, "format": "json"})
    data = r.json()

    # json to dataframe
    rows = []
    for entry in data["results"]["bindings"]:
        item_url = entry["item"]["value"]
        qid = item_url.rsplit("/", 1)[-1]
        title_de = entry["title_de"]["value"]
        rows.append([qid, title_de])

    german_df = pd.DataFrame(rows, columns=["qid", "title_de"])
    return german_df


if __name__ == "__main__":
    # load movies
    movies = load_movies(INPUT_CSV)
    print(movies.columns)

    # extract Q-ids
    qids = movies["qid"].unique().tolist()

    # get german title
    german_titles = fetch_german_titles(qids)

    # merge dataframes
    merged = movies.merge(german_titles, on="qid", how="left")
    result = merged[["Movie", "title_de"]].rename(columns={"Movie": "title_en"})

    # save as csv
    result.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print("csv saved to", OUTPUT_CSV)
