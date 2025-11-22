# h_fandom_request_bond_girls_with_images.py

import requests
import wikitextparser as wtp
import pandas as pd
import re
from pathlib import Path

"""
This file retrieves the "Eon series James Bond girls" table from the Bond girl page on the James Bond fandom wiki.
It parses the wikitext content to extract structured data about Bond girls from the specified page.
Steps:
    1. Extract Bond girls data from Fandom wiki page and only keep track of the main Bond girls
    2. Retrieve character image URLs from Fandom API
    3. Post-process data to fix known issues and fill missing images from character database
Output:
    - CSV file in folder extract_knowledge/bond_girls (with images)
"""

# ---- Step 1: Extract Bond Girls from Fandom Wiki ----
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

        return bond_girls_data

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


def clean_film_name(film_name):
    """Remove quotes and extra text from film names"""
    # Remove double quotes
    film_name = film_name.replace("''", "")
    # Remove version text like "2006 version"
    film_name = re.sub(r'\d{4}\s*version', '', film_name)
    return film_name.strip()


# ---- Step 2: Retrieve character image URL from Fandom API ----
def get_bond_girl_image_url(character_name, actress_name=''):
    """
    Tries to find Bond girl image from Fandom wiki
    Tries both "Character (Actress)" and just "Character"
    """
    url = "https://jamesbond.fandom.com/api.php"

    # Build search titles in order of preference
    search_titles = []

    # Try 1: Character (Actress) - most common format on Fandom
    if actress_name:
        search_titles.append(f"{character_name} ({actress_name})")

    # Try 2: Just character name
    search_titles.append(character_name)

    for title in search_titles:
        params = {
            "action": "query",
            "titles": title,
            "prop": "pageimages",
            "piprop": "original",
            "format": "json",
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()

            if 'error' in data:
                continue

            # Parse response to find image URL
            pages = data.get('query', {}).get('pages', {})

            for page_id, page_data in pages.items():
                if page_id == '-1':  # Page doesn't exist
                    continue

                # Try to get the original image URL
                original = page_data.get('original', {})
                if original and 'source' in original:
                    img_url = original['source']
                    # Clean up URL - remove revision parameters
                    img_url = img_url.split('/revision/')[0] if '/revision/' in img_url else img_url
                    img_url = img_url.split('?')[0]  # Remove query parameters
                    return img_url, title

        except Exception as e:
            continue

    return None, None


# ---- Helper function to extract main actress ----
def extract_main_actress(actress_string):
    """Extract the main actress name (last actress in the list, typically first + last name)"""
    # Actresses are space-separated
    actresses_list = actress_string.split()

    if len(actresses_list) >= 2:
        # Get last two words as the main actress (first + last name)
        return ' '.join(actresses_list[-2:])
    elif len(actresses_list) == 1:
        return actresses_list[0]
    else:
        return ''


# ---- Main function to extract main Bond girls with images ----
def extract_main_bond_girls_with_images():
    """Extract main Bond girls from Fandom wiki and fetch their images"""

    print("Fetching Bond girls data from Fandom wiki...")
    bond_girls_data = get_bond_girls_table("Bond girl")

    if not bond_girls_data:
        print("Failed to retrieve Bond girls data")
        return

    print(f"Found {len(bond_girls_data)} movies with Bond girls\n")

    # Extract ONLY main Bond girls
    results = []

    for idx, movie_data in enumerate(bond_girls_data):
        film = clean_film_name(movie_data.get('Film', ''))
        main_bond_girl = movie_data.get('Main Bond girl', '')
        all_actresses = movie_data.get('Actress', '')

        # Extract the main actress (last one in the list)
        main_actress = extract_main_actress(all_actresses)

        print(f"[{idx+1}/{len(bond_girls_data)}] {film}: {main_bond_girl} ({main_actress})")

        # Get image URL for this Bond girl - try with actress name first
        img_url, found_title = get_bond_girl_image_url(main_bond_girl, main_actress)

        if img_url:
            print(f"Image found")
        else:
            print(f"No image found")

        results.append({
            'bond_girl': main_bond_girl,
            'actress': main_actress,
            'movie': film,
            'image_url': img_url if img_url else '',
            'search_title': found_title if found_title else ''
        })

    results_df = pd.DataFrame(results)
    return results_df


# ---- Step 3: Post Data Cleaning ----
def clean_bond_girl_data(df, characters_csv_path):
    """
    Apply post-processing corrections using data from all_movie_characters_with_image.csv
    This fixes incorrect actress names and adds missing image URLs
    """
    # Load the reference character data
    char_df = pd.read_csv(characters_csv_path, sep=';')

    print("\n--- Step 4: Data Cleaning ---")
    print(f"Loaded {len(char_df)} characters from reference database")

    # Manual corrections based on known issues in bond_girls_with_images_test.csv
    corrections = [
        # Fix Tracy Bond actress name
        {
            "bond_girl": "Tracy Bond (Teresa di Vicenzo)",
            "movie": "On Her Majesty's Secret Service",
            "correct_actress": "Diana Rigg"
        },
        # Fix Jinx actress name
        {
            "bond_girl": 'Giacinta "Jinx" Johnson',
            "movie": "Die Another Day",
            "correct_actress": "Halle Berry"
        },
        # Fix Pam Bouvier actress name
        {
            "bond_girl": "Pam Bouvier",
            "movie": "Licence to Kill",
            "correct_actress": "Carey Lowell"
        }
    ]

    # Apply manual corrections
    for correction in corrections:
        mask = (
            (df['bond_girl'] == correction['bond_girl']) &
            (df['movie'] == correction['movie'])
        )
        if mask.any():
            old_actress = df.loc[mask, 'actress'].values[0]
            df.loc[mask, 'actress'] = correction['correct_actress']
            print(f"Corrected actress: {correction['bond_girl']} - '{old_actress}' -> '{correction['correct_actress']}'")

    # Fill missing image URLs from character database
    for idx, row in df.iterrows():
        # If image URL is missing, try to find it in the character database
        if not row['image_url'] or pd.isna(row['image_url']):
            # First try exact match by character name and movie
            char_match = char_df[
                (char_df['character'] == row['bond_girl']) &
                (char_df['movie'] == row['movie'])
            ]

            # If no exact match, try partial matching for complex names
            if char_match.empty:
                # Try matching with actress name and movie
                char_match = char_df[
                    (char_df['actor'] == row['actress']) &
                    (char_df['movie'] == row['movie'])
                ]

            if not char_match.empty and char_match.iloc[0]['image_url']:
                img_url = char_match.iloc[0]['image_url']
                search_title = char_match.iloc[0]['search_title']
                df.at[idx, 'image_url'] = img_url
                df.at[idx, 'search_title'] = search_title
                print(f"Added image for {row['bond_girl']} from character database")

    return df


if __name__ == "__main__":
    # Step 1-3: Extract Bond girls with images
    bond_girls_df = extract_main_bond_girls_with_images()

    # Save to CSV
    output_dir = Path(__file__).parent.parent / "extract_knowledge" / "bond_girls"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "bond_girls_with_images.csv"

    results_df = pd.DataFrame(bond_girls_df)
    results_df = results_df[['bond_girl', 'actress', 'movie', 'image_url', 'search_title']]
    results_df.to_csv(output_file, index=False, encoding='utf-8', sep=';')

    print(f"Main Bond girls with images saved to:")
    print(f"{output_file}")

    # Apply data cleaning
    characters_csv = Path(__file__).parent.parent / "extract_knowledge" / "characters" / "all_movie_characters_with_image.csv"

    if characters_csv.exists():
        bond_girls_df = clean_bond_girl_data(bond_girls_df, characters_csv)

        # Save cleaned data to the same file
        bond_girls_df.to_csv(output_file, index=False, encoding='utf-8', sep=';')
        print(f"\nCleaned Bond girls with images saved to:")
        print(f"{output_file}")
        print(f"Total Bond girls: {len(bond_girls_df)}")
        print(f"Bond girls with images: {bond_girls_df['image_url'].notna().sum()}")
    else:
        print(f"\nWarning: Character reference file not found at {characters_csv}")
        print(f"Skipping data cleaning step.")