#!/usr/bin/env python3
"""
oauth_grants_to_inventory.py — Discover step.

Take an OAuth-grants export (Google Workspace, Microsoft 365, Slack, Atlassian,
GitHub, etc.) and produce AI Asset Register rows — one per AI app / vendor that
appears in the export.

Why this is its own script: every IdP ships its OAuth export with a different
schema. This script reads CSV with whatever columns it has and tries hard to
map them to the register format using a flexible column-alias table. You can
also pass --column-map to override.

Heuristics for "is this an AI app?":
  - app name / publisher / homepage matches the AI vendor list (configurable
    via --ai-vendors, defaults to a built-in list).
  - scope set includes a high-write OAuth scope on mail / drive / calendar /
    chat / ticketing / CRM (the H-002 hunt criteria).

The script is read-only. Even when run against a live export, it does not
write to any system except the output files.

Usage:
  python3 oauth_grants_to_inventory.py --in oauth_export.csv --out scan-output/oauth_assets.csv
  python3 oauth_grants_to_inventory.py --in m365_export.csv --column-map app=AppDisplayName,publisher=PublisherName,scopes=Permissions,users=Users
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SCRIPTS = _HERE.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lib.inventory import REGISTER_FIELDS, short_id  # noqa: E402


DEFAULT_AI_VENDORS: tuple[str, ...] = (
    "openai", "chatgpt",
    "anthropic", "claude",
    "google ai", "gemini", "bard",
    "microsoft copilot", "github copilot", "copilot",
    "perplexity",
    "cohere", "mistral", "groq", "together",
    "huggingface", "hugging face",
    "replicate", "runwayml", "stability",
    "writer", "jasper", "writesonic",
    "grammarly", "notion ai",
    "zapier", "n8n", "make", "workato",  # often host AI workflows
    "glean", "harvey", "hebbia",
    "otter", "fathom", "fireflies",
)


HIGH_WRITE_SCOPE_TOKENS: tuple[str, ...] = (
    # Google
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/chat.messages",
    # Microsoft Graph
    "Mail.Send", "Mail.ReadWrite", "Files.ReadWrite", "Files.ReadWrite.All",
    "Calendars.ReadWrite", "Chat.ReadWrite", "ChannelMessage.Send",
    "Sites.ReadWrite.All",
    # Slack
    "chat:write", "files:write", "channels:write",
    # GitHub
    "repo", "workflow", "write:packages",
    # Generic
    "write", "modify", "send", "delete",
)


COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "app": ("app", "application", "appdisplayname", "application_name", "name"),
    "publisher": ("publisher", "publishername", "vendor", "verified_publisher", "developer"),
    "scopes": ("scopes", "permissions", "oauthscopes", "scope", "delegated_permissions", "permission_set"),
    "users": ("users", "user_count", "usercount", "consenting_users", "consents"),
    "tenant": ("tenant", "tenant_id", "directoryid", "workspace"),
    "homepage": ("homepage", "publisherurl", "websiteurl"),
}


def normalize_header(h: str) -> str:
    return h.strip().lower().replace("-", "_").replace(" ", "_")


def find_column(headers: list[str], aliases: tuple[str, ...]) -> str | None:
    norm = {normalize_header(h): h for h in headers}
    for a in aliases:
        a_norm = normalize_header(a)
        if a_norm in norm:
            return norm[a_norm]
    return None


def parse_column_map(s: str | None) -> dict[str, str]:
    """Parse --column-map 'app=AppName,scopes=Perms' style."""
    if not s:
        return {}
    out: dict[str, str] = {}
    for piece in s.split(","):
        piece = piece.strip()
        if not piece:
            continue
        if "=" not in piece:
            raise SystemExit(f"--column-map entry missing '=': {piece}")
        k, v = piece.split("=", 1)
        out[k.strip().lower()] = v.strip()
    return out


def is_ai_app(app: str, publisher: str, vendor_terms: tuple[str, ...]) -> bool:
    blob = f"{app} {publisher}".lower()
    return any(term in blob for term in vendor_terms)


def has_high_write_scope(scopes: str) -> bool:
    s = scopes.lower()
    return any(tok.lower() in s for tok in HIGH_WRITE_SCOPE_TOKENS)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Convert an OAuth grants CSV export into AI Asset Register rows.",
    )
    p.add_argument("--in", dest="in_path", required=True, help="Input OAuth-grants CSV.")
    p.add_argument("--out", dest="out_path", required=True, help="Output CSV (Asset Register format).")
    p.add_argument(
        "--column-map",
        help="Override column mapping, e.g. 'app=AppDisplayName,scopes=Permissions,users=Users'.",
    )
    p.add_argument(
        "--ai-vendors",
        default=",".join(DEFAULT_AI_VENDORS),
        help="Comma-separated list of vendor name fragments treated as AI.",
    )
    p.add_argument(
        "--include-non-ai",
        action="store_true",
        help="Also emit rows for non-AI apps that hold high-write scopes (useful in shadow-AI sweeps).",
    )
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    ns = parse_args(argv)
    in_path = Path(ns.in_path).resolve()
    out_path = Path(ns.out_path).resolve()
    overrides = parse_column_map(ns.column_map)
    vendor_terms = tuple(v.strip().lower() for v in ns.ai_vendors.split(",") if v.strip())

    if not in_path.exists():
        print(f"error: input not found: {in_path}", file=sys.stderr)
        return 1

    today = _dt.date.today().isoformat()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            print("error: empty CSV (no header).", file=sys.stderr)
            return 1
        headers = list(reader.fieldnames)

        col = {
            key: overrides.get(key) or find_column(headers, aliases)
            for key, aliases in COLUMN_ALIASES.items()
        }
        if not col["app"]:
            print(
                f"error: could not find an 'app' column in headers {headers}. "
                f"Pass --column-map app=<your column>.",
                file=sys.stderr,
            )
            return 1

        out_rows: list[dict[str, str]] = []
        for row in reader:
            app = (row.get(col["app"]) or "").strip()
            if not app:
                continue
            publisher = (row.get(col["publisher"]) or "").strip() if col["publisher"] else ""
            scopes = (row.get(col["scopes"]) or "").strip() if col["scopes"] else ""
            users = (row.get(col["users"]) or "").strip() if col["users"] else ""
            tenant = (row.get(col["tenant"]) or "").strip() if col["tenant"] else ""
            homepage = (row.get(col["homepage"]) or "").strip() if col["homepage"] else ""

            ai = is_ai_app(app, publisher, vendor_terms)
            high_write = has_high_write_scope(scopes)
            if not ai and not (ns.include_non_ai and high_write):
                continue

            asset_class = "saas_llm" if ai else "embedded_copilot"
            name = app

            out_rows.append({
                "asset_id": short_id(name, asset_class),
                "name": name,
                "asset_class": asset_class,
                "vendor": publisher,
                "tenant": tenant,
                "owner": "",
                "business_use": "",
                "data_classification": "",
                "identity_context": "user",  # OAuth grants are user-context unless noted
                "can_read": "true",
                "can_write": "true" if high_write else "",
                "can_send": "true" if "send" in scopes.lower() else "",
                "can_publish": "",
                "can_deploy": "",
                "can_delete": "true" if "delete" in scopes.lower() else "",
                "can_approve": "",
                "can_modify_security_controls": "",
                "connectors": "",
                "oauth_scopes": scopes[:1000],
                "model": "",
                "api_key_location": "",
                "first_seen": today,
                "last_reviewed": today,
                "sanctioned": "",
                "notes": (
                    f"OAuth grant; users={users}; homepage={homepage}; "
                    f"ai_vendor_match={'yes' if ai else 'no'}; "
                    f"high_write_scope={'yes' if high_write else 'no'}"
                ).strip("; "),
            })

    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REGISTER_FIELDS)
        writer.writeheader()
        for r in out_rows:
            writer.writerow({k: r.get(k, "") for k in REGISTER_FIELDS})

    print(f"input: {in_path}")
    print(f"output: {out_path}")
    print(f"rows emitted: {len(out_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
