#!/usr/bin/env python3
"""Assert ledger.json ids match incidents/*.json without changing detection data."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_ECOSYSTEMS = {"npm", "pypi"}
REQUIRED_KEYS = ("id", "detection_source", "packages")


def _validate_packages(label: str, packages: object) -> int:
    errors = 0
    if not isinstance(packages, list) or not packages:
        print(f"{label}: packages must be a non-empty array", file=sys.stderr)
        return 1
    for pkg in packages:
        if not isinstance(pkg, dict):
            print(f"{label}: package entry is not an object", file=sys.stderr)
            errors += 1
            continue
        name = pkg.get("package")
        if not isinstance(name, str) or not name.strip():
            print(f"{label}: package entry missing package name", file=sys.stderr)
            errors += 1
        eco = pkg.get("ecosystem")
        if eco not in ALLOWED_ECOSYSTEMS:
            print(f"{label}: bad ecosystem {eco!r}", file=sys.stderr)
            errors += 1
        versions = pkg.get("versions")
        if not isinstance(versions, list) or not versions:
            print(
                f"{label}: package {name!r} versions must be a non-empty array",
                file=sys.stderr,
            )
            errors += 1
        elif any(not isinstance(v, str) or not v.strip() for v in versions):
            print(
                f"{label}: package {name!r} has a non-string or empty version",
                file=sys.stderr,
            )
            errors += 1
    return errors


def _validate_record(label: str, data: dict) -> int:
    errors = 0
    for key in REQUIRED_KEYS:
        if key not in data:
            print(f"{label}: missing {key}", file=sys.stderr)
            errors += 1
    errors += _validate_packages(label, data.get("packages"))
    return errors


def validate(root: Path | None = None) -> int:
    root = ROOT if root is None else root
    index_path = root / "ledger.json"
    incidents_dir = root / "incidents"

    rows = json.loads(index_path.read_text())
    if not isinstance(rows, list):
        print("ledger.json is not an array", file=sys.stderr)
        return 1

    index_ids: list[str] = []
    errors = 0
    for i, row in enumerate(rows):
        label = f"ledger.json[{i}]"
        if not isinstance(row, dict) or not row.get("id"):
            print(f"{label} missing id", file=sys.stderr)
            return 1
        index_ids.append(str(row["id"]))
        errors += _validate_record(label, row)

    if len(index_ids) != len(set(index_ids)):
        print("duplicate ids in ledger.json", file=sys.stderr)
        return 1

    files = {p.stem: p for p in incidents_dir.glob("*.json")}
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

    for incident_id, path in files.items():
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            print(f"{path.name}: not a JSON object", file=sys.stderr)
            errors += 1
            continue
        if data.get("id") != incident_id:
            print(f"{path.name}: id {data.get('id')!r} != filename", file=sys.stderr)
            errors += 1
        errors += _validate_record(path.name, data)

    if errors:
        print(f"{errors} validation error(s)", file=sys.stderr)
        return 1

    print(f"ok: {len(index_ids)} incidents")
    return 0


def main() -> int:
    return validate()


if __name__ == "__main__":
    raise SystemExit(main())
