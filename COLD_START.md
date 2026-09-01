# Cold-start instructions

Use this checklist when opening a new session in the repository.

1. Confirm the working directory with `pwd` and inspect `git status --short` without changing unrelated work.
2. Read `AGENTS.md`, `MEMORY.md`, `TODO.md`, and the relevant month README.
3. Identify the next unchecked article with `rg -n 'July|\[ \]' TODO.md` and inspect that lesson or confirm it is absent.
4. Check the concept map and direct sources before drafting. Browse only to verify a clear factual gap.
5. Edit one target file at a time with `apply_patch`; preserve existing user changes.
6. Run `python3 scripts/validate_lessons.py <lesson> --run-python`, `wc -w`, and `git diff --check`.
7. Update the matching TODO row and README link/status. Missing lessons stay `planned`.
8. Keep console output summarized. Never claim substantive review or monthly completion from mechanical validation alone.
9. Before a monthly push, run `python3 scripts/audit_lesson_similarity.py months/2026-07 --fail-on-findings`; rewrite any findings.
10. Commit only the requested completed batch, then push when authorized. Leave review findings as explicit follow-up work.

## Scope guard

The active user priority overrides parked work. Do not resume May, rebuild existing articles, or review all months while July expansion is active unless the user changes the priority.
