import json
import random
import urllib.request
import re
import time

def fetch_imdb_title(imdb_id):
    if not imdb_id:
        return "NO ID"
    url = f"https://v3.sg.media-imdb.com/suggestion/x/{imdb_id}.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        data = json.loads(response)
        if 'd' in data and len(data['d']) > 0:
            return data['d'][0]['l']
        return "TITLE NOT FOUND"
    except Exception as e:
        return f"ERROR: {e}"

# Путь к файлу с данными
input_file = r'data\imdb_import_clean.json'

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        movies = json.load(f)
except FileNotFoundError:
    print(f"Error: {input_file} not found. Run extract_from_letterboxd.py first.")
    exit()

# Выбираем случайные 13% фильмов для проверки
num_to_check = max(1, round(len(movies) * 0.13))
random_movies = random.sample(movies, num_to_check)

print(f"Checking {num_to_check} random movies from {input_file}...\n")

for i, m in enumerate(random_movies):
    expected_name = m['name']
    imdb_id = m['imdb']
    print(f"[{i+1}/{num_to_check}] Checking '{expected_name}' (ID: {imdb_id})...")
    actual_title = fetch_imdb_title(imdb_id)
    print(f"   -> IMDb Title: {actual_title}")
    time.sleep(0.5) # небольшая задержка, чтобы не спамить
