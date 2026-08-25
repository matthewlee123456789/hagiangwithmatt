# AGENT BRIEF — hagiangwithmatt.com

> **CÁCH DÙNG (đọc phần này rồi bỏ qua, phần còn lại dành cho AI):**
> Đặt file này ở thư mục gốc của dự án. Trong IDE, thêm nó vào context vĩnh viễn
> — Antigravity/Cursor: `.agent/rules/` hoặc `.cursorrules`; Windsurf: `.windsurfrules`;
> Claude Code: đổi tên thành `CLAUDE.md`. Sau đó dùng các prompt trong file
> `KICKOFF-PROMPTS.md` để chạy từng việc một.

---

## 1. Project context

You are working on **hagiangwithmatt.com**, the website of Matthew Lee ("Matt"),
an independent tour guide in Ha Giang, northern Vietnam. He was born in Dong Van
to a Tay family, guides small motorbike and trekking trips himself, and sells
four tours priced $190–$549.

**This is not a corporate travel site.** Its entire competitive advantage is that
it sounds like one real person who lives there. Every change you make must
protect that.

### Stack

- Static HTML. No framework, no build step, no package.json.
- Plain CSS. No Tailwind, no preprocessor.
- Minimal vanilla JS. No jQuery, no React, no libraries.
- Bilingual: English at root, Vietnamese under `/vi/`.
- Images already optimised as `.webp`. Video as `.mp4`.
- **Hosted on GitHub Pages**, custom domain via `CNAME`.

**Do not introduce build tooling, frameworks, npm dependencies, or CSS libraries.**
If you think one is genuinely necessary, stop and ask first.

### Hosting constraint — read before touching any URL

GitHub Pages **cannot issue HTTP 301 redirects**. It serves static files only.
`_redirects` is a Netlify/Cloudflare Pages mechanism and is ignored here.
`.htaccess` is an Apache mechanism and is also ignored.

The consequences are binding:

- **Never create a `_redirects` file.** If you see one in a spec or an older
  prompt, that instruction is wrong — flag it and stop.
- **Do not rename or move any URL that is already live and indexed** unless
  Matt has explicitly confirmed a hosting migration first.
- New pages may use clean directory URLs. Existing pages keep their `.html`
  extension. Mixed URL styles cost nothing in search; broken URLs cost a lot.

### Current URL structure

```
/index.html   /about.html   /tours.html   /gallery.html
/reviews.html /faq.html     /contact.html
/classic-loop.html   /off-the-map.html   /cao-bang.html   /forest-and-stone.html
/vi/...  (mirror of the above)
/ads/bike-en.html   /ads/food-en.html   ← to be deleted, see Task 1
```

### Target URL structure

Existing pages **stay where they are**. Only new pages get clean URLs:

```
KEEP AS-IS (already indexed, no redirect possible)
/index.html   /about.html   /tours.html   /gallery.html
/reviews.html /faq.html     /contact.html
/classic-loop.html   /off-the-map.html   /cao-bang.html   /forest-and-stone.html

DELETE (Task 1)
/ads/

NEW — use directory URLs with index.html inside
/local-favourites/         → local-favourites/index.html
/blog/                     → blog/index.html
/blog/<slug>/              → blog/<slug>/index.html
/plan-your-trip/           → plan-your-trip/index.html

/vi/  mirrors all of the above
```

One exception worth fixing, because it is a duplicate rather than a move:
`/` and `/index.html` currently both resolve. Point every internal link and the
canonical at `/`, and leave `/index.html` reachable. No redirect needed —
canonical alone resolves it for search engines.

> **If Matt later migrates hosting to Cloudflare Pages or Netlify**, real 301s
> become available and the full clean-URL migration can be reconsidered as a
> separate task. Do not attempt it before that happens.

### The four tours (authoritative — do not alter these numbers)

