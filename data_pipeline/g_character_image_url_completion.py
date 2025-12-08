# g_character_image_url_completion.py

import pandas as pd
from pathlib import Path

"""
This file applies missing image URL corrections to the character data.
It handles known missing image URLs by restoring the correct ones. The URLs are sourced manually from Fandom (via DevTool).
It focuses on multi-occurence characters and iconic villains.
    -> Input: CSV file extract_knowledge/characters/all_movie_characters_with_image.csv
    -> Output: Updated CSV file in the same directory and same name (overwrites the input file)

Overview of corrected characters:
    - Auric Goldfinger (1 entry)
    - Colonel Rosa Klebb (1 entry)
    - Domino Derval (1 entry)
    - Dr. Christmas Jones (1 entry)
    - Dr. Kananga/Mr. Big (1 entry)
    - Emile Leopold Locque (1 entry)
    - Emilio Largo (1 entry)
    - Ernst Stavro Blofeld (5 entries - different actors/movies)
    - General Georgi Koskov (1 entry)
    - General Gogol (4 entries - different movies)
    - M (7 entries - Judi Dench in different movies)
    - Q (1 entry)
    - Rubelvitch (2 entries - different movies)
    - Sheriff J.W. Pepper (2 entries - different movies)
    - Sir Fredrick Gray (6 entries - different movies)
"""

