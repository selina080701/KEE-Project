# fandom_request_character.py

import requests
import pandas as pd
from pathlib import Path

def get_character_image_url(character_name, movie_name, actor_name):
    """Retrieve James Bond character image URL from Fandom API
    
    Tries to find character-specific image for a movie, with actor info as fallback
    """
    url = "https://jamesbond.fandom.com/api.php"
    
    # Build search titles in order of preference
    search_titles = []
    
    # Try 1: For James Bond, try with actor first
    if character_name == "James Bond" and actor_name and actor_name != "Unknown":
        search_titles.append(f"James Bond ({actor_name})")
    
    # Try 2: Character (Movie)
    search_titles.append(f"{character_name} ({movie_name})")
    
    # Try 3: Character (Actor)
    if actor_name and actor_name != "Unknown":
        search_titles.append(f"{character_name} ({actor_name})")
    
    # Try 4: Just character name
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

# ---- Fetch images for all character-movie combinations and save to CSV ----
def save_character_images(csv_file):    
    # Load CSV with semicolon separator
    df = pd.read_csv(csv_file, sep=';')
    
    print(f"Total entries: {len(df)}\n")
    
    results = []
    
    for idx, row in df.iterrows():
        character = row['character']
        actor = row['actor']
        movie = row['movie']
        
        print(f"[{idx+1}/{len(df)}] {character} → {actor} ({movie})")
        
        # Get image URL for this specific character-movie combination
        img_url, found_title = get_character_image_url(character, movie, actor)
        
        if img_url:
            print(f"  ✓ Found: {found_title}")
        
        results.append({
            'character': character,
            'actor': actor,
            'movie': movie,
            'image_url': img_url if img_url else '',
            'search_title': found_title if found_title else ''
        })
    
    # Save to CSV
    output_dir = Path("extract_knowledge/characters")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "all_movie_characters_with_image_1.csv"
    
    results_df = pd.DataFrame(results)
    results_df = results_df[['character', 'actor', 'movie', 'image_url', 'search_title']]
    results_df.to_csv(output_file, index=False, encoding='utf-8', sep=';')
    
    print(f"\n✓ Character images saved to {output_file}")
    print(f"  Total: {len(results)} entries")
    print(f"  With images: {results_df['image_url'].notna().sum()}")




if __name__ == "__main__":
    csv_file = Path("extract_knowledge/characters/all_movie_characters.csv")
    
    if not csv_file.exists():
        print(f"Error: {csv_file} not found!")
    else:
        save_character_images(csv_file)