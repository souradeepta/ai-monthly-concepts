# November 2026 — trustworthy agents in production and science

Status: **Planned — source queue prepared; lesson drafting has not started.**

November will continue the repository’s engineering focus on agents as stateful systems. The working theme is how evaluation, monitoring, storage, scientific workflows, and human oversight determine whether a capable model becomes a dependable product component. The month is not complete until 20 individual article files exist and pass the repository lesson contract.

## Completion contract

The month requires 20 individual `01-*.md` through `20-*.md` article files. Every finished article must contain at least 2,400 substantive words, a dated direct source, two colored Mermaid diagrams, a dependency-free runnable Python example, numbered local implementation steps, interview Q&A, glossary, references, and a fact/inference claim ledger. Planned entries do not count as articles.

## Initial source queue

| Candidate | Engineering concept | Direct source | Initial decision |
|---|---|---|---|
| nov-01 | Benchmarking everyday life-task assistance | [LifeVal — OpenAI — 2026-11-02](https://openai.com/index/lifeval/) | queued |
| nov-02 | Wet-lab data interpretation benchmarks | [BioBasicsBench — OpenAI — 2026-11-06](https://openai.com/index/biobasicsbench/) | queued |
| nov-03 | Autonomous Linux vulnerability patching | [A thousand fewer paths to root — OpenAI — 2026-11-04](https://openai.com/index/a-thousand-fewer-paths-to-root/) | queued |
| nov-04 | Layered monitoring for frontier model misalignment | [How we detect frontier model misalignment — OpenAI — 2026-10-29](https://openai.com/index/how-we-detect-frontier-model-misalignment/) | queued |
| nov-05 | Scaling Git for agent-generated changes | [Scaling Git at OpenAI — OpenAI Engineering — 2026-11-02](https://openai.com/news/engineering/scaling-git-at-openai/) | queued |
| nov-06 | Scientific understanding from model-assisted mathematics | [Working with academic communities — OpenAI — 2026-10-26](https://openai.com/index/working-with-academic-communities-to-build-scientific-understanding/) | queued |
| nov-07 | AI-assisted physical-world engineering | [Accelerating engineering for the physical world — OpenAI — 2026-11-03](https://openai.com/index/accelerating-engineering-for-the-physical-world/) | queued |
| nov-08 | Continual-learning retention and consolidation | [The sleep framework — Google Research — 2026-10-27](https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning/) | queued |
| nov-09 | Human definition of ambiguous evaluation criteria | [Agile Deliberation — Google Research — 2026-11-04](https://research.google/blog/agile-deliberation-how-ai-helps-humans-define-the-gray-areas/) | queued |
| nov-10 | Stateful enterprise-agent contracts | [CRM-Agent-Bench — arXiv:2610.32004](https://arxiv.org/abs/2610.32004) | queued |

The remaining candidates will be selected after checking overlap with October and the January–October lessons. Vendor measurements will be labeled as source claims rather than independent verification.

## Research rules

- Prefer November primary sources, official engineering posts, papers, benchmarks, and incident reports.
- Freeze a candidate only when the source describes a distinct processing, control-plane, evaluation, or operational mechanism.
- Keep release facts separate from engineering inference in every claim ledger.
- Use dependency-light local exercises and avoid private APIs or paid services.

## Lesson files

Lessons 01–20 are not yet drafted. Add each link here only after its article file exists; keep any unfinished entry marked `planned`.

## Required checks

```text
python3 scripts/validate_lessons.py months/2026-11/01-<slug>.md --run-python
git diff --check
python3 scripts/audit_lesson_similarity.py months/2026-11 --fail-on-findings
```
