import json
import re
import spacy
from geopy.geocoders import Nominatim
import time
import pandas as pd

nlp = spacy.load("en_core_web_lg")
PLACE_LABELS = {"GPE", "LOC", "FAC"}

# ------------ Cleaning ------------
def clean_place_name(name):
    name = re.sub(r"\[\[|\]\]", "", name)
    name = re.sub(r".*\|", "", name)
    name = name.strip(" \"\n\t")
    return name

def postprocess_places(raw_places):
    cleaned = set()
    for p in raw_places:
        cp = clean_place_name(p)
        if len(cp) < 3:
            continue
        cleaned.add(cp)
    return sorted(cleaned)

# ------------ Extraction ------------
def extract_places(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    text = json.dumps(data)
    doc = nlp(text)

    raw = []

    for ent in doc.ents:
        if ent.label_ in PLACE_LABELS:
            raw.append(ent.text)

    return raw

# ------------ Geocoding ------------
geolocator = Nominatim(user_agent="a_view_to_a_kill_map")

def geocode_locations(locations):
    coords = []
    for loc in locations:
        try:
            geo = geolocator.geocode(loc)
            if geo:
                coords.append({
                    "name": loc,
                    "lat": geo.latitude,
                    "lon": geo.longitude
                })
            time.sleep(1)
        except:
            pass

    with open("geocoded_locations/geocoded_locations.csv", "w", encoding="utf-8") as f:
        df = pd.DataFrame(coords)
        df.to_csv(f, index=False)
    return coords

# ------------ Pipeline ------------
raw_places = extract_places("fandom_wiki_pages/A_View_to_a_Kill_film.json")
final_places = postprocess_places(raw_places)
geo_locations = geocode_locations(final_places)
