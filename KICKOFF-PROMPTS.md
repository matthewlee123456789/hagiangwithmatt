# KICKOFF PROMPTS — dán từng cái một vào IDE

> **Cách dùng:** chạy **một prompt mỗi phiên**. Đừng dán cả file. Sau mỗi phiên,
> đọc báo cáo agent trả về, kiểm tra kết quả, commit, rồi mới sang phiên tiếp theo.
> Agent làm nhiều việc cùng lúc sẽ làm ẩu và trộn lẫn các thay đổi.
>
> **Trước khi bắt đầu:** `git checkout -b seo-overhaul` và đảm bảo
> `AGENT-BRIEF.md` đã nằm trong context vĩnh viễn của IDE.

---

## PHIÊN 0 — Cho agent đọc hiểu dự án trước

```
Read AGENT-BRIEF.md in full, then explore this repository yourself: the
directory structure, index.html, classic-loop.html, and the main CSS file.

Do not change anything yet. Report back with:

1. The actual class names and markup used for the advertisement blocks
   (there are two modals plus two inline blocks referencing ads/bike-en.html
   and ads/food-en.html).
2. Which CSS rules and JS functions control them.
3. The two font families the site currently loads, and the CSS custom
   properties or colour values already in use.
4. How the header and footer are shared between pages — are they duplicated
   in every file, or injected by JS?
5. Whether robots.txt and sitemap.xml exist, and what they contain.
6. Anything in the codebase that contradicts AGENT-BRIEF.md.

Answer in a short structured report. Ask me any question you need answered
before starting Task 1.
```

Điểm 4 quan trọng: nếu header/footer bị lặp lại trong từng file HTML, agent sẽ
phải sửa 20+ file cho mỗi thay đổi nhỏ. Nếu vậy, hãy cân nhắc yêu cầu agent
gom chúng lại trước.

---

## PHIÊN 1 — Việc 1: gỡ quảng cáo

```
Task 1 of 3: remove all third-party advertising from the site.

Work on branch `task-1-remove-ads`.

Note on current state: two sidebar advertisement blocks have already been
deleted in an earlier session. Everything below is still outstanding. Start
by auditing what actually remains rather than assuming — run the grep
commands in section B of viec-1-go-quang-cao.md first and report what you
find before you change anything.

Follow viec-1-go-quang-cao.md, which is in this repository. In short:

1. Delete the two advertisement modals from index.html and its Vietnamese
   mirror.
2. Delete any remaining inline advertisement blocks on both language
   versions.
3. Remove every CSS rule that supported them. Pay particular attention to
   any rule that sets overflow:hidden on body — a leftover scroll lock is
   the most common bug after removing a modal.
4. Remove the JavaScript that opened, closed or timed the modals. Verify no
   orphaned selectors remain that would throw a null reference.
5. Delete the ads/ directory. Add `Disallow: /ads/` to robots.txt and make
   sure no /ads/ URL appears in sitemap.xml.
6. Fill the two gaps left behind, using the replacement markup specified in
   section E of viec-1-go-quang-cao.md: a strip linking to /local-favourites/
   after the tours section, and a contact CTA after the FAQ section. Style
   them with the site's existing classes — do not invent a new design system.
7. Add local-favourites.html to the repository at /local-favourites/index.html.
   It is already written. Do three things to it: replace the CSS custom
   properties in :root with the site's real font stack, splice in the site's
   existing header and footer where the comment blocks indicate, and leave
   every {{ }} placeholder untouched.
8. Create CONTENT-TODO.md and log every {{ }} placeholder in local-favourites.
9. Link /local-favourites/ from the main navigation and the footer, and add
   it to sitemap.xml with priority 0.7.

Before you start, run PageSpeed Insights mentally is not possible — instead,
record the number of HTTP requests and total page weight of index.html as it
is now, so we can compare afterwards.

Do not deploy. Commit in logical steps. When finished, report: files changed,
what I need to verify manually on a real phone, and what is blocked on me.
```

---

## PHIÊN 2 — Việc 2: cài Schema JSON-LD

