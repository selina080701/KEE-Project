from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def get_film_info_dbpedia(title: str) -> pd.DataFrame:
    # set data source
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    # prepare sparql query
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?film ?title ?releaseDate ?runtime ?actorName
    WHERE {{
      ?film a dbo:Film ;
            foaf:name ?title .
      FILTER (langMatches(lang(?title), "en"))
      FILTER regex(?title, "{title}", "i")

      OPTIONAL {{ ?film dbo:releaseDate ?releaseDate . }}
      OPTIONAL {{ ?film dbo:runtime ?runtime . }}
      OPTIONAL {{ ?film dbo:starring ?actor .
                 ?actor foaf:name ?actorName .
                 FILTER(langMatches(lang(?actorName), "en")) }}
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
            "title": r.get("title", {}).get("value"),
            "releaseDate": r.get("releaseDate", {}).get("value"),
            "runtime": r.get("runtime", {}).get("value"),
            "actor": r.get("actorName", {}).get("value")
        })

    return pd.DataFrame(data)

def get_filmography_dbpedia(actor_name: str):
    """
    Gets a person's filmography from dbpedia.
    :param actor_label: (film) actor label
    """
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    # find persons' URI; one entry is enough
    find_uri = f"""
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT DISTINCT ?actor WHERE {{
      ?actor a ?type ; foaf:name ?name .
      FILTER(?type IN (dbo:Actor, dbo:Person))
      FILTER(langMatches(lang(?name), "en"))
      FILTER regex(?name, "{actor_name}", "i")
    }}
    LIMIT 1
    """
    # execute qry
    sparql.setQuery(find_uri)
    uri_results = sparql.query().convert()

    # nothing found, go back
    if not uri_results["results"]["bindings"]:
        print("Kein Schauspieler gefunden.")
        return pd.DataFrame()

    # extract actor's URI
    actor_uri = uri_results["results"]["bindings"][0]["actor"]["value"]

    # find filmography of the actor
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?film ?title ?releaseDate ?directorName
    WHERE {{
      ?film a dbo:Film ;
            dbo:starring <{actor_uri}> .
      OPTIONAL {{ ?film rdfs:label ?title . FILTER(langMatches(lang(?title), "en")) }}
      OPTIONAL {{ ?film dbo:releaseDate ?releaseDate . }}
      OPTIONAL {{ ?film dbo:director ?director .
                 ?director rdfs:label ?directorName .
                 FILTER(langMatches(lang(?directorName), "en")) }}
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
        title = r.get("title", {}).get("value")
        # take only entries with a title
        if not title:  # None oder leere Strings überspringen
            continue

        data.append({
            "film_uri": r.get("film", {}).get("value"),
            "title": title,
            "releaseDate": r.get("releaseDate", {}).get("value"),
            "director": r.get("directorName", {}).get("value")
        })

    # if no films are found, give back a None
    if not data:
        print("no films found.")
        return None

    return pd.DataFrame(data)

# main handler
if __name__ == "__main__":
    # set a film title
    title = "The Longest Day"
    print(f'get actors of the film {title} using dbpedia')
    df = get_film_info_dbpedia(title)
    df = df['actor']
    for actor in df:
        if actor is not None:
            print(f'{actor}')
            films_actor = get_filmography_dbpedia(actor)
            if not films_actor.empty:
                for film in films_actor['title']:
                    print(f'\t{film}')
            else:
                print(f'\t no film found')
        else:
            print(f'not valid actor')
