# p_merge_all_data_to_json.py

import csv
import json
import os
from pathlib import Path

"""
This script merges all extracted knowledge data from CSV into a single JSON file.
The 25 James Bond movies are organized as the top-level root nodes.

CSV files processed:
- bond_girls_with_images.csv
- all_movie_characters_with_image.csv
- all_movies_geocoded.csv
- movie_title_en_de.csv
- all_movie_songs.csv
- all_movie_vehicles_with_image.csv
- villains_with_images.csv
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

    # Dictionary to organize data by movie
    movies_dict = {}


    # ---- 1. Read bond girls ----
    bond_girls_path = base_dir / "extract_knowledge/bond_girls/bond_girls_with_images.csv"
    bond_girls = read_csv_with_semicolon(bond_girls_path)

    for girl in bond_girls:
        movie = girl['movie']
        if movie not in movies_dict:
            movies_dict[movie] = {
                "title_en": movie,
                "title_de": "",
                "bond_girls": [],
                "characters": [],
                "locations": [],
                "songs": [],
                "vehicles": [],
                "villains": []
            }
        movies_dict[movie]['bond_girls'].append({
            "name": girl['bond_girl'],
            "actress": girl['actress'],
            "image_url": girl.get('image_url', '')
        })


    # ---- 2. Read all movie characters ----
    characters_path = base_dir / "extract_knowledge/characters/all_movie_characters_with_image.csv"
    characters = read_csv_with_semicolon(characters_path)

    for char in characters:
        movie = char['movie']
        if movie not in movies_dict:
            movies_dict[movie] = {
                "title_en": movie,
                "title_de": "",
                "bond_girls": [],
                "characters": [],
                "locations": [],
                "songs": [],
                "vehicles": [],
                "villains": []
            }
        movies_dict[movie]['characters'].append({
            "name": char['character'],
            "actor": char['actor'],
            "image_url": char.get('image_url', '')
        })


    # ---- 3. Read geocoded locations (comma-separated) ----
    locations_path = base_dir / "extract_knowledge/geocoded_locations/all_movies_geocoded.csv"
    locations = read_csv_with_comma(locations_path)

    for loc in locations:
        movie = loc['movie']
        if movie not in movies_dict:
            movies_dict[movie] = {
                "title_en": movie,
                "title_de": "",
                "bond_girls": [],
                "characters": [],
                "locations": [],
                "songs": [],
                "vehicles": [],
                "villains": []
            }
        movies_dict[movie]['locations'].append({
            "name": loc['name'],
            "latitude": loc.get('lat', ''),
            "longitude": loc.get('lon', '')
        })


    # ---- 4. Read German titles (comma-separated) ----
    titles_path = base_dir / "extract_knowledge/movie_title_german/movie_title_en_de.csv"
    titles = read_csv_with_comma(titles_path)

    title_dict = {}
    for title in titles:
        title_dict[title['title_en']] = title['title_de']

    # Add German titles to movies
    for movie in movies_dict:
        if movie in title_dict:
            movies_dict[movie]['title_de'] = title_dict[movie]


    # ---- 5. Read songs ----
    songs_path = base_dir / "extract_knowledge/songs/all_movie_songs.csv"
    songs = read_csv_with_semicolon(songs_path)

    for song in songs:
        movie = song['movie']
        if movie not in movies_dict:
            movies_dict[movie] = {
                "title_en": movie,
                "title_de": "",
                "bond_girls": [],
                "characters": [],
                "locations": [],
                "songs": [],
                "vehicles": [],
                "villains": []
            }
        movies_dict[movie]['songs'].append({
            "title": song['song'],
            "performer": song['performer'],
            "composer": song.get('composer', ''),
            "youtube_link": song.get('youtube_link', '')
        })


    # ---- 6. Read vehicles ----
    vehicles_path = base_dir / "extract_knowledge/vehicles/all_movie_vehicles_with_image.csv"
    vehicles = read_csv_with_semicolon(vehicles_path)

    for vehicle in vehicles:
        movie = vehicle['movie']
        if movie not in movies_dict:
            movies_dict[movie] = {
                "title_en": movie,
                "title_de": "",
                "bond_girls": [],
                "characters": [],
                "locations": [],
                "songs": [],
                "vehicles": [],
                "villains": []
            }
        movies_dict[movie]['vehicles'].append({
            "name": vehicle['vehicle'],
            "image_url": vehicle.get('image_url', '')
        })

    # ---- 7. Read villains ----
    villains_path = base_dir / "extract_knowledge/villains/villains_with_images.csv"
    villains = read_csv_with_semicolon(villains_path)

    for villain in villains:
        movie = villain['Film']
        if movie not in movies_dict:
            movies_dict[movie] = {
                "title_en": movie,
                "title_de": "",
                "bond_girls": [],
                "characters": [],
                "locations": [],
                "songs": [],
                "vehicles": [],
                "villains": []
            }
        movies_dict[movie]['villains'].append({
            "name": villain['Villain'],
            "actor": villain['Portrayed by'],
            "image_url": villain.get('image_url', ''),
        })


    # Convert dictionary to list
    knowledge_data['movies'] = [
        {"movie": movie, **data}
        for movie, data in sorted(movies_dict.items())
    ]
    knowledge_data['metadata']['total_movies'] = len(movies_dict)

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