```
Task 2 of 3: add structured data across the site.

Work on branch `task-2-schema`.

All the JSON-LD is already written in 02-schema-va-meta.md in this repository.
Your job is to place it correctly, not to invent it.

1. Add the TravelAgency graph node to every page, English and Vietnamese.
   Use @id "https://hagiangwithmatt.com/#organization" so other nodes can
   reference it rather than repeat it.
2. Add the Person node to /about/ with @id ".../about/#matt".
3. Add a TouristTrip node with its Offer array to each of the four tour pages.
   The template in the file is for the Classic Loop; adapt it for the other
   three using the price and duration table in AGENT-BRIEF.md section 1.
   Take the itinerary steps from the actual copy already on each page — do
   not write new ones.
4. Add FAQPage to /faq/ and to index.html. Only mark up questions that are
   genuinely visible on that page.
5. Add BreadcrumbList to every page except the homepage, and render a visible
   breadcrumb trail in the HTML to match. A breadcrumb in schema but not on
   the page is a mismatch.
6. Add the Review nodes to /reviews/ for every review currently on that page.
   Do not invent reviews, ratings, names or dates. If a review has no date,
   ask me.
7. Add VideoObject for the homepage hero video.
8. Fix the technical issues while you are in each head block:
   - reciprocal hreflang en / vi / x-default on both language versions
   - the empty href on the homepage logo — it should point to "/"
   - meta author: use "Matthew Lee" everywhere, replacing "Matt"
   - canonical: absolute, self-referencing, on every page
   - unify /index.html and / — point every internal link and canonical at
     "/". Do not attempt a redirect; GitHub Pages cannot issue one, and the
     canonical is sufficient here.
9. Consolidate multiple JSON-LD blocks per page into a single @graph array.

Validate every page type with the Rich Results Test structure in mind. Report
which pages you validated and any warnings you could not resolve.

Do not deploy.
```

---

## PHIÊN 3 — Việc 3a: dựng khung blog

```
Task 3 of 3, part A: build the blog infrastructure. No articles yet.

Work on branch `task-3-blog`.

1. Do NOT migrate any existing URL. This site is on GitHub Pages, which
   cannot issue 301 redirects — see the hosting constraint in AGENT-BRIEF.md
   section 1. Existing .html paths stay exactly as they are. Never create a
   _redirects file.

   The only URL work in this task: make every internal link and every
   canonical point at "/" rather than "/index.html", so the homepage stops
   resolving as two URLs.

2. Build blog/_template.html following the blog post specification in
   AGENT-BRIEF.md section 4. It must include:
   - the full head block with all meta and OG tags, using {{ }} slots
   - visible breadcrumb
   - article header: eyebrow, h1, standfirst, "Last updated" line
   - a table of contents generated from the h2 headings
   - the article body shell
   - a "What this means for your trip" CTA block linking to a tour
   - an author box for Matt with his portrait and one paragraph of bio
   - JSON-LD @graph with BlogPosting + BreadcrumbList
   Style it with the site's existing CSS. Add no new fonts.

3. Build /blog/index.html — the article listing page. Cards with title,
   standfirst, date and reading time. No infinite scroll, no JS pagination;
   plain HTML.

4. Build /plan-your-trip/index.html as an editorial hub: a page in Matt's
   voice that walks a reader through the articles in the order they would
   actually need them, from "should I come at all" to "what do I pack".
   Leave the article links as placeholders for now.

5. Do NOT create tag pages yet. Read the restraint note in AGENT-BRIEF.md
   section 4 before you consider it.

6. Add the blog and hub to sitemap.xml and to the main navigation.

Show me the template rendered with dummy content before you write any real
articles. Do not deploy.
```

---

## PHIÊN 4 — Việc 3b: viết bài blog (một bài mỗi phiên)

Đây là phiên bạn sẽ lặp lại tám lần. Đổi phần trong ngoặc mỗi lần.

```
Write blog article 2 of 8: "Is the Ha Giang Loop safe?"

Slug:     /blog/is-ha-giang-loop-safe/
Keyword:  is ha giang loop safe
Length:   about 1,800 words

Read AGENT-BRIEF.md section 2 (the voice) and section 4 (the blog spec)
again before you write. Then read the FAQ answer about solo female travellers
and the "Safety" card in the "What you are actually paying for" section on
index.html — that existing copy is the tonal target and the factual seed.
Expand it. Do not replace it or contradict it.

Structure it around these h2 questions:
- What actually causes accidents here
- The roads people worry about, and the ones they should
- Landslides are not a rumour
- Helmets, and why the thin ones are not helmets
- Riding yourself versus riding with someone
- What happens if something goes wrong
- Travelling alone
- My own rules on the road

Requirements:
- Answer the title question in the first three sentences. No scene-setting.
- Include at least one passage that costs Matt money to say — a reason not
  to come, or a case where a guide is unnecessary.
- One table or structured list.
- Four internal links, one of them to /tours/classic-loop/.
- Every statistic, distance, hospital name, road number, insurance detail
  and personal anecdote becomes {{TODO:}}. You do not know these. Log each
  one in CONTENT-TODO.md.
- Fill the JSON-LD. Set datePublished and dateModified to today.
- Write four image slots with descriptive alt text in Matt's voice and
  keyword-bearing filenames, using placeholder src paths.

When done, run the banned-word and Americanism greps from AGENT-BRIEF.md
section 5 against your own output and fix anything they catch. Then give me
a list of every {{TODO:}} as questions I can answer in one sitting.
```

