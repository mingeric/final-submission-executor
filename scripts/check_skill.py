#!/usr/bin/env python3
"""Validate the structure and frontmatter of a final-submission-executor skill package.

Usage: python3 scripts/check_skill.py <root>
Exit code 0 means the package is structurally complete. This is a packaging
check, not a scientific validation.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "README_CN.md",
    "LICENSE",
    "requirements.txt",
    "references/01-execution-contract.md",
    "references/02-task-ledger-and-blockers.md",
    "references/03-scientific-computation-gates.md",
    "references/04-visual-qa-and-print-spec.md",
    "references/05-canonical-overwrite-and-sync.md",
    "references/06-final-acceptance.md",
    "scripts/check_skill.py",
    "scripts/validate_final_submission.py",
    "templates/TASK_LEDGER.tsv",
    "templates/CANONICAL_MANIFEST.tsv",
    "templates/FINAL_ACCEPTANCE.md",
    "tests/test_scripts.py",
    ".github/workflows/validate.yml",
]
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".tsv", ".cff", ".txt", ".json"}
# Built from parts so the checker does not flag its own source code.
SECRET_PARTS = [("/", "Users/"), ("/", "home/"), ("BEGIN ", "PRIVATE KEY"), ("gh", "p_")]
SECRET_PREFIX = "s" + "k-"


def frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def validate(root: Path) -> tuple[bool, list[str], list[str]]:
    checks: list[str] = []
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        path = root / rel
        if path.is_file() and path.stat().st_size > 0:
            checks.append(f"OK file {rel}")
        else:
            failures.append(f"MISSING or empty file {rel}")

    skill = root / "SKILL.md"
    if skill.is_file():
        fields = frontmatter(skill.read_text(encoding="utf-8"))
        if fields.get("name") == "final-submission-executor":
            checks.append("OK frontmatter name")
        else:
            failures.append("frontmatter name must be final-submission-executor")
        if len(fields.get("description", "")) >= 40:
            checks.append("OK frontmatter description")
        else:
            failures.append("frontmatter description is missing or too short")

    # No personal absolute paths or credentials in published package text.
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        markers = [left + right for left, right in SECRET_PARTS]
        for marker in markers:
            if marker in text:
                failures.append(f"unsafe literal {marker!r} in {path.relative_to(root)}")
        offset = 0
        while True:
            found = text.find(SECRET_PREFIX, offset)
            if found < 0:
                break
            tail = text[found + len(SECRET_PREFIX): found + len(SECRET_PREFIX) + 24]
            if len(tail) >= 20 and tail[:20].isalnum():
                failures.append(f"possible API key in {path.relative_to(root)}")
            offset = found + 1
    return not failures, checks, failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    ok, checks, failures = validate(root)
    for line in checks:
        print(line)
    for line in failures:
        print("FAIL", line, file=sys.stderr)
    print(f"check_skill: {'PASS' if ok else 'FAIL'} ({len(checks)} ok, {len(failures)} failed)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
