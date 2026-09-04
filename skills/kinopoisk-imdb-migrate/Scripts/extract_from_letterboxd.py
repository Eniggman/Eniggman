import csv
import re
import json
import time
import concurrent.futures
import urllib.request
import urllib.error

def fetch_imdb_id(row):
    name = row['Name']
    uri = row['Letterboxd URI']
    rating = int(float(row['Rating']) * 2) if row['Rating'] else None
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(uri, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            # Look for IMDb link
            match = re.search(r'href="https?://www\.imdb\.com/title/(tt\d+)/?.*?"', html)
            if match:
                imdb_id = match.group(1)
                return {'name': name, 'rating': rating, 'imdb': imdb_id}
            else:
                print(f"No IMDb ID found on Letterboxd page for: {name}")
                return None
    except Exception as e:
        print(f"Error fetching {name} ({uri}): {e}")
        return None

def main():
    movies = []
    with open('letterboxd_export/ratings.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        movies = list(reader)
        
    print(f"Starting extraction for {len(movies)} movies from Letterboxd...")
    
    results = []
    # Use ThreadPoolExecutor to speed up fetching, but keep max_workers reasonable to avoid bans
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_imdb_id, movie): movie for movie in movies}
        
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result()
            if result:
                results.append(result)
            if i % 10 == 0:
                print(f"Processed {i}/{len(movies)} movies...")
                
    print(f"Successfully extracted {len(results)} IMDb IDs.")
    
    # Save the new clean JSON
    # Reverse it so the oldest ratings are at the bottom (meaning they get imported first if the script processes top-to-bottom)
    # Actually, the user asked to reverse the list last time so the first ones go first. 
    # Let's just reverse the original list from Letterboxd which is newest first.
    # If we reverse it, the oldest imported to Letterboxd becomes the first in the JSON.
    results.reverse()
    
    with open('data/imdb_import_clean.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print("Saved to data/imdb_import_clean.json")

if __name__ == "__main__":
    main()
