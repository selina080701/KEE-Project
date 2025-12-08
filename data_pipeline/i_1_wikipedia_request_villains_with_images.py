# i_1_wikipedia_request_villains_with_images.py

import requests
import pandas as pd
import re
from pathlib import Path

"""
This file retrieves the villain table from Wikipedia's "List of James Bond villains" page (https://en.wikipedia.org/wiki/List_of_James_Bond_villains#Eon_Productions).
It parses the table content to extract structured data about villains from Eon Productions films.
Steps:
    1. Extract villains data from Wikipedia table (Eon Productions only)
    2. Retrieve character image URLs from Fandom API
    3. Post data cleaning:
        3a. Manual corrections based on known issues
        3b. Fill missing image URLs from character database
        3c. Add additional villains that are known but missing/incomplete in Wikipedia (Text based on Fandom Information)
Output:
    - CSV file in folder extract_knowledge/villains (with images)
"""

# ---- Step 1: Extract Villains from Wikipedia ----
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

        return villains_data

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


# ---- Step 2: Retrieve character image URL from Fandom API ----
def get_villain_image_url(villain_name, actor_name=''):
    """
    Tries to find villain image from Fandom wiki
    Tries both "Villain (Actor)" and just "Villain"
    """
    url = "https://jamesbond.fandom.com/api.php"

    # Build search titles in order of preference
    search_titles = []

    # Try 1: Villain (Actor) - most common format on Fandom
    if actor_name:
        # Clean actor name - remove "(body)" or "(voice)" annotations
        clean_actor = re.sub(r'\s*\([^)]*\)', '', actor_name).strip()
        if clean_actor:
            search_titles.append(f"{villain_name} ({clean_actor})")

    # Try 2: Just villain name
    search_titles.append(villain_name)

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


# ---- Main function to extract villains with images ----
def extract_villains_with_images():
    """Extract villains from Wikipedia and fetch their images from Fandom"""

    print("Fetching villains data from Wikipedia...")
    villains_data = get_villains_from_wikipedia()

    if not villains_data:
        print("Failed to retrieve villains data")
        return None

    print(f"Found {len(villains_data)} villains from Wikipedia\n")

    # Extract villains and fetch images
    results = []

    for idx, villain_data in enumerate(villains_data):
        film = villain_data.get('Film', '')
        villain = villain_data.get('Villain', '')
        actor = villain_data.get('Portrayed by', '')
        objective = villain_data.get('Objective', '')
        outcome = villain_data.get('Outcome', '')
        status = villain_data.get('Status', '')

        print(f"[{idx+1}/{len(villains_data)}] {film}: {villain} ({actor})")

        # Get image URL for this villain
        img_url, found_title = get_villain_image_url(villain, actor)

        if img_url:
            print(f"Image found")
        else:
            print(f"No image found")

        results.append({
            'Film': film,
            'Villain': villain,
            'Portrayed by': actor,
            'Objective': objective,
            'Outcome': outcome,
            'Status': status,
            'image_url': img_url if img_url else '',
            'search_title': found_title if found_title else ''
        })

    results_df = pd.DataFrame(results)
    return results_df


# ---- Step 3: Post Data Cleaning ----
def clean_villain_data(df, characters_csv_path):
    """
    Apply post-processing corrections using data from all_movie_characters_with_image.csv
    and add manual villain entries that must be present even if Wikipedia or Fandom
    entries are missing or incomplete.
    """

    # Load the reference character data
    char_df = pd.read_csv(characters_csv_path, sep=';')

    # ---------------------------------------
    # Step 3a: Manual corrections before filling missing images from character database
    # ---------------------------------------
    corrections = [
        # Fix Dr. Julius No villain name
        {
            "Film": "Dr. No",
            "Villain": "Dr.No",
            "correct_villain": "Dr. Julius No"
        },
        # Fix From Russia with Love film name
        {
            "Film": "From Russia With Love",
            "correct_film": "From Russia with Love"
        },
        # Fix Gustav Graves / Colonel Tan-Sun Moon villain name
        {
            "Film": "Die Another Day",
            "Villain": "Gustav Graves / Colonel Tan-Sun Moon",
            "correct_villain": "Gustav Graves",
        },]

    # Apply manual corrections
    for correction in corrections:
        # Build mask based on available fields
        if 'Villain' in correction:
            mask = (
                (df['Villain'] == correction['Villain']) &
                (df['Film'] == correction['Film'])
            )
        else:
            mask = (df['Film'] == correction['Film'])

        if mask.any():
            old_villain = df.loc[mask, 'Villain'].values[0]
            old_film = df.loc[mask, 'Film'].values[0]

            if 'correct_villain' in correction:
                df.loc[mask, 'Villain'] = correction['correct_villain']
                print(f"Corrected villain in {correction['Film']}: '{old_villain}' -> '{correction['correct_villain']}'")

            if 'correct_film' in correction:
                df.loc[mask, 'Film'] = correction['correct_film']
                print(f"Corrected film name: '{old_film}' -> '{correction['correct_film']}'")

    # ---------------------------------------
    # Step 3b: Fill missing image URLs from character database
    # ---------------------------------------
    for idx, row in df.iterrows():
        # If image URL is missing, try to find it in the character database
        if not row['image_url'] or pd.isna(row['image_url']):
            # First try exact match by villain name and film
            char_match = char_df[
                (char_df['character'] == row['Villain']) &
                (char_df['movie'] == row['Film'])
            ]

            # If no exact match, try matching with actor name and movie
            if char_match.empty and row['Portrayed by']:
                # Clean actor name from Wikipedia (remove annotations like "(body)", "(voice)")
                clean_actor = re.sub(r'\s*\([^)]*\)', '', row['Portrayed by']).strip()

                char_match = char_df[
                    (char_df['actor'] == clean_actor) &
                    (char_df['movie'] == row['Film'])
                ]

            if not char_match.empty and char_match.iloc[0]['image_url']:
                img_url = char_match.iloc[0]['image_url']
                search_title = char_match.iloc[0]['search_title']
                df.at[idx, 'image_url'] = img_url
                df.at[idx, 'search_title'] = search_title
                print(f"Added image for {row['Villain']} from character database")

    return df



if __name__ == "__main__":
    # Step 1-2: Extract villains with images
    villains_df = extract_villains_with_images()

    if villains_df is not None:
        # Save to CSV
        output_dir = Path(__file__).parent.parent / "extract_knowledge" / "villains"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "villains_with_images.csv"

        # Reorder columns to match expected format (without search_title in main columns)
        column_order = ['Film', 'Villain', 'Portrayed by', 'Objective', 'Outcome', 'Status', 'image_url']
        villains_df_output = villains_df[column_order]
        villains_df_output.to_csv(output_file, index=False, encoding='utf-8', sep=';')

        print(f"\nVillains with images saved to:")
        print(f"{output_file}")

        # Step 3: Apply data cleaning
        characters_csv = Path(__file__).parent.parent / "extract_knowledge" / "characters" / "all_movie_characters_with_image.csv"

        if characters_csv.exists():
            villains_df = clean_villain_data(villains_df, characters_csv)

            # Save cleaned data to the same file
            villains_df_output = villains_df[column_order]
            villains_df_output.to_csv(output_file, index=False, encoding='utf-8', sep=';')
            print(f"Total villains: {len(villains_df)}")
            print(f"Villains with images: {villains_df['image_url'].notna().sum()}")
        else:
            print(f"Warning: Character reference file not found at {characters_csv}")
            print(f"Skipping data cleaning step.")