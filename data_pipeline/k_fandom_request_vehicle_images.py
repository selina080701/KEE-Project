# k_fandom_request_vehicle_images.py

import requests
import pandas as pd
from pathlib import Path

"""
This file retrieves vehicle image URLs from the James Bond Fandom API based on a CSV file containing vehicle data.
It saves the results to a new CSV file including the retrieved image URLs.
    -> Input CSV: extract_knowledge/vehicles/all_movie_vehicles.csv
    -> Output CSV: extract_knowledge/vehicles/all_movie_vehicles_with_image.csv
"""

# ---- Retrieve vehicle image URL from Fandom API ----
def get_vehicle_image_url(vehicle_name, image_filename):
    """
    Tries to find vehicle image URL using the image filename or vehicle name
    """
    url = "https://jamesbond.fandom.com/api.php"

    # Method 1: Try to get the image info directly using the filename
    if image_filename and image_filename != "Unknown - Infobox.png" and image_filename != "No image":
        params = {
            "action": "query",
            "titles": f"File:{image_filename}",
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json",
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if page_id == '-1':
                    break

                imageinfo = page_data.get('imageinfo', [])
                if imageinfo and 'url' in imageinfo[0]:
                    img_url = imageinfo[0]['url']
                    # Clean up URL - remove revision parameters
                    img_url = img_url.split('/revision/')[0] if '/revision/' in img_url else img_url
                    img_url = img_url.split('?')[0]
                    return img_url, f"File:{image_filename}"
        except Exception as e:
            pass

    # Method 2: Try to get the image from the vehicle page
    search_titles = [vehicle_name]

    for title in search_titles:
        params = {
            "action": "query",
            "titles": title,
            "prop": "pageimages",
            "piprop": "original",
            "format": "json",
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()

            if 'error' in data:
                continue

            pages = data.get('query', {}).get('pages', {})

            for page_id, page_data in pages.items():
                if page_id == '-1':
                    continue

                original = page_data.get('original', {})
                if original and 'source' in original:
                    img_url = original['source']
                    img_url = img_url.split('/revision/')[0] if '/revision/' in img_url else img_url
                    img_url = img_url.split('?')[0]
                    return img_url, title

        except Exception as e:
            continue

    return None, None

# ---- Fetch images for all vehicles and save to CSV ----
def save_vehicle_images(csv_file, output_file):
    df = pd.read_csv(csv_file, sep=';')

    print(f"Total entries: {len(df)}\n")

    results = []

    for idx, row in df.iterrows():
        vehicle = row['vehicle']
        image = row['image']
        sequence = row['sequence']
        movie = row['movie']

        print(f"[{idx+1}/{len(df)}] {vehicle} ({movie})")

        # Get image URL for this vehicle
        img_url, found_title = get_vehicle_image_url(vehicle, image)

        if img_url:
            print(f"Found: {found_title}")
        else:
            print(f"Not found")

        results.append({
            'vehicle': vehicle,
            'image': image,
            'sequence': sequence,
            'movie': movie,
            'image_url': img_url if img_url else ''
        })

    # Save to CSV
    results_df = pd.DataFrame(results)
    results_df = results_df[['vehicle', 'image', 'sequence', 'movie', 'image_url']]
    results_df.to_csv(output_file, index=False, encoding='utf-8', sep=';')

    print(f"Total: {len(results)} entries saved to {output_file}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "extract_knowledge/vehicles"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "all_movie_vehicles_with_image.csv"
    
    input_file = output_dir / "all_movie_vehicles.csv"

    if not input_file.exists():
        print(f"Error: {input_file} not found!")
    else:
        save_vehicle_images(input_file, output_file)