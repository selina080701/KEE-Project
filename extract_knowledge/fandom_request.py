import requests
import wikitextparser as wtp
import csv


def get_page_text(movie_title):
    url = "https://jamesbond.fandom.com/api.php"
    params = {
        "action": "parse",
        "page": movie_title,
        "format": "json",
        "prop": "wikitext"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    wikitext = data['parse']['wikitext']['*']

    parsed = wtp.parse(wikitext)

    sections = {}
    for sec in parsed.sections:
        title = sec.title if sec.title else "intro"
        sections[title] = sec.contents.strip()

    return sections


def get_bond_movie_data(movie_title):
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
        wikitext = data['parse']['wikitext']['*']
        
        # Parse mit wikitextparser
        parsed = wtp.parse(wikitext)
        templates = parsed.templates
        
        for template in templates:
            name = template.name.strip().lower()
            print(f"Name: {name}")

        movie_data = {}
        for template in templates:
            if 'Infobox' in template.name:
                for arg in template.arguments:
                    key = arg.name.strip()
                    value = arg.value.strip()
                    movie_data[key] = value
        
        return movie_data
    
    except Exception as e:
        print(f"Fehler bei {movie_title}: {e}")
        return None


if __name__ == "__main__":
    skyfall_box = get_bond_movie_data("Skyfall (film)")
    print(skyfall_box)

    skyfall_text = get_page_text("Skyfall (film)")
    print(skyfall_text)

