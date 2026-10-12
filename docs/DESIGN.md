# Argus design system

The rules every screen follows. Pictures are in [`design/`](../design/README.md). Tokens live in `app/globals.css`.

## 1. Brand idea

Argus Panoptes, the hundred-eyed giant of Greek myth, set to watch what others couldn't afford to lose. The art style is **Greek black-figure vase painting**: flat black figures, fine incised sand lines, terracotta ground. Philosophy, science and the planets (orbits, constellations, armillary spheres) are part of the world.

- **Logo:** "Hundred", a golden-angle spiral of dots with one terracotta eye. Sizes L (100 dots), M (34) and S (13). Wordmark in Michroma with Λ for the A. Files in `design/brand/logo/` and `public/brand/`.
- **Illustrations:** `public/brand/*.jpg`. New ones must match: black-figure style, terracotta ground, Argus covered in open eyes. No text in images.

## 2. Colour: three colours, two surfaces

| Role | Token | Hex | Use |
| --- | --- | --- | --- |
| Terracotta (the vase) | `terra-500` | `#c0551e` | Landing grounds, logo, large fills |
| | `terra-400` | `#d06f3c` | Critical row fill; links/small text on ink |
| | `terra-300` | `#e0946a` | Warning text |
| Ink (inside the figure) | `ink-950` | `#16110c` | Page background (the product is **dark only**) |
| | `ink-900` / `850` | `#1e1711` / `#271e16` | Cards / drawers, popovers |
| | `ink-800` / `700` | `#33271d` / `#482a16` | Hairlines / strong borders |
| Sand (the incised line) | `sand-100` | `#f6ddb8` | Headings, emphasis |
| | `sand-200` | `#efc796` | Body text, primary buttons (ink text) |
| | `sand-500` | `#a8865f` | Secondary text |
| | `sand-600` | `#7e654a` | Borders only, never text |

No other hues. No blue, green, yellow or red anywhere, charts included.

## 3. Risk: Mono-2 (never colour alone)

| Tier | Health | Number | Label | Row | Eye |
| --- | --- | --- | --- | --- | --- |
| Safe | ≥ 2.00x | `sand-500`, dimmed | none (sr-only) | normal | lid low, ash iris |
| Watch | 1.50–2.00x | `sand-200` | "Watch" | normal | half open, hollow |
| Warning | 1.20–1.50x | `terra-300`, **underlined** | "Warning" | normal | wide, solid terracotta |
| Critical | < 1.20x | ink on fill | "Act now" chip | **whole row terracotta** | fully open, glowing |

- Thresholds live in `lib/positions/risk.ts` (`TIERS`). The chat prompt uses the same ones. Change both together.
- In the product, **terracotta means danger and nothing else**. On the landing page it's the brand ground.
- The critical row is the only row that changes background. Everything else uses weight and lightness.
- **Risk eye** (`components/brand/RiskEye.tsx`): the lid and iris ease over 600 ms `cubic-bezier(.2,.8,.2,1)`, and critical glows with a 1.6 s pulse. It's the only pictorial icon that carries meaning on its own.

## 4. Type: Michroma speaks, Plex Mono works

- **Michroma** (`font-display`): logo, one page title per screen, section headings (caps), landing headlines, and the single hero number per view. 18 px and up. **Never** in body, buttons, labels or tables.
- **IBM Plex Mono**: everything else, weights 400 and 500. Body 14–16 px, line height 1.5–1.6, tabular numbers.
- Scale: Display 56/1.05 · H1 34/1.1 · H2 20/1.2 caps · Hero number 40 · Body 15/1.6 · Label 11–12 caps +8–10% tracking · Data 13–14 tabular.
- Fonts are self-hosted with `@fontsource` (no Google Fonts requests).

## 5. Components

- **Buttons** (`components/ui`): **Primary** = sand fill, ink text, one per view. **Secondary** = outline. **Simulate** = dashed, for anything hypothetical. **Danger** = terracotta, only for acting on a risky position. **Ghost** = text only. Minimum height 44 px (36 px small).
- **Square corners everywhere.** No border radius, no drop shadows on cards, and 1 px borders in `ink-800`.
- **Charts:** actual = solid sand · simulated = dashed sand · liquidation = terracotta line · danger zone = faint terracotta band.
- **Icons:** Phosphor **Light**, 16–22 px, sand-coloured. Use glyphs first: `→` means going somewhere inside Argus, `↗` means leaving it (Solscan, a protocol, docs), and `+ / −` open and close accordions. `×` is for close, always in a 44 px button with an `aria-label`.
- **States:** the loading state is "Argus is opening his eyes…" with the `OpeningEye` component. Empty is "Nothing to watch yet.", and errors name what failed ("Argus lost sight of Pyth for 12 seconds.").

## 6. Voice: a watchman, not a hype man

- **Calm when fine, loud only when not.** Words get shorter as risk rises.
- **Say the number and the fix:** "SOL / USDC is at 1.07x. Add $16,760 to return to 1.50x."
- **Myth is seasoning, not sauce.** Myth names (Hermes, "opening his eyes") belong on the landing page and in loading and empty states, never in a critical alert or the product's main UI.
- **Never promise what Argus can't do.** No "guaranteed", "never get liquidated" or "risk-free", and no emoji.

| Say | Not |
| --- | --- |
| Argus watches | our AI, the bot |
| Rehearse the crash | backtest, scenario analysis |
| Buffer | top-up, rescue |
| Act now (only below 1.20x) | URGENT, Danger, Rekt |
| Nothing to watch yet. | No data found |

**Formats:**
- Health: `1.31x`, two decimals.
- Money: `$1,842,500`.
- Change: `−20.4%`, with a true minus sign and always signed.
- Address: `7xKX…3tKG`.
- Case: sentence case; capitals only for 11 px labels.

## 7. Motion

- One easing everywhere: `cubic-bezier(.2,.8,.2,1)`. Slow and calm: Argus watches, he doesn't bounce.
- Landing motion lives in `features/landing/motion.css` and `MotionRoot.tsx`. Add `data-reveal` (fade up), `data-reveal="group"` + `data-wipe` (illustration wipe), and `style={{"--d":"120ms"}}` for stagger. No new animation library.
- **Every animation must switch off under `prefers-reduced-motion`.**
- In the product, only motion with a meaning: eye transitions, the critical pulse, and the drawer and panel opening. No decorative motion near money.

## 8. Accessibility (non-negotiable)

- Text contrast ≥ 4.5:1 (sand-200 on ink is 11.9:1). `sand-600` is never used for text.
- Risk is always carried by the number and a word as well as the eye. Nothing depends on colour alone.
- Touch targets ≥ 44 px, visible focus rings (already global), labels on every input, and no sideways scrolling at 390 px.
