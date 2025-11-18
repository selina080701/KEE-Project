# extract_vehicles_single_movie.py

import json
import re
import pandas as pd

# ------------ Vehicle Extraction ------------
def extract_vehicles(input_text, output_csv):
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
    print(f"Processing {len(rows)} rows in 'Major vehicles' section.")
    
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
            
            # Get image filename if available
            image_filename = ""
            if image_match:
                image_filename = image_match.group(1).strip()
            
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
                    "sequence": sequence if sequence else "No description available"
                })
    
    # Save as CSV
    df = pd.DataFrame(vehicle_data)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['vehicle'])
    
    df.to_csv(output_csv, index=False, encoding="utf-8", sep=';')
    
    print(f"Extracted {len(df)} vehicles.")
    
    return vehicle_data



if __name__ == "__main__":
    movie_title = "Diamonds_Are_Forever"  # Change movie title here
    vehicles = extract_vehicles(f"extract_knowledge/fandom_wiki_pages/{movie_title}_film.json", f"extract_knowledge/vehicles/{movie_title}_film.csv")
    
    print("\nExtracted Vehicles (first 10):")
    for entry in vehicles[:10]:
        print(f"  {entry['vehicle']}")
        print(f"    Image: {entry['image']}")
        print(f"    Sequence: {entry['sequence'][:80]}..." if len(entry['sequence']) > 80 else f"    Sequence: {entry['sequence']}")