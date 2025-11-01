import pandas as pd
import requests

def clean_raw_imdb_data(input_file: str, output_file: str):
    df = pd.read_csv(input_file, sep=',')
    # extract relevant columns
    df = df[['rank',
             'name',
             'year',
             'genre',
             'directors',
             'budget',
             'rating']]
    df.to_csv(output_file, index=False, sep=';')


def retrieve_wikidata_movie_id(title, year):
    query = f"""
    SELECT ?film WHERE {{
    {{
    ?film wdt:P31 wd:Q11424.          # Instance of Film
    }} UNION {{
    ?film wdt:P31 wd:Q202866.         # Instance of Animated Film
    }} UNION {{
    ?film wdt:P31 wd:Q24862.          # Instance of Short Film
    }} UNION {{
    ?film wdt:P31 wd:Q271669.         # Instance of Documentary Film
    }} UNION {{
    ?film wdt:P31 wd:Q226730.         # Instance of Silent Film
    }} UNION {{
    ?film wdt:P31 wd:Q20650540.         # Instance of Anime Film
    }}
      ?film rdfs:label ?label.
      ?film wdt:P577 ?date.             # publication date
      FILTER(LCASE(STR(?label)) = LCASE("{title}"))
      FILTER(LANG(?label) = "en")
      FILTER(YEAR(?date) = {year})
    }}
    LIMIT 1
    """
    url = "https://query.wikidata.org/sparql"
    r = requests.get(url, params={"query": query, "format": "json"})
    results = r.json()["results"]["bindings"]
    return results[0]["film"]["value"] if results else None

def add_wikidata_ids_to_dataframe(input_file: str, output_file: str):
    df = pd.read_csv(input_file, sep=";")
    df["wikidata_id"] = df.apply(
        lambda row: retrieve_wikidata_movie_id(row["name"], row["year"]),
        axis=1
    )
    df.to_csv(output_file, index=False, sep=";")
    
if __name__ == "__main__":
    #clean_raw_imdb_data('./data/imdb_1_top_250_raw.csv', './data/imdb_2_top_250_cleaned.csv')
    add_wikidata_ids_to_dataframe('./data/imdb_2_top_250_cleaned.csv', './data/imdb_3_top_250_with_id.csv')