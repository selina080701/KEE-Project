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


if __name__ == "__main__":  
    # Get all JSON files from fandom_wiki_pages directory
    input_dir = Path("extract_knowledge/fandom_wiki_pages")
    json_files = list(input_dir.glob("*_film.json"))
    
    if not json_files:
        print("No JSON files found in 'fandom_wiki_pages' directory.")
    else:
        print(f"Found {len(json_files)} JSON files to process.\n")

        # Collect all song data
        all_songs = []
        
        # Process each file
        for json_file in sorted(json_files):
            # Remove "_film" suffix and replace underscores with spaces for readable movie title
            movie_title = json_file.stem.replace("_film", "").replace("_", " ")
            
            print(f"Processing: {json_file.name}")
            print(f"  Movie: {movie_title}")
            
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
                print(f"  ✗ Error processing {json_file.name}: {e}")
                     
        # Save all data to a single CSV
        if all_songs:
            df = pd.DataFrame(all_songs)
            
            # Reorder columns
            columns = ['movie', 'song', 'performer', 'composer']
            df = df[columns]
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['movie', 'song'])
            
            # Create output directory if it doesn't exist
            output_dir = Path("extract_knowledge/songs")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save to CSV
            output_file = output_dir / "all_movie_songs.csv"
            df.to_csv(output_file, index=False, encoding="utf-8", sep=';')

            print(f"=" * 60)
            print(f"Processing complete!")
            print(f"Total songs extracted: {len(df)}")
            print(f"Saved to: {output_file}")
            print(f"=" * 60)
            print(f"\nAll extracted songs:")
            print(df.to_string(index=False))
        else:
            print("\n" + "=" * 60)
            print("No songs were extracted from any files.")
            print("=" * 60)