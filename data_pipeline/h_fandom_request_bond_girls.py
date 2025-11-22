# fandom_request_bond_girls.py

import requests
import wikitextparser as wtp
import json
import re
from pathlib import Path


def get_bond_girls_table(page_name):
    """Retrieve the 'Eon series James Bond girls' table from the Bond girl page"""
    url = "https://jamesbond.fandom.com/api.php"
    params = {
        "action": "parse",
        "page": page_name,
        "format": "json",
        "prop": "wikitext"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if 'error' in data:
            print(f"Error retrieving {page_name}: {data['error']['info']}")
            return None

        wikitext = data['parse']['wikitext']['*']
        parsed = wtp.parse(wikitext)

        # Find the Films section and extract the Eon series table
        bond_girls_data = []

        for section in parsed.sections:
            section_title = section.title.strip() if section.title else ""

            # Look for the Films section
            if section_title == "Films":
                # Parse tables in this section
                section_parsed = wtp.parse(section.contents)
                tables = section_parsed.tables

                # The first table should be "Eon series James Bond girls"
                if tables:
                    table = tables[0]  # First table is Eon series
                    table_data = table.data()

                    if table_data and len(table_data) > 1:
                        # First row is headers
                        headers = [clean_wikitext(h) for h in table_data[0]]

                        # Process each data row
                        for row in table_data[1:]:
                            row_dict = {}
                            for i, cell in enumerate(row):
                                if i < len(headers):
                                    row_dict[headers[i]] = clean_wikitext(cell)
                            bond_girls_data.append(row_dict)
                break

        return {
            "title": page_name,
            "table_name": "Eon series James Bond girls",
            "bond_girls": bond_girls_data
        }

    except Exception as e:
        print(f"Error processing {page_name}: {e}")
        return None


def clean_wikitext(text):
    """Clean wikitext markup from cell content"""
    if not text:
        return ""

    # Remove [[ ]] links but keep the display text
    text = re.sub(r'\[\[([^|\]]+\|)?([^\]]+)\]\]', r'\2', text)

    # Remove {{ }} templates (simplified)
    text = re.sub(r'\{\{[^}]+\}\}', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text.strip()

def save_data_to_json(data, filename):
    """Save extracted movie-data to a JSON file"""
    output_dir = Path("fandom_wiki_pages")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filepath}")



if __name__ == "__main__":
    page_name = "Bond girl"
    data = get_bond_girls_table(page_name)
    if data:
        filename = "extract_knowledge/bond_girls/bond_girls.json"
        save_data_to_json(data, filename)
        print(f"Extracted {len(data['bond_girls'])} Bond girls from the Eon series table")
    
