# Cold-start handoff

## Last confirmed remote state

- Branch: `main`; latest pushed standards commit: `8723ab5`.
- The remote contains curriculum maps, selected rich articles, visual assets, and the 2,400-word standard/validator.
- It intentionally does **not** contain the unreviewed January–March article batches.

## Local draft state — do not commit yet

- January: 20 untracked article files. They mechanically reach 2,400 words but Terra rejected them for a repeated generic operations appendix, templating leaks, and patch artifacts. Rewrite per topic before any commit.
- February: 20 untracked article files. Structural headings were corrected, but the review found them short/generic and weakly tied to February-specific primary evidence. Rewrite to 2,400 substantive words each.
- March: existing `01` and `02` plus 18 untracked drafts. Review found `03–20` short/generic and not adequately tied to March developments. Rewrite them; also ensure `01–02` meet the 2,400-word rule.
- April–August do not yet have 20 individual articles each; do not claim they do.

## Non-negotiable acceptance gate

1. Exactly 20 `01-*.md` … `20-*.md` article files per month.
2. Run `python3 scripts/validate_lessons.py months/2026-MM`.
3. Review for topic-specific depth, accurate/month-specific sources, no repeated filler, and no templating artifacts.
4. Update README to link all 20 articles.
5. Commit only the reviewed monthly batch; push only after the working tree is clean except unrelated drafts.

## Next safe order

1. Finish substantive January rewrite and Terra re-review.
2. Rewrite/review February, then March.
3. Create April–August in the same source-first, review-per-month workflow.

## User preferences

- Keep chat concise; preserve output-file quality.
- Audience is CS student/SDE2; treat articles as system-design posts.
- Luna for bounded drafting; Terra for review when available.
- Use primary sources plus reputable industry/publication context.
