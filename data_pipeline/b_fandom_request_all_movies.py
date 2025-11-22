# b_fandom_request_all_movies.py

import requests
import wikitextparser as wtp
import json
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from utils.bond_films import BOND_FILMS

"""
This file retrieves unstructured text data from the James Bond Fandom Wiki for all movies in the BOND_FILMS list.
It extracts sections and infoboxes from each movie's wiki page and saves the data in JSON format.
    -> Input: BOND_FILMS list from utils/bond_films.py
    -> Output: JSON files in extract_knowledge/fandom_wiki_pages/ directory
"""

def get_fandom_page_text(movie_title):
    """Retrieve Wikitext and parse Sections and Infoboxes"""
    url = "https://jamesbond.fandom.com/api.php"
    params = {
        "action": "parse",
        "page": movie_title,
        "format": "json",
        "prop": "wikitext"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if 'error' in data:
            print(f"Error retrieving {movie_title}: {data['error']['info']}")
            return None

        wikitext = data['parse']['wikitext']['*']
        parsed = wtp.parse(wikitext)

        # Extract sections
        sections = {}
        for sec in parsed.sections:
            title = sec.title if sec.title else "intro"
            sections[title] = sec.contents.strip()

        # Extract infoboxes
        infobox = {}
        templates = parsed.templates
        for template in templates:
            if 'Infobox' in template.name.strip():
                for arg in template.arguments:
                    key = arg.name.strip()
                    value = arg.value.strip()
                    infobox[key] = value
                break
        return {"title": movie_title,
                "sections": sections,
                "infobox": infobox}
    
    except Exception as e:
        print(f"Error processing {movie_title}: {e}")
        return None

def save_data_to_json(data, filename):
    """Save extracted movie-data to a JSON file"""
    base_dir = Path(__file__).resolve().parent.parent
    
    output_dir = base_dir / "extract_knowledge/fandom_wiki_pages"
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filepath}")


if __name__ == "__main__":
    successful = 0
    failed = 0
    
    for i, film in enumerate(BOND_FILMS, start=1):
        print(f"Processing ({i}/{len(BOND_FILMS)}): {film}")

        movie_data = get_fandom_page_text(film)

        if movie_data:
            filename = film.replace(" ", "_").replace("(", "").replace(")", "") + ".json"
            save_data_to_json(movie_data, filename)
            successful += 1
        else:
            failed += 1

    print(f"Successfully processed: {successful}")
    print(f"Failed to process: {failed}")