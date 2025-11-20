# json_to_csv.py

import json
import csv
import os
import pandas as pd

def convert_villains_json_to_csv(json_path, csv_path):
    """Convert the villains JSON to CSV format."""

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rows = []

    for entry in data['villains']:
        rows.append({
            'Film': entry.get('Film', ''),
            'Villain': entry.get('Villain', ''),
            'Portrayed by': entry.get('Portrayed by', ''),
            'Objective': entry.get('Objective', ''),
            'Outcome': entry.get('Outcome', ''),
            'Status': entry.get('Status', '')
        })

    # Write to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Film', 'Villain', 'Portrayed by', 'Objective', 'Outcome', 'Status']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV file created: {csv_path}")
    print(f"Total rows: {len(rows)}")


def append_image_url(df_villains, df_url):
    """Append column 'image URLs' from all characters to villains where available."""

    df_villains = pd.read_csv(df_villains, sep=';', encoding='utf-8')
    df_url = pd.read_csv(df_url, sep=';', encoding='utf-8')

    df_villains = df_villains.merge(
        df_url,
        left_on=['Film', 'Villain'],
        right_on=['movie', 'character'],
        how='left'
    )

    df_villains = df_villains.drop(columns=['movie', 'character', 'actor', 'search_title'])
    df_villains.to_csv('villains_with_images.csv', sep=';', index=False, encoding='utf-8')


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(script_dir, 'villains.json')
    csv_path = os.path.join(script_dir, 'villains.csv')

    convert_villains_json_to_csv(json_path, csv_path)

    append_image_url(os.path.join(script_dir, 'villains.csv'), os.path.join(script_dir, '../characters/all_movie_characters_with_image.csv'))