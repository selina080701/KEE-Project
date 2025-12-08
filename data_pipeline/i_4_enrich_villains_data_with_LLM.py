# i_4_enrich_villains_data_with_LLM.py

import csv
import json
import sys
from pathlib import Path
from groq import Groq

"""
This script enriches villain data by generating missing Status, Objective, and Outcome fields using an the Groq-LLM.
It reads the merged villains CSV file and fills in missing information for villains that don't have complete data.

Input:
    - extract_knowledge/villains/all_villains_with_images.csv
Output:
    - extract_knowledge/villains/all_villains_with_images.csv (updated in place)
"""

# Define base directory and paths
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from utils.config import GROQ_API_KEY

INPUT_FILE = BASE_DIR / "extract_knowledge" / "villains" / "all_villains_with_images.csv"
OUTPUT_FILE = BASE_DIR / "extract_knowledge" / "villains" / "all_villains_with_images.csv"

API_KEY = GROQ_API_KEY

SYSTEM_PROMPT = """
You are an expert on James Bond movies with detailed knowledge of all villains and their storylines.

Given a villain's information (Film, Villain name, and Portrayed by), provide:
1. **Objective**: A concise description of the villain's main goal or evil plan in the movie (1-2 sentences)
2. **Outcome**: What happened to their plan - was it foiled by Bond? How? (1-2 sentences)
3. **Status**: The villain's fate at the end of the movie (1 sentence, e.g., "Killed by Bond", "Arrested", "Survives", etc.)

Be specific and accurate to the James Bond film and use clear, concise language.

Return ONLY a JSON object with this exact structure:
{
  "objective": "...",
  "outcome": "...",
  "status": "..."
}

Do NOT include any explanations or additional text outside the JSON object.
"""


def call_groq(prompt):
    """Call Groq API to generate villain data."""
    client = Groq(api_key=API_KEY)
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
        temperature=0.3,  # Slightly higher for more creative but still accurate responses
        response_format={"type": "json_object"},
    )
    return resp.choices[0].message.content


def is_field_empty(value):
    """Check if a field is empty, None, or just whitespace."""
    return value is None or str(value).strip() == ""


def enrich_villain_data():
    """Enrich villain data by generating missing Status, Objective, and Outcome fields."""
    villains = []
    enriched_count = 0
    skipped_count = 0
    error_count = 0

    # Read villain data
    print(f"Reading villains from: {INPUT_FILE.name}")
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        villains = list(reader)

    print(f"Loaded {len(villains)} villains")
    print("\nProcessing villains with missing data...\n")

    # Process each villain
    for idx, villain in enumerate(villains, 1):
        # Check if any field is missing
        needs_enrichment = (
            is_field_empty(villain.get('Objective')) or
            is_field_empty(villain.get('Outcome')) or
            is_field_empty(villain.get('Status'))
        )

        if not needs_enrichment:
            skipped_count += 1
            continue

        # Generate enrichment data
        villain_name = villain.get('Villain', 'Unknown')
        film = villain.get('Film', 'Unknown')
        actor = villain.get('Portrayed by', 'Unknown')

        print(f"[{idx}/{len(villains)}] Enriching: {villain_name} from '{film}'")

        user_prompt = f"""
Film: {film}
Villain: {villain_name}
Portrayed by: {actor}

Please provide the Objective, Outcome, and Status for this villain.
"""

        try:
            result_json = call_groq(user_prompt)
            result = json.loads(result_json)

            # Update only empty fields
            if is_field_empty(villain.get('Objective')):
                villain['Objective'] = result.get('objective', '')
            if is_field_empty(villain.get('Outcome')):
                villain['Outcome'] = result.get('outcome', '')
            if is_field_empty(villain.get('Status')):
                villain['Status'] = result.get('status', '')

            enriched_count += 1
            print(f"Successfully enriched")

        except Exception as e:
            error_count += 1
            print(f"Error: {str(e)}")
            continue

    # Write updated data back to CSV
    print(f"\nWriting enriched data to: {OUTPUT_FILE.name}")
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ['Film', 'Villain', 'Portrayed by', 'Objective', 'Outcome', 'Status', 'image_url']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(villains)

    # Print summary
    print(f"Total villains processed: {len(villains)}")
    print(f"Villains already complete: {skipped_count}")
    print(f"Villains enriched: {enriched_count}")
    print(f"Errors encountered: {error_count}")
    print(f"\nOutput saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    enrich_villain_data()
