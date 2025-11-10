# fandom_request_single_movie.py

import requests
import wikitextparser as wtp
import json
from pathlib import Path


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
    output_dir = Path("./extract_knowledge/fandom_wiki_pages")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filepath}")



if __name__ == "__main__":
    movie_title = "A View to a Kill (film)"
    data = get_fandom_page_text(movie_title)
    if data:
        filename = movie_title.replace(" ", "_").replace("(", "").replace(")", "") + ".json"
        save_data_to_json(data, filename)
    
