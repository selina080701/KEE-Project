# d_fandom_request_movie_posters.py

import requests
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from utils.bond_films import BOND_FILMS

"""
This file retrieves movie poster URLs from the James Bond Fandom Wiki for all movies in the BOND_FILMS list.
It saves the movie titles along with their corresponding poster URLs in a CSV file.
    -> Input: BOND_FILMS list from utils/bond_films.py
    -> Output: CSV file in extract_knowledge/movie_posters/ directory
"""

def get_movie_poster_url(movie_title):
    """Retrieve James Bond movie poster URL from Fandom API"""
    url = "https://jamesbond.fandom.com/api.php"
    
    # Get the page content to find the main image
    params = {
        "action": "query",
        "titles": movie_title,
        "prop": "pageimages",
        "piprop": "original",
        "format": "json",
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if 'error' in data:
            print(f"Error retrieving {movie_title}: {data['error']['info']}")
            return None
        
        # Parse response to find image URL
        pages = data.get('query', {}).get('pages', {})

        for page_id, page_data in pages.items():
            if page_id == '-1':  # Page doesn't exist
                print(f"Page not found for {movie_title}")
                return None
            
            # Try to get the original image URL
            original = page_data.get('original', {})
            if original and 'source' in original:
                print(f"Found image for {movie_title}: {original['source']}")
                return original['source']
            
        print(f"No poster found for {movie_title}")
        return None
    
    except Exception as e:
        print(f"Exception occurred for {movie_title}: {e}")
        return None
    

def save_poster_url(movie_list):
    results = []

    for i, film in enumerate(movie_list, start=1):
        print(f"[{i}/{len(movie_list)}] {film}")

        # get poster URL
        poster_url = get_movie_poster_url(film)
        results.append({
            'title': film,
            'poster_url': poster_url if poster_url else ''
        })

        # save to CSV
        project_root = Path(__file__).parent.parent
        output_dir = project_root / "extract_knowledge/movie_posters"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "movie_poster_url.csv"

        with open (output_file, 'w', newline='', encoding='utf-8') as f:
            f.write("title,poster_url\n")
            for item in results:
                f.write(f"{item['title']},{item['poster_url']}\n")
        
        print(f"Poster URLs saved to {output_file}")

if __name__ == "__main__":
    save_poster_url(BOND_FILMS)