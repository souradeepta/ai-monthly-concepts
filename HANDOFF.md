# Article-production handoff

## Active priority

Quality cleanup is proceeding month by month. January is the reference-clean month: all 20 lessons pass mechanics and the month-wide similarity audit. February is active next; lessons 02–20 have received three cleanup batches, while eight duplicated scaffold blocks remain. Do not mark February approved until its similarity audit passes.

## Current repository state

- January–August each contain 20 numbered article files.
- January lessons pass validation, runnable examples, whitespace checks, and similarity audit.
- February lesson 01 was rewritten around enterprise control-plane boundaries and passes its lesson checks.
- February lessons 02–20 pass individual validators and `git diff --check`; the February similarity audit still reports shared blocks.
- March has duplicated long prose across its lesson set and requires the same cleanup approach.
- May has one reported similarity pair; April, June, July, and August have several lessons below the 2,400-word target.
- `LICENSE.md`, `LICENSE-CODE.md`, and `DISCLOSURES.md` are present. Preserve existing user changes; do not reset or discard unrelated edits.

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

1. Continue February lessons 02–20 by replacing the remaining eight shared scaffold blocks with concept-specific prose.
2. Re-run every February validator and the month similarity audit; only then begin March.
3. Clean March’s duplicated long paragraphs, then resolve May’s remaining similarity pair.
4. Expand under-target lessons in April, June, July, and August to at least 2,400 substantive words, validating each lesson after editing.
5. Perform substantive source and quality review before any month is marked approved, committed, or pushed.

## Communication rules

Do not use persistent goals or unattended loops. Work in meaningful batches, suppress raw console output, and report factual outcomes: files or batch changed, checks passed/failed, remaining blocker, and next batch.

## Agent-review handoff

- Terra review completed for January–August. Priority findings: February and March need source-first rebuilds because similarity failures are systemic; May lessons 15–20 are stubs; several April, June, July, and August lessons need word-count, source, or status cleanup.
- Luna repairs verified in April (seven under-target lessons) and June (lessons 03–06). A May repair agent expanded several lessons but left 15–20 incomplete and the month audit failing. A March repair agent handled 04–18 but left residual similarity findings.
- February lessons have received multiple local and Luna rewrite batches. Validators pass, but the month similarity audit still reports broad near-duplicate prose; do not mark February complete.
- The orchestration runtime currently reports a one-subagent capacity. Completed agents must be explicitly closed to release slots; a fresh session may be required if the scheduler retains stale records. The repository has no setting that controls this limit.
- When agent capacity is available, run Terra read-only review first, then Luna repair on disjoint month paths. Agents must not commit or push; the main session integrates and validates their work.