### Bảy bài còn lại của Phase 1

Đổi ba dòng đầu và phần cấu trúc `h2`; giữ nguyên toàn bộ phần yêu cầu.

| Lần | Slug | Từ khóa | Số từ | Nguồn nội dung sẵn có trên site |
|---|---|---|---|---|
| 1 | `/blog/ha-giang-loop-guide/` | ha giang loop guide | 3.000 | trang `classic-loop`, toàn bộ FAQ |
| 3 | `/blog/best-time-to-visit-ha-giang/` | best time to visit ha giang | 2.000 | mục "When to come" trên trang tour |
| 4 | `/blog/ha-giang-loop-cost/` | ha giang loop cost | 1.800 | mục Included / Not included |
| 5 | `/blog/solo-female-ha-giang-loop/` | ha giang loop solo female | 1.600 | câu FAQ đầu tiên |
| 6 | `/blog/easy-rider-vs-self-drive/` | easy rider vs self drive ha giang | 1.500 | bảng giá hai mức trên mỗi trang tour |
| 7 | `/blog/ha-giang-market-days/` | ha giang market days | 1.400 | ⚠️ gần như toàn bộ là `{{TODO}}` |
| 8 | `/blog/hanoi-to-ha-giang/` | hanoi to ha giang bus | 1.600 | mục "not included: sleeper bus" |

Với bài 7, dùng prompt này thay vì prompt chuẩn:

```
Write article 7: "Ha Giang Market Days".

This article is almost entirely facts I have to supply. Do not invent a
single market day, location or opening time.

Build the page: the intro in Matt's voice explaining why market day dictates
the route, a section on what actually happens at a highland market, a section
on etiquette and photography, and a closing CTA.

Then build the central table with these columns — Market · Day it runs ·
Where · Worth a detour for — and fill every single cell with a numbered
{{TODO:1}}, {{TODO:2}} and so on. Include rows for at least: Dong Van,
Meo Vac, Lung Cu, Quan Ba, Yen Minh, Du Gia, Sa Phin, Pho Bang, Lung Phin.

Output the TODO list as a numbered questionnaire I can answer offline in
one sitting, then paste back.
```

---

## PHIÊN 5 — Kiểm tra cuối trước khi lên production

```
Final QA pass before deploy. Do not deploy — report only.

Run every check in AGENT-BRIEF.md section 5 and report results in a table.

Then verify manually and report:
1. Every page has exactly one h1 and no skipped heading levels.
2. Every canonical is absolute and self-referencing.
3. hreflang is reciprocal on all EN/VI pairs and includes x-default.
4. No page is accidentally noindex.
5. sitemap.xml lists every live URL and no dead ones, with lastmod dates.
6. No _redirects, .htaccess, netlify.toml or vercel.json exists — none of
   them work on GitHub Pages. No existing .html URL has been renamed or moved.
7. No internal link 404s.
8. Every image has width, height and alt.
9. No {{TODO}} remains in any file intended for publication.
10. CONTENT-TODO.md accurately reflects what is still open.

Give me a go/no-go recommendation with the specific blockers listed.
```

---

## Cách xử lý khi agent đi chệch

Ba tình huống hay gặp và câu để kéo nó về:

**Agent viết văn du lịch sáo rỗng:**
```
Stop. Read AGENT-BRIEF.md section 2 again, in full. Your draft contains
[trích ra 2–3 câu cụ thể] which are exactly the register the brief forbids.
Rewrite. Every paragraph needs one concrete thing you could photograph, and
the piece needs at least one passage that costs Matt money to say.
```

**Agent bịa số liệu, tên quán, lịch chợ:**
```
You invented [chỉ rõ ra]. You have no source for this and neither do I.
Replace it with a {{TODO:}} placeholder phrased as a question I can answer,
log it in CONTENT-TODO.md, and audit the rest of your output for anything
else you asserted without a source.
```

**Agent tự ý thêm framework, thư viện, build tool:**
```
Revert that. AGENT-BRIEF.md section 1 is explicit: static HTML, plain CSS,
vanilla JS, no dependencies. Solve it without adding anything to the stack.
```
