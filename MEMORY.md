# Local memory

## User preferences

- Be concise; optimize for low token use and free tools.
- Conserve chat and workflow tokens, never by reducing the quality or useful depth of output files.
- Git read-only commands (`status`, `diff`, `log`, `show`) and `git push` are authorized for this repository.
- Continue article production until all January–August 2026 articles are complete; do not stop after partial batches.
- Workflow override: push completed article drafts first; perform substantive review as a later follow-up pass to maximize progress under limited usage.
- Default routing: Luna for easy bounded work; Terra for review; override only for quality.
- Audience: CS student and SDE2.
- Lessons should use multiple detailed diagrams, practical code, local implementation steps, explained prerequisites, interview Q&A, glossary, references, and a claim ledger.
- Every lesson/article needs historical background, what changed, impact on current processing/architecture, and real-world applications with constraints.
- Every individual article must be at least 2,400 substantive words; generic template padding is not acceptable.
- Current user-directed sequencing: expand April–June draft coverage month by month now; then return to July/August missing-file coverage. Defer strict review and approval until after the expansion pass. Do not mislabel drafts as complete.
- Current override: park the May expansion objective and prioritize creating and expanding July 2026 articles. Resume May only after the user redirects work back to it.
- For the active August checklist, continue directly from the next unchecked article after each completed mechanics pass; do not request repeated approval. Keep chat and console reporting to one concise completed-work line.
- Suppress raw console output by default. Run checks silently and report only concise factual summaries (completed file, word count, pass/fail, and blocker when applicable).

## Project state

- Repository is public: `souradeepta/ai-monthly-concepts`.
- August 2026 has four lessons: evaluations, agent memory, late interaction retrieval, and agent controls.
- Use first-party sources; source facts must be distinguishable from inference.
- Hard rule: every individual lesson is at least 2,400 substantive, topic-specific words. Repeated template appendices do not count as quality.
- Local uncommitted batches exist for January, February, and March. Do not commit them until they pass both mechanical and Terra substantive review.
- A January overlap audit found cloned long prose in drafts 09–20. They remain unapproved and require source-specific rewrites; Function Calling (08) had its cloned block removed and passes the current similarity check with Structured Output (07).
- User-directed priority: create missing/stub articles in April–July first, then August 05–20; defer reconstruction of existing January–March drafts until that coverage work is complete.

## Low-token workflow

- Read only the target lesson, `AGENTS.md`, `TODO.md`, and linked sources.
- Reuse templates and source URLs. One drafting pass plus one focused review.
- Do not copy articles, use paid APIs, or run multi-agent research without need.
- After draft coverage is complete, expand each draft and run `python3 scripts/audit_lesson_similarity.py <reviewed lesson files or month> --fail-on-findings` before a monthly push.
- For each expanded lesson, use `python3 scripts/validate_lessons.py <lesson> --run-python` for the repeated structural, diagram, word-count, whitespace, and runnable-example check; use the similarity audit only for a reviewed batch.

## Execution discipline

- Do not create a persistent goal for open-ended article production. It can trigger automatic continuation loops that consume turns without editing files.
- Every continuation must begin with a concrete file action or verification command; never send status-only replies to an automatic continuation.
- If an automation loop appears, stop using that mechanism, state the cause once, then resume normal scoped edits. Do not repeat empty “still working” updates.

## Workflow handoff memory

- Use `HANDOFF.md` for active article-production scope, sequence, and definition of done.
- Use `COLD_START.md` at the beginning of every new session; read memory, TODO, README, and the target lesson before editing.
- Apply tables when they materially clarify comparisons, state transitions, trade-offs, or decisions; avoid decorative tables.
- Keep July active until articles 01–20 pass mechanics and similarity checks; May remains parked.
- User allows a modest word-count shortfall when the lesson is substantively complete; still target 2,400 and retain required sections/checks.

## Tooling lesson: Claude-style Git isolation

- Claude Code’s documented parallel workflow uses Git worktrees, each with its own checkout and branch while sharing repository history and remote; subagents can be isolated the same way.
- Worktrees prevent concurrent file collisions but do not remove the need for write access to shared Git metadata. In this environment, `.git` is read-only by default, so staging and committing require elevated or persistent Git permission.
- If future runs need to push, check Git metadata permissions early and request the narrow `git add`/`git commit` elevation rather than treating the repository as broken.
