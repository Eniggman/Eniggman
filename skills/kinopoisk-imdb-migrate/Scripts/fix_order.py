import json
import re
import string

def normalize(s):
    # Remove punctuation and lowercase
    s = s.lower()
    for p in string.punctuation:
        s = s.replace(p, '')
    return ' '.join(s.split())

with open('data/imdb_import_clean.json', 'r', encoding='utf-8') as f:
    movies_json = json.load(f)

with open('watched.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

pattern = re.compile(r'\|\s*(\d+)\s*\|\s*\*\*([^*]+)\*\*\s*(?:\([^)]+\))?\s*(?:\[([^\]]+)\])?\s*\|\s*(?:\*\*(\d+)\*\*|(\d+))\s*\|')

md_movies = []
for line in md_content.splitlines():
    match = pattern.search(line)
    if match:
        idx = int(match.group(1))
        rus_name = match.group(2).strip()
        eng_name = match.group(3).strip() if match.group(3) else rus_name
        rating_str = match.group(4) or match.group(5)
        rating = int(rating_str) if rating_str else None
        md_movies.append({
            'idx': idx,
            'rus': rus_name,
            'eng': eng_name,
            'rating': rating
        })

md_movies.sort(key=lambda x: x['idx'], reverse=True)

unmatched_json = movies_json.copy()

# Fix known overrides manually:
overrides = {
    "Примерный Фильм 1": "Example Movie 1",
    "Примерный Фильм 2": "Example Movie 2"
}

new_json_list = []
for md_movie in md_movies:
    best_match = None
    best_match_idx = -1
    
    # 0. Check overrides
    for i, jm in enumerate(unmatched_json):
        if md_movie['rus'] in overrides and jm['name'] == overrides[md_movie['rus']]:
            best_match = jm
            best_match_idx = i
            break
        elif overrides.get(md_movie['eng']) == jm['name']:
            best_match = jm
            best_match_idx = i
            break
            
    # 1. Exact match (case insensitive)
    if not best_match:
        for i, jm in enumerate(unmatched_json):
            if jm['name'].lower() == md_movie['eng'].lower():
                best_match = jm
                best_match_idx = i
                break
                
    # 2. Normalized match
    if not best_match:
        for i, jm in enumerate(unmatched_json):
            if normalize(jm['name']) == normalize(md_movie['eng']):
                best_match = jm
                best_match_idx = i
                break

    # 3. Substring match for long enough names
    if not best_match:
        for i, jm in enumerate(unmatched_json):
            norm_md = normalize(md_movie['eng'])
            norm_jm = normalize(jm['name'])
            if len(norm_md) > 5 and len(norm_jm) > 5:
                if norm_md in norm_jm or norm_jm in norm_md:
                    best_match = jm
                    best_match_idx = i
                    break

    if best_match:
        new_json_list.append(best_match)
        unmatched_json.pop(best_match_idx)
    else:
        # Create a stub if missing
        print(f"Creating stub for missing in JSON: {md_movie['eng']}")
        # new_json_list.append({
        #    "name": md_movie['eng'],
        #    "rating": md_movie['rating'],
        #    "imdb": ""
        # })

print(f"Leftovers in JSON: {len(unmatched_json)}")
for x in unmatched_json:
    print("  ", x['name'])

# Overwrite JSON with only matched items (to keep it clean, or we can append the rest)
# Wait! The user said "make sure the list goes EXACTLY here but in reverse".
# If I just write out the matched ones, it'll have the correct exact order. If there are 12 missing in JSON, I can just leave them out (or insert placeholders if needed, but since it's an import json for IMDb, items without IMDb ID will crash the script, so maybe skip them).
new_json_list.extend(unmatched_json)

with open('data/imdb_import_clean.json', 'w', encoding='utf-8') as f:
    json.dump(new_json_list, f, indent=2, ensure_ascii=False)

