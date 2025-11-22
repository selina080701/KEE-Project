# g_character_data_cleaning.py

import pandas as pd
from pathlib import Path

"""
This file applies post-processing corrections to the character data with images.
It handles known data quality issues including character name corrections, actor corrections,
and image URL restorations. There are also provisions to add missing entries and remove unwanted ones.
    -> Input: CSV file extract_knowledge/characters/all_movie_characters_with_image.csv
    -> Output: Cleaned CSV file in the same directory
"""

# ---- Post-processing data cleaning ----
def clean_data(df):
    """
    Correct known data issues in the extracted DataFrame.
    This function applies manual corrections based on known errors in the source data.
    """
    corrections = [
        # Character name corrections
        {
            "character": "General Anatol Gogol",
            "actor": "Walter Gotell",
            "movie": "A View to a Kill",
            "correct_character": "General Gogol"
        },
        {
            "character": "General Anatol Gogol",
            "actor": "Walter Gotell",
            "movie": "For Your Eyes Only",
            "correct_character": "General Gogol"
        },
        {
            "character": "General Anatol Gogol",
            "actor": "Walter Gotell",
            "movie": "Moonraker",
            "correct_character": "General Gogol"
        },
        {
            "character": "General Anatol Gogol",
            "actor": "Walter Gotell",
            "movie": "Octopussy",
            "correct_character": "General Gogol"
        },
        {
            "character": "General Anatol Gogol",
            "actor": "Walter Gotell",
            "movie": "The Spy Who Loved Me",
            "correct_character": "General Gogol"
        },

        # Actor corrections
        {
            "character": "Erich Kriegler",
            "actor": "Unknown",
            "movie": "For Your Eyes Only",
            "correct_actor": "John Wyman"
        },
        {
            "character": "Auric Goldfinger",
            "actor": "Unknown",
            "movie": "Goldfinger",
            "correct_actor": "Gert Fröbe"
        },
        {
            "character": "Emilio Largo",
            "actor": "Unknown",
            "movie": "Thunderball",
            "correct_actor": "Adolfo Celi"
        },

        # Image URL corrections (restore correct URLs)
        {
            "character": "Sir Fredrick Gray",
            "actor": "Geoffrey Keen",
            "movie": "A View to a Kill",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/e6/Fredrick_Gray_%28The_Spy_Who_Loved_Me%29_-_Profile.png",
            "correct_search_title": "Sir Fredrick Gray"
        },
        {
            "character": "Dr. Christmas Jones",
            "actor": "Denise Richards",
            "movie": "The World Is Not Enough",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/6/6f/Christmas_Jones_%28Denise_Richards%29_-_Profile.jpg",
            "correct_search_title": "Dr. Christmas Jones"
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Donald Pleasence",
            "movie": "You Only Live Twice",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/ec/Blofeld_%28You_Only_Live_Twice%29_-_Profile.png",
            "correct_search_title": "Ernst Stavro Blofeld (Donald Pleasence)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "Tomorrow Never Dies",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "Domino Derval",
            "actor": "Claudine Auger",
            "movie": "Thunderball",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/8/82/Domino_Derval_-_Profile.png",
            "correct_search_title": "Domino Derval"
        },
        {
            "character": "Rubelvitch",
            "actor": "Eva Rueber-Staier",
            "movie": "The Spy Who Loved Me",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/b/b0/Screenshot_2015-06-20_19.14.00.png",
            "correct_search_title": "Rubelvitch"
        },
        {
            "character": "Emilio Largo",
            "actor": "Adolfo Celi",
            "movie": "Thunderball",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/7/78/Emilio_Largo_%28Adolfo_Celi%29_-_Profile.jpg",
            "correct_search_title": "Emilio Largo (Adolfo Celi)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "The World Is Not Enough",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "General Georgi Koskov",
            "actor": "Jeroen Krabbé",
            "movie": "The Living Daylights",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/a/a8/General_Gogol_%28Walter_Gotell%29_-_Profile.jpg",
            "correct_search_title": "General Georgi Koskov"
        },
        {
            "character": "Q",
            "actor": "Peter Burton",
            "movie": "Dr. No",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/3/34/Q_%28Peter_Burton%29_-_Profile.png",
            "correct_search_title": "Q (Peter Burton)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "Casino Royale",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Charles Gray",
            "movie": "Diamonds Are Forever",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/9/95/Blofeld_Profile_%28Charles_Gray%29.png",
            "correct_search_title": "Ernst Stavro Blofeld (Charles Gray)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "Die Another Day",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "Emile Leopold Locque",
            "actor": "Michael Gothard",
            "movie": "For Your Eyes Only",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/6/6f/Emile_Leopold_Locque_-_Profile.png",
            "correct_search_title": "Emile Leopold Locque"
        },
        {
            "character": "General Gogol",
            "actor": "Walter Gotell",
            "movie": "For Your Eyes Only",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/a/a8/General_Gogol_%28Walter_Gotell%29_-_Profile.jpg",
            "correct_search_title": "General Gogol"
        },
                {
            "character": "General Gogol",
            "actor": "Walter Gotell",
            "movie": "The Spy Who Loved Me",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/a/a8/General_Gogol_%28Walter_Gotell%29_-_Profile.jpg",
            "correct_search_title": "General Gogol"
        },
        {
            "character": "Sir Fredrick Gray",
            "actor": "Geoffrey Keen",
            "movie": "For Your Eyes Only",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/e6/Fredrick_Gray_%28The_Spy_Who_Loved_Me%29_-_Profile.png",
            "correct_search_title": "Sir Fredrick Gray"
        },
        {
            "character": "Colonel Rosa Klebb",
            "actor": "Lotte Lenya",
            "movie": "From Russia with Love",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/d/de/Rosa-klebb-from-russia-with-love.png",
            "correct_search_title": ""
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Anthony Dawson",
            "movie": "From Russia with Love",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/8/87/Blofeld_%28Dawson-Pohlmann%29_-_Profile.jpg",
            "correct_search_title": "Ernst Stavro Blofeld(Anthony_Dawson)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "GoldenEye",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "Auric Goldfinger",
            "actor": "Gert Fröbe",
            "movie": "Goldfinger",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/d/d9/Auric_Goldfinger_%28Gert_Fr%C3%B6be%29_-_Profile.png",
            "correct_search_title": "Auric Goldfinger"
        },
        {
            "character": "Dr. Kananga/Mr. Big",
            "actor": "Yaphet Kotto",
            "movie": "Live and Let Die",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/4/4c/Dr._Kananga_%28Yaphet_Kotto%29_-_Profile.jpg",
            "correct_search_title": "Dr. Kananga/Mr. Big (Yaphet Kotto)"
        },
        {
            "character": "Sheriff J.W. Pepper",
            "actor": "Clifton James",
            "movie": "The Man with the Golden Gun",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/c/cd/J.W._Pepper_%28The_Man_With_The_Golden_Gun%29_-_Profile.jpg",
            "correct_search_title": "Sheriff J.W. Pepper"
        },
        {
            "character": "Sheriff J.W. Pepper",
            "actor": "Clifton James",
            "movie": "Live and Let Die",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/b/b7/J.W._Pepper_%28Clifton_James%29_-_Profile.jpg",
            "correct_search_title": "Sheriff J.W. Pepper"
        },
        {
            "character": "General Gogol",
            "actor": "Walter Gotell",
            "movie": "Moonraker",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/a/a8/General_Gogol_%28Walter_Gotell%29_-_Profile.jpg",
            "correct_search_title": "General Gogol"
        },
        {
            "character": "Sir Fredrick Gray",
            "actor": "Geoffrey Keen",
            "movie": "Moonraker",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/e6/Fredrick_Gray_%28The_Spy_Who_Loved_Me%29_-_Profile.png",
            "correct_search_title": "Sir Fredrick Gray"
        },
        {
            "character": "Rubelvitch",
            "actor": "Eva Rueber-Staier",
            "movie": "Octopussy",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/b/b0/Screenshot_2015-06-20_19.14.00.png",
            "correct_search_title": "Rubelvitch"
        },
        {
            "character": "Sir Fredrick Gray",
            "actor": "Geoffrey Keen",
            "movie": "Octopussy",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/e6/Fredrick_Gray_%28The_Spy_Who_Loved_Me%29_-_Profile.png",
            "correct_search_title": "Sir Fredrick Gray"
        },
        {
            "character": "Sir Fredrick Gray",
            "actor": "Geoffrey Keen",
            "movie": "The Living Daylights",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/e6/Fredrick_Gray_%28The_Spy_Who_Loved_Me%29_-_Profile.png",
            "correct_search_title": "Sir Fredrick Gray"
        },
                {
            "character": "Sir Fredrick Gray",
            "actor": "Geoffrey Keen",
            "movie": "The Spy Who Loved Me",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/e6/Fredrick_Gray_%28The_Spy_Who_Loved_Me%29_-_Profile.png",
            "correct_search_title": "Sir Fredrick Gray"
        },
        {
            "character": "General Gogol",
            "actor": "Walter Gotell",
            "movie": "Octopussy",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/a/a8/General_Gogol_%28Walter_Gotell%29_-_Profile.jpg",
            "correct_search_title": "General Gogol"
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Telly Savalas",
            "movie": "On Her Majesty's Secret Service",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/7/78/Blofeld_%28Telly_Savalas%29_-_Profile.png",
            "correct_search_title": " Ernst Stavro Blofeld (Telly Savalas)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "Quantum of Solace",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "Skyfall",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Anthony Dawson",
            "movie": "Thunderball",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/8/87/Blofeld_%28Dawson-Pohlmann%29_-_Profile.jpg",
            "correct_search_title": "Ernst Stavro Blofeld (Anthony Dawson)"
        },
    ]

    # Entries to add if they don't exist
    entries_to_add = [
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Anthony Dawson",
            "movie": "Thunderball",
            "image_url": "https://static.wikia.nocookie.net/jamesbond/images/8/87/Blofeld_%28Dawson-Pohlmann%29_-_Profile.jpg",
            "search_title": "Ernst Stavro Blofeld (Anthony Dawson)"
        }
    ]

    # Entries to remove (character, actor, movie combinations)
    entries_to_remove = [
        {"character": "Captain", "actor": "Pip Torrens", "movie": "Tomorrow Never Dies"},
        {"character": "Captain", "actor": "Bruce Alexander", "movie": "Tomorrow Never Dies"}
    ]

    # Apply corrections
    for correction in corrections:
        # Build the mask to identify rows to correct
        mask = (
            (df['character'] == correction['character']) &
            (df['actor'] == correction['actor']) &
            (df['movie'] == correction['movie'])
        )

        # Apply character name correction
        if 'correct_character' in correction:
            df.loc[mask, 'character'] = correction['correct_character']

        # Apply actor name correction
        if 'correct_actor' in correction:
            df.loc[mask, 'actor'] = correction['correct_actor']

        # Apply image URL correction
        if 'correct_image_url' in correction:
            df.loc[mask, 'image_url'] = correction['correct_image_url']

        # Apply search title correction
        if 'correct_search_title' in correction:
            df.loc[mask, 'search_title'] = correction['correct_search_title']

    # Add new entries if they don't exist
    for entry in entries_to_add:
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
            print(f"Added: {entry['character']} ({entry['actor']}) in {entry['movie']}")

    # Remove unwanted entries
    for entry in entries_to_remove:
        mask = (
            (df['character'] == entry['character']) &
            (df['actor'] == entry['actor']) &
            (df['movie'] == entry['movie'])
        )

        if mask.any():
            df = df[~mask]
            print(f"Removed: {entry['character']} ({entry['actor']}) in {entry['movie']}")

    return df


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    input_dir = base_dir / "extract_knowledge/characters"
    input_file = input_dir / "all_movie_characters_with_image.csv"
    output_file = input_dir / "all_movie_characters_with_image.csv" # overwrite the same file

    if not input_file.exists():
        print(f"Error: {input_file} not found!")
    else:
        # Load CSV with semicolon separator
        df = pd.read_csv(input_file, sep=';')
        print(f"Loaded {len(df)} entries from {input_file.name}")

        # Apply corrections
        df_cleaned = clean_data(df)

        # Save cleaned data back to the same file
        df_cleaned.to_csv(output_file, index=False, encoding='utf-8', sep=';')

        print(f"Cleaning complete!")
        print(f"Cleaned data saved to: {output_file}")
        print(f"Total entries: {len(df_cleaned)}")
        print(f"Entries with images: {df_cleaned['image_url'].notna().sum()}")