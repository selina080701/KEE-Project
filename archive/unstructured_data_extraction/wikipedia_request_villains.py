# wikipedia_request_villains.py

import requests
import pandas as pd
import json
import re
from pathlib import Path


def get_villains_from_wikipedia():
    """Retrieve the villains tables from Wikipedia's List of James Bond villains page"""
    url = "https://en.wikipedia.org/wiki/List_of_James_Bond_villains"

    try:
        # Use pandas to read all tables from the Wikipedia page
        # Need to add User-Agent header to avoid 403 error
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Fetch the page content with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse tables from the HTML content
        tables = pd.read_html(response.text)

        villains_data = []

        # Refer to the eon_productions table
        eon_table_found = False

        # Process each table that contains villain data
        for i, table in enumerate(tables):
            # Convert column names to strings and clean them
            table.columns = [str(col).strip() for col in table.columns]

            # Check if this table contains villain-related data
            columns_lower = [col.lower() for col in table.columns]

            # Skip tables that don't have a "Film" column
            if 'film' not in columns_lower:
                continue

            # Only process the first table with Film column (Eon Productions)
            if eon_table_found:
                break
            eon_table_found = True

            # Process each row in the table
            for idx, row in table.iterrows():
                row_dict = {}
                for col in table.columns:
                    value = row[col]
                    # Clean the value
                    if pd.notna(value):
                        row_dict[col] = clean_text(str(value))
                    else:
                        row_dict[col] = ""

                # Only add rows that have a Film value
                film_col = [col for col in table.columns if col.lower() == 'film']
                if film_col and row_dict.get(film_col[0], "").strip():
                    villains_data.append(row_dict)

        return {
            "title": "List of James Bond villains",
            "source": url,
            "villains": villains_data
        }

    except Exception as e:
        print(f"Error processing Wikipedia page: {e}")
        return None


def clean_text(text):
    """Clean text from cell content"""
    if not text:
        return ""

    # Remove citation references like [1], [2], etc.
    text = re.sub(r'\[\d+\]', '', text)

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
    data = get_villains_from_wikipedia()
    if data:
        script_dir = Path(__file__).parent
        filepath = script_dir / "villains.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filepath}")
        print(f"Extracted {len(data['villains'])} villains from Wikipedia")