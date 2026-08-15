# Ha Giang With Matt

Personal-brand travel website for **Matthew Lee**, a local guide, easy rider and trekking guide based in Đồng Văn, Hà Giang, Việt Nam.

Live site: <https://hagiangwithmatt.com>

## What this is

A hand-built static site. No framework, no build step, no dependencies.

- **HTML5** — semantic, one `<h1>` per page, correct heading order
- **CSS3** — one stylesheet, design tokens, mobile-first, ~39 KB
- **Vanilla JavaScript** — one file, ~11 KB, no libraries

Everything degrades. Turn JavaScript off and every page still reads correctly.

## Structure

```
index.html              Home
about.html              Matt's story
tours.html              Hub for all four trips
classic-loop.html       3 days · 2 nights
off-the-map.html        4 days · 3 nights, off-road + trekking
cao-bang.html           5 days · 4 nights, Ha Giang to Cao Bang
forest-and-stone.html   5 days · 4 nights, trekking
gallery.html            Photographs, with a lightbox
reviews.html            Awaiting real reviews
faq.html                Ten questions, with FAQPage schema
contact.html            Four-field form that opens WhatsApp

css/style.css           The whole stylesheet
js/script.js            The whole script
images/                 WebP, responsive srcset
robots.txt
sitemap.xml
CNAME
```

## Motion

Roughly 526 elements across the site animate individually. `js/script.js` walks each
section, tags every heading, paragraph, list item, image, table row, price cell and
card with `data-anim`, gives each one a staggered delay, and reveals them with an
`IntersectionObserver` when the section enters the viewport.

Also included: a reading-progress hairline, scroll-spy on tour sub-navigation,
height-animated accordions, a parallax banner on desktop only, cross-page view
transitions, and a mobile call-to-action bar that slides in past the hero.

All of it switches off under `prefers-reduced-motion: reduce`.

## SEO

- Per-page `title`, `meta description`, canonical, Open Graph and Twitter Card
- `hreflang` pairs for the planned Vietnamese edition at `/vi/`
- Schema.org: `LocalBusiness`, `Person`, `WebSite`, `TouristTrip` with `Offer`,
  `FAQPage`, `AboutPage`, `ContactPage`, `ItemList`
- Descriptive alt text on every image, `loading="lazy"` below the fold
- `robots.txt` and a full `sitemap.xml`

## Deploying to GitHub Pages

1. Create a repository and push these files to the root of the `main` branch.
2. Settings → Pages → Source: **Deploy from a branch** → `main` / `/ (root)`.
3. The `CNAME` file points the site at `hagiangwithmatt.com`. At your domain
   registrar add these DNS records:

   | Type  | Name | Value |
   |-------|------|-------|
   | A     | @    | 185.199.108.153 |
   | A     | @    | 185.199.109.153 |
   | A     | @    | 185.199.110.153 |
   | A     | @    | 185.199.111.153 |
   | CNAME | www  | `<your-username>.github.io` |

4. Back in Settings → Pages, tick **Enforce HTTPS** once the certificate is issued.

Verify the DNS values against GitHub's current documentation before you rely on
them — GitHub has changed these addresses before.

## Still to do

- Hero background photo or video — the slot is in `index.html`, commented and ready
- Real traveller reviews for `reviews.html`
- Vietnamese edition at `/vi/`
- `favicon.ico` and the Open Graph share image at `images/og/og-home.jpg`
- Confirm who guides Forest & Stone, and name them plainly

## Licence

Photographs and written content © Matthew Lee. Not for reuse.
