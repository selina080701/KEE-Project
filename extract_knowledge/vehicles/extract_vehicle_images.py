# extract_vehicles_images.py

import json
import re
import pandas as pd
from pathlib import Path
from urllib.parse import quote

# ------------ Helper Function ------------
def generate_fandom_image_url(filename):
    """
    Generate Fandom Wiki image URL from filename
    Example: "Vehicle - Ford Mustang.png" -> "https://jamesbond.fandom.com/wiki/File:Vehicle_-_Ford_Mustang.png"
    """
    if not filename or filename == "No image":
        return ""
    
    # URL encode the filename (spaces become %20, etc.)
    encoded_filename = quote(filename)
    
    # Fandom Wiki URL pattern
    base_url = "https://jamesbond.fandom.com/wiki/File:"
    
    return base_url + encoded_filename

# ------------ Extraction ------------
def extract_vehicles(input_text, movie_title):
    with open(input_text, "r", encoding="utf-8") as f:
        data = json.load(f)

    sections = data.get("sections", {})
    
    # Search for Section "Major vehicles"
    vehicle_text = None
    for key in sections:
        if "major vehicles" in key.lower():
            vehicle_text = sections[key]
            break
    
    if not vehicle_text:
        print("No 'Major vehicles' section found.")
        return []

    vehicle_data = []
    
    # Split by table rows (|-) to get individual vehicle entries
    rows = re.split(r'\|-\n', vehicle_text)
    
    for row in rows:
        if not row.strip():
            continue
        
        # Extract Image filename from [[File:...]] or [[File:...|...]]
        image_match = re.search(r'\[\[File:([^\]|]+)(?:\|[^\]]+)?\]\]', row)
        
        # Extract Vehicle Type from bold markup: '''Vehicle Name'''
        vehicle_match = re.search(r"'''[^']*\[\[([^\]]+)\]\][^']*'''", row)
        
        # Extract Movie Sequence (description after the vehicle type)
        sequence_match = re.search(r"''' - ([^\n]+)", row)
        
        if vehicle_match:
            # Process Vehicle Name
            vehicle_full = vehicle_match.group(1)
            
            # Handle pipe syntax: [[Link|Display]] -> take "Display" or full if no pipe
            if '|' in vehicle_full:
                vehicle_name = vehicle_full.split('|')[-1].strip()
            else:
                vehicle_name = vehicle_full.strip()
            
            # Get image filename and URL if available
            image_filename = ""
            image_url = ""
            if image_match:
                image_filename = image_match.group(1).strip()
                image_url = generate_fandom_image_url(image_filename)
            
            # Get sequence/description if available
            sequence = ""
            if sequence_match:
                sequence = sequence_match.group(1).strip()
                # Clean up any remaining wiki markup
                sequence = re.sub(r'\[\[([^\]|]+)\|?([^\]]*)\]\]', r'\2', sequence)
                sequence = re.sub(r'\[\[([^\]]+)\]\]', r'\1', sequence)
                # Remove any remaining markup
                sequence = re.sub(r"'''", '', sequence)
                sequence = sequence.strip()
            
            if vehicle_name:
                vehicle_data.append({
                    "vehicle": vehicle_name,
                    "image": image_filename if image_filename else "No image",
                    "image_url": image_url,
                    "sequence": sequence if sequence else "No description available",
                    "movie": movie_title
                })
    
    print(f"Extracted {len(vehicle_data)} vehicles.")
    return vehicle_data


# ------------ Main Execution ------------
if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = Path("extract_knowledge/vehicles")
    output_dir.mkdir(exist_ok=True)
    
    # Get all JSON files from fandom_wiki_pages directory
    input_dir = Path("extract_knowledge/fandom_wiki_pages")
    json_files = list(input_dir.glob("*_film.json"))
    
    if not json_files:
        print("No JSON files found in 'fandom_wiki_pages' directory.")
    else:
        print(f"Found {len(json_files)} JSON files to process.\n")

        # Collect all vehicle data
        all_vehicles = []
        
        # Process each file
        for json_file in json_files:
            # Remove "_film" suffix and replace underscores with spaces for readable movie title
            movie_title = json_file.stem.replace("_film", "").replace("_", " ")
            
            print(f"Processing: {json_file.name} (Movie: {movie_title})")
            try:
                vehicles = extract_vehicles(str(json_file), movie_title)
                
                if vehicles:
                    all_vehicles.extend(vehicles)
                    print(f"First 3 entries:")
                    for entry in vehicles[:3]:
                        print(f"  {entry['vehicle']}")
                        print(f"    Image: {entry['image']}")
                        print(f"    URL: {entry['image_url']}")
                else:
                    print(f"No vehicles extracted")
                    
            except Exception as e:
                print(f"Error processing {json_file.name}: {e}")
            
            print()  # Empty line between movies
                  
        # Save all data to a single CSV
        if all_vehicles:
            df = pd.DataFrame(all_vehicles)
            
            # Remove duplicates (same vehicle and movie)
            df = df.drop_duplicates(subset=['vehicle', 'movie'])
            
            # Reorder columns
            df = df[['vehicle', 'image', 'image_url', 'sequence', 'movie']]
            
            # Save to CSV
            output_file = output_dir / "all_movie_vehicles.csv"
            df.to_csv(output_file, index=False, encoding="utf-8", sep=';')

            print(f"\nProcessing complete")
            print(f"Total entries: {len(df)}")
            print(f"Saved to: {output_file}")
            print(f"\nFirst 5 entries with URLs:")
            for idx, row in df.head(5).iterrows():
                print(f"\n{row['vehicle']}")
                print(f"  Movie: {row['movie']}")
                print(f"  Image: {row['image']}")
                print(f"  URL: {row['image_url']}")
                print(f"  Sequence: {row['sequence'][:60]}..." if len(row['sequence']) > 60 else f"  Sequence: {row['sequence']}")
        else:
            print("\nNo vehicles were extracted from any files.")