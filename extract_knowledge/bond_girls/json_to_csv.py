# json_to_csv.py

import json
import csv
import re

def clean_film_name(film):
    """Remove wiki formatting from film names."""
    # Remove '' quotes around film names
    return re.sub(r"''", "", film).strip()

def parse_names_and_actresses(encounters_str, actresses_str):
    """
    Parse the space-separated names and actresses.
    This is tricky because both names and actresses can have multiple words.
    We'll try to match them by count and common patterns.
    """
    # Handle cases where names are concatenated without spaces
    # e.g., "Pam BouvierLupe Lamora" or "Countess Lisl von SchlafMelina Havelock"

    # Common patterns for splitting
    # Look for lowercase followed by uppercase (indicates new name)
    encounters_str = re.sub(r'([a-z])([A-Z])', r'\1 \2', encounters_str)
    actresses_str = re.sub(r'([a-z])([A-Z])', r'\1 \2', actresses_str)

    # Split on common name separators
    # Names often have patterns like "First Last" or "Title First Last"

    # For actresses, common patterns include full names
    # We need to be smart about splitting

    # Count likely number of entries by looking for capital letters that start names
    # This is a heuristic approach

    encounters = split_names(encounters_str)
    actresses = split_names(actresses_str)

    # Try to match counts
    if len(encounters) != len(actresses):
        # If counts don't match, return as single entries
        return [(encounters_str, actresses_str)]

    return list(zip(encounters, actresses))

def split_names(text):
    """
    Split a string of names into individual names.
    Uses heuristics based on common name patterns.
    """
    # Handle special annotations like "(implied)"
    text = re.sub(r'\s*\(implied\)', '', text)

    # List of known name patterns to help with splitting
    # This is based on the data we've seen

    # Try splitting by looking at patterns
    # Most names are "FirstName LastName" or have titles

    words = text.split()
    names = []
    current_name = []

    for i, word in enumerate(words):
        current_name.append(word)

        # Check if this might be end of a name
        # Heuristics:
        # 1. If next word starts with capital and current word doesn't end with common prefixes
        # 2. If current word is a common last name ending

        is_end = False

        if i == len(words) - 1:
            is_end = True
        else:
            next_word = words[i + 1]
            # Check if next word starts a new name
            # Titles and prefixes that indicate continuation
            continuations = ['von', 'di', 'O\'', 'du', 'de']

            if word.lower() in continuations:
                is_end = False
            elif word in ['Dr.', 'Prof.', 'Miss', 'Countess']:
                is_end = False
            elif next_word in ['Jr.', 'Sr.', 'III', 'II']:
                is_end = False
            elif next_word[0].isupper() and len(current_name) >= 2:
                # Likely a new name starting
                is_end = True
            elif next_word[0].isupper() and word[0].isupper() and len(word) > 2:
                # Two capitalized words in sequence, might be end
                # But need at least firstname lastname
                if len(current_name) >= 2:
                    is_end = True

        if is_end:
            names.append(' '.join(current_name))
            current_name = []

    if current_name:
        names.append(' '.join(current_name))

    return names

def find_main_bond_girl_actress(main_girl, encounters_pairs):
    """Find the actress for the main bond girl from the encounters list."""
    main_girl_clean = main_girl.strip()

    for encounter, actress in encounters_pairs:
        if main_girl_clean in encounter or encounter in main_girl_clean:
            return actress

    # If not found in encounters, return empty
    return ""

def convert_json_to_csv(json_path, csv_path):
    """Convert the bond girls JSON to CSV format."""

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rows = []

    for entry in data['bond_girls']:
        film = clean_film_name(entry['Film'])
        encounters_str = entry['Sexual encounters']
        actresses_str = entry['Actress']
        main_bond_girl = entry['Main Bond girl']

        # Parse names and actresses
        pairs = parse_names_and_actresses(encounters_str, actresses_str)

        # Find main bond girl actress
        main_girl_actress = find_main_bond_girl_actress(main_bond_girl, pairs)

        # Create rows for each encounter
        for encounter, actress in pairs:
            rows.append({
                'movie': film,
                'female_encounters': encounter,
                'actress_female_encounters': actress,
                'main_bond_girl': main_bond_girl,
                'actress_main_bond_girl': main_girl_actress
            })

    # Write to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['movie', 'female_encounters', 'actress_female_encounters',
                      'main_bond_girl', 'actress_main_bond_girl']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV file created: {csv_path}")
    print(f"Total rows: {len(rows)}")

if __name__ == "__main__":
    import os

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(script_dir, 'bond_girls.json')
    csv_path = os.path.join(script_dir, 'bond_girls.csv')

    convert_json_to_csv(json_path, csv_path)