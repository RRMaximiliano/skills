#!/usr/bin/env python3
"""Static Stata project audit for DIME-style reproducibility checks.

This script is intentionally conservative: it finds review leads, not proof of
incorrectness. Use it when Stata is unavailable or before a manual code review.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


@dataclass
class Finding:
    severity: str
    rule: str
    path: str
    line: int
    message: str
    fix: str


def iter_do_files(root: Path) -> Iterable[Path]:
    ignored = {".git", "__pycache__", ".venv", "venv"}
    for path in root.rglob("*.do"):
        if any(part in ignored for part in path.parts):
            continue
        yield path


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def strip_stata_comment(line: str) -> str:
    text = line.strip()
    if text.startswith("*"):
        return ""
    if text.startswith("//"):
        return ""
    return re.sub(r"//.*$", "", line)


def normalized(line: str) -> str:
    return strip_stata_comment(line).strip().lower()


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def add(
    findings: list[Finding],
    severity: str,
    rule: str,
    path: Path,
    root: Path,
    line: int,
    message: str,
    fix: str,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            rule=rule,
            path=rel(path, root),
            line=line,
            message=message,
            fix=fix,
        )
    )


def has_nearby_check(lines: list[str], index: int, window: int = 12) -> bool:
    start = max(0, index - window)
    nearby = "\n".join(normalized(line) for line in lines[start:index])
    return any(token in nearby for token in ("isid ", "assert ", "iesave "))


def audit_file(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    lines = read_lines(path)

    for i, line in enumerate(lines, start=1):
        text = normalized(line)
        if not text:
            continue

        if re.search(r"\bmerge\s+m:m\b", text):
            add(
                findings,
                "P0",
                "merge-m-to-m",
                path,
                root,
                i,
                "`merge m:m` can duplicate or drop relationships silently.",
                "Replace with 1:1, 1:m, or m:1 after proving uniqueness on each side.",
            )

        if re.search(r"\bduplicates\s+drop\b.*,\s*force\b", text):
            add(
                findings,
                "P1",
                "duplicates-drop-force",
                path,
                root,
                i,
                "`duplicates drop, force` removes records without documenting resolution.",
                "Use `ieduplicates`/`iecompdup` or document duplicate review before dropping.",
            )

        if re.search(r"\bappend\b.*,\s*force\b", text):
            add(
                findings,
                "P1",
                "append-force",
                path,
                root,
                i,
                "`append, force` can hide type or label incompatibilities.",
                "Harmonize variable types and labels before appending; keep source indicators.",
            )

        if re.search(r"\bcd\s+([\"']?)(/users/|[a-z]:\\)", text):
            add(
                findings,
                "P2",
                "hardcoded-cd",
                path,
                root,
                i,
                "Working directory is hardcoded to a machine-specific path.",
                "Move the path to a single project-root setup block or master do-file.",
            )

        if re.search(r"([\"'])(/users/|[a-z]:\\)", text):
            add(
                findings,
                "P2",
                "hardcoded-user-path",
                path,
                root,
                i,
                "Machine-specific user path appears in code.",
                "Use project-root globals/macros and relative project folders.",
            )

        if re.search(r"^save\s+", text) and "iesave" not in text:
            if not has_nearby_check(lines, i - 1):
                add(
                    findings,
                    "P2",
                    "save-without-nearby-id-check",
                    path,
                    root,
                    i,
                    "`save` appears without a nearby `isid`, `assert`, or `iesave` check.",
                    "Check unique IDs and key invariants before saving important datasets.",
                )

        prior_context = "\n".join(normalized(x) for x in lines[max(0, i - 8): i - 1])
        if re.search(r"\bdrop\s+if\b", text) and not re.search(r"\bcount\s+if\b", prior_context):
            add(
                findings,
                "P3",
                "drop-without-nearby-count",
                path,
                root,
                i,
                "`drop if` appears without a nearby count documenting affected rows.",
                "Count and justify dropped observations before dropping them.",
            )

    return findings


def audit_project(root: Path) -> tuple[list[Finding], dict[str, object]]:
    do_files = sorted(iter_do_files(root))
    findings: list[Finding] = []
    all_text = []

    for path in do_files:
        lines = read_lines(path)
        all_text.extend(normalized(line) for line in lines)
        findings.extend(audit_file(path, root))

    text_blob = "\n".join(all_text)
    master_candidates = [
        path
        for path in do_files
        if re.search(r"(master|main|run).*\.do$", path.name, flags=re.IGNORECASE)
    ]

    if do_files and not master_candidates:
        add(
            findings,
            "P2",
            "missing-master-do",
            root / ".",
            root,
            0,
            "No obvious master/main/run do-file found.",
            "Add or document a single entry-point script that runs the workflow.",
        )

    has_version_setup = re.search(r"^version\s+\d+", text_blob, flags=re.MULTILINE)
    if do_files and "ieboilstart" not in text_blob and not has_version_setup:
        add(
            findings,
            "P2",
            "missing-version-setup",
            root / ".",
            root,
            0,
            "No `ieboilstart` or explicit Stata `version` setup found.",
            "Set reproducibility settings in the master do-file, preferably with `ieboilstart`.",
        )

    if do_files and "which ietoolkit" not in text_blob and "ssc install ietoolkit" not in text_blob:
        add(
            findings,
            "P2",
            "missing-ietoolkit-setup",
            root / ".",
            root,
            0,
            "No visible `ietoolkit` dependency setup found.",
            "Install, bundle, or expose `ietoolkit` before using DIME commands.",
        )

    summary = {
        "root": str(root),
        "do_files": len(do_files),
        "master_candidates": [rel(path, root) for path in master_candidates],
        "findings": len(findings),
    }
    findings.sort(key=lambda item: (SEVERITY_ORDER[item.severity], item.path, item.line, item.rule))
    return findings, summary


def print_text(findings: list[Finding], summary: dict[str, object]) -> None:
    print("Static Stata audit")
    print(f"Root: {summary['root']}")
    print(f"Do-files scanned: {summary['do_files']}")
    masters = summary["master_candidates"]
    if masters:
        print("Master candidates: " + ", ".join(masters))
    else:
        print("Master candidates: none found")
    print(f"Findings: {summary['findings']}")
    print()

    if not findings:
        print("No static findings. This does not prove the workflow is DIME-ready.")
        return

    for item in findings:
        location = item.path if item.line == 0 else f"{item.path}:{item.line}"
        print(f"{item.severity} [{item.rule}] {location}")
        print(f"  Issue: {item.message}")
        print(f"  Fix: {item.fix}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Static audit for Stata research projects.")
    parser.add_argument("root", nargs="?", default=".", help="Project root to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    findings, summary = audit_project(root)

    if args.json:
        print(json.dumps({"summary": summary, "findings": [asdict(item) for item in findings]}, indent=2))
    else:
        print_text(findings, summary)

    return 1 if any(item.severity in {"P0", "P1"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