| Tour | Slug | Duration | Price |
|---|---|---|---|
| The Classic Loop | `classic-loop` | 3 days, 2 nights | Easy rider $230 · Self-drive $190 |
| Off The Map | `off-the-map` | 4 days, 3 nights | Easy rider $275 · Self-drive $245 |
| Ha Giang → Cao Bang | `ha-giang-cao-bang` | 5 days, 4 nights | $549 |
| Forest & Stone | `forest-and-stone` | 5 days, 4 nights | $345 |

Group size on every tour: **2–5 guests, never merged with another group.**
Contact: WhatsApp `+84983648362` · `matt@hagiangwithmatt.com`

### Task state — keep this table current

The three tasks are sequential. Do not start one before the previous is signed
off. **Update this table at the end of every session** and state in your report
what you changed here.

| Task | Scope | State |
|---|---|---|
| 1 | Remove all advertising, add `/local-favourites/` | 🟢 content-complete, one open item — all ad cleanup finished (no modals ever existed in this codebase, verified); `/local-favourites/` and `/vi/local-favourites/` fully populated: 8 named venues across 5 areas, a motorbike-rental section with Matt's real per-model price table, real photos in `images/favourites/` (sourced from `imageblog/`, gitignored, not deployed), zero `{{TODO:}}` remaining anywhere in the repo. Linked from both navs, both footers, the tours-section strip, and `sitemap.xml` at priority 0.7. Only open item: the exact section-E ad-gap replacement markup from `viec-1-go-quang-cao.md` was never supplied, so what's live is Claude's own construction in the site's existing voice/classes, not copied from a spec — and the FAQ→Contact gap on `index.html` still has no replacement CTA (a full `.contact` section already follows immediately after, so this may not need one). Matt should read the two pages once before this task is signed off |
| 2 | Structured data + head-block fixes | 🟢 substantially complete. Head-block fixes from the earlier pass (absolute `/` links, canonical/hreflang, meta author, sitemap `lastmod`, video below 900px, custom `404.html`) all confirmed still in place. Added this session: `TouristTrip`+`Offer` on all 4 tour pages and as an `ItemList` on `index.html`/`tours.html`; `WebSite`/`Person`/`LocalBusiness` graph on `index.html`; `AboutPage`, `ContactPage`, `FAQPage` on their respective pages; `BreadcrumbList` on all 21 subpages (EN+VI); `LocalBusiness`+`AggregateRating` (5.0, 3 reviews) plus individual `Review` objects (matching the real, on-page Facebook/Messenger quotes — nothing invented) on `reviews.html`/`vi/reviews.html`. All 49 JSON-LD blocks sitewide validated as parseable JSON. Also gave each of the 4 tour pages its own `og:image`/`twitter:image` (previously all four shared `og-home.jpg`), and fixed `cao-bang.html`/`forest-and-stone.html` to use their real tour photos instead of stale generic stock (`dong-van-town`/`trekking`) images left over from before the homepage cards were updated. **Still open: `VideoObject` schema for the hero/why-banner video, and this has not been checked with Google's Rich Results Test** (no live URL to test against yet — see production note below) |
| 3 | Blog infrastructure and articles | 🟢 all 8 Phase-1 articles live locally on `main`: `blog/_template.html`, `blog/index.html` (hub, card grid of all 8), and the 8 articles themselves (`ha-giang-loop-guide`, `is-ha-giang-loop-safe`, `best-time-to-visit-ha-giang`, `ha-giang-loop-cost`, `solo-female-ha-giang-loop`, `easy-rider-vs-self-drive`, `ha-giang-market-days`, `hanoi-to-ha-giang`). Article 7 (market days) and article 8 (Hanoi bus) both needed Matt's own input and got it — real cho lui market schedules and real bus operator names/price, not invented. "Blog" nav link wired into header + footer of every EN page. Zero `{{TODO:}}` remaining outside the source template. **Not done: VI translations** (blog is EN-only for now, no `/vi/blog/`) and tag pages (§4 says restraint required, correctly skipped — not enough articles yet to justify one) |

