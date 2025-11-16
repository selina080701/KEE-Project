# extract_characters_single_movie.py

import json
import re
import pandas as pd

# ------------ Extraction ------------
def extract_characters(input_text, output_csv):
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
        
        # Pattern: [[Character Name (Actor Name)|Display Name]]<br>([[Actor Name]])
        # or: [[Character Name]]<br>([[Actor Name]])
        
        # Extract the part between the first [[ ]] and <br>
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
            
            if character and actor:
                cast_data.append({
                    "character": character,
                    "actor": actor
                })
        
        # Fallback for entries without actor
        elif character_match and not actor_match:
            character_full = character_match.group(1)
            if '|' in character_full:
                character = character_full.split('|')[1].strip()
            else:
                character = character_full.strip()
            
            character = re.sub(r'\s*\([^)]+\)$', '', character).strip()
            
            if character:
                cast_data.append({
                    "character": character,
                    "actor": "Unknown"
                })
    
    # Save as CSV
    df = pd.DataFrame(cast_data)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['character', 'actor'])
    
    df.to_csv(output_csv, index=False, encoding="utf-8", sep=';')
    
    print(f"Extracted {len(df)} character-actor pairs.")
    return cast_data


# # ------------ Main Execution ------------
if __name__ == "__main__":
    movie_title = "A_View_to_a_Kill"  # Change this to the desired movie title
    characters = extract_characters(f"fandom_wiki_pages/{movie_title}_film.json", f"characters/{movie_title}_film.csv")
    
    print("\nExtracted Cast:")
    for entry in characters[:15]:  # Show the first 15
        print(f"  {entry['character']} → {entry['actor']}")