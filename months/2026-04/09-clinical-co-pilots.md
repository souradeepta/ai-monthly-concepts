# Clinical co-pilots

Status: draft — expansion and review pending
Sources: [Google DeepMind — 2026-04-30](https://deepmind.google/blog/ai-co-clinician/)

## In one sentence

A clinical co-pilot can organize evidence and propose questions or documentation, but clinical authority, patient consent, escalation, and final decisions remain with accountable professionals and governed workflows.

## Draft lesson

High-stakes AI should be designed as assistance, not delegated judgment. A clinical workflow needs patient identity handling, consent, source provenance, uncertainty, a clear handoff, and an audit trail that fits the health system's controls. A model summary may be useful, but it is not a diagnosis, prescription, or authorization to alter care.

Google DeepMind's April 30 announcement describes AI co-clinician as a research initiative and reports a simulation study involving hypothetical telemedical encounters. This is not evidence of general clinical deployment safety. Engineering teams should separate retrospective benchmark results from prospective validation in the intended population and workflow.

Start with constrained tasks such as retrieval of approved clinical guidance or drafting a note for professional review. Require source citations, display missing evidence, and make a reviewer explicitly accept, edit, or reject a suggestion. Test wrong-patient context, stale guideline versions, conflicting sources, transcription errors, and a model output that appears certain despite insufficient evidence.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| Google DeepMind announced AI co-clinician research and describes simulations of telemedical encounters. | [Announcement](https://deepmind.google/blog/ai-co-clinician/) | Fact, vendor research claim |
| Professional review and prospective workflow validation are required design controls. | Systems-design reasoning | Inference |
