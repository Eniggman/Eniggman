import json
import os
import glob

# Delete old chunks
chunk_dir = 'data/import_chunks'
for f in glob.glob(os.path.join(chunk_dir, 'part_*.json')):
    os.remove(f)

# Load full json
with open('data/imdb_import_clean.json', 'r', encoding='utf-8') as f:
    movies = json.load(f)

# Chunk sizes
chunks = [5, 10, 20, 40]

start = 0
part_num = 1

for size in chunks:
    end = start + size
    chunk_data = movies[start:end]
    filename = os.path.join(chunk_dir, f"part_{part_num}_{size}_items.json")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(chunk_data, f, indent=2, ensure_ascii=False)
    print(f"Created {filename} with {len(chunk_data)} items")
    start = end
    part_num += 1

# Remaining items in the last part
remaining_data = movies[start:]
remaining_size = len(remaining_data)
filename = os.path.join(chunk_dir, f"part_{part_num}_{remaining_size}_items.json")
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(remaining_data, f, indent=2, ensure_ascii=False)
print(f"Created {filename} with {len(remaining_data)} items")

print("All chunks regenerated based on the updated 177 items JSON.")
