# Instructions for working on Argus

Argus v2 is a read-only Solana liquidation-risk watcher (Kamino + Jupiter Lend) with an AI chat (Ask Argus, on Claude).
Owner: Shamir. Repo: `Shamirdheen/ARGUS-`, deployed on Vercel from `main`.

## Read first
1. `AGENTS.md`: this is **Next.js 16.4**. Check `node_modules/next/dist/docs/` before using any Next API you're unsure of.
2. `docs/DESIGN.md`: the design system (colour, risk tiers, type, components, voice, motion, accessibility).
3. `docs/ARCHITECTURE.md`: how data flows today, known gaps and the upgrade phases.
4. `design/README.md`: pictures of every screen, and which ones are built.

## Hard rules
- **Read-only.** Never request a wallet signature, never build anything that moves funds (auto-protect is Phase 3, behind a security review).
- **Never commit secrets.** `.env*` is git-ignored except `.env.example`. Never print or log `ANTHROPIC_API_KEY`.
- **The brand is locked.** Use only the tokens in `app/globals.css`. Risk is shown by lightness, weight, the risk eye and a word, **never by hue alone and never with red/yellow/green**. Michroma only for titles, headings and the hero number.
- **One source of truth for maths:** `lib/positions/risk.ts`. The UI, chat tools and any future watcher import from it; never re-implement a formula. Tier thresholds change in `TIERS` *and* `features/ask/prompt.ts` together.
- **Claude never does arithmetic in Ask Argus.** Add a computed field or a tool instead.
- **Demo data is always labelled "Demo".** Never present demo or mock-up numbers as a user's real data. Mock-ups in `design/` show protocols v2 doesn't support. Don't copy their figures.
- **Every animation respects `prefers-reduced-motion`.** No new animation or UI libraries without asking.
- Keep the structure: `app/` routes · `features/<domain>/` · `components/ui` + `components/brand` · `lib/`.

## Code standard (Shamir's)
Readable, single responsibility, reusable, maintainable, no over-engineering. Simple beats clever.
For every change, say: **what it does, why it's written that way, and what breaks if it's wrong.**

## Workflow
- `git pull` before starting. More than one agent pushes to this repo.
- Before pushing: `npm run lint` and `npm run build` must pass. For UI changes, check 1440 px and 390 px widths (no sideways scrolling).
- Small commits with clear messages. Push to `main` only when the build passes; use a branch for anything experimental.
- If a design decision isn't covered by `docs/DESIGN.md`, ask rather than invent.
