import argparse
import json
import re
from pathlib import Path

# Experimental only. This prototype does not preserve all econ/event cross
# references, such as event_id/effects_item_def links, and must not be used for
# production VPK builds without a full reference graph pass.

STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')
HERO_RE = re.compile(r'"(npc_dota_hero_[^"]+)"\s+"1"')


def unquote(token):
    return token[1:-1]


def find_string(text, value, start=0, end=None):
    if end is None:
        end = len(text)
    needle = f'"{value}"'
    return text.find(needle, start, end)


def find_matching_brace(text, open_pos):
    depth = 0
    pos = open_pos
    in_string = False
    escaped = False
    while pos < len(text):
        ch = text[pos]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return pos
        pos += 1
    raise ValueError(f"No matching brace for position {open_pos}")


def find_named_block(text, name):
    name_pos = find_string(text, name)
    if name_pos < 0:
        raise ValueError(f'Block "{name}" not found')
    open_pos = text.find("{", name_pos)
    if open_pos < 0:
        raise ValueError(f'Block "{name}" has no opening brace')
    close_pos = find_matching_brace(text, open_pos)
    return name_pos, open_pos, close_pos + 1


def iter_child_blocks(text, open_pos, close_exclusive):
    pos = open_pos + 1
    while pos < close_exclusive - 1:
        match = STRING_RE.search(text, pos, close_exclusive)
        if not match:
            break
        key = unquote(match.group(0))
        brace = text.find("{", match.end(), close_exclusive)
        next_string = STRING_RE.search(text, match.end(), close_exclusive)
        if brace < 0 or (next_string and next_string.start() < brace):
            pos = match.end()
            continue
        end = find_matching_brace(text, brace) + 1
        yield key, match.start(), end, brace, end - 1
        pos = end


def map_items(text):
    _, items_open, items_end = find_named_block(text, "items")
    result = {}
    for key, start, end, _, _ in iter_child_blocks(text, items_open, items_end):
        if key.isdigit():
            result[key] = (start, end)
    return result


def item_heroes(block):
    return set(HERO_RE.findall(block))


def has_modded_path(block):
    lowered = block.lower()
    markers = (
        "kisilev_ind/",
        "8213/",
        "jxj/",
        "models123/",
        "particles123/",
        "youtube.com/@ardysa",
        "this item has been modded",
    )
    return any(marker in lowered for marker in markers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod", required=True)
    parser.add_argument("--default", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--replace-all-inactive", action="store_true")
    args = parser.parse_args()

    mod_path = Path(args.mod)
    default_path = Path(args.default)
    config_path = Path(args.config)
    output_path = Path(args.output)
    report_path = Path(args.report)

    mod_text = mod_path.read_text(encoding="utf-8", errors="replace")
    default_text = default_path.read_text(encoding="utf-8", errors="replace")
    config = json.loads(config_path.read_text(encoding="utf-8"))

    active = {f"npc_dota_hero_{hero}" for hero in config.get("active_roster", [])}
    default_items = map_items(default_text)
    mod_items = map_items(mod_text)

    replacements = []
    skipped_active = 0
    skipped_no_default = 0
    skipped_no_hero = 0
    skipped_unmodded = 0

    for item_id, (start, end) in mod_items.items():
        block = mod_text[start:end]
        heroes = item_heroes(block)
        if not heroes:
            skipped_no_hero += 1
            continue
        if heroes & active:
            skipped_active += 1
            continue
        if item_id not in default_items:
            skipped_no_default += 1
            continue
        if not args.replace_all_inactive and not has_modded_path(block):
            skipped_unmodded += 1
            continue
        default_start, default_end = default_items[item_id]
        default_block = default_text[default_start:default_end]
        if block != default_block:
            replacements.append((start, end, default_block, item_id, sorted(heroes)))

    chunks = []
    cursor = 0
    for start, end, replacement, _, _ in sorted(replacements, key=lambda item: item[0]):
        chunks.append(mod_text[cursor:start])
        chunks.append(replacement)
        cursor = end
    chunks.append(mod_text[cursor:])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(chunks), encoding="utf-8", newline="")

    hero_counts = {}
    for _, _, _, _, heroes in replacements:
        for hero in heroes:
            hero_counts[hero] = hero_counts.get(hero, 0) + 1

    lines = [
        "# items_game sanitize report",
        "",
        f"Mod file: {mod_path}",
        f"Default file: {default_path}",
        f"Output file: {output_path}",
        f"Active heroes protected: {len(active)}",
        f"Mod item blocks: {len(mod_items)}",
        f"Default item blocks: {len(default_items)}",
        f"Replaced inactive item blocks: {len(replacements)}",
        f"Skipped active item blocks: {skipped_active}",
        f"Skipped no-hero item blocks: {skipped_no_hero}",
        f"Skipped no default item block: {skipped_no_default}",
        f"Skipped inactive unmodded blocks: {skipped_unmodded}",
        "",
        "## Replacements by hero",
    ]
    for hero, count in sorted(hero_counts.items()):
        lines.append(f"- {hero}: {count}")
    lines.extend(["", "## First replacements"])
    for _, _, _, item_id, heroes in replacements[:200]:
        lines.append(f"- {item_id}: {', '.join(heroes)}")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
