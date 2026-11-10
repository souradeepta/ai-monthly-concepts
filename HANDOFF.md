# Article-production handoff

## Active priority

October 2026 draft production is complete. All 20 lessons exist from October primary sources and pass individual validators, runnable examples, whitespace checks, and the month-wide similarity audit; substantive fact-check and quality review remain. November has a source queue and README but no lesson files.

## Current repository state

- January–August each contain 20 numbered article files.
- January lessons pass validation, runnable examples, whitespace checks, and similarity audit.
- February lessons 01–13 complete mechanics rewrite, source pass, and substantive review; month-wide similarity audit and lessons 14–20 remain.
- February lesson 14 has been source-first rewritten around verifier-guided mathematical reasoning; it passes its individual validator, runnable example, and `git diff --check`. Lessons 15–20 remain generic scaffold rewrites.
- March has duplicated long prose across its lesson set and requires the same cleanup approach.
- May has one reported similarity pair; April, June, July, and August have several lessons below the 2,400-word target.
- `LICENSE.md`, `LICENSE-CODE.md`, and `DISCLOSURES.md` are present. Preserve existing user changes; do not reset or discard unrelated edits.
- September 01–20 pass the individual validator with runnable examples, the 20-lesson similarity audit, and `git diff --check`; all are above the substantive word target and include topic-specific quantitative reasoning. September coverage is complete.
- October 01–20 pass the individual validator with runnable examples, `git diff --check`, and the month-wide similarity audit; substantive review remains incomplete.

## Definition of done

For each article:

- Use the monthly concept and linked primary/context sources; label facts versus engineering inferences.
- Include the required lesson sections, two colored Mermaid diagrams, a runnable low-cost Python example, numbered steps, interview Q&A, glossary, references, and claim ledger.
- Reach at least 2,400 substantive words, pass `scripts/validate_lessons.py <lesson> --run-python`, and pass `git diff --check`.
- Keep explanations topic-specific; do not reuse boilerplate paragraphs, generic appendices, diagrams, or code across lessons.
- Run `python3 scripts/audit_lesson_similarity.py <month> --fail-on-findings` before considering a month review-complete.
- Update `TODO.md` only with factual milestones; substantive approval remains separate from mechanics.

## Working loop

1. Read `MEMORY.md`, `TODO.md`, the target lesson, and its monthly README.
2. Select a concrete batch, usually one duplicated block across a month or a small set of short lessons.
3. Edit with `apply_patch`; preserve unrelated dirty-worktree changes.
4. Run affected validators with `--run-python`, `git diff --check`, and the month similarity audit.
5. Record the batch result, remaining blocker count, and next batch in the final handoff.

## Next sequence

1. Run a substantive fact-check and quality review across October 01–20; keep the month open until findings are repaired.
2. Preserve the completed September review record and source ledger.
3. Begin November source triage from `months/2026-11/README.md` after October review is complete.
4. Return to February lesson 15, then continue March similarity cleanup, May stubs, and under-target April/June–August lessons.

## Communication rules

Do not use persistent goals or unattended loops. Work in meaningful batches, suppress raw console output, and report factual outcomes: files or batch changed, checks passed/failed, remaining blocker, and next batch.

## Agent-review handoff

- Terra review completed for January–August. Priority findings: February and March need source-first rebuilds because similarity failures are systemic; May lessons 15–20 are stubs; several April, June, July, and August lessons need word-count, source, or status cleanup.
- Luna repairs verified in April (seven under-target lessons) and June (lessons 03–06). A May repair agent expanded several lessons but left 15–20 incomplete and the month audit failing. A March repair agent handled 04–18 but left residual similarity findings.
- February lessons have received multiple local and Luna rewrite batches. Validators pass, but the month similarity audit still reports broad near-duplicate prose; do not mark February complete.
- The orchestration runtime currently reports a one-subagent capacity. Completed agents must be explicitly closed to release slots; a fresh session may be required if the scheduler retains stale records. The repository has no setting that controls this limit.
- When agent capacity is available, run Terra read-only review first, then Luna repair on disjoint month paths. Agents must not commit or push; the main session integrates and validates their work.
