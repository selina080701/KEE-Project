# fandom_request_bond_girl_images.py

import requests
import pandas as pd
from pathlib import Path

# ---- Retrieve character image URL from Fandom API ----
def get_bond_girl_image_url(character_name, actress_name):
    """
    Tries to find Bond girl image from Fandom wiki
    """
    url = "https://jamesbond.fandom.com/api.php"

    # Build search titles in order of preference
    search_titles = []

    # Try 1: Character (Actress)
    if actress_name and actress_name != "Unknown":
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

# ---- Fetch images for unique main Bond girls and save to CSV ----
def save_bond_girl_images(csv_file):
    # Load CSV with semicolon separator
    df = pd.read_csv(csv_file, sep=";")

    # Get unique main bond girls with their first actress
    unique_bond_girls = df.groupby('main_bond_girl').first().reset_index()
    unique_bond_girls = unique_bond_girls[['main_bond_girl', 'actress_main_bond_girl', 'movie']]

    print(f"Total unique main Bond girls: {len(unique_bond_girls)}\n")

    results = []

    for idx, row in unique_bond_girls.iterrows():
        character = row['main_bond_girl']
        actress = row['actress_main_bond_girl']
        movie = row['movie']

        print(f"[{idx+1}/{len(unique_bond_girls)}] {character} ({actress})")

        # Get image URL for this Bond girl
        img_url, found_title = get_bond_girl_image_url(character, actress)

        if img_url:
            print(f"  Found: {found_title}")
            print(f"  URL: {img_url}")
        else:
            print(f"  Not found")

        results.append({
            'bond_girl': character,
            'actress': actress,
            'movie': movie,
            'image_url': img_url if img_url else '',
            'search_title': found_title if found_title else ''
        })

    # Save to CSV
    output_dir = Path(__file__).parent
    output_file = output_dir / "bond_girls_with_images.csv"

    results_df = pd.DataFrame(results)
    results_df = results_df[['bond_girl', 'actress', 'movie', 'image_url', 'search_title']]
    results_df.to_csv(output_file, index=False, encoding='utf-8')

    print(f"\nBond girl images saved to {output_file}")
    print(f"  Total: {len(results)} entries")
    print(f"  With images: {sum(1 for r in results if r['image_url'])}")


if __name__ == "__main__":
    csv_file = Path(__file__).parent / "bond_girls.csv"

    if not csv_file.exists():
        print(f"Error: {csv_file} not found!")
    else:
        save_bond_girl_images(csv_file)