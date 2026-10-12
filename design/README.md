# Argus design files

Everything designed for Argus v2, exported from the Claude Design canvas on 12 Oct 2026.
**The rules live in [`docs/DESIGN.md`](../docs/DESIGN.md). These files are the pictures.**

| Folder | What's in it |
| --- | --- |
| `screens/` | Product screens and the landing mock-up, as PNG |
| `system/` | Brand, type, components, risk colours, living favicon spec, voice and copy |
| `explorations/` | The 4 starting style directions (raw brutalism, neobrutalism, flat-glass, maximalism) and logo rounds 1–3. History only |
| `research/` | Inspiration research: the sites you picked from the Inspo catalogue (4 batches, with palettes, fonts and signature moves) and the catalogue studies (full, maximalism, brutalism) |
| `tools/` | Generators: `final_logo.py` (Hundred logo, Vogel spiral) and `boards/*.py` (how the canvas boards were built). Reference only; paths point at the old workspace |
| `brand/argus-logo-hundred.zip` | The logo kit as one download |
| `brand/logo/` | Final "Hundred" logo kit: lockups, marks (L/M/S × terracotta/dark/mono), app icon, PNGs |
| `brand/argus-tokens.css` | The original colour/type token file. The live version is `app/globals.css` |
| `source/` | Canvas sources (`.dc.html`) and layout (`canvas.json`). They need the Claude Design runtime; open the PNGs instead |

## Screens and build status

| Screen | File | In the app? |
| --- | --- | --- |
| Landing | `screens/Landing.png` | Built and extended (tutorial, illustrated myth chapters, motion). The code is now ahead of this mock-up |
| Overview | `screens/Overview.png` | Built (`/app`) |
| Positions + drawer | `screens/Positions.png` | Built (`/app/positions`) |
| Wallet connect | `screens/Wallet.png` | Built (wallet modal, restyled) |
| Ask Argus ⌘K bar | `screens/Ask-bar.png` | Partly: ⌘K opens the side panel, no command palette yet |
| Ask Argus panel | `screens/Ask-panel.png` | Built |
| Terminal | `screens/Terminal.png` | Not built |
| Risk Radar | `screens/Radar.png` | Not built |
| Alerts | `screens/Alerts.png` | Not built (needs the Phase 2 watcher, see `docs/ARCHITECTURE.md`) |
| Activity | `screens/Activity.png` | Not built (needs stored history) |
| Living favicon | `system/Favicon.png` | Not built. Spec is complete |

`system/Risk-eye.png` is a snapshot of the interactive risk-eye board (at 1.58x, Watch). The live version is the app component `components/brand/RiskEye.tsx`.

**How we got here:** four style directions (`explorations/style-*`) → the hero illustration set the palette → brand locked (Hundred logo, Mono-2 risk, Michroma + Plex Mono) → screens. The direction is black-figure vase painting; the four style boards are not the direction.

## Mock-up data is not product truth

The mock-ups show protocols and numbers that v2 doesn't support yet (Drift, Marginfi, Raydium, "7 positions", slot numbers). At launch Argus reads **Kamino and Jupiter Lend** only. Never copy mock-up figures into the product.

Placeholders still open in the mock-ups: `[COLLATERAL WATCHED]`, `[N]`, `[PRICING]`, `[CHANNEL]`, `[LEGAL LINKS]`, `[DECIDE: approve vs automatic]`.
