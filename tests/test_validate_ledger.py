#!/usr/bin/env python3
"""Fixture tests for scripts/validate_ledger.py. Does not rewrite live incidents."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_ledger.py"
SPEC = importlib.util.spec_from_file_location("validate_ledger", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
validate_ledger = importlib.util.module_from_spec(SPEC)
sys.modules["validate_ledger"] = validate_ledger
SPEC.loader.exec_module(validate_ledger)

VALID_ID = "example-pkg-2026-01-01"
VALID_RECORD = {
    "id": VALID_ID,
    "detection_source": "osv",
    "packages": [
        {"package": "example-pkg", "ecosystem": "npm", "versions": ["1.0.0"]},
    ],
}


def _write_ledger(root: Path, rows: list[dict], incidents: list[dict]) -> None:
    (root / "incidents").mkdir()
    (root / "ledger.json").write_text(json.dumps(rows), encoding="utf-8")
    for incident in incidents:
        path = root / "incidents" / f"{incident['id']}.json"
        path.write_text(json.dumps(incident), encoding="utf-8")


def _run(root: Path) -> tuple[int, str]:
    stderr = io.StringIO()
    stdout = io.StringIO()
    with redirect_stderr(stderr), redirect_stdout(stdout):
        code = validate_ledger.validate(root)
    return code, stderr.getvalue() + stdout.getvalue()


class ValidateLedgerTests(unittest.TestCase):
    def test_valid_index_and_file_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_ledger(root, [VALID_RECORD], [VALID_RECORD])
            code, out = _run(root)
            self.assertEqual(code, 0)
            self.assertIn("ok: 1 incidents", out)

    def test_index_row_missing_packages_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index_row = {
                "id": VALID_ID,
                "detection_source": "osv",
            }
            _write_ledger(root, [index_row], [VALID_RECORD])
            code, out = _run(root)
            self.assertEqual(code, 1)
            self.assertIn("ledger.json[0]: missing packages", out)
            self.assertIn("packages must be a non-empty array", out)

    def test_index_package_missing_versions_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index_row = {
                "id": VALID_ID,
                "detection_source": "osv",
                "packages": [{"package": "example-pkg", "ecosystem": "npm"}],
            }
            _write_ledger(root, [index_row], [VALID_RECORD])
            code, out = _run(root)
            self.assertEqual(code, 1)
            self.assertIn("ledger.json[0]: package 'example-pkg' versions must be a non-empty array", out)

    def test_file_missing_package_name_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad_file = {
                "id": VALID_ID,
                "detection_source": "osv",
                "packages": [{"ecosystem": "npm", "versions": ["1.0.0"]}],
            }
            _write_ledger(root, [VALID_RECORD], [bad_file])
            code, out = _run(root)
            self.assertEqual(code, 1)
            self.assertIn(f"{VALID_ID}.json: package entry missing package name", out)


if __name__ == "__main__":
    unittest.main()
