# CONTENT TODO

Every `{{TODO:}}` placeholder currently in the repo, per AGENT-BRIEF.md §3.1.
Check with `grep -rn "{{TODO" --include="*.html" .` — nothing on this list may
ship live until it's answered and the placeholder is replaced.

## /local-favourites/ — closed out

All six placeholders answered and removed from both language versions:

- Ha Giang City hotel confirmed as **Discovery Hostel** (the folder name
  "rabithotel" didn't match what the photo's signage actually showed —
  went with the photo).
- **A Lành Camping** (Meo Vac) and **Thẩm Mã Retreat** (Yen Minh) spellings
  confirmed.
- Motorbike rental section rewritten: it's Matt's own fleet, not a third
  party. Real price table added (Wave 110cc 180k · Future 125cc 300k ·
  Winner 150cc 350k · XR 150cc 550k, VND/day).
- The shared "what to expect" paragraph rewritten properly (two short
  paragraphs — what's good, then the honest decor downside) instead of
  asking Matt to edit Claude's placeholder draft.

`grep -rn "{{TODO" --include="*.html" .` now returns nothing. Task 1 has no
outstanding content blockers — the only remaining item is whatever
`viec-1-go-quang-cao.md` would have specified for the ad-gap replacement
markup (see AGENT-BRIEF.md's Task 1 row), which was never supplied.

## /blog/ — closed out, zero open placeholders

All 8 Phase-1 articles are built from `blog/_template.html`, plus
`blog/index.html` (the hub page listing all 8) and a "Blog" nav link wired
into the header and footer of every EN page including `404.html`. The
breadcrumb and JSON-LD in every article point at `/blog/`, which now
resolves instead of 404ing.

`grep -rn "{{TODO" --include="*.html" .` returns nothing outside
`blog/_template.html` itself (a source file, never published).

| File | Section | Placeholder | Resolution |
|---|---|---|---|
| blog/ha-giang-loop-guide/index.html | "What does it cost?" | Daily self-drive budget | ✅ answered 2026-08-25: ~300k VND food, ~100k petrol, 500k–1M homestay/hotel |
| blog/ha-giang-loop-cost/index.html | "Self-drive costs" | Same daily budget | ✅ answered, same numbers, full table added |
| blog/best-time-to-visit-ha-giang/index.html | "September to November" | Flower-season name/window | ✅ answered: buckwheat (tam giác mạch) festival, every November |
| blog/ha-giang-loop-guide/index.html | "Common mistakes first-timers make" | 2-3 more real mistakes Matt sees | Matt couldn't answer this one — sentence softened to the one mistake already established (compressing the route into 2 days) rather than leaving a placeholder or inventing more |
| blog/ha-giang-loop-cost/index.html | "Costs people forget" | Where/how an independent traveller gets the border-area permit | Matt couldn't answer this one — softened to generic honest advice (ask at your hotel or a local police station) rather than asserting an unverified process |

`blog/ha-giang-market-days/index.html` and `blog/hanoi-to-ha-giang/index.html`
are both built from real data Matt supplied 2026-08-25 (the 8 cho lui rotating
markets with their zodiac-day cycles, and the three Hanoi–Ha Giang bus
operators + price) — no placeholders in either.
