import pandas as pd
import requests
import time

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

if __name__ == "__main__":
    #clean_raw_data('jamesbond.csv', 'jamesbond_clean.csv')
    add_wikidata_ids_to_dataframe('jamesbond_clean.csv', 'jamesbond_with_id.csv')
