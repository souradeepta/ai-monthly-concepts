# AI Monthly Concepts

A compact, source-backed study repo for monthly AI concepts. It turns important AI changes into lessons a CS student or software engineer can use.

Follow the repository's [lesson standards](LESSON_STANDARDS.md) for article depth, sources, diagrams, exercises, and completion checks.

Answer the calibration questions in [`PROFILE.md`](PROFILE.md). The first monthly index is [`months/2026-08/README.md`](months/2026-08/README.md).
The completed September lessons are indexed in [`months/2026-09/README.md`](months/2026-09/README.md). October research and writing is underway in [`months/2026-10/README.md`](months/2026-10/README.md).
Use [`LEARNING_PATH.md`](LEARNING_PATH.md) for the recommended study order.
Build [`projects/secure-agent-lab`](projects/secure-agent-lab/README.md) after the August lessons to connect the concepts locally.
Use [`SOURCES.md`](SOURCES.md) to extend monthly research beyond ten concepts when distinct, high-impact developments warrant it.
See [`ARCHITECTURE_VISUALS.md`](ARCHITECTURE_VISUALS.md) for the system-design visual layer and local animation.
Read [`DISCLOSURES.md`](DISCLOSURES.md) for source attribution, AI-assistance, vendor-claim, external-service, and no-warranty disclosures. Repository licensing is described in [`LICENSE.md`](LICENSE.md); original code uses [`LICENSE-CODE.md`](LICENSE-CODE.md).

## Repository layout

```text
months/YYYY-MM/  one index plus short lessons
sources/         optional cached metadata only; never copied articles
scripts/         cheap, deterministic helpers (no paid API)
agents/          narrow role prompts
AGENTS.md        contribution rules
```

Run `python3 scripts/validate_lessons.py months/2026-06 --run-python` for the repeatable lesson structure and example check. Run `python3 scripts/audit_lesson_similarity.py months/2026-06 --fail-on-findings` as the later batch overlap check.

## Operating plan

1. **Collect (weekly, 20 min):** check the source feeds; record only current-month announcements, papers, docs, technical reports, or evaluations.
2. **Triage (10 min):** retain an item only if it creates a durable concept, changes engineering practice, or explains a larger change. Target **3–5 concepts/month**.
3. **Teach:** write 20 separate articles per month, each targeting at least 2,400 substantive words and following `LESSON_STANDARDS.md`.
4. **Verify (5 min):** every factual claim needs a direct source and date; label interpretations as inference.
5. **Review (monthly, 30 min):** mark each concept `durable`, `emerging`, or `watch`; add a five-question self-check.

## Free-tier / low-token rules

- Browse first-party feeds and official paper pages; use no paid news APIs.
- Store URLs, dates, and a 1–2 sentence note, not article copies.
- Read relevant excerpts before asking an AI to summarize.
- Use one focused prompt per lesson: `Explain <concept> for a software engineer; max 700 words; distinguish facts from inference.`
- Keep a claim ledger to prevent repeated research.

## Monthly definition of done

- 20 individual article files exist and are linked from the monthly README.
- Each lesson meets `LESSON_STANDARDS.md`; incomplete entries remain labeled planned.
- The month passes individual validation and similarity review before it is marked complete.