Note on branches: `task-1-remove-ads` holds all of Task 1's work.
`phase-1-technical` branches off it and holds the technical fixes above.
Both are now merged into `main` (confirmed via `git merge-base --is-ancestor`).
This session's structured-data work was committed directly to `main`.
`main` is not yet pushed to `origin/main` — see the note below, this is the
one thing actually blocking everything in this file from going live.

### Production vs. this repo — read before trusting either

On 2026-08-25, a session was told production still had all the original ad
blocks, an empty logo href, and `meta author="Matt"` — asked to verify
rather than assume, and did: `git fetch origin` showed `origin/main` had
moved via a GitHub web "Add files via upload" commit that this repo's git
history never saw. That upload turned out to be a mid-session snapshot —
it already had the hero photo slideshow and the four fonts, but predated
the logo swap, all ad removal, and the meta-author fix. So "production" and
"this repo's `main`" are two different, diverged histories, and neither
git push nor a plain merge will reconcile them safely without checking
what's actually live first. Before starting Phase 2 or merging any branch
toward `main`, re-fetch `origin/main` and diff it — don't assume the state
described in an old session's report (including this one) still holds.

If a prompt asks you to begin a task whose predecessor is not ✅, say so and
ask before proceeding.

---

## 2. THE VOICE — read this before writing a single word of copy

This is the most important section in the brief. The site's copy is unusually
good and the fastest way to destroy this project is to write generic travel
content over it.

### What the voice sounds like

Real lines from the existing site:

> "I am not going to tell you this is the best tour in Vietnam. I do not know
> that, and neither does anyone who says it."

> "If your dates are wrong for Ha Giang, I will say so before you book."

> "Proper helmets, insured bikes, and a riding speed that makes people behind
> us impatient."

> "The plan is a draft."

> "Because this is not a place I discovered for tourism. It's home."

### Rules

1. **First person, always.** Matt is speaking. Never "we at Ha Giang With Matt"
   or "our expert guides". There is one guide and it is him.

2. **British English.** `travellers`, `metres`, `kilometres`, `favourite`,
   `realise`, `organised`. Never `travelers`, `meters`, `favorite`.

3. **Full forms over contractions, mostly.** The site writes "I do not overtake",
   "it is not a rumour", "I will tell you". This flat, slightly formal register
   is a deliberate tic. Use contractions sparingly, for warmth, not by default.

4. **Short declarative sentences.** Fragments are allowed. Rhythm matters more
   than grammatical completeness.

5. **Concrete beats abstract.** Not "stunning scenery" — "a road with no sign
   telling us where it goes". Not "authentic cuisine" — "we eat where I eat".
   Every paragraph should contain at least one thing you could photograph.

6. **Admit the downside.** This is the signature move. Every piece of content
   should contain at least one honest negative: what the trip does not include,
   when not to come, who this is wrong for, what the risk actually is. Content
   without a downside reads as marketing and breaks the voice.

7. **No superlatives, no hype.** The brand explicitly refuses to claim "best".

8. **No exclamation marks. No emoji. No rhetorical questions as headings.**

### Banned words and phrases — never write these

```
breathtaking · stunning · unforgettable · hidden gem · must-see · must-visit
nestled · vibrant · bustling · embark · immerse · immersive · picturesque
adventure of a lifetime · once-in-a-lifetime · off the beaten path
awe-inspiring · jaw-dropping · like something out of a postcard
a feast for the senses · dive in · unlock · discover the magic
whether you're a seasoned rider or a complete beginner
in today's fast-paced world · look no further · we've got you covered
Vietnam is a country of contrasts · nature lovers will rejoice
```

Also banned: opening a blog post with a scene-setting paragraph before answering
the question. Answer first, then elaborate.

### Vietnamese place names

Use the unaccented form as primary — foreign readers search that way. Introduce
the accented form **once**, in brackets, on first mention only.

