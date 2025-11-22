# a_data_preparation.py
import pandas as pd
import requests
import time
from pathlib import Path

"""
This file takes the raw James Bond dataset and performs data cleaning and enrichment in two steps:
    1. Cleans the raw dataset by selecting relevant columns and saving to a new CSV.
        -> Input: jamesbond.csv
        -> Output: jamesbond_clean.csv
    2. Takes the cleaned input dataset and adds Wikidata movie IDs to each movie entry.
        -> Input: jamesbond_clean.csv
        -> Output: jamesbond_with_id.csv
    3. In an additional step, a list of bond films is created for use in the fandom data extraction.
        -> Input: jamesbond_with_id.csv
        -> Output: utils/bond_films.py
"""

def clean_raw_data(input_file: str, output_file: str):
    df = pd.read_csv(input_file, sep=',')
    # extract relevant columns
    df = df[['Year',
             'Movie',
             'Bond',
             'Director',
             'Budget_Adj',
             'Film_Length',
             'Avg_User_IMDB',
             'Avg_User_Rtn_Tom']]
    df.to_csv(output_file, index=False, sep=';')


def retrieve_wikidata_movie_id(title):
    query = f"""
    SELECT ?film WHERE {{
      ?film wdt:P179 wd:Q2484680.
      OPTIONAL {{ ?film rdfs:label ?label. FILTER(LANG(?label) = "en") }}
      OPTIONAL {{ ?film skos:altLabel ?altLabel. FILTER(LANG(?altLabel) = "en") }}
      FILTER(
        LCASE(STR(?label)) = LCASE("{title}") ||
        LCASE(STR(?altLabel)) = LCASE("{title}") ||
        CONTAINS(LCASE(?label), LCASE("{title}")) ||
        CONTAINS(LCASE(?altLabel), LCASE("{title}"))
      )
    }}
    LIMIT 1
    """
    url = "https://query.wikidata.org/sparql"
    r = requests.get(url, params={"query": query, "format": "json"})

    if r.status_code != 200:
        print(f"HTTP {r.status_code} für Titel: {title}")
        return None

    results = r.json().get("results", {}).get("bindings", [])
    if results:
        return results[0]["film"]["value"]
    else:
        print(f"Kein Treffer für: {title}")
        return None


def add_wikidata_ids_to_dataframe(input_file: str, output_file: str):
    df = pd.read_csv(input_file, sep=";")
    df["wikidata_id"] = df["Movie"].apply(lambda x: (time.sleep(2), retrieve_wikidata_movie_id(x))[1])
    df.to_csv(output_file, index=False, sep=";")

def create_bond_films_list(input_file: str, output_file: str):
    df = pd.read_csv(input_file, sep=";")
    bond_films = df["Movie"].tolist()
    with open(output_file, 'w') as f:
        f.write("BOND_FILMS = [\n")
        for film in bond_films:
            f.write(f'    "{film} (film)",\n')
        f.write("]\n")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    
    """
    Step 1: Clean raw data
    """
    input_raw_file = base_dir / 'data/jamesbond.csv'
    output_clean_file = base_dir / 'data/jamesbond_clean.csv'
    #clean_raw_data(input_raw_file, output_clean_file)

    """
    Step 2: Add Wikidata IDs
    """
    input_clean_file = base_dir / 'data/jamesbond_clean.csv'
    output_clean_file = base_dir / 'data/jamesbond_with_id.csv'
    #add_wikidata_ids_to_dataframe(input_clean_file, output_clean_file)

    """
    Step 3: Create bond films list
    """
    input_with_id_file = base_dir / 'data/jamesbond_with_id.csv'
    output_bond_films_file = base_dir / 'utils/bond_films.py'
    create_bond_films_list(input_with_id_file, output_bond_films_file)


# ---- To Do ----
# - Add Producer column to raw data cleaning step
# - Add new movie 'No Time to Die' to raw data cleaning step
# - Delete Budget and Film Length columns from raw data cleaning step
