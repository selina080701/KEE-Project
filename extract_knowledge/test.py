import json
import re
import spacy
from geopy.geocoders import Nominatim
import time
import pandas as pd

nlp = spacy.load("en_core_web_lg")
PLACE_LABELS = {"GPE", "LOC", "FAC"}

# ------------ Extraction ------------
def extract_places(input_text, output_csv):
    with open(input_text, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Limit text search to specific fields
    sections = data.get("sections", {})

    locations_text = ""
    if "Locations" in sections:
        locations_text += str(sections["Locations"])
    if "Film locations" in sections:
        locations_text += str(sections["Film locations"])
    if "Shooting locations" in sections:
        locations_text += str(sections["Shooting locations"])
    
    if not locations_text:
        print("No location-related fields found.")
        return []

    # Remove wiki link syntax [[...]] but keep the display text
    locations_text = re.sub(r"\[\[([^\]|]+)(\|[^\]]+)?\]\]", r"\1", locations_text)

    # spaCy Named Entity Recognition
    doc = nlp(locations_text)
    places = sorted(set(ent.text for ent in doc.ents if ent.label_ in PLACE_LABELS))

    with open(output_csv, "w", encoding="utf-8") as f:
        df = pd.DataFrame(places, columns=["location"])
        df.to_csv(f, index=False)

    return places


# ------------ Cleaning ------------
def clean_place_name(name):
    #name = re.sub(r"\[\[|\]\]", "", name)       # remove [ OR ] brackets
    #name = re.sub(r".*\|", "", name)            # remove everything before and including |
    #name = name.strip(" \"\n\t")                # strip whitespace and quotes
    #name = re.sub(r".*\*", "", name)            # remove everything before an * asterisk
    #name = re.sub(r"\s*\(.*?\)\s*", "", name)   # remove text within parentheses
    #return name
    pass

def postprocess_places(raw_places):
    cleaned = set()
    for p in raw_places:
        cp = clean_place_name(p)
        if len(cp) < 3: # skip very short names
            continue
        cleaned.add(cp)
    return sorted(cleaned)


# ------------ Geocoding ------------
geolocator = Nominatim(user_agent="James_Bond_Universe_Geocoder")

def geocode_locations(locations):
    coords = []
    for loc in locations:
        try:
            geo = geolocator.geocode(loc)
            if geo:
                coords.append({
                    "name": loc,
                    "lat": geo.latitude,
                    "lon": geo.longitude,
                    "movie": "A View to a Kill"
                })
            time.sleep(1)
        except:
            pass

    with open("geocoded_locations/geocoded_locations_raw.csv", "w", encoding="utf-8") as f:
        df = pd.DataFrame(coords)
        df.to_csv(f, index=False)
    return coords

# ------------ Manual deletion of specific lines ------------
def delete_specific_names(input_file, output_file, names_to_delete):
    """
    Deletes rows based on names in the 'name' column.
    
    Args:
        input_file: Path to the input CSV file
        output_file: Path to the output CSV file
        names_to_delete: List of names to delete
    """
    df = pd.read_csv(input_file)
    
    # Filter rows whose names are not in the list to delete
    df_filtered = df[~df['name'].isin(names_to_delete)]
    df_filtered.to_csv(output_file, index=False, lineterminator='\n')
    
    print(f"Deleted: {len(df) - len(df_filtered)} rows")
    print(f"Remaining: {len(df_filtered)} rows")
    print(f"Saved to: {output_file}")



if __name__ == "__main__":
    raw_places = extract_places(input_text="fandom_wiki_pages/A_View_to_a_Kill_film.json",
                                output_csv="geocoded_locations/extracted_locations.csv")
    
    
    #final_places = postprocess_places(raw_places)
    #geo_locations = geocode_locations(final_places)

"""
    # manual post processing to delete specific names
    names_to_delete = ['\""A View', '"\""For"', 'link', 'U.S.', 'Silicon', 'Jenny']
    delete_specific_names(input_file="geocoded_locations/geocoded_locations_raw.csv", 
                          output_file="geocoded_locations/geocoded_locations.csv", 
                          names_to_delete=names_to_delete)
"""