# ---- Complete missing image URLs ----
def complete_image_urls(df):
    """
    Add or correct missing image URLs for characters.
    This function applies manual URL corrections based on known missing data.
    """
    url_corrections = [
        # Image URL corrections (ordered alphabetically by character name)
        {
            "character": "Auric Goldfinger",
            "actor": "Gert Fröbe",
            "movie": "Goldfinger",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/d/d9/Auric_Goldfinger_%28Gert_Fr%C3%B6be%29_-_Profile.png",
            "correct_search_title": "Auric Goldfinger"
        },
        {
            "character": "Colonel Rosa Klebb",
            "actor": "Lotte Lenya",
            "movie": "From Russia with Love",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/d/de/Rosa-klebb-from-russia-with-love.png",
            "correct_search_title": ""
        },
        {
            "character": "Domino Derval",
            "actor": "Claudine Auger",
            "movie": "Thunderball",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/8/82/Domino_Derval_-_Profile.png",
            "correct_search_title": "Domino Derval"
        },
        {
            "character": "Dr. Christmas Jones",
            "actor": "Denise Richards",
            "movie": "The World Is Not Enough",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/6/6f/Christmas_Jones_%28Denise_Richards%29_-_Profile.jpg",
            "correct_search_title": "Dr. Christmas Jones"
        },
        {
            "character": "Dr. Kananga/Mr. Big",
            "actor": "Yaphet Kotto",
            "movie": "Live and Let Die",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/4/4c/Dr._Kananga_%28Yaphet_Kotto%29_-_Profile.jpg",
            "correct_search_title": "Dr. Kananga/Mr. Big (Yaphet Kotto)"
        },
        {
            "character": "Emile Leopold Locque",
            "actor": "Michael Gothard",
            "movie": "For Your Eyes Only",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/6/6f/Emile_Leopold_Locque_-_Profile.png",
            "correct_search_title": "Emile Leopold Locque"
        },
        {
            "character": "Emilio Largo",
            "actor": "Adolfo Celi",
            "movie": "Thunderball",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/7/78/Emilio_Largo_%28Adolfo_Celi%29_-_Profile.jpg",
            "correct_search_title": "Emilio Largo (Adolfo Celi)"
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Anthony Dawson",
            "movie": "From Russia with Love",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/8/87/Blofeld_%28Dawson-Pohlmann%29_-_Profile.jpg",
            "correct_search_title": "Ernst Stavro Blofeld(Anthony_Dawson)"
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Anthony Dawson",
            "movie": "Thunderball",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/8/87/Blofeld_%28Dawson-Pohlmann%29_-_Profile.jpg",
            "correct_search_title": "Ernst Stavro Blofeld (Anthony Dawson)"
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Charles Gray",
            "movie": "Diamonds Are Forever",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/9/95/Blofeld_Profile_%28Charles_Gray%29.png",
            "correct_search_title": "Ernst Stavro Blofeld (Charles Gray)"
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Donald Pleasence",
            "movie": "You Only Live Twice",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/ec/Blofeld_%28You_Only_Live_Twice%29_-_Profile.png",
            "correct_search_title": "Ernst Stavro Blofeld (Donald Pleasence)"
        },
        {
            "character": "Ernst Stavro Blofeld",
            "actor": "Telly Savalas",
            "movie": "On Her Majesty's Secret Service",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/7/78/Blofeld_%28Telly_Savalas%29_-_Profile.png",
            "correct_search_title": " Ernst Stavro Blofeld (Telly Savalas)"
        },
        {
            "character": "General Georgi Koskov",
            "actor": "Jeroen Krabbé",
            "movie": "The Living Daylights",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/a/a8/General_Gogol_%28Walter_Gotell%29_-_Profile.jpg",
            "correct_search_title": "General Georgi Koskov"
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
            "movie": "Moonraker",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/a/a8/General_Gogol_%28Walter_Gotell%29_-_Profile.jpg",
            "correct_search_title": "General Gogol"
        },
        {
            "character": "General Gogol",
            "actor": "Walter Gotell",
            "movie": "Octopussy",
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
            "character": "M",
            "actor": "Judi Dench",
            "movie": "Casino Royale",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "Die Another Day",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "GoldenEye",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
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
            "character": "M",
            "actor": "Judi Dench",
            "movie": "The World Is Not Enough",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "M",
            "actor": "Judi Dench",
            "movie": "Tomorrow Never Dies",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/5/5b/M_%28Casino_Royale%29_-_Profile.png",
            "correct_search_title": "M (Judi Dench)"
        },
        {
            "character": "Q",
            "actor": "Peter Burton",
            "movie": "Dr. No",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/3/34/Q_%28Peter_Burton%29_-_Profile.png",
            "correct_search_title": "Q (Peter Burton)"
        },
        {
            "character": "Rubelvitch",
            "actor": "Eva Rueber-Staier",
            "movie": "Octopussy",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/b/b0/Screenshot_2015-06-20_19.14.00.png",
            "correct_search_title": "Rubelvitch"
        },
        {
            "character": "Rubelvitch",
            "actor": "Eva Rueber-Staier",
            "movie": "The Spy Who Loved Me",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/b/b0/Screenshot_2015-06-20_19.14.00.png",
            "correct_search_title": "Rubelvitch"
        },
        {
            "character": "Sheriff J.W. Pepper",
            "actor": "Clifton James",
            "movie": "Live and Let Die",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/b/b7/J.W._Pepper_%28Clifton_James%29_-_Profile.jpg",
            "correct_search_title": "Sheriff J.W. Pepper"
        },
        {
            "character": "Sheriff J.W. Pepper",
            "actor": "Clifton James",
            "movie": "The Man with the Golden Gun",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/c/cd/J.W._Pepper_%28The_Man_With_The_Golden_Gun%29_-_Profile.jpg",
            "correct_search_title": "Sheriff J.W. Pepper"
        },
        {
            "character": "Sir Fredrick Gray",
            "actor": "Geoffrey Keen",
            "movie": "A View to a Kill",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/e6/Fredrick_Gray_%28The_Spy_Who_Loved_Me%29_-_Profile.png",
            "correct_search_title": "Sir Fredrick Gray"
        },
        {
            "character": "Sir Fredrick Gray",
            "actor": "Geoffrey Keen",
            "movie": "For Your Eyes Only",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/e6/Fredrick_Gray_%28The_Spy_Who_Loved_Me%29_-_Profile.png",
            "correct_search_title": "Sir Fredrick Gray"
        },
        {
            "character": "Sir Fredrick Gray",
            "actor": "Geoffrey Keen",
            "movie": "Moonraker",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/e/e6/Fredrick_Gray_%28The_Spy_Who_Loved_Me%29_-_Profile.png",
            "correct_search_title": "Sir Fredrick Gray"
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
            "character": "General Georgi Koskov",
            "actor": "Jeroen Krabbé",
            "movie": "The Living Daylights",
            "correct_image_url": "https://static.wikia.nocookie.net/jamesbond/images/6/6f/General_Koskov_-_Profile.png",
            "correct_search_title": "General Georgi Koskov"
        }
    ]

    updated_count = 0

    # Apply image URL corrections
    for correction in url_corrections:
        # Build the mask to identify rows to correct
        mask = (
            (df['character'] == correction['character']) &
            (df['actor'] == correction['actor']) &
            (df['movie'] == correction['movie'])
        )

        if mask.any():
            # Apply image URL correction
            df.loc[mask, 'image_url'] = correction['correct_image_url']

            # Apply search title correction
            if 'correct_search_title' in correction:
                df.loc[mask, 'search_title'] = correction['correct_search_title']

            updated_count += 1
            print(f"Updated: {correction['character']} ({correction['actor']}) in {correction['movie']}")

    print(f"\nTotal image URLs updated: {updated_count}")
    return df


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    input_dir = base_dir / "extract_knowledge/characters"
    input_file = input_dir / "all_movie_characters_with_image.csv"
    output_file = input_dir / "all_movie_characters_with_image.csv"  # overwrite the same file

    if not input_file.exists():
        print(f"Error: {input_file} not found!")
    else:
        # Load CSV with semicolon separator
        df = pd.read_csv(input_file, sep=';')
        print(f"Loaded {len(df)} entries from {input_file.name}\n")

        # Apply image URL corrections
        df_updated = complete_image_urls(df)

        # Save updated data back to the same file
        df_updated.to_csv(output_file, index=False, encoding='utf-8', sep=';')

        print(f"\nImage URL completion finished!")
        print(f"Updated data saved to: {output_file}")
        print(f"Total entries: {len(df_updated)}")
        print(f"Entries with images: {df_updated['image_url'].notna().sum()}")
