#!/usr/bin/env python3
"""Report suspicious prose reuse between lesson articles.

This is an editorial review aid, not a plagiarism detector. It ignores headings,
tables, code fences, links, and short boilerplate, then compares normalized prose
using exact long paragraphs and 12-word shingles. A reported pair must be read by
an editor: shared domain terms are legitimate, copied explanations are not.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path


def prose_paragraphs(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if paragraph.startswith(("#", "|", "Sources:", "- [")):
            continue
        normalized = " ".join(re.findall(r"[a-z0-9]+", paragraph.lower()))
        if len(normalized.split()) >= 35:
            paragraphs.append(normalized)
    return paragraphs


def shingles(paragraphs: list[str], width: int = 12) -> set[str]:
    tokens = " ".join(paragraphs).split()
    return {" ".join(tokens[index:index + width]) for index in range(len(tokens) - width + 1)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path, help="lesson files or directories")
    parser.add_argument("--fail-on-findings", action="store_true")
    parser.add_argument("--minimum-shared-shingles", type=int, default=8)
    args = parser.parse_args()

    files = sorted(
        path for item in args.paths
        for path in ([item] if item.is_file() else item.glob("[0-9][0-9]-*.md"))
    )
    bodies = {path: prose_paragraphs(path) for path in files}
    paragraph_index: dict[str, list[Path]] = defaultdict(list)
    for path, paragraphs in bodies.items():
        for paragraph in set(paragraphs):
            paragraph_index[hashlib.sha256(paragraph.encode()).hexdigest()].append(path)

    findings: list[str] = []
    for paths in paragraph_index.values():
        if len(paths) > 1:
            findings.append("reused long paragraph: " + ", ".join(map(str, paths)))

    fingerprints = {path: shingles(paragraphs) for path, paragraphs in bodies.items()}
    for left, right in combinations(files, 2):
        shared = fingerprints[left] & fingerprints[right]
        if len(shared) >= args.minimum_shared_shingles:
            findings.append(f"{left} <> {right}: {len(shared)} shared 12-word shingles")

    if findings:
        print("Suspicious lesson overlap; inspect and rewrite shared explanations:")
        print("\n".join(findings))
        return 1 if args.fail_on_findings else 0
    print(f"No suspicious long-paragraph or 12-word-shingle overlap across {len(files)} lessons.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
