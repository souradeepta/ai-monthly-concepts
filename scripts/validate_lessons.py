#!/usr/bin/env python3
"""Fail when a lesson is missing required learning-system-design sections."""
from pathlib import Path
import re
import sys

REQUIRED = (
    "## In one sentence", "## Background", "## What changed",
    "## Impact on current processing", "## Real-world applications", "## Mental model", "## Engineering consequence",
    "## Build it locally", "## Interview Q&A", "## Glossary",
    "## References", "## Claim ledger",
)

def validate(path: Path) -> list[str]:
    text = path.read_text()
    issues = [h for h in REQUIRED if h not in text]
    if len(re.findall(r"\b\w+\b", text)) < 2_400:
        issues.append("2,400-word minimum")
    if text.count("```mermaid") < 2:
        issues.append("two Mermaid diagrams")
    if "```python" not in text:
        issues.append("runnable Python example")
    if not re.search(r"^\d+\. ", text, re.M):
        issues.append("numbered local steps")
    return issues

def main() -> int:
    months = sys.argv[1:] or [f"months/2026-{m:02d}" for m in range(1, 9)]
    bad = 0
    for month in map(Path, months):
        lessons = sorted(month.glob("[0-9][0-9]-*.md"))
        if len(lessons) != 20:
            print(f"{month}: expected 20 articles, found {len(lessons)}")
            bad += 1
        for lesson in lessons:
            if issues := validate(lesson):
                print(f"{lesson}: missing {', '.join(issues)}")
                bad += 1
    return bool(bad)

if __name__ == "__main__":
    raise SystemExit(main())
