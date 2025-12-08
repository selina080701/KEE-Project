# e_extract_characters_all_movies.py

import json
import re
import pandas as pd
from pathlib import Path

"""
This file extracts character and actor information from the downloaded JSON files
representing James Bond movie pages from wiki fandom. It specifically looks for sections titled
"Cast and characters" or "Cast & characters". The extracted data is saved into a single CSV file.
    -> Input: JSON files in extract_knowledge/fandom_wiki_pages/ directory
    -> Output: CSV file in extract_knowledge/characters/ directory
"""

# ------------ Character Extraction ------------
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
    
    # Pattern to look for character and actor pairs in the text. Example:
    # "Le Chiffre (Mads Mikkelsen) - Profile.jpg|[[Le Chiffre (Mads Mikkelsen)|Le Chiffre]]<br>([[Mads Mikkelsen]])|link=..."
    
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
                    "actor": actor,
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
            
            if character:
                cast_data.append({
                    "character": character,
                    "actor": "Unknown",
                    "movie": movie_title
                })
        
    print(f"Extracted {len(cast_data)} character-actor pairs.")
    return cast_data

# ------------ Post Data cleaning ------------
def clean_data(df):
    """
    Correct known data issues in the extracted DataFrame.
    """
    # Add actor names, where "Unknown" was returned, and the correct actor is known from other sources
    actor_corrections = [
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Unknown",
            "movie": "From Russia with Love",
            "correct_actor": "Anthony Dawson"       # Blofeld was portrayed by Anthony Dawson in From Russia with Love
        },
        {
            "character": "Erich Kriegler",
            "actor": "Unknown",
            "movie": "For Your Eyes Only",
            "correct_actor": "John Wyman"           # Kriegler was portrayed by John Wyman in For Your Eyes Only
        },
        {
            "character": "Auric Goldfinger",
            "actor": "Unknown",
            "movie": "Goldfinger",
            "correct_actor": "Gert Fröbe"           # Goldfinger was portrayed by Gert Fröbe in Goldfinger
        },
        {
            "character": "Emilio Largo",
            "actor": "Unknown",
            "movie": "Thunderball",
            "correct_actor": "Adolfo Celi"          # Largo was portrayed by Adolfo Celi in Thunderball
        }
    ]

    # Apply actor corrections
    for correction in actor_corrections:
        mask = (
            (df['character'] == correction['character']) &
            (df['actor'] == correction['actor']) &
            (df['movie'] == correction['movie'])
        )
        df.loc[mask, 'actor'] = correction['correct_actor']

    # Harmonize character names for known inconsistencies
    # Format: {"old_name": "new_name", "actor": "actor_name"} - applies across all movies for that actor
    character_harmonizations = [
        {
            "old_name": "General Anatol Gogol",
            "new_name": "General Gogol",
            "actor": "Walter Gotell"                # Harmonize character name of General Gogol throughout all movies
        },
        {
            "old_name": "Dr. Kananga/Mr. Big",
            "new_name": "Dr. Kananga / Mr. Big",
            "actor": "Yaphet Kotto"                # Harmonize character name of Dr. Kananga / Mr. Big
        },
            
    ]

    # Apply character name harmonizations
    for harmonization in character_harmonizations:
        mask = (
            (df['character'] == harmonization['old_name']) &
            (df['actor'] == harmonization['actor'])
        )
        df.loc[mask, 'character'] = harmonization['new_name']

    # Rename Blofeld entry in Spectre to include Franz Oberhauser alias
    blofeld_spectre_rename = [
        {
            "old_character": "Ernst Stavro Blofeld",
            "new_character": "Franz Oberhauser / Ernst Stavro Blofeld",
            "actor": "Christoph Waltz",
            "movie": "Spectre"
        }
    ]

    for rename in blofeld_spectre_rename:
        mask = (
            (df['character'] == rename['old_character']) &
            (df['actor'] == rename['actor']) &
            (df['movie'] == rename['movie'])
        )
        if mask.any():
            df.loc[mask, 'character'] = rename['new_character']
            print(f"Renamed character: {rename['old_character']} to {rename['new_character']} in {rename['movie']}")

    # Remove unwanted characters, as this will show up in multi occurrences of "Captain"
    df = df[df['character'] != 'Captain']

    # Add missing Blofeld entry in Thunderball
    missing_entries = [
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Anthony Dawson",
            "movie": "Thunderball"
        }
    ]

    for entry in missing_entries:
        # Check if entry already exists
        mask = (
            (df['character'] == entry['character']) &
            (df['actor'] == entry['actor']) &
            (df['movie'] == entry['movie'])
        )

        if not mask.any():
            # Entry doesn't exist, add it
            new_row = pd.DataFrame([entry])
            df = pd.concat([df, new_row], ignore_index=True)
            print(f"Added missing entry: {entry['character']} ({entry['actor']}) in {entry['movie']}")

    return df

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent  
    input_folder = base_dir / "extract_knowledge/fandom_wiki_pages"
    json_files = list(input_folder.glob("*_film.json"))

    output_folder = base_dir / "extract_knowledge/characters"
    output_folder.mkdir(exist_ok=True)
    
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
                    print(f"First 5 entries:")
                    for entry in characters[:5]:
                        print(f"{entry['character']} → {entry['actor']}")
                else:
                    print(f"No characters extracted")
                    
            except Exception as e:
                print(f"Error processing {json_file.name}: {e}")
                  
        # Save all data to a single CSV
        if all_characters:
            df = pd.DataFrame(all_characters)
            
            # Remove duplicates (same character, actor, and movie)
            df = df.drop_duplicates(subset=['character', 'actor', 'movie'])
            
            # Save to CSV
            output_file = output_folder / "all_movie_characters.csv"
            df.to_csv(output_file, index=False, encoding="utf-8", sep=';')

            print(f"\nProcessing complete")
            print(f"Total entries: {len(df)}")
            print(f"Saved to: {output_file}")
            print(f"\nFirst 10 entries:")
            print(df.head(10).to_string(index=False))
        else:
            print("\nNo characters were extracted from any files.")

        # Additional data cleaning and save again
        if all_characters:
            df = clean_data(df)
            # Optionally, save the cleaned data again
            cleaned_output_file = output_folder / "all_movie_characters.csv"
            df.to_csv(cleaned_output_file, index=False, encoding="utf-8", sep=';')
            print(f"\nCleaned data saved to: {cleaned_output_file}")