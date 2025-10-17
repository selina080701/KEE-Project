from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def get_wikidata_film_info(title: str):
    # set data source
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    # prepare sparql query
    query = f"""
    SELECT ?film ?filmLabel ?releaseDate ?duration ?actorLabel
    WHERE {{
      ?film wdt:P31 wd:Q11424;       # instance of: film
            rdfs:label "{title}"@en.
      OPTIONAL {{ ?film wdt:P577 ?releaseDate. }}
      OPTIONAL {{ ?film wdt:P2047 ?duration. }}
      OPTIONAL {{ ?film wdt:P161 ?actor. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 100
    """

    # execute sparql query and convert result into a list
    sparql.setQuery(query)
    results = sparql.query().convert()

    # prepare the structure of the return value
    data = []
    for r in results["results"]["bindings"]:
        data.append({
            "title": r.get("filmLabel", {}).get("value"),
            "releaseDate": r.get("releaseDate", {}).get("value"),
            "duration": r.get("duration", {}).get("value"),
            "actor": r.get("actorLabel", {}).get("value")
        })

    return pd.DataFrame(data)


def get_filmography_wikidata(actor_label: str):
    """
    Gets a person's filmography from Wikidata.
    :param actor_label: (film) actor label
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    # find persons' URI; one entry is enough
    find_uri = f"""
    SELECT ?actor WHERE {{
      ?actor rdfs:label "{actor_label}"@en .
    }}
    LIMIT 1
    """
    # execute qry
    sparql.setQuery(find_uri)
    uri_results = sparql.query().convert()

    # nothing found, go back
    if not uri_results["results"]["bindings"]:
        print("no actor found.")
        return pd.DataFrame()

    # extract actor's URI
    actor_uri = uri_results["results"]["bindings"][0]["actor"]["value"]

    # find filmography of the actor
    #SELECT distinct ?film ?filmLabel ?releaseDate ?directorLabel

    query = f"""
    SELECT distinct ?film ?filmLabel ?releaseDate ?directorLabel
    WHERE {{
      ?film wdt:P31 wd:Q11424;          # Film
            wdt:P161 <{actor_uri}>.     # Schauspieler
      OPTIONAL {{ ?film wdt:P577 ?releaseDate. }}
      OPTIONAL {{ ?film wdt:P57 ?director. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    ORDER BY DESC(?releaseDate)
    LIMIT 100
    """
    # execute qry
    sparql.setQuery(query)
    results = sparql.query().convert()

    # prepare result set
    data = []
    for r in results["results"]["bindings"]:
        title = r.get("filmLabel", {}).get("value")
        # take only entries with a title
        if not title:  # None oder leere Strings überspringen
            continue

        data.append({
            "title": r.get("filmLabel", {}).get("value"),
            "releaseDate": r.get("releaseDate", {}).get("value"),
            "director": r.get("directorLabel", {}).get("value")
        })

    # if no films are found, give back an empty dataframe
    if not data:
        print("no films found.")
        return pd.DataFrame()

    return pd.DataFrame(data)

# main handler
if __name__ == "__main__":
    # set a film title
    title = "The Longest Day"
    print(f'get actors of the film {title} using wikidata')
    df = get_wikidata_film_info(title)
    df = df['actor']
    for actor in df:
        if actor is not None:
            print(f'{actor}')
            films_actor = get_filmography_wikidata(actor)
            if not films_actor.empty:
                for film in films_actor['title']:
                    print(f'\t{film}')
            else:
                print(f'\t no film found')
        else:
            print(f'not valid actor')