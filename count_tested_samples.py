#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

SAMPLE_RE = re.compile(r"^(sample_.+?_idx(?P<idx>\d+)_s(?P<seed>\d+))(?:_(?P<suffix>.+))?$")


def sample_key(path: Path):
    name = path.name
    stem = name
    for ext in (".png", ".pt", ".glb", ".obj", ".ply"):
        if stem.endswith(ext):
            stem = stem[: -len(ext)]
            break
    match = SAMPLE_RE.match(stem)
    if not match:
        return None
    return match.group(1), int(match.group("idx")), int(match.group("seed"))


def load_total_from_split(vis_dir: Path, split_path: str | None):
    if split_path is None:
        repo_root = vis_dir.resolve().parents[1]
        split_file = repo_root / "configs" / "splits" / "test.json"
    else:
        split_file = Path(split_path)
        if not split_file.is_absolute():
            split_file = (Path.cwd() / split_file).resolve()
    if not split_file.exists():
        return None, split_file
    with split_file.open("r") as f:
        data = json.load(f)
    return len(data), split_file


def main():
    parser = argparse.ArgumentParser(description="Count completed SK-Adapter eval samples in a vis output directory.")
    parser.add_argument("vis_dir", nargs="?", default=Path(__file__).resolve().parent,
                        type=Path, help="Directory containing sample_* outputs")
    parser.add_argument("--split", default=None,
                        help="Optional split json for total sample count. Defaults to ../../configs/splits/test.json")
    parser.add_argument("--show-incomplete", action="store_true",
                        help="Print incomplete sample prefixes")
    args = parser.parse_args()

    vis_dir = args.vis_dir.resolve()
    samples = {}

    for path in vis_dir.iterdir():
        if not path.is_file() or not path.name.startswith("sample_"):
            continue
        parsed = sample_key(path)
        if not parsed:
            continue
        key, idx, seed = parsed
        entry = samples.setdefault(key, {"idx": idx, "seed": seed, "files": set(), "render_count": 0})
        entry["files"].add(path.name)
        if re.search(r"_render_\d\d\.png$", path.name):
            entry["render_count"] += 1

    completed = []
    incomplete = []
    for key, info in samples.items():
        files = info["files"]
        has_gaussian = f"{key}_gaussian.pt" in files
        has_last_render = f"{key}_render_11.png" in files
        has_glb = f"{key}.glb" in files
        is_complete = has_gaussian and has_last_render
        row = (info["idx"], key, info["render_count"], has_gaussian, has_last_render, has_glb)
        if is_complete:
            completed.append(row)
        else:
            incomplete.append(row)

    completed.sort()
    incomplete.sort()
    total, split_file = load_total_from_split(vis_dir, args.split)

    print(f"vis_dir: {vis_dir}")
    print(f"detected sample prefixes: {len(samples)}")
    print(f"completed samples: {len(completed)}")
    print(f"incomplete/running samples: {len(incomplete)}")
    if total is not None:
        pct = (len(completed) / total * 100.0) if total else 0.0
        print(f"split total: {total} ({split_file})")
        print(f"progress: {len(completed)}/{total} = {pct:.1f}%")
    else:
        print(f"split total: unknown (not found: {split_file})")

    if completed:
        print(f"completed idx range: {completed[0][0]}..{completed[-1][0]}")

    if incomplete:
        print("\nincomplete samples:")
        for idx, key, render_count, has_gaussian, has_last_render, has_glb in incomplete[:50]:
            missing = []
            if not has_gaussian:
                missing.append("gaussian.pt")
            if not has_last_render:
                missing.append("render_11.png")
            if not has_glb:
                missing.append("glb")
            print(f"  idx={idx} renders={render_count:02d} missing={','.join(missing) or 'none'} {key}")
        if len(incomplete) > 50:
            print(f"  ... {len(incomplete) - 50} more")
    elif args.show_incomplete:
        print("\nincomplete samples: none")


if __name__ == "__main__":
    main()
