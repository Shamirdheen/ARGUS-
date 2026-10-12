# Argus v2

A hundred eyes on your collateral. Argus watches Solana lending positions (Kamino, Jupiter Lend) and tells you which one breaks first and what to do before the liquidators do.

## Docs and design

- [`CLAUDE.md`](CLAUDE.md): rules for anyone (human or AI) working in this repo
- [`docs/DESIGN.md`](docs/DESIGN.md): design system: colour, risk tiers, type, components, voice, motion
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): data flow, known gaps, upgrade phases
- [`design/`](design/README.md): every screen as PNG, logo kit, canvas sources

## Run

```bash
cp .env.example .env.local   # add ANTHROPIC_API_KEY
npm install
npm run dev
```

## Routes

| Route | What it is |
| --- | --- |
| `/` | Landing. Paste a wallet or launch the app. |
| `/app` | Overview: closest-to-liquidation, totals, SOL shock cards, positions. |
| `/app/positions` | Full table, position drawer with price rehearsal and fix amounts. |
| `/api/positions?wallet=` | Normalised `Position[]`. Live Kamino when reachable, otherwise the labelled demo book. |
| `/api/chat` | Ask Argus on Claude. Streams NDJSON (`text`, `action`, `error`, `done`). Tools: `simulate_price_move`, `suggest_action`. |

Press ⌘K / Ctrl+K anywhere in the app to ask Argus.

## Structure

```
app/                 routes + API route handlers
components/brand/    RiskEye, OpeningEye
components/ui/       Button, Card, Label, Health, Status, Stat
features/portfolio/  PortfolioProvider (wallet → positions, 30s refresh), Overview
features/positions/  PositionTable, PositionDrawer, PositionsPage
features/ask/        AskPanel, system prompt, event types
features/wallet/     Wallet Standard providers + button (read-only: public key only)
lib/positions/       Position type, risk tiers + maths, demo book, Kamino adapter
```

## Risk tiers

Safe ≥ 2.00x · Watch ≥ 1.50x · Warning ≥ 1.20x · Act now below. Shown with lightness, weight and the risk eye, never hue alone.

## Status

- Kamino adapter reads Kamino's public REST API defensively and falls back to the demo book on any failure. It has not yet been verified against a live wallet.
- Jupiter Lend positions are demo-only until its adapter lands.
- Argus is read-only. It never requests a signature.
