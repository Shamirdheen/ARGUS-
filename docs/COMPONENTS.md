# Components

The live catalogue is the **`/kit`** page (`app/kit/page.tsx`): it renders the real components, so it can't go out of date. Screenshots are in `design/built/components/`. Visual rules are in `docs/DESIGN.md`.

## Brand (`components/brand/RiskEye.tsx`)

| Component | Props | Use |
| --- | --- | --- |
| `RiskEye` | `risk`, `size=22`, `onFill`, `glow`, `className` | The risk indicator. 22 px in rows, 56–60 in cards, 84–96 as a hero. `onFill` draws it in ink on the terracotta critical row. `glow` only matters at critical |
| `OpeningEye` | `label="Argus is opening his eyes…"` | The only loading indicator |

## UI primitives (`components/ui/index.tsx`)

| Component | Props | Use |
| --- | --- | --- |
| `Button` | `kind`: primary · secondary · simulate · danger · ghost; `small` | One primary per view. `simulate` (dashed) for anything hypothetical. `danger` only for acting on a risky position |
| `Card` | `className` | Ink-900 panel, 1 px ink-800 border, square corners |
| `H1` / `H2` | children | Michroma page title / caps section heading |
| `Label` | children, `className` | 11 px caps label |
| `Health` | `value`, `onFill`, `className` | Health factor text styled by tier (dim / normal / underlined / ink-on-fill) |
| `Status` | `risk`, `onFill` | Eye + word (Watch, Warning, "Act now" chip; Safe is screen-reader only) |
| `Stat` | `label`, `value`, `sub` | Number tile |
| `cx(...)` | class names | Joins class names, ignores falsy |
| `Ticker` (`components/ui/Ticker.tsx`) | `value`, `className`, children | Wrap a number; it glows once when `value` changes (not on first render). Use for live figures only |

## Feature components

| Component | File | What it does |
| --- | --- | --- |
| `AppShell` | `features/shell/AppShell.tsx` | App header (logo, nav, Demo badge, Ask Argus ⌘K, wallet), demo note bar, mounts the drawer + Ask panel |
| `PortfolioProvider` / `usePortfolio` | `features/portfolio/PortfolioProvider.tsx` | Wallet (or `?wallet=`) → `/api/positions` every 30 s; selection; Ask panel open/seed; ⌘K (Esc is handled by each panel so it can animate out) |
| `Overview` | `features/portfolio/Overview.tsx` | Closest-to-liquidation card, totals, "If SOL falls" shock cards, compact table |
| `PositionTable` | `features/positions/PositionTable.tsx` | Sorted by risk; critical row inverts; click opens the drawer. `compact` hides money columns |
| `PositionDrawer` | `features/positions/PositionDrawer.tsx` | Full figures, price-rehearsal slider, add/repay amounts back to 1.50x, "Ask Argus about this" |
| `PositionsPage` | `features/positions/PositionsPage.tsx` | `/app/positions` |
| `AskPanel` | `features/ask/AskPanel.tsx` | Streaming chat, starter questions, action cards from `suggest_action`, Stop button |
| `WalletProviders` / `WalletButton` | `features/wallet/` | Wallet Standard (no bundled adapters), read-only connect/disconnect. Styles: `wallet-adapter.css` is the library's CSS **minus its Google Fonts import**; loaded only on `/app` routes |
| `ScanForm` | `features/landing/ScanForm.tsx` | Landing address box → `/app?wallet=…` (base58 check) |
| `Tutorial` | `features/landing/Tutorial.tsx` | Three illustrated steps with live demos |
| `BeforeAfter` | `features/landing/BeforeAfter.tsx` | 1.18x → 1.31x count-up |
| `MotionRoot`, `useInViewOnce`, `tween`, `prefersReducedMotion` | `features/landing/MotionRoot.tsx` | Landing motion engine (see `docs/LANDING.md`) |
| `useExit` | `features/shell/useExit.ts` | `const { leaving, close } = useExit(onDone)`: plays a panel's exit animation, then closes (instantly with reduced motion) |
| `app-motion.css` | `features/shell/app-motion.css` | Product motion classes (see `docs/DESIGN.md` §7) |

## Adding a component
1. Check `/kit` and this file first; extend what exists before adding something new.
2. Use tokens only (`app/globals.css`). Square corners, 1 px borders, minimum 44 px targets.
3. Anything showing risk takes a `risk` or health value and uses `RiskEye` / `Health` / `Status`. Don't restyle tiers locally.
4. Add it to `/kit` and to this table in the same commit.
