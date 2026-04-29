#!/usr/bin/env python3
"""
scan_repo_for_ai.py — Discover step.

Walk a directory tree (typically a Git repo) and surface AI assets:
  * LLM SDK imports (Python, JS/TS, Go-ish)
  * Model API hostnames (api.openai.com, etc.)
  * Environment variables that gate AI access
  * Hardcoded API keys to AI providers (flagged, NOT exfiltrated)
  * MCP server / client configuration
  * Vector store / RAG framework usage
  * Prompt / system-prompt files (by filename pattern)

Outputs three files in --out:
  findings.json  raw line-level findings (snippets redacted)
  assets.csv     AI Asset Register-aligned rows
  assets.json    same data, JSON

This script:
  - Uses only the Python standard library.
  - Never logs the value of an API key — only file path, line, and key type.
  - Skips .git/, node_modules/, virtualenvs, build dirs, lockfiles, binaries.
  - Reads files as UTF-8 with errors='replace' so it tolerates mixed encodings.

Usage:
  python3 scan_repo_for_ai.py /path/to/repo --out scan-output/
  python3 scan_repo_for_ai.py /path/to/repo --out scan-output/ --max-bytes 2000000
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Make the parent 'scripts/' dir importable when running from anywhere.
_HERE = Path(__file__).resolve().parent
_SCRIPTS = _HERE.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lib import ai_signatures as sigs  # noqa: E402
from lib.inventory import (  # noqa: E402
    Finding,
    assets_from_findings,
    make_relative,
    write_assets_csv,
    write_assets_json,
    write_findings_json,
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Scan a directory tree for AI assets (Discover step of D-Control).",
    )
    p.add_argument("path", help="Root directory to scan.")
    p.add_argument(
        "--out",
        default="scan-output/",
        help="Output directory (default: ./scan-output/).",
    )
    p.add_argument(
        "--max-bytes",
        type=int,
        default=2_000_000,
        help="Skip files larger than this many bytes (default: 2,000,000).",
    )
    p.add_argument(
        "--include-prompts",
        action="store_true",
        default=True,
        help="Also flag files whose names look like prompt files (default: on).",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file warnings.",
    )
    return p.parse_args(argv)


def _redact_snippet(line: str, signature_name: str) -> str:
    """If the signature is a key pattern, return a redacted preview."""
    is_key = signature_name.endswith("-key") or signature_name.endswith("-token")
    if is_key:
        return "[REDACTED — key match]"
    # Otherwise return a trimmed view of the line.
    s = line.strip()
    return s[:240] + ("…" if len(s) > 240 else "")


def scan_file(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = make_relative(str(path), str(root))

    # Filename signals (prompt files).
    basename = path.name
    for pat in sigs.PROMPT_FILE_PATTERNS:
        if pat.match(basename):
            findings.append(
                Finding(
                    file=rel,
                    line=0,
                    signature=f"prompt-file:{basename}",
                    asset_class="custom_internal_agent",
                    snippet=f"prompt/system message file: {basename}",
                    note="prompt-file (filename match)",
                )
            )
            break

    # Content signals — only for text-like files.
    if not sigs.is_text_path(basename, path.suffix):
        return findings

    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, start=1):
                # Cheap pre-filter: skip lines unlikely to match anything (no letters).
                if not any(ch.isalpha() for ch in line):
                    continue
                for sig in sigs.ALL_CONTENT_SIGNATURES:
                    if sig.pattern.search(line):
                        findings.append(
                            Finding(
                                file=rel,
                                line=lineno,
                                signature=sig.name,
                                asset_class=sig.asset_class,
                                snippet=_redact_snippet(line, sig.name),
                                note=sig.note,
                            )
                        )
    except (OSError, UnicodeError):
        # Read errors should not abort the whole scan.
        return findings

    return findings


def walk(root: Path, max_bytes: int, quiet: bool) -> list[Finding]:
    all_findings: list[Finding] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skip-dirs in-place so os.walk doesn't descend.
        dirnames[:] = [d for d in dirnames if d not in sigs.SKIP_DIR_NAMES]

        for fname in filenames:
            if fname in sigs.SKIP_FILE_NAMES:
                continue
            full = Path(dirpath) / fname
            try:
                size = full.stat().st_size
            except OSError:
                continue
            if size > max_bytes:
                if not quiet:
                    print(f"skip (too large {size} bytes): {full}", file=sys.stderr)
                continue

            try:
                all_findings.extend(scan_file(full, root))
            except Exception as e:  # noqa: BLE001
                if not quiet:
                    print(f"error scanning {full}: {e}", file=sys.stderr)
    return all_findings


def main(argv: list[str]) -> int:
    ns = parse_args(argv)
    root = Path(ns.path).resolve()
    if not root.exists():
        print(f"error: path does not exist: {root}", file=sys.stderr)
        return 1
    if not root.is_dir():
        print(f"error: path is not a directory: {root}", file=sys.stderr)
        return 1

    out_dir = Path(ns.out).resolve()

    findings = walk(root, max_bytes=ns.max_bytes, quiet=ns.quiet)
    assets = assets_from_findings(findings, discovery_source="git_scan")

    write_findings_json(out_dir, findings)
    write_assets_csv(out_dir, assets)
    write_assets_json(out_dir, assets)

    print(f"scanned root: {root}")
    print(f"findings: {len(findings)}")
    print(f"inferred assets: {len(assets)}")
    print(f"outputs in: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
