import spacy
import json
import re

# Load the spaCy model for English
nlp = spacy.load("en_core_web_lg")

# named entitity recognition labels for places
PLACE_LABELS = {"GPE", "LOC", "FAC"}


def extract_places(json_path):
    """
    Extracts place names from fandom-wiki-pages (json) using spaCy's NER capabilities.
    Args:
        text (str): The input text from which to extract place names.
    Returns:
        list: A list of unique place names found in the text.
    """
    
    # load json file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict):
        text = data.get("Locations") or data.get("Film locations") or json.dumps(data)
    else:
        text = json.dumps(data)

    # process the text with spaCy
    doc = nlp(text)
    places = set()

    for ent in doc.ents:
        if ent.label_ in PLACE_LABELS:
            places.add(ent.text)
            print(f"Named Entity: '{ent.text}'   ->   Label: '{ent.label_}'")
    
    return list(places)


if __name__ == "__main__":
    json_path = "./extract_knowledge/fandom_wiki_pages/A_View_to_a_Kill_film.json"
    
    places = extract_places(json_path)