```
✅  Ma Pi Leng Pass (Mã Pì Lèng)  →  then "Ma Pi Leng" for the rest of the piece
✅  Dong Van (Đồng Văn) · Nho Que (Nho Quế) · Meo Vac (Mèo Vạc)
✅  Du Gia (Du Già) · Lung Cu (Lũng Cú) · Quan Ba (Quản Bạ) · Lung Tam (Lũng Tám)
❌  Mã Pì Lèng used throughout an English article
❌  Mapileng, Ma-Pi-Leng
```

Add imperial units in brackets where useful: `620 km (385 miles)`,
`1,500 m (4,900 ft)`.

---

## 3. HARD GUARDRAILS

### 3.1. Never invent facts — this is the rule that matters most

You do not know Ha Giang. Matt does. If you fabricate a detail, it will appear
on a page that a real traveller relies on, and it will damage his reputation.

**Never invent, under any circumstances:**

- Names of homestays, restaurants, shops, bus companies, mechanics, hotels
- Prices in VND or USD other than the four tour prices listed above
- Opening hours, phone numbers, addresses
- Market day schedules (which market runs on which day)
- Distances in km, altitudes in metres, journey times
- Festival dates, weather statistics, rainfall figures
- Review quotes or traveller names
- Anything presented as Matt's personal memory or experience

**Instead, emit a placeholder in this exact format:**

```
{{TODO: name of the homestay Matt uses in Dong Van}}
{{TODO: distance Ha Giang City → Dong Van in km}}
{{TODO: Matt — one sentence, what actually happened here?}}
```

Then log every placeholder in `CONTENT-TODO.md` at the repo root:

```markdown
| File | Line | Placeholder | Status |
|---|---|---|---|
| blog/ha-giang-market-days/index.html | 84 | Which day Meo Vac market runs | open |
```

**Never publish a page while it still contains `{{TODO:}}`.** Check with:

```bash
grep -rn "{{TODO" --include="*.html" .
```

### 3.2. Do not deploy

Commit to a branch. Never push to production, never run a deploy command,
never modify DNS or hosting settings. Matt reviews before anything goes live.

### 3.3. Do not touch these without asking

- Existing copy on `index.html`, `about.html`, and the four tour pages.
  You may add structured data and fix technical issues around it, but do not
  rewrite the prose. It is the best asset the site has.
- The `videos/` and `images/` directories.
- Anything under `/vi/` that involves translating tone — flag it for Matt.

### 3.4. Performance budget

- No web fonts beyond what the site already loads.
- No third-party scripts except analytics (Plausible preferred over GA4 — it
  needs no cookie banner).
- Any new page: under 150 KB total, under 20 requests.
- Every `<img>` needs `width`, `height`, `loading="lazy"` (except the LCP image,
  which gets `fetchpriority="high"` and no lazy loading), and a descriptive
  `alt` written in the site's voice.

### 3.5. Quality floor for any HTML you write

- Exactly one `<h1>` per page; heading levels never skip.
- Visible `:focus-visible` outline on every interactive element.
- `@media (prefers-reduced-motion: reduce)` respected.
- Responsive from 320 px up. Test at 360 px.
- Colour contrast ≥ 4.5:1 for body text on `#1B1B19`.
- Absolute self-referencing `<link rel="canonical">` on every page.
- Reciprocal `hreflang` on both EN and VI versions, plus `x-default`.

### 3.6. Working method

- **One task per branch, one concern per commit.** Do not bundle Task 1 and
  Task 2 into one changeset.
- Before editing a file, read it fully. Do not pattern-match from filenames.
- After each task, output a short report: files changed, what to verify manually,
  what is blocked on Matt.
- If a task is ambiguous, ask **one** specific question rather than guessing.

---

## 4. Blog post specification

Applies to every article under `/blog/`.

### Structure

