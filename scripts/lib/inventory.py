"""
Helpers for emitting AI Asset Register rows aligned to
templates/ai-asset-schema.json.

Scanners produce *findings* (per-line matches in source). This module groups
findings into *assets* and writes:
  - <out>/findings.json   raw findings, with file/line/snippet (REDACTED)
  - <out>/assets.csv      one row per inferred asset, register-aligned
  - <out>/assets.json     same data, JSON form
"""

from __future__ import annotations

import csv
import datetime as _dt
import hashlib
import json
import os
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


# Order must match templates/ai-asset-register.csv exactly.
REGISTER_FIELDS: tuple[str, ...] = (
    "asset_id",
    "name",
    "asset_class",
    "vendor",
    "tenant",
    "owner",
    "business_use",
    "data_classification",
    "identity_context",
    "can_read",
    "can_write",
    "can_send",
    "can_publish",
    "can_deploy",
    "can_delete",
    "can_approve",
    "can_modify_security_controls",
    "connectors",
    "oauth_scopes",
    "model",
    "api_key_location",
    "first_seen",
    "last_reviewed",
    "sanctioned",
    "notes",
)


@dataclass
class Finding:
    """A single source-level match. Never carries a key value."""

    file: str
    line: int
    signature: str
    asset_class: str
    snippet: str  # may contain "[REDACTED]" where a key was matched
    note: str = ""


@dataclass
class Asset:
    """An inferred AI asset row."""

    asset_id: str
    name: str
    asset_class: str
    vendor: str = ""
    tenant: str = ""
    owner: str = ""
    business_use: str = ""
    data_classification: str = ""
    identity_context: str = ""
    can_read: str = ""
    can_write: str = ""
    can_send: str = ""
    can_publish: str = ""
    can_deploy: str = ""
    can_delete: str = ""
    can_approve: str = ""
    can_modify_security_controls: str = ""
    connectors: str = ""
    oauth_scopes: str = ""
    model: str = ""
    api_key_location: str = ""
    first_seen: str = ""
    last_reviewed: str = ""
    sanctioned: str = ""
    notes: str = ""
    discovery_source: str = ""
    evidence_files: list[str] = field(default_factory=list)


def short_id(name: str, asset_class: str) -> str:
    """Stable, short asset_id: AI-<8-hex>."""
    h = hashlib.sha1(f"{asset_class}::{name}".encode("utf-8")).hexdigest()[:8]
    return f"AI-{h}"


def assets_from_findings(findings: Iterable[Finding], discovery_source: str) -> list[Asset]:
    """
    Group findings into assets keyed by (signature, asset_class).
    Each unique signature becomes one inferred asset; per-file evidence
    is preserved on the Asset for the analyst.
    """
    grouped: dict[tuple[str, str], list[Finding]] = defaultdict(list)
    for f in findings:
        grouped[(f.signature, f.asset_class)].append(f)

    today = _dt.date.today().isoformat()
    assets: list[Asset] = []
    for (sig, asset_class), items in sorted(grouped.items()):
        name = sig
        # Set api_key_location only when the signature is a key pattern.
        api_key_location = ""
        if any(item.note.lower().endswith("key") or "token" in item.note.lower() for item in items):
            api_key_location = "; ".join(sorted({f"{i.file}:{i.line}" for i in items}))[:1000]

        assets.append(
            Asset(
                asset_id=short_id(name, asset_class),
                name=name,
                asset_class=asset_class,
                first_seen=today,
                last_reviewed=today,
                sanctioned="",  # Define step decides
                notes=f"Auto-discovered by {discovery_source}; {len(items)} match(es) across {len({i.file for i in items})} file(s).",
                api_key_location=api_key_location,
                discovery_source=discovery_source,
                evidence_files=sorted({i.file for i in items}),
            )
        )
    return assets


def write_findings_json(out_dir: Path, findings: list[Finding]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "findings.json"
    with path.open("w", encoding="utf-8") as fh:
        json.dump([asdict(f) for f in findings], fh, indent=2, sort_keys=True)
    return path


def write_assets_csv(out_dir: Path, assets: list[Asset]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "assets.csv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REGISTER_FIELDS)
        writer.writeheader()
        for a in assets:
            row = {k: getattr(a, k, "") for k in REGISTER_FIELDS}
            writer.writerow(row)
    return path


def write_assets_json(out_dir: Path, assets: list[Asset]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "assets.json"
    with path.open("w", encoding="utf-8") as fh:
        json.dump(
            [
                {
                    **{k: getattr(a, k, "") for k in REGISTER_FIELDS},
                    "discovery_source": a.discovery_source,
                    "evidence_files": a.evidence_files,
                }
                for a in assets
            ],
            fh,
            indent=2,
            sort_keys=True,
        )
    return path


def make_relative(path: str, root: str) -> str:
    """Return a repo-relative path string when possible; absolute otherwise."""
    try:
        return os.path.relpath(path, root)
    except ValueError:
        return path
