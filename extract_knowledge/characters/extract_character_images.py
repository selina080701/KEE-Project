# extract_character_images.py

import json
import re
import pandas as pd
from pathlib import Path
from urllib.parse import quote

# ------------ Helper Function ------------
def generate_fandom_image_url(filename):
    """
    Generate Fandom Wiki image URL from filename
    Example: "Bond - Profile.png" -> "https://jamesbond.fandom.com/wiki/File:Bond_-_Profile.png"
    """
    if not filename or filename == "No image":
        return ""
    
    # URL encode the filename (spaces become %20, etc.)
    encoded_filename = quote(filename)
    
    # Fandom Wiki URL pattern
    base_url = "https://jamesbond.fandom.com/wiki/File:"
    
    return base_url + encoded_filename

# ------------ Extraction ------------
def extract_characters(input_text, movie_title):
    with open(input_text, "r", encoding="utf-8") as f:
        data = json.load(f)

    sections = data.get("sections", {})
    
    # Search for Section "Cast and characters" or "Cast & characters"
    cast_text = None
    for key in sections:
        if "cast" in key.lower() and "character" in key.lower():
            cast_text = sections[key]
            break
    
    if not cast_text:
        print("No 'Cast and characters' section found.")
        return []

    cast_data = []
    
    # Pattern for the Gallery-Format:
    # Example: "Le Chiffre (Mads Mikkelsen) - Profile.jpg|[[Le Chiffre (Mads Mikkelsen)|Le Chiffre]]<br>([[Mads Mikkelsen]])|link=..."
    
    # Split by newlines to get individual entries
    lines = cast_text.split('\n')
    
    for line in lines:
        # Skip gallery tags and empty lines
        if not line.strip() or '<gallery' in line or '</gallery>' in line:
            continue
        
        # Extract image filename (before the first |)
        # Pattern: filename.png|[[Character]]...
        image_match = re.match(r'^([^|]+\.(?:png|jpg|jpeg|gif|webp))', line, re.IGNORECASE)
        
        # Extract the character part between the first [[ ]] and <br>
        character_match = re.search(r'\[\[([^\]]+)\]\]', line)
        
        # Extract the actor from ([[Actor Name]])
        actor_match = re.search(r'\(\[\[([^\]]+)\]\]\)', line)
        
        if character_match and actor_match:
            # Process Character Name
            character_full = character_match.group(1)
            
            # If format "Name (Actor)|Display" -> take "Display" or "Name"
            if '|' in character_full:
                character = character_full.split('|')[1].strip()
            else:
                character = character_full.strip()
            
            # Remove any (Actor Name) from the character name
            character = re.sub(r'\s*\([^)]+\)$', '', character).strip()
            
            # Process Actor Name
            actor = actor_match.group(1).strip()
            
            # Get image filename if available
            image_filename = ""
            image_url = ""
            if image_match:
                image_filename = image_match.group(1).strip()
                image_url = generate_fandom_image_url(image_filename)
            
            if character and actor:
                cast_data.append({
                    "character": character,
                    "actor": actor,
                    "image": image_filename if image_filename else "No image",
                    "image_url": image_url,
                    "movie": movie_title
                })
        
        # Fallback for entries without actor
        elif character_match and not actor_match:
            character_full = character_match.group(1)
            if '|' in character_full:
                character = character_full.split('|')[1].strip()
            else:
                character = character_full.strip()
            
            character = re.sub(r'\s*\([^)]+\)$', '', character).strip()
            
            # Get image filename if available
            image_filename = ""
            image_url = ""
            if image_match:
                image_filename = image_match.group(1).strip()
                image_url = generate_fandom_image_url(image_filename)
            
            if character:
                cast_data.append({
                    "character": character,
                    "actor": "Unknown",
                    "image": image_filename if image_filename else "No image",
                    "image_url": image_url,
                    "movie": movie_title
                })
        
    print(f"Extracted {len(cast_data)} character-actor pairs.")
    return cast_data


# # ------------ Main Execution ------------
if __name__ == "__main__":
    # Get all JSON files from fandom_wiki_pages directory
    input_dir = Path("extract_knowledge/fandom_wiki_pages")
    json_files = list(input_dir.glob("*_film.json"))
    
    if not json_files:
        print("No JSON files found in 'fandom_wiki_pages' directory.")
    else:
        print(f"Found {len(json_files)} JSON files to process.\n")

        # Collect all character data
        all_characters = []
        
        # Process each file
        for json_file in json_files:
            # Remove "_film" suffix and replace underscores with spaces for readable movie title
            movie_title = json_file.stem.replace("_film", "").replace("_", " ")
            
            print(f"Processing: {json_file.name} (Movie: {movie_title})")
            try:
                characters = extract_characters(str(json_file), movie_title)
                
                if characters:
                    all_characters.extend(characters)
                    print(f"First 3 entries:")
                    for entry in characters[:3]:
                        print(f"  {entry['character']} → {entry['actor']}")
                        print(f"    Image: {entry['image']}")
                        print(f"    URL: {entry['image_url']}")
                else:
                    print(f"No characters extracted")
                    
            except Exception as e:
                print(f"Error processing {json_file.name}: {e}")
            
            print()  # Empty line between movies
                  
        # Save all data to a single CSV
        if all_characters:
            df = pd.DataFrame(all_characters)
            
            # Remove duplicates (same character, actor, and movie)
            df = df.drop_duplicates(subset=['character', 'actor', 'movie'])
            
            # Reorder columns
            df = df[['character', 'actor', 'image', 'image_url', 'movie']]
            
            # Save to CSV
            output_file = Path("extract_knowledge/characters/all_movie_characters.csv")
            df.to_csv(output_file, index=False, encoding="utf-8", sep=';')

            print(f"\nProcessing complete")
            print(f"Total entries: {len(df)}")
            print(f"Saved to: {output_file}")
            print(f"\nFirst 5 entries with URLs:")
            for idx, row in df.head(5).iterrows():
                print(f"\n{row['character']} ({row['actor']})")
                print(f"  Movie: {row['movie']}")
                print(f"  URL: {row['image_url']}")
        else:
            print("\nNo characters were extracted from any files.")