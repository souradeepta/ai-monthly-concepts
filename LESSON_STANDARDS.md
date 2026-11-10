# Lesson standards

This document is the concise authoring and review contract for monthly articles. `AGENTS.md` remains the repository instruction source; this file makes the acceptance criteria easy to apply to each article.

## Article and month requirements

- A month has 20 separate article files named `01-<slug>.md` through `20-<slug>.md`. README entries and concept maps do not count as articles.
- Each article targets at least 2,400 substantive, topic-specific words. Examples, references, headings, and repeated boilerplate do not substitute for explanation.
- A monthly README links existing articles. Missing work is labeled `planned`; a month is complete only when all 20 lessons meet this standard.

## Evidence and claims

- Prefer primary sources: papers, official documentation, technical posts, benchmarks, and incident reports. Secondary sources may add context but cannot be the only evidence.
- Read the source for the lesson's specific concept. Link to it rather than reproducing its text.
- Separate dated release or report facts from engineering inference. Vendor measurements are claims made by that publisher unless independently verified.
- Do not invent developments. Explain the historical baseline, what the source changed, and the limits of what its evidence establishes.
- Include a claim ledger with columns `Claim`, `Source`, and `Fact or inference`.

## Required teaching content

Every lesson explains its prerequisites and teaches the concept for a CS student or SDE2 audience. Define jargon at first use. Cover historical baseline, current processing and architecture impact, realistic applications and constraints, trade-offs, failure modes, and operational consequences.

Include these sections (titles may be adapted to the topic):

1. Concept, status, and dated sources.
2. In one sentence; background; what changed and why; architecture impact; applications and constraints; mental model.
3. What changed this month; engineering consequence; limits and failure modes.
4. At least two topic-specific, colored Mermaid diagrams: one component/data-flow view and one sequence, state, or failure-flow view.
5. A 15–30 minute exercise, a low-cost runnable example, and numbered local implementation steps.
6. Interview questions and answers, glossary, references, and claim ledger.

## Quality and verification

- Examples must be runnable with stated dependencies and must demonstrate the lesson's concept. State clearly what a toy example does not prove.
- Make diagrams, examples, and explanations specific to the article. Do not reuse prose, generic appendices, diagrams, or code across lessons.
- Separate capability claims from reliability and safety claims.
- Run `python3 scripts/validate_lessons.py <lesson> --run-python` and `git diff --check` for a lesson mechanics pass. Review facts and substantive quality separately; mechanical validation is not approval.
- Before treating a month as review-complete or pushing it as complete, run `python3 scripts/audit_lesson_similarity.py <month> --fail-on-findings`. Findings require rewriting or review, not waiver.
