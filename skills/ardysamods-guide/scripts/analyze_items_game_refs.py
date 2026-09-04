import argparse
import json
import re
from pathlib import Path


STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')
HERO_RE = re.compile(r'"(npc_dota_hero_[^"]+)"\s+"1"')
MOD_PATH_RE = re.compile(
    r"(kisilev_ind/|8213/|jxj/|models123/|particles123/|youtube\.com/@ardysa|this item has been modded)",
    re.IGNORECASE,
)
NUMERIC_PAIR_RE = re.compile(r'"(?P<key>[^"]+)"\s+"(?P<value>\d+)"')
REFERENCE_KEY_RE = re.compile(
    r"(^|_)(item_def|itemdef|effects_item_def|required_item|required_item_def|"
    r"bundle|bundle_item|contained_item|contains|loot|reward|recipe|tool|target|"
    r"set_item|style_unlock|quest_item|drop_item|grant_item|source_item)($|_)",
    re.IGNORECASE,
)


def unquote(token):
    return token[1:-1]


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
    name_pos = text.find(f'"{name}"')
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
        yield key, match.start(), end
        pos = end


def map_items(text):
    _, items_open, items_end = find_named_block(text, "items")
    result = {}
    for key, start, end in iter_child_blocks(text, items_open, items_end):
        if key.isdigit():
            result[key] = (start, end)
    return result


def item_heroes(block):
    return set(HERO_RE.findall(block))


def has_modded_path(block):
    return bool(MOD_PATH_RE.search(block))


def line_number(text, pos):
    return text.count("\n", 0, pos) + 1


def build_reference_index(text, candidate_ranges):
    candidate_ids = set(candidate_ranges)
    refs_by_id = {item_id: [] for item_id in candidate_ids}
    for match in NUMERIC_PAIR_RE.finditer(text):
        item_id = match.group("value")
        if item_id not in candidate_ids:
            continue
        key = match.group("key")
        if not REFERENCE_KEY_RE.search(key):
            continue
        own_start, own_end = candidate_ranges[item_id]
        if own_start <= match.start() < own_end:
            continue
        refs_by_id[item_id].append(
            {
                "key": key,
                "line": line_number(text, match.start()),
                "offset": match.start(),
            }
        )
    return refs_by_id


def summarize_refs(refs):
    counts = {}
    for ref in refs:
        counts[ref["key"]] = counts.get(ref["key"], 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def main():
    parser = argparse.ArgumentParser(
        description="Analyze items_game item blocks before any sanitizer edits."
    )
    parser.add_argument("--mod", required=True)
    parser.add_argument("--default", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--json-report")
    parser.add_argument(
        "--hero",
        action="append",
        default=[],
        help="Limit analysis to one or more hero names, for example lion or bounty_hunter.",
    )
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()

    mod_path = Path(args.mod)
    default_path = Path(args.default)
    config_path = Path(args.config)
    report_path = Path(args.report)

    mod_text = mod_path.read_text(encoding="utf-8", errors="replace")
    default_text = default_path.read_text(encoding="utf-8", errors="replace")
    config = json.loads(config_path.read_text(encoding="utf-8"))

    active = {f"npc_dota_hero_{hero}" for hero in config.get("active_roster", [])}
    hero_filter = {
        hero if hero.startswith("npc_dota_hero_") else f"npc_dota_hero_{hero}"
        for hero in args.hero
    }
    mod_items = map_items(mod_text)
    default_items = map_items(default_text)

    candidate_ranges = {}
    candidates_by_id = {}
    protected_active = 0
    inactive_unmodded = 0
    no_hero = 0
    no_default = 0

    for item_id, item_range in mod_items.items():
        start, end = item_range
        block = mod_text[start:end]
        heroes = item_heroes(block)
        if not heroes:
            no_hero += 1
            continue
        if hero_filter and not (heroes & hero_filter):
            continue
        if heroes & active:
            protected_active += 1
            continue
        if not has_modded_path(block):
            inactive_unmodded += 1
            continue
        if item_id not in default_items:
            no_default += 1
        default_block = (
            default_text[default_items[item_id][0] : default_items[item_id][1]]
            if item_id in default_items
            else ""
        )
        candidate_ranges[item_id] = item_range
        candidates_by_id[item_id] = {
            "item_id": item_id,
            "heroes": sorted(heroes),
            "line": line_number(mod_text, start),
            "has_default": item_id in default_items,
            "differs_from_default": bool(default_block and block != default_block),
        }

    refs_by_id = build_reference_index(mod_text, candidate_ranges)
    candidates = []
    for item_id, item in candidates_by_id.items():
        refs = refs_by_id[item_id]
        item["reference_count"] = len(refs)
        item["reference_keys"] = summarize_refs(refs)
        item["sample_refs"] = refs[:10]
        candidates.append(item)

    candidates.sort(
        key=lambda item: (
            -item["reference_count"],
            ",".join(item["heroes"]),
            int(item["item_id"]),
        )
    )

    risky = [item for item in candidates if item["reference_count"] > 0]
    safe_direct = [
        item
        for item in candidates
        if item["reference_count"] == 0
        and item["has_default"]
        and item["differs_from_default"]
    ]

    lines = [
        "# items_game reference analysis",
        "",
        f"Mod file: `{mod_path}`",
        f"Default file: `{default_path}`",
        f"Config: `{config_path}`",
        "",
        "## Summary",
        "",
        f"- Active heroes protected: `{len(active)}`",
        f"- Hero filter: `{', '.join(sorted(hero_filter)) if hero_filter else 'none'}`",
        f"- Mod item blocks: `{len(mod_items)}`",
        f"- Default item blocks: `{len(default_items)}`",
        f"- Inactive modded candidate blocks: `{len(candidates)}`",
        f"- Risky candidates with references: `{len(risky)}`",
        f"- Direct-replace candidates without references: `{len(safe_direct)}`",
        f"- Skipped active item blocks: `{protected_active}`",
        f"- Skipped no-hero item blocks: `{no_hero}`",
        f"- Skipped inactive unmodded blocks: `{inactive_unmodded}`",
        f"- Candidates missing default block: `{no_default}`",
        "",
        "## Risky Referenced Candidates",
        "",
    ]
    for item in risky[: args.limit]:
        refs = ", ".join(f"{key}={count}" for key, count in item["reference_keys"].items())
        lines.append(
            f"- `{item['item_id']}` line `{item['line']}` heroes `{', '.join(item['heroes'])}` refs `{item['reference_count']}` ({refs})"
        )
        for ref in item["sample_refs"][:3]:
            lines.append(f"  - `{ref['key']}` at line `{ref['line']}`")

    lines.extend(["", "## Direct Replace Candidates", ""])
    for item in safe_direct[: args.limit]:
        lines.append(
            f"- `{item['item_id']}` line `{item['line']}` heroes `{', '.join(item['heroes'])}`"
        )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if args.json_report:
        json_path = Path(args.json_report)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(
                {
                    "summary": {
                        "active_heroes_protected": len(active),
                        "mod_item_blocks": len(mod_items),
                        "default_item_blocks": len(default_items),
                        "inactive_modded_candidates": len(candidates),
                        "risky_referenced_candidates": len(risky),
                        "direct_replace_candidates_without_refs": len(safe_direct),
                        "skipped_active": protected_active,
                        "skipped_no_hero": no_hero,
                        "skipped_inactive_unmodded": inactive_unmodded,
                        "candidates_missing_default": no_default,
                    },
                    "risky": risky,
                    "safe_direct": safe_direct,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