```
URL          /blog/<slug>/            kebab-case, no stopwords, no dates
<title>      ≤ 60 chars, keyword first, ends with " | Ha Giang With Matt"
<h1>         different wording from <title>, written for a human
meta desc    150–158 chars, contains the keyword and a reason to click
Opening      2–3 sentences that ANSWER the question immediately
Body         <h2> per sub-question, <h3> for detail
Length       1,200–3,000 words depending on the article
Images       ≥ 4, .webp, keyword-bearing filenames, alt text in Matt's voice
             ✅ ma-pi-leng-pass-morning-fog.webp
             ❌ IMG_4821.webp
Tables       ≥ 1 table or structured list (targets featured snippets)
Links        3–5 internal links, at least one to a tour page
Schema       BlogPosting + BreadcrumbList (+ FAQPage if the article has a Q&A block)
CTA          closing section, Matt's voice, links to the most relevant tour
Freshness    visible "Last updated: <Month Year>" + matching dateModified
```

### Required honesty block

Every article must contain at least one passage where Matt says something
against his own commercial interest. Examples: this trip is wrong for you if…,
do not come in these months, you can do this yourself without a guide, this
attraction is overrated. If your draft has no such passage, rewrite it.

### Template

Build `blog/_template.html` first and reuse it. It contains the head block,
breadcrumb, article shell, table of contents, CTA, footer and the JSON-LD graph
with `{{ }}` slots.

### Article backlog

The full list of 28 articles with slugs and target keywords is in
`01-audit-va-chien-luoc.md`, section 5. Write in this order:

**Phase 1 — write these eight first**

| # | Slug | Target keyword | Words |
|---|---|---|---|
| 1 | `/blog/ha-giang-loop-guide/` | ha giang loop guide | 3,000 (pillar) |
| 2 | `/blog/is-ha-giang-loop-safe/` | is ha giang loop safe | 1,800 |
| 3 | `/blog/best-time-to-visit-ha-giang/` | best time to visit ha giang | 2,000 |
| 4 | `/blog/ha-giang-loop-cost/` | ha giang loop cost | 1,800 |
| 5 | `/blog/solo-female-ha-giang-loop/` | ha giang loop solo female | 1,600 |
| 6 | `/blog/easy-rider-vs-self-drive/` | easy rider vs self drive ha giang | 1,500 |
| 7 | `/blog/ha-giang-market-days/` | ha giang market days | 1,400 |
| 8 | `/blog/hanoi-to-ha-giang/` | hanoi to ha giang bus | 1,600 |

Articles 2 and 5 will convert best — the existing FAQ already answers both
questions better than anyone else in the market. Expand that material, do not
replace it.

Article 7 is the one no competitor can copy, and it is **entirely dependent on
Matt's input**. Build the page structure and the table, fill every cell with
`{{TODO:}}`, and hand it back.

### Tag pages — restraint required

Do not generate a tag page per keyword. Thin tag archives are an SEO liability.

- Maximum 8 tags total.
- A tag gets an indexable page only once ≥ 5 articles carry it. Below that,
  `noindex`.
- Every tag page needs a 150–200 word human-written intro, not just a link list.
- Preferred alternative: one editorial hub at `/plan-your-trip/` that walks the
  reader through the articles in order, written by Matt.

---

## 5. Definition of done

A task is complete only when all of these pass:

```bash
# no leftover ad references
grep -rn "ads/" --include="*.html" --include="*.css" --include="*.js" .

# no unfilled placeholders in anything published
grep -rn "{{TODO\|{{" --include="*.html" .

# no banned words
grep -rniE "breathtaking|stunning|unforgettable|hidden gem|nestled|must-see|immersive|bustling|embark" --include="*.html" .

# no American spellings
grep -rn "traveler\|favorite\|meters\b\|kilometers" --include="*.html" .

# no hosting mechanisms that GitHub Pages ignores
ls _redirects .htaccess vercel.json netlify.toml 2>/dev/null
```

Plus, manually:

- [ ] Rich Results Test passes with no errors
- [ ] PageSpeed Insights mobile ≥ 85, LCP < 2.5 s, CLS < 0.1
- [ ] Page scrolls correctly on a real phone
- [ ] Browser console is clean
- [ ] `CONTENT-TODO.md` is up to date
- [ ] Report written for Matt
