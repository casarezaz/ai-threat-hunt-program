#!/usr/bin/env python3
"""
scan_env_for_ai.py — Discover step (environment / configuration files).

Targeted scanner for the kinds of files where AI access is *configured*
even when the application code is in another repo:
  * .env, .env.*, .envrc
  * shell rc files (.bashrc, .zshrc, .profile)  — only when explicitly listed
  * docker-compose.yml, docker-compose.*.yml
  * kubernetes manifests
  * Terraform / OpenTofu (.tf, .tfvars)
  * GitHub Actions / GitLab CI / CircleCI / Buildkite YAML
  * Generic JSON / YAML / TOML configs

Same redaction guarantee as scan_repo_for_ai.py: API keys are flagged by
location and type only; values are never written to output.

Usage:
  python3 scan_env_for_ai.py /path/to/configs --out scan-output/
  python3 scan_env_for_ai.py ~/.zshrc ~/.bashrc --out scan-output/
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

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


CONFIGY_BASENAMES: frozenset[str] = frozenset({
    ".env", ".envrc",
    ".bashrc", ".zshrc", ".profile", ".bash_profile", ".zprofile",
    "docker-compose.yml", "docker-compose.yaml",
})

CONFIGY_SUFFIXES: frozenset[str] = frozenset({
    ".env",
    ".yml", ".yaml",
    ".json", ".jsonc",
    ".toml",
    ".tf", ".tfvars", ".hcl",
    ".ini", ".cfg", ".conf",
    ".ps1", ".sh", ".bash", ".zsh",
})


# Subset of signatures most relevant for env / config files.
ENV_RELEVANT: tuple = (
    *sigs.AI_ENV_VARS,
    *sigs.MODEL_API_HOSTS,
    *sigs.API_KEY_PATTERNS,
    *sigs.MCP_HINTS,
    *sigs.VECTOR_STORE,
)


def is_target(path: Path) -> bool:
    if path.name in CONFIGY_BASENAMES:
        return True
    if path.suffix.lower() in CONFIGY_SUFFIXES:
        return True
    # docker-compose.<env>.yml
    if path.name.startswith("docker-compose.") and path.suffix.lower() in {".yml", ".yaml"}:
        return True
    # .env.* files
    if path.name.startswith(".env."):
        return True
    return False


def _redact_snippet(line: str, signature_name: str) -> str:
    is_key = signature_name.endswith("-key") or signature_name.endswith("-token")
    if is_key:
        return "[REDACTED — key match]"
    s = line.strip()
    return s[:240] + ("…" if len(s) > 240 else "")


def scan_file(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = make_relative(str(path), str(root))
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, start=1):
                if not any(ch.isalpha() for ch in line):
                    continue
                for sig in ENV_RELEVANT:
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
        return findings
    return findings


def walk_paths(paths: list[Path], quiet: bool) -> list[Finding]:
    all_findings: list[Finding] = []
    for p in paths:
        if not p.exists():
            if not quiet:
                print(f"skip (missing): {p}", file=sys.stderr)
            continue
        if p.is_file():
            if is_target(p):
                all_findings.extend(scan_file(p, p.parent))
            continue
        # Directory traversal.
        for dirpath, dirnames, filenames in os.walk(p):
            dirnames[:] = [d for d in dirnames if d not in sigs.SKIP_DIR_NAMES]
            for fname in filenames:
                full = Path(dirpath) / fname
                if not is_target(full):
                    continue
                try:
                    all_findings.extend(scan_file(full, p))
                except Exception as e:  # noqa: BLE001
                    if not quiet:
                        print(f"error scanning {full}: {e}", file=sys.stderr)
    return all_findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Scan environment / config files for AI provider references and exposed keys.",
    )
    p.add_argument("paths", nargs="+", help="One or more files or directories to scan.")
    p.add_argument("--out", default="scan-output/", help="Output directory.")
    p.add_argument("--quiet", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    ns = parse_args(argv)
    paths = [Path(p).resolve() for p in ns.paths]
    out_dir = Path(ns.out).resolve()

    findings = walk_paths(paths, quiet=ns.quiet)
    assets = assets_from_findings(findings, discovery_source="env_scan")

    write_findings_json(out_dir, findings)
    write_assets_csv(out_dir, assets)
    write_assets_json(out_dir, assets)

    print(f"scanned: {len(paths)} target(s)")
    print(f"findings: {len(findings)}")
    print(f"inferred assets: {len(assets)}")
    print(f"outputs in: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
