import json
import re
import spacy
from geopy.geocoders import Nominatim
import time
import pandas as pd
from pathlib import Path

nlp = spacy.load("en_core_web_lg")
PLACE_LABELS = {"GPE", "LOC", "FAC"}

# ------------ Extraction ------------
def extract_places(input_text, movie_name):
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
        print(f"No location-related fields found in {movie_name}.")
        return []

    # Remove wiki link syntax [[...]] but keep the display text
    locations_text = re.sub(r"\[\[([^\]|]+)(\|[^\]]+)?\]\]", r"\1", locations_text)

    # spaCy Named Entity Recognition
    doc = nlp(locations_text)
    places = sorted(set(ent.text for ent in doc.ents if ent.label_ in PLACE_LABELS))
    return places

# ------------ Geocoding ------------
geolocator = Nominatim(user_agent="James_Bond_Universe_Geocoder")

def geocode_locations(locations, movie_name):
    coords = []
    for loc in locations:
        try:
            geo = geolocator.geocode(loc)
            if geo:
                coords.append({
                    "name": loc,
                    "lat": geo.latitude,
                    "lon": geo.longitude,
                    "movie": movie_name
                })
            time.sleep(1)
        except:
            pass

    return coords


# ------------ Manual deletion of specific lines, if needed ------------
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
    json_folder = Path("fandom_wiki_pages")

    output_folder = Path("geocoded_locations")
    output_folder.mkdir(exist_ok=True)
    
    all_geocoded = []
    json_files = list(json_folder.glob("*_film.json"))
    print(f"Found {len(json_files)} JSON files\n")
    
    for json_file in json_files:
        # Extract movie title from filename (e.g. "Licence_to_Kill_film.json" -> "Licence to Kill")
        movie_name = json_file.stem.replace("_film", "").replace("_", " ")
        print(f"Processing: {movie_name}")
        
        # Extract places
        raw_places = extract_places(input_text=json_file, movie_name=movie_name)
        print(f"Found {len(raw_places)} unique places")
        
        # Geocode places
        if raw_places:
            geo_locations = geocode_locations(locations=raw_places,

                                              movie_name=movie_name)
            all_geocoded.extend(geo_locations)
            print(f"Geocoded {len(geo_locations)} locations\n")
        else:
            print(f"No places to geocode\n")
    
    # Save all results to a CSV
    output_file = output_folder / "all_movies_geocoded.csv"
    df = pd.DataFrame(all_geocoded)
    df.to_csv(output_file, index=False)


"""
    # manual post processing to delete specific names
    names_to_delete = ['\""A View', '"\""For"', 'link', 'U.S.', 'Silicon', 'Jenny']
    delete_specific_names(input_file="geocoded_locations/geocoded_locations_raw.csv", 
                          output_file="geocoded_locations/geocoded_locations.csv", 
                          names_to_delete=names_to_delete)
"""