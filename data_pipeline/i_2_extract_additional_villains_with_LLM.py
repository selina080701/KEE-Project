# i_2_extract_additional_villains_with_LLM.py¨

import csv
import json
import sys
from pathlib import Path
from groq import Groq

"""
In addition to the extracted main villains from Wikipedia, this script uses a Large Language Model (LLM)
to classify villain-characters from the CSV file containing all movie characters:
Input:
    - extract_knowledge/characters/all_movie_characters_with_image.csv
Output:
    - extract_knowledge/villains/villains_with_LLM.csv
    - A list of characters classified as villains based on the system prompt.
"""

# Define base directory and paths
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from utils.config import GROQ_API_KEY

INPUT_FILE = BASE_DIR / "extract_knowledge" / "characters" / "all_movie_characters_with_image.csv"
OUTPUT_FILE = BASE_DIR / "extract_knowledge" / "villains" / "villains_with_LLM.csv"
EXISTING_VILLAINS_FILE = BASE_DIR / "extract_knowledge" / "villains" / "villains_with_images.csv"

API_KEY = GROQ_API_KEY

SYSTEM_PROMPT = """
You are an expert on James Bond movies.
Given the following character information:

- character name
- actor
- film
- search_title

Determine whether the character is a SIGNIFICANT and ICONIC VILLAIN who plays a major antagonistic role.

A James Bond villain worthy of inclusion is defined as:
- Main antagonist / mastermind of the film (the primary villain)
- Major henchmen who are memorable, have significant screen time, and directly engage with Bond in combat or confrontation
- Only include secondary villains if they are well-known and iconic characters from the franchise

DO NOT classify as villains:
- Minor characters with brief appearances
- Background henchmen without names or speaking roles
- Allies or neutral characters
- Characters who merely work for villains but don't actively oppose Bond
- Generic guards, soldiers, or unnamed thugs
- Bond Girls or love interests (even if they betray Bond)
- Supporting accomplices without significant antagonistic roles
- Informants, contacts, or minor associates of the main villain
- Characters who appear in only one or two scenes

IMPORTANT: Be EXTREMELY SELECTIVE. Only include villains that are memorable and iconic.
When in doubt, mark as NOT a villain (is_villain = false).

Return ONLY a JSON object with the structure:
{
  "is_villain": true/false,
  "film": "...",
  "villain": "...",
  "portrayed_by": "...",
  "image_url": "..."
}

Rules:
- If the character is not a significant villain → is_villain = false and all other fields empty strings.
- Be VERY SELECTIVE - only mark truly important and iconic villains as is_villain = true.
- Do NOT include explanations.
"""


def call_groq(prompt):
    """Call Groq API to determine if a character is a villain."""
    client = Groq(api_key=API_KEY)
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return resp.choices[0].message.content


def load_existing_villains():
    """Load existing villains from villains_with_images.csv to avoid duplicates."""
    existing_villains = set()

    try:
        with open(EXISTING_VILLAINS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                # Create a normalized key: (film, villain_name)
                villain_key = (row['Film'].strip().lower(), row['Villain'].strip().lower())
                existing_villains.add(villain_key)
    except FileNotFoundError:
        print(f"Warning: {EXISTING_VILLAINS_FILE} not found. Proceeding without duplicate check.")

    return existing_villains


def extract_villains_with_llm():
    """Extract villains from character list using LLM classification."""
    villains = []

    # Load existing villains to check for duplicates
    existing_villains = load_existing_villains()
    print(f"Loaded {len(existing_villains)} existing villains from villains_with_images.csv")

    skipped_duplicates = 0
    processed_count = 0

    # Read character data
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            processed_count += 1

            # Show progress every 50 characters
            if processed_count % 50 == 0:
                print(f"Processed {processed_count} characters... Found {len(villains)} new villains so far.")

            user_prompt = f"""
Character: {row['character']}
Actor: {row['actor']}
Movie: {row['movie']}
search_title: {row['search_title']}
image_url: {row['image_url']}
"""
            result_json = call_groq(user_prompt)
            result = json.loads(result_json)

            if result["is_villain"]:
                # Check if this villain already exists
                villain_key = (result["film"].strip().lower(), result["villain"].strip().lower())

                if villain_key in existing_villains:
                    skipped_duplicates += 1
                    print(f"Skipping duplicate: {result['villain']} from {result['film']}")
                else:
                    villains.append(result)
                    print(f"Found new villain: {result['villain']} from {result['film']}")

    # Export villains as CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Film", "Villain", "Portrayed by", "Objective", "Outcome", "Status", "image_url"])

        for v in villains:
            writer.writerow([v["film"], v["villain"], v["portrayed_by"], "", "", "", v["image_url"]])

    print(f"Processing complete!")
    print(f"Total characters processed: {processed_count}")
    print(f"Duplicates skipped: {skipped_duplicates}")
    print(f"New villains found: {len(villains)}")
    print(f"villains_with_LLM.csv created!")

    return villains


if __name__ == "__main__":
    extract_villains_with_llm()
