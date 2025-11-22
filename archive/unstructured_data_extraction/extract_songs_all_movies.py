import json
import re
import pandas as pd
from pathlib import Path

# ------------ Song Extraction ------------
def extract_song_info(input_file, movie_title):
    """
    Extract song and performer information from the infobox of the movie JSON files.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    infobox = data.get("infobox", {})
    
    if not infobox:
        print(f"No infobox found for {movie_title}")
        return None
    
    # Extract song and performer
    song_raw = infobox.get("song", "")
    performer_raw = infobox.get("performer", "")
    composer_raw = infobox.get("composer", "")
    
    # Clean up the fields (remove markdown links and quotes)
    def clean_field(text):
        if not text:
            return ""
        
        # Remove quotes at the beginning and end
        text = text.strip().strip('"\'')
        
        # Extract text from [[link|display]] or [[link]] format
        # Pattern: [[text|display]] -> display or [[text]] -> text
        matches = re.findall(r'\[\[([^\]]+)\]\]', text)
        if matches:
            # Take the last part after | if exists
            cleaned_parts = []
            for match in matches:
                if '|' in match:
                    cleaned_parts.append(match.split('|')[-1].strip())
                else:
                    cleaned_parts.append(match.strip())
            text = ', '.join(cleaned_parts)
        
        # Remove any remaining brackets or HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        text = text.strip()
        
        return text
    
    song = clean_field(song_raw)
    performer = clean_field(performer_raw)
    composer = clean_field(composer_raw)
    
    # Only return if we have at least a song
    if song:
        return {
            "movie": movie_title,
            "song": song,
            "performer": performer if performer else "Unknown",
            "composer": composer if composer else ""
        }
    
    return None

# ---- Create List of YouTube URLs for Movie Opening Sequences ----
def create_youtube_urls():
    """
    Manually created mapping of movie titles to their YouTube opening sequence URLs.
    """ 
    return {
        "A View to a Kill": "https://youtu.be/hWVbVT3igdw?si=Ndam6Q-IDECf9RCW",
        "Casino Royale": "https://youtu.be/A1AMUmkj-ck?si=YBgYd8nF8rAEn06C",
        "Diamonds Are Forever": "https://youtu.be/ZwbEuzJCnqI?si=xH-BoyxMvlyF6knx",
        "Die Another Day": "https://youtu.be/ZVFDshqlmOQ?si=FjvbqAWargVkyU3F",
        "Dr. No": "https://youtu.be/oTo3YtPxG5k?si=v2Yx2a4--kAEgaqI",
        "For Your Eyes Only": "https://youtu.be/8kNksLL0    sv4?si=RcjZ713gXyavBz4Q",
        "From Russia with Love": "https://youtu.be/RIY8KDrx-E8?si=enJ7nKJGq1Y2l-4o",
        "GoldenEye": "https://youtu.be/qGPBFvDz_HM?si=OJlOnDWRcRWeZMTG",
        "Goldfinger": "https://youtu.be/6D1nK7q2i8I?si=7f-l_tJqg-riV2tO",
        "Licence to Kill": "https://youtu.be/Ju_by-sC79c?si=kO0Rn-FoJ9YVgTUA",
        "Live and Let Die": "https://youtu.be/sn8alMYSu44?si=a6Q7bd-rNj4ZtvUM",
        "Moonraker": "https://youtu.be/gt3oQN0cAv0?si=sBE9o7fKiXP-YgOi",
        "No Time to Die": "https://youtu.be/83YuaW09ueI?si=0jeUBYMHHF9ZRh61",
        "Octopussy": "https://youtu.be/213t3YeQosE?si=k8JyqEwV5KHJb3o9",
        "On Her Majesty's Secret Service": "https://youtu.be/WYRf_S9DLfk?si=tDaNqMy0WlychzGl",
        "Quantum of Solace": "https://youtu.be/B4LpSzKnEtA?si=cQUB9HTuXNDG-XCI",
        "Skyfall": "https://youtu.be/DeumyOzKqgI?si=5aH1fvbGm0D0uwzT",
        "Spectre": "https://youtu.be/G9LxUQL_Ucg?si=4N9YBt6lGD2H8ZSA",
        "The Living Daylights": "https://youtu.be/y9p0FJnk2vM?si=Wm2IJrNLqdfZsonm",
        "The Man with the Golden Gun": "https://youtu.be/PSbj2Mx2By8?si=lSTEzJTfxcNSlcdv",
        "The Spy Who Loved Me": "https://youtu.be/isAUOa50wdA?si=DWFVFD8GU7826luA",
        "The World Is Not Enough": "https://youtu.be/LzvNDR5OrqM?si=cIzQiwbeyxNOCrDs",
        "Thunderball": "https://youtu.be/Ia6-5gC5ArM?si=9UalFYNXPHhPaq1L",
        "Tomorrow Never Dies": "https://youtu.be/SDe1xi4tGUA?si=HgeN7UlCN8dA7v7i",
        "You Only Live Twice": "https://youtu.be/hs8uYxTJ530?si=D7V00R6Skoe1vicl"
}

# ---- Add YouTube URLs to DataFrame ----
def map_youtube_urls(df):
    youtube_urls = create_youtube_urls()
    df['youtube_url'] = df['movie'].map(youtube_urls)
    return df



if __name__ == "__main__":  
    base_dir = Path(__file__).parent.parent
    input_dir = base_dir / "extract_knowledge/fandom_wiki_pages"
    input_files = list(input_dir.glob("*_film.json"))
    
    if not input_files:
        print("No JSON files found in 'fandom_wiki_pages' directory.")
    else:
        print(f"Found {len(input_files)} JSON files to process.\n")

        # Collect all song data
        all_songs = []
        
        # Process each file
        for json_file in sorted(input_files):
            # Remove "_film" suffix and replace underscores with spaces for readable movie title
            movie_title = json_file.stem.replace("_film", "").replace("_", " ")
            
            print(f"Processing: {json_file.name}")
            print(f"Movie: {movie_title}")
            
            try:
                song_info = extract_song_info(str(json_file), movie_title)
                
                if song_info:
                    all_songs.append(song_info)
                    print(f"Song: {song_info['song']}")
                    print(f"Performer: {song_info['performer']}")
                    if song_info['composer']:
                        print(f"Composer: {song_info['composer']}")
                else:
                    print(f"No song information found")
                    
            except Exception as e:
                print(f"Error processing {json_file.name}: {e}")
                     
        # Save all data to a CSV and add YouTube Links
        if all_songs:
            df = pd.DataFrame(all_songs)
            
            # Reorder columns
            columns = ['movie', 'song', 'performer', 'composer', 'youtube_link']
            df = df[columns]
            df = map_youtube_urls(df)
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['movie', 'song'])
            
            # Create output directory if it doesn't exist
            output_dir = base_dir / "extract_knowledge/songs"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save to CSV
            output_file = output_dir / "all_movie_songs_test.csv"
            df.to_csv(output_file, index=False, encoding="utf-8", sep=';')
            print(f"Songs data saved to {output_file}")