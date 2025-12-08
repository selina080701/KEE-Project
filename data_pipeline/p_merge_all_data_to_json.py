# p_merge_all_data_to_json.py

import csv
import json
import os
from pathlib import Path

"""
This script merges all extracted knowledge data from CSV/JSON into a single JSON file.
The 25 James Bond movies are organized as the top-level root nodes.

CSV/JSON files processed:
- jamesbond_with_id.csv
- bond_girls_with_images.csv
- all_movie_characters_with_image.csv
- all_movies_geocoded.csv
- movie_title_en_de.csv
- all_movie_songs.csv
- all_movie_vehicles_with_image.csv
- all_villains_with_images.csv
- bond_info.json
"""

def read_csv_with_semicolon(file_path):
    """Read CSV file with semicolon delimiter"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            data.append(row)
    return data


def read_csv_with_comma(file_path):
    """Read CSV file with comma delimiter"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            data.append(row)
    return data


def merge_csvs_to_json(output_file):
    # Initialize the main data structure
    knowledge_data = {
        "movies": [],
        "metadata": {
            "total_movies": 0,
            "creation_date": "2025-11-23"
        }
    }

    # Load Bond actor info from JSON
    bond_info_path = base_dir / "extract_knowledge/bond_info/bond_info.json"
    if bond_info_path.exists():
        with open(bond_info_path, "r", encoding="utf-8") as f:
            bond_actors = json.load(f)
    else:
        bond_actors = {}

    # Map actor label -> QID to link movies to actors
    actor_name_to_qid = {}
    for qid, info in bond_actors.items():
        label = (info.get("label") or "").strip()
        if label:
            actor_name_to_qid[label] = qid

    # Dictionary to organize data by movie
    movies_dict = {}

    # ---- 1. Read movie metadata from jamesbond_with_id.csv ----
    movie_metadata_path = base_dir / "data/jamesbond_with_id.csv"
    movie_metadata = read_csv_with_semicolon(movie_metadata_path)

    for movie_info in movie_metadata:
        movie = movie_info['Movie']
        bond_actor_name = movie_info['Bond'].strip()
        bond_actor_qid = actor_name_to_qid.get(bond_actor_name)

        movies_dict[movie] = {
            "title_en": movie,
            "title_de": "",
            "year": movie_info['Year'],
            "bond_actor": bond_actor_name,
            "bond_actor_qid": bond_actor_qid,
            "director": movie_info['Director'],
            "producer": movie_info['Producer'],
            "imdb_rating": movie_info['Avg_User_IMDB'],
            "rotten_tomatoes_rating": movie_info['Avg_User_Rtn_Tom'],
            "wikidata_id": movie_info['wikidata_id'],
            "bond_girls": [],
            "characters": [],
            "locations": [],
            "songs": [],
            "vehicles": [],
            "villains": []
        }

    # ---- 2. Read bond girls ----
    bond_girls_path = base_dir / "extract_knowledge/bond_girls/bond_girls_with_images.csv"
    bond_girls = read_csv_with_semicolon(bond_girls_path)

    for girl in bond_girls:
        movie = girl['movie']
        if movie in movies_dict:
            movies_dict[movie]['bond_girls'].append({
                "name": girl['bond_girl'],
                "actress": girl['actress'],
                "image_url": girl.get('image_url', '')
            })


    # ---- 3. Read all movie characters ----
    characters_path = base_dir / "extract_knowledge/characters/all_movie_characters_with_image.csv"
    characters = read_csv_with_semicolon(characters_path)

    for char in characters:
        movie = char['movie']
        if movie in movies_dict:
            movies_dict[movie]['characters'].append({
                "name": char['character'],
                "actor": char['actor'],
                "image_url": char.get('image_url', '')
            })


    # ---- 4. Read geocoded locations (comma-separated) ----
    locations_path = base_dir / "extract_knowledge/geocoded_locations/all_movies_geocoded.csv"
    locations = read_csv_with_comma(locations_path)

    for loc in locations:
        movie = loc['movie']
        if movie in movies_dict:
            movies_dict[movie]['locations'].append({
                "name": loc['name'],
                "latitude": loc.get('lat', ''),
                "longitude": loc.get('lon', '')
            })


    # ---- 5. Read German titles (comma-separated) ----
    titles_path = base_dir / "extract_knowledge/movie_title_german/movie_title_en_de.csv"
    titles = read_csv_with_comma(titles_path)

    title_dict = {}
    for title in titles:
        title_dict[title['title_en']] = title['title_de']

    # Add German titles to movies
    for movie in movies_dict:
        if movie in title_dict:
            movies_dict[movie]['title_de'] = title_dict[movie]


    # ---- 6. Read songs ----
    songs_path = base_dir / "extract_knowledge/songs/all_movie_songs.csv"
    songs = read_csv_with_semicolon(songs_path)

    for song in songs:
        movie = song['movie']
        if movie in movies_dict:
            movies_dict[movie]['songs'].append({
                "title": song['song'],
                "performer": song['performer'],
                "composer": song.get('composer', ''),
                "youtube_link": song.get('youtube_link', '')
            })


    # ---- 7. Read vehicles ----
    vehicles_path = base_dir / "extract_knowledge/vehicles/all_movie_vehicles_with_image.csv"
    vehicles = read_csv_with_semicolon(vehicles_path)

    for vehicle in vehicles:
        movie = vehicle['movie']
        if movie in movies_dict:
            movies_dict[movie]['vehicles'].append({
                "name": vehicle['vehicle'],
                "image_url": vehicle.get('image_url', ''),
                "sequence_in_movie": vehicle.get('sequence', '')
            })

    # ---- 8. Read villains ----
    villains_path = base_dir / "extract_knowledge/villains/all_villains_with_images.csv"
    villains = read_csv_with_semicolon(villains_path)

    for villain in villains:
        movie = villain['Film']
        if movie in movies_dict:
            movies_dict[movie]['villains'].append({
                "name": villain['Villain'],
                "actor": villain['Portrayed by'],
                "image_url": villain.get('image_url', ''),
                "Objective": villain.get('Objective', ''),
                "Outcome": villain.get('Outcome', ''),
                "Status": villain.get('Status', '')
            })

    # Convert dictionary to list
    knowledge_data['movies'] = [
        {"movie": movie, **data}
        for movie, data in sorted(movies_dict.items())
    ]
    knowledge_data['metadata']['total_movies'] = len(movies_dict)

    # Add actors as a separate top-level block
    knowledge_data['actors'] = bond_actors

    # Write to JSON file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_data, f, ensure_ascii=False, indent=2)

    return knowledge_data


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    json_output = base_dir / "data/triple_store/james_bond_knowledge.json"
    knowledge_data = merge_csvs_to_json(json_output)

    print(f"JSON output: {json_output}")
    print(f"Total movies: {knowledge_data['metadata']['total_movies']}")