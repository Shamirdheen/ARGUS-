# Landing page: everything on it

Route `/`, file `app/page.tsx`. Pictures of each section: `design/built/landing-sections/`. Motion videos: `design/built/video/`.

## Sections, top to bottom

| # | Section | Code | Images | Motion |
| --- | --- | --- | --- | --- |
| 01 | **Hero**: "A hundred eyes on your collateral." + scan box | `app/page.tsx`, `features/landing/ScanForm.tsx` | `hero.jpg` | Headline rises line by line (100/220/340 ms), scan box fades in (650 ms), art settles from 1.07× zoom over 14 s |
| 02 | **Proof**: 2 protocols · 30s · 0 signatures, with footnotes | `app/page.tsx` (`PROOF`) | none | Cards reveal 900 ms + 120 ms stagger |
| 03 | **How it works**: 01 Connect / 02 Watch / 03 Act early | `app/page.tsx` (`STEPS`) | none | Heading reveals, steps stagger 140 ms |
| 04 | **Night-watch band**: "Every block. Every position. All night." | `app/page.tsx` | `frieze.jpg` | Sky drifts ±1.5% over 60 s (loops); line reveals |
| 05 | **Tutorial**: "Three things Argus teaches you." | `features/landing/Tutorial.tsx` | `tut-eye.jpg`, `tut-dial.jpg`, `tut-ask.jpg` | Cards stagger 0/140/280 ms. Step 1 eye demos itself once (2.20x → 1.05x over 2.6 s) until touched. Hover lifts the card and leans the image |
| 06 | **Before / after**: 1.18x → 1.31x | `features/landing/BeforeAfter.tsx` | none | Number counts up 1.18 → 1.31 over 1.6 s; eye calms from critical to warning |
| 07 | **The real interface**: sample positions table | `app/page.tsx` (`book` from `lib/positions/demo.ts`) | none | Copy reveals; table and each row stagger 110 ms |
| 08 | **Why the name**: chapters I Argus · II Hermes · III Premeditatio malorum | `app/page.tsx` (`MYTH`) | `watch.jpg`, `hermes.jpg`, `stoic.jpg` | Illustration wipes open left→right (1.3 s) while settling from 1.12× zoom; text follows 300 ms later; hover leans the image |
| 09 | **FAQ** | `app/page.tsx` (`FAQ`) | none | Native `<details>`, typographic `+ / −` |
| 10 | **Footer**: "Argus never sleeps. Now neither does your collateral." + ΛRGUS | `app/page.tsx` | `argus-mark-L-terracotta.svg` | Copy reveals; wordmark rises; logo mark "breathes" (5 s loop) |

All copy follows the voice rules in `docs/DESIGN.md` §6. The numbers in the tutorial and the sample table are **computed from the demo book**, never typed by hand.

## Motion system

Files: `features/landing/motion.css` (all keyframes and transitions) and `features/landing/MotionRoot.tsx` (one shared IntersectionObserver, plus the `useInViewOnce` and `tween` helpers).

| Hook | What it does | Use |
| --- | --- | --- |
| `data-reveal` | Fade + rise 28 px when it scrolls into view (0.9 s) | Any block |
| `style={{"--d":"120ms"}}` | Delay, for staggering siblings | Lists, grids |
| `data-reveal="group"` + child `data-wipe` | The group triggers; the child image wipes open | Illustrations (a fully clipped element never counts as "in view", so the trigger must be the parent) |
| `.hero-line > span` | Masked line rise on load | Hero headline only |
| `.hero-fade`, `.hero-art` | Load-time fade / slow settle | Hero only |
| `.sky-drift` | 60 s alternating pan | The frieze only |
| `.lean` / `.lift` | Hover: image scales 1.035 / card rises 3 px | Image cards |
| `.mark-breathe` | Slow rotate/scale loop | Footer mark only |
| `useInViewOnce(ref, fn)` + `tween(from, to, ms, set)` | Run a number animation once when visible | Count-ups, self-demos |

Rules:
- Easing: `cubic-bezier(.2,.8,.2,1)` (same as the risk eye).
- **Everything is inside `@media (prefers-reduced-motion: no-preference)`.** Reduced-motion users get the finished state instantly; `tween` jumps to the end value.
- No animation libraries. No bouncing, no parallax on text, nothing that moves near a number the user must read.

## Images (`public/brand/`)

| File | Size | Shows | Canva media id |
| --- | --- | --- | --- |
| `hero.jpg` | 1680×944 | Argus covered in eyes, at a laptop, orbital rings | MAHXuFHojps (style reference for all others) |
| `frieze.jpg` | 1776×896 | Sky of eyes joined like a price chart, temple, Greek-key border | MAHXujP-Q5Y |
| `watch.jpg` | 1680×944 | Argus from behind on a hilltop, guarding amphorae and chests | MAHXutrBXoc |
| `hermes.jpg` | 1680×944 | Hermes piping; Argus's eyes closing | MAHXurH5Mwc |
| `stoic.jpg` | 1680×944 | Argus rehearsing a wave against five amphorae; the first is cracking | MAHXukNBac4 |
| `tut-eye.jpg` | 1000×1000 | Argus raising a hand to three eyes: shut, half, glowing | MAHXuraG9Hw |
| `tut-dial.jpg` | 1000×1000 | Argus turning a bronze wheel; the water level falls | MAHXurx0LWY |
| `tut-ask.jpg` | 644×644 | Crop of the hero: Argus's hands on the laptop | (crop of hero.jpg) |

New illustrations: generate with the hero (and ideally `stoic.jpg`) as style references. Black-figure on terracotta, Argus covered in open eyes, no text. Export JPG around 1680 px wide, about 150–270 KB, and keep alt text descriptive.

## Not on the landing page yet (decided against for now)
- A fourth tutorial step ("two ways back" scales illustration): folded into step 2.
- Real stats (collateral watched, wallets): placeholders until there's real usage data. Never invent them.
