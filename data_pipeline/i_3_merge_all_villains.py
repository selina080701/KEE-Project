# i_3_merge_all_villains.py

import pandas as pd
from pathlib import Path

"""
This file merges the extracted villains from Wikipedia and the classified villain-characters by the LLM into a single CSV file.
Only villains with images are retained in the final output.
Input:
    - extract_knowledge/villains/villains_with_images.csv
    - extract_knowledge/villains/villains_with_LLM.csv
Output:
    - extract_knowledge/villains/all_villains_with_images.csv
"""

# Define base directory and paths
BASE_DIR = Path(__file__).parent.parent
WIKIPEDIA_VILLAINS_FILE = BASE_DIR / "extract_knowledge" / "villains" / "villains_with_images.csv"
LLM_VILLAINS_FILE = BASE_DIR / "extract_knowledge" / "villains" / "villains_with_LLM.csv"
OUTPUT_FILE = BASE_DIR / "extract_knowledge" / "villains" / "all_villains_with_images.csv"


def merge_villains():
    # Load Wikipedia villains
    print(f"\nLoading Wikipedia villains from: {WIKIPEDIA_VILLAINS_FILE.name}")
    df_wikipedia = pd.read_csv(WIKIPEDIA_VILLAINS_FILE, sep=';')
    print(f"Loaded {len(df_wikipedia)} villains from Wikipedia")

    # Load LLM-classified villains
    print(f"\nLoading LLM-classified villains from: {LLM_VILLAINS_FILE.name}")
    df_llm = pd.read_csv(LLM_VILLAINS_FILE, sep=';')
    print(f"Loaded {len(df_llm)} villains from LLM classification")

    # Ensure both dataframes have the same columns
    required_columns = ['Film', 'Villain', 'Portrayed by', 'Objective', 'Outcome', 'Status', 'image_url']

    # Verify columns exist
    for col in required_columns:
        if col not in df_wikipedia.columns:
            print(f"Warning: Column '{col}' missing from Wikipedia data")
        if col not in df_llm.columns:
            print(f"Warning: Column '{col}' missing from LLM data")

    # Concatenate both dataframes
    print("\nMerging datasets...")
    df_merged = pd.concat([df_wikipedia, df_llm], ignore_index=True)
    print(f"Total entries after merge: {len(df_merged)}")

    # Remove duplicates based on Film and Villain name (case-insensitive)
    print("\nRemoving duplicates...")
    initial_count = len(df_merged)

    # Create normalized keys for duplicate detection
    df_merged['_film_lower'] = df_merged['Film'].str.strip().str.lower()
    df_merged['_villain_lower'] = df_merged['Villain'].str.strip().str.lower()

    # Remove duplicates, keeping the first occurrence (Wikipedia takes precedence)
    df_merged = df_merged.drop_duplicates(subset=['_film_lower', '_villain_lower'], keep='first')

    # Drop temporary columns
    df_merged = df_merged.drop(columns=['_film_lower', '_villain_lower'])

    duplicates_removed = initial_count - len(df_merged)
    print(f"Removed {duplicates_removed} duplicate entries")
    print(f"Remaining entries: {len(df_merged)}")

    # Filter out entries without images
    print("\nFiltering villains with images...")
    df_with_images = df_merged[df_merged['image_url'].notna() & (df_merged['image_url'] != '')]

    villains_without_images = len(df_merged) - len(df_with_images)
    print(f"Removed {villains_without_images} villains without images")
    print(f"Final count with images: {len(df_with_images)}")

    # Sort by Film name for better readability
    df_with_images = df_with_images.sort_values(by='Film')

    # Save merged data
    print(f"\nSaving merged data to: {OUTPUT_FILE.name}")
    df_with_images.to_csv(OUTPUT_FILE, index=False, encoding='utf-8', sep=';')


    print(f"\nFinal statistics:")
    print(f"  Wikipedia villains: {len(df_wikipedia)}")
    print(f"  LLM villains: {len(df_llm)}")
    print(f"  Total after merge: {initial_count}")
    print(f"  Duplicates removed: {duplicates_removed}")
    print(f"  Without images: {villains_without_images}")
    print(f"  Final output: {len(df_with_images)} villains")
    print(f"\nOutput saved to: {OUTPUT_FILE}")

    return df_with_images


if __name__ == "__main__":
    merge_villains()
