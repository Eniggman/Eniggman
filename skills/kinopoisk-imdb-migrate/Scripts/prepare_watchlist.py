import json
import urllib.request
import urllib.parse
import time
import os
import re

input_file = r'data\watch_later.txt'
output_json = r'data\imdb_watchlist_import.json'
chunk_dir = r'data\watchlist_chunks'

if not os.path.exists(chunk_dir):
    os.makedirs(chunk_dir)

# Manual overrides for tricky titles
manual_fixes = {
    "Конец грёбаного мира": "tt6257970",
    
}

def get_imdb_id(title):
    if title in manual_fixes:
        return manual_fixes[title], title, "FIXED"
        
    query = title.replace('(сериал)', '').strip()
    encoded_query = urllib.parse.quote(query)
    url = f"https://v3.sg.media-imdb.com/suggestion/x/{encoded_query}.json"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if 'd' in data and len(data['d']) > 0:
                for item in data['d']:
                    if item['id'].startswith('tt'):
                        return item['id'], item['l'], item.get('y', '????')
    except Exception as e:
        print(f"Error searching for {title}: {e}")
    return None, None, None

def main():
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    titles = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('=') or "СПИСОК ФИЛЬМОВ" in line:
            continue
        titles.append(line)

    # Invert order
    titles.reverse()

    results = []
    print(f"Searching for {len(titles)} titles...")

    for i, title in enumerate(titles):
        imdb_id, found_title, year = get_imdb_id(title)
        if imdb_id:
            results.append({
                "name": found_title,
                "original_name": title,
                "year": year,
                "imdb": imdb_id
            })
        else:
            print(f"  NOT FOUND: {title}")
            results.append({
                "name": title,
                "original_name": title,
                "year": "????",
                "imdb": "NOT_FOUND"
            })
        
        if title not in manual_fixes:
            time.sleep(0.1)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    chunk_size = 40
    for i in range(0, len(results), chunk_size):
        chunk = results[i:i + chunk_size]
        chunk_num = (i // chunk_size) + 1
        filename = os.path.join(chunk_dir, f"watchlist_part_{chunk_num}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, indent=2, ensure_ascii=False)

    print(f"Finished! Saved {len(results)} items to {output_json}")

if __name__ == "__main__":
    main()
