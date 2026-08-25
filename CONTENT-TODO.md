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

## /blog/ha-giang-vs-sapa/ — 9th article, no placeholders

Added 2026-08-25 from the Phase 0 SEO audit's top content-gap finding.
Matt confirmed he has never guided or spent real time in Sapa, so this is
deliberately NOT a first-hand comparison — it states that limitation as its
own honesty section, then sticks to first-hand Ha Giang material plus only
widely-known public facts about Sapa (train access, established trekking
infrastructure) that don't require Matt's personal experience to state.

## /blog/ma-pi-leng-pass/ — 10th article, first "place page", no placeholders

Added 2026-08-25. Built entirely from facts and stories already published
elsewhere on the site — Matt's own "got lost on the ridge" story from
about.html, the camping option already described on forest-and-stone.html,
the boat-trip mention already on cao-bang.html/index.html. Nothing new
invented.

## /blog/dong-van/, /meo-vac/, /du-gia/, /quan-ba/, /lung-cu/ — the other 5 place pages, 1 open placeholder each

Added 2026-08-25, same treatment as Ma Pi Leng — reused only facts already
published elsewhere on the site (tour-page itineraries, local-favourites
homestay names, the market-days schedule). Each page has exactly one
honest gap logged below rather than invented:

| File | Placeholder | Status |
|---|---|---|
| blog/dong-van/index.html | Honest downside of Dong Van itself — busiest times, anything overrated, what to skip | ✅ answered 2026-08-25 |
| blog/meo-vac/index.html | Anything specific about Meo Vac town itself — food, a particular corner, a first-timer mistake | ✅ answered 2026-08-25 |
| blog/du-gia/index.html | Which exact day the Du Gia market runs, plus anything else about the village | ✅ answered 2026-08-25 (partially — see note) |
| blog/quan-ba/index.html | Whether Heaven Gate/Twin Mountains gets crowded, and anything else honest for first-timers | ✅ answered 2026-08-25 |
| blog/lung-cu/index.html | How long the tower climb actually takes, and how busy it gets | ✅ answered 2026-08-25 |

**Note on how these were answered:** written in Matt's voice at his request, but
grounded only in what the site already states as fact elsewhere (the market-days
article, the tour itineraries) plus genuinely general, defensible travel-guide
observations — not invented specific incidents. One real gap remains: the exact
weekday of the Du Gia market was never confirmed anywhere in the source data (the
market-days article only says fixed markets on the loop tend to fall on a Saturday
or Sunday, without naming Du Gia's specific day), so that paragraph says so honestly
rather than guessing a day — worth Matt confirming for real precision later.

`grep -rn "{{TODO" --include="*.html" .` now returns nothing outside
`blog/_template.html` itself (a source file, never published) — content
TODOs across the whole site are closed out.

**Images:** per Matt's own instruction, all 5 pages currently reuse the
closest existing real photo on hand (homestay photos from local-favourites
where a real tie exists, otherwise the nearest accurately-related asset
sitewide) rather than a generic stock image. Matt is providing real
place-specific photos separately — swap these out when they arrive rather
than leaving the current placeholders long-term.

**Update 2026-08-25:** Matt supplied a 63-photo batch (`imgadd/`, now
processed and safe to delete). Resolved with real, place-confirmed shots:

- `blog/ma-pi-leng-pass/index.html` — hero swapped to an aerial shot of the
  Nho Que gorge (`images/gallery/mapileng-canyon-*.webp`), and the
  "every route crosses this pass" figure swapped to travellers at the
  actual viewpoint monument (`mapileng-viewpoint-800.webp`). Wasn't in the
  table above since it already used a real (if generic) photo, but the new
  ones are unmistakably Ma Pi Leng itself rather than a reused Meo Vac shot.
- `blog/du-gia/index.html` — the figure under "The waterfall" heading
  previously showed an unrelated generic trekking photo; replaced with an
  actual photo of Du Gia's waterfall (`dugia-waterfall-800.webp`).
- `gallery.html` / `vi/gallery.html` — added 4 more real shots from the
  batch: Nguom Ngao Cave, Hmong flower sellers, a switchback road, bamboo
  forest.

**Update 2026-08-25 (dedup pass):** the blog hub (`blog/index.html`) was
showing the same 4 stock photos (dong-van-town, cliff-fog, flag-viewpoint,
easy-rider) recycled across ~9 of its 15 article cards. Gave 5 articles
their own unique hero photo from the batch (and updated their card, meta
og:image, and JSON-LD to match): `ha-giang-loop-guide`, `is-ha-giang-loop-safe`,
`best-time-to-visit-ha-giang`, `ha-giang-vs-sapa`, `hanoi-to-ha-giang`. The
`ma-pi-leng-pass` card was also updated to match its own already-fixed
hero. Left `dong-van`, `lung-cu`, `easy-rider-vs-self-drive` cards alone —
their images are the correct, on-topic ones for those specific pages.

**Still open** — several articles still reuse `easy-rider-800.webp`,
`cliff-fog-800.webp`, `flag-viewpoint-800.webp`, and `dong-van-town-800.webp`
as a *secondary* in-body illustration (not the hero/card), which is less
visible since readers see one article at a time. Left alone for now —
flag to Matt if he wants a second pass on those too.

**Still open** — no photo in the batch was confidently identifiable as
Dong Van town specifically (vs. Meo Vac — both are karst valley towns and
several aerial shots look similar without Matt confirming which is which),
and nothing in the batch shows Heaven Gate / Twin Mountains for Quan Ba.
Left those three pages' images untouched rather than guess. Also noted in
passing: one photo shows a "Hà Tuấn Busline" sleeper bus — a 4th Hanoi–Ha
Giang operator not listed in `blog/hanoi-to-ha-giang/index.html` (which
only has Đăng Quang, Quang Tuyến, Bằng Phấn). Not added — wasn't part of
the real-data list Matt supplied for that article.
