#!/usr/bin/env python3
"""Check lesson structure; optionally execute each first fenced Python example."""
import argparse
from pathlib import Path
import re
import subprocess
import sys
import tempfile

REQUIRED = (
    "## In one sentence", "## Background", "## What changed",
    "## Impact on current processing", "## Real-world applications", "## Mental model", "## Engineering consequence",
    "## Build it locally", "## Interview Q&A", "## Glossary",
    "## References", "## Claim ledger",
)

def validate(path: Path, run_python: bool = False) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues = [h for h in REQUIRED if h not in text]
    if len(re.findall(r"\b\w+\b", text)) < 2_400:
        issues.append("2,400-word minimum")
    if text.count("```mermaid") < 2:
        issues.append("two Mermaid diagrams")
    if "```python" not in text:
        issues.append("runnable Python example")
    if not re.search(r"^\d+\. ", text, re.M):
        issues.append("numbered local steps")
    if re.search(r"[ \t]+$", text, re.M):
        issues.append("trailing whitespace")
    if run_python and "```python" in text:
        match = re.search(r"^```python\s*$\n(.*?)^```\s*$", text, re.M | re.S)
        if not match:
            issues.append("extractable Python example")
        else:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as example:
                example.write(match.group(1))
                example_path = Path(example.name)
            try:
                result = subprocess.run(
                    [sys.executable, str(example_path)],
                    text=True,
                    capture_output=True,
                    timeout=15,
                )
                if result.returncode:
                    message = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "non-zero exit"
                    issues.append(f"runnable Python example ({message})")
            except subprocess.TimeoutExpired:
                issues.append("runnable Python example (timed out)")
            finally:
                example_path.unlink(missing_ok=True)
    return issues


def collect_lessons(items: list[Path]) -> list[Path]:
    lessons: list[Path] = []
    for item in items:
        if item.is_file():
            lessons.append(item)
        elif item.is_dir():
            lessons.extend(sorted(item.glob("[0-9][0-9]-*.md")))
        else:
            print(f"{item}: path not found", file=sys.stderr)
    return lessons

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="lesson files or month directories")
    parser.add_argument("--run-python", action="store_true", help="run the first fenced Python example in each lesson")
    args = parser.parse_args()
    items = args.paths or [Path(f"months/2026-{m:02d}") for m in range(1, 9)]
    bad = 0
    for item in items:
        if item.is_dir() and len(list(item.glob("[0-9][0-9]-*.md"))) != 20:
            print(f"{item}: expected 20 articles, found {len(list(item.glob('[0-9][0-9]-*.md')))}")
            bad += 1
    for lesson in collect_lessons(items):
        if issues := validate(lesson, run_python=args.run_python):
            print(f"{lesson}: missing {', '.join(issues)}")
            bad += 1
    return bool(bad)

if __name__ == "__main__":
    raise SystemExit(main())
