#!/usr/bin/env python3
"""Assert ledger.json ids match incidents/*.json without changing detection data."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "ledger.json"
INCIDENTS = ROOT / "incidents"
ALLOWED_ECOSYSTEMS = {"npm", "pypi"}
REQUIRED_KEYS = ("id", "detection_source", "packages")


def main() -> int:
    rows = json.loads(INDEX.read_text())
    if not isinstance(rows, list):
        print("ledger.json is not an array", file=sys.stderr)
        return 1

    index_ids: list[str] = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or not row.get("id"):
            print(f"ledger.json[{i}] missing id", file=sys.stderr)
            return 1
        index_ids.append(str(row["id"]))

    if len(index_ids) != len(set(index_ids)):
        print("duplicate ids in ledger.json", file=sys.stderr)
        return 1

    files = {p.stem: p for p in INCIDENTS.glob("*.json")}
    index_set = set(index_ids)
    file_set = set(files)
    missing_files = sorted(index_set - file_set)
    extra_files = sorted(file_set - index_set)
    if missing_files or extra_files:
        print(
            f"index-only: {len(missing_files)} file-only: {len(extra_files)}",
            file=sys.stderr,
        )
        for name in (missing_files + extra_files)[:20]:
            print(name, file=sys.stderr)
        return 1

    errors = 0
    for incident_id, path in files.items():
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            print(f"{path.name}: not a JSON object", file=sys.stderr)
            errors += 1
            continue
        if data.get("id") != incident_id:
            print(f"{path.name}: id {data.get('id')!r} != filename", file=sys.stderr)
            errors += 1
        for key in REQUIRED_KEYS:
            if key not in data:
                print(f"{path.name}: missing {key}", file=sys.stderr)
                errors += 1
        packages = data.get("packages")
        if not isinstance(packages, list) or not packages:
            print(f"{path.name}: packages must be a non-empty array", file=sys.stderr)
            errors += 1
            continue
        for pkg in packages:
            if not isinstance(pkg, dict):
                print(f"{path.name}: package entry is not an object", file=sys.stderr)
                errors += 1
                continue
            eco = pkg.get("ecosystem")
            if eco not in ALLOWED_ECOSYSTEMS:
                print(f"{path.name}: bad ecosystem {eco!r}", file=sys.stderr)
                errors += 1

    if errors:
        print(f"{errors} incident file error(s)", file=sys.stderr)
        return 1

    print(f"ok: {len(index_ids)} incidents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
