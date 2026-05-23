#!/usr/bin/env python3
"""Repository integrity reporting for Phase 1 canonicalization."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPECTED_DOCS: tuple[str, ...] = (
    "SYSTEM_MAP.md",
    "ARCHITECTURE.md",
    "ROADMAP.md",
    "archive/REPOSITORY_MAP.md",
    "docs/network/FUNDING_TRACE.md",
    "public/status/PROJECT_STATUS.md",
    "public/metrics/system_metrics.json",
)

SIBLING_REPOS_TO_CHECK: tuple[str, ...] = (
    "Quantum-pi-forge",
    "Quantum-pi-forge_backup",
    "OINIO_Forge",
    "oinio-forge",
    "onio-swarm",
    "sovereign-root",
    "offline-dev-guardian",
    "pi-forge-quantum-genesis",
)


@dataclass(frozen=True)
class RepositoryEntry:
    name: str
    path: str
    exists: bool
    has_git: bool
    classification: str


@dataclass(frozen=True)
class MissingDocument:
    path: str
    required: bool


@dataclass(frozen=True)
class IntegrityReport:
    generated_at_utc: str
    canonical_root: str
    duplicate_roots: list[RepositoryEntry]
    orphan_backups: list[RepositoryEntry]
    repositories_detected: list[RepositoryEntry]
    missing_documentation: list[MissingDocument]
    checks: dict[str, bool]


def classify_repo(name: str) -> str:
    lowered = name.lower()
    if name == "Quantum-pi-forge":
        return "canonical"
    if "backup" in lowered:
        return "backup"
    if "archive" in lowered:
        return "archive"
    return "sibling"


def discover_repositories(canonical_root: Path) -> list[RepositoryEntry]:
    forge_parent = canonical_root.parent
    entries: list[RepositoryEntry] = []

    for repo_name in SIBLING_REPOS_TO_CHECK:
        repo_path = forge_parent / repo_name
        exists = repo_path.exists()
        has_git = (repo_path / ".git").exists() if exists else False
        entry = RepositoryEntry(
            name=repo_name,
            path=str(repo_path),
            exists=exists,
            has_git=has_git,
            classification=classify_repo(repo_name),
        )
        entries.append(entry)

    return entries


def find_duplicate_roots(repositories: list[RepositoryEntry]) -> list[RepositoryEntry]:
    duplicates: list[RepositoryEntry] = []
    for repo in repositories:
        if repo.exists and repo.name != "Quantum-pi-forge":
            if "forge" in repo.name.lower() or "oinio" in repo.name.lower():
                duplicates.append(repo)
    return duplicates


def find_orphan_backups(repositories: list[RepositoryEntry]) -> list[RepositoryEntry]:
    orphans: list[RepositoryEntry] = []
    for repo in repositories:
        if repo.exists and "backup" in repo.name.lower():
            if not repo.has_git:
                orphans.append(repo)
    return orphans


def find_missing_docs(canonical_root: Path) -> list[MissingDocument]:
    missing: list[MissingDocument] = []
    for relative_path in EXPECTED_DOCS:
        if not (canonical_root / relative_path).exists():
            missing.append(MissingDocument(path=relative_path, required=True))
    return missing


def generate_report(canonical_root: Path) -> IntegrityReport:
    repositories = discover_repositories(canonical_root)
    duplicate_roots = find_duplicate_roots(repositories)
    orphan_backups = find_orphan_backups(repositories)
    missing_docs = find_missing_docs(canonical_root)

    checks: dict[str, bool] = {
        "canonical_root_exists": canonical_root.exists(),
        "canonical_root_has_git": (canonical_root / ".git").exists(),
        "required_docs_complete": len(missing_docs) == 0,
        "orphan_backups_detected": len(orphan_backups) > 0,
        "duplicate_roots_detected": len(duplicate_roots) > 0,
    }

    return IntegrityReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        canonical_root=str(canonical_root),
        duplicate_roots=duplicate_roots,
        orphan_backups=orphan_backups,
        repositories_detected=repositories,
        missing_documentation=missing_docs,
        checks=checks,
    )


def to_json_dict(report: IntegrityReport) -> dict[str, Any]:
    return {
        "generated_at_utc": report.generated_at_utc,
        "canonical_root": report.canonical_root,
        "duplicate_roots": [asdict(entry) for entry in report.duplicate_roots],
        "orphan_backups": [asdict(entry) for entry in report.orphan_backups],
        "repositories_detected": [asdict(entry) for entry in report.repositories_detected],
        "missing_documentation": [asdict(entry) for entry in report.missing_documentation],
        "checks": report.checks,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate deterministic repository integrity report."
    )
    parser.add_argument(
        "--canonical-root",
        default=".",
        help="Path to canonical repository root (default: current directory).",
    )
    parser.add_argument(
        "--output",
        default="public/metrics/integrity_report.json",
        help="Output path for JSON report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    canonical_root = Path(args.canonical_root).resolve()
    output_path = Path(args.output).resolve()

    report = generate_report(canonical_root)
    payload = to_json_dict(report)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())