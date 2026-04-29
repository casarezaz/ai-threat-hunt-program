#!/usr/bin/env python3
"""
merge_inventory.py — merge multiple AI Asset Register CSVs into one.

Each scanner emits its own assets.csv. This script unions them, deduplicates
by (asset_class, name), and merges per-row data conservatively:
  - For boolean-ish capability columns: 'true' wins over '' or 'false'.
  - For multi-value columns (oauth_scopes, connectors): values joined and deduped.
  - For first_seen / last_reviewed: keep the earliest first_seen, latest last_reviewed.
  - Notes: concatenated with '; '.

Usage:
  python3 merge_inventory.py scan-output/*.csv --out templates/ai-asset-register.csv

Pass any number of inputs; missing files are reported but do not abort.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SCRIPTS = _HERE.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lib.inventory import REGISTER_FIELDS  # noqa: E402


BOOLEAN_COLS: frozenset[str] = frozenset({
    "can_read", "can_write", "can_send", "can_publish",
    "can_deploy", "can_delete", "can_approve", "can_modify_security_controls",
    "sanctioned",
})

MULTI_VALUE_COLS: frozenset[str] = frozenset({
    "oauth_scopes",
    "connectors",
})


def merge_value(col: str, existing: str, incoming: str) -> str:
    if not incoming:
        return existing
    if not existing:
        return incoming
    if col in BOOLEAN_COLS:
        # 'true' wins.
        if existing.strip().lower() == "true" or incoming.strip().lower() == "true":
            return "true"
        return existing
    if col in MULTI_VALUE_COLS:
        merged = {p.strip() for p in (existing + ";" + incoming).split(";") if p.strip()}
        return "; ".join(sorted(merged))
    if col == "first_seen":
        return min(existing, incoming)  # ISO dates sort lexicographically
    if col == "last_reviewed":
        return max(existing, incoming)
    if col == "notes":
        return f"{existing}; {incoming}".strip("; ")
    # Otherwise prefer existing if both are non-empty and differ.
    if existing == incoming:
        return existing
    return existing  # be conservative — analyst can review


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Merge multiple AI Asset Register CSVs into a single deduplicated register.",
    )
    p.add_argument("inputs", nargs="+", help="Input CSV files (one or more).")
    p.add_argument("--out", required=True, help="Output CSV path.")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    ns = parse_args(argv)
    out_path = Path(ns.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    merged: dict[tuple[str, str], dict[str, str]] = {}
    for inp in ns.inputs:
        path = Path(inp).resolve()
        if not path.exists():
            print(f"skip (missing): {path}", file=sys.stderr)
            continue
        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                continue
            for row in reader:
                name = (row.get("name") or "").strip()
                asset_class = (row.get("asset_class") or "").strip()
                if not name or not asset_class:
                    continue
                key = (asset_class, name)
                if key not in merged:
                    merged[key] = {f: (row.get(f) or "").strip() for f in REGISTER_FIELDS}
                else:
                    for f in REGISTER_FIELDS:
                        merged[key][f] = merge_value(f, merged[key][f], (row.get(f) or "").strip())

    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REGISTER_FIELDS)
        writer.writeheader()
        for (_, _), row in sorted(merged.items()):
            writer.writerow(row)

    print(f"inputs: {len(ns.inputs)}")
    print(f"unique assets: {len(merged)}")
    print(f"output: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
