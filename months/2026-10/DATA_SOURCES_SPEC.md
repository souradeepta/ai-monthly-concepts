# October 2026 — data-sources and lesson implementation specification

Status: **initial queue only; October is not complete.**

Read the direct source before drafting its mapped lesson. Use the source to establish release-specific facts, then use general systems knowledge to explain interfaces, state, queues, permissions, tests, cost, latency, and failure modes. Label engineering recommendations as inference. Do not promote a candidate to a completed lesson merely because its source is interesting.

## First mapped lesson

| Queue | Filename | Direct source | Evidence to extract |
|---:|---|---|---|
| 01 | `01-model-generated-streamable-interfaces.md` | [GPT-6 and Intelligent UI for everyone — OpenAI — 2026-10-07](https://openai.com/index/gpt-6-for-everyone/) | OpenAI’s description of graphics, buttons, forms, charts, and interactive experiences; the native streamable component library; the compiler that processes UI as it is generated; the stated progressive rendering behavior; internal evaluation claims and their attribution; rollout and model-availability boundaries. |

## Overlap boundary for lesson 01

This lesson is about a model selecting and composing a typed interface representation while the response streams. It must not become a generic frontend tutorial, a general multimodal-model lesson, or a copy of August’s unified multimodal models. The differentiator is the response protocol and rendering pipeline: component vocabulary, validation, partial state, progressive updates, event permissions, and fallback when a generated interface is malformed or unsafe.

## Safe local example

Use a dependency-free Python simulator that validates a small component tree, streams valid patches, rejects unknown component types, and separates display data from event actions. Do not call a paid API or execute model-generated code. The exercise should make the difference between “the model emitted text” and “the model proposed a UI state transition” concrete.

## Acceptance gates

Every article must pass `scripts/validate_lessons.py <file> --run-python`, `git diff --check`, and the month-wide similarity audit before the month is marked complete. All 20 article files must exist and be linked by the monthly README.
