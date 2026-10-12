# Argus architecture

## Today (v2 launch)

```
Browser (Next.js client)
 ├─ Wallet Standard (Phantom / Solflare / Backpack): public key only, never a signature
 ├─ PortfolioProvider ── every 30s ──► GET  /api/positions?wallet=…
 └─ AskPanel ───────────────────────► POST /api/chat {messages, snapshot}
                                         streams NDJSON: text | action | error | done
Vercel (serverless, no database)
 ├─ app/api/positions/route.ts
 │    validate base58 → Kamino adapter (REST, 6s timeout)
 │    → borrows found ? source:"live" : demo book + note
 ├─ app/api/chat/route.ts
 │    system prompt (features/ask/prompt.ts) + positions JSON with precomputed numbers
 │    → Claude (ARGUS_MODEL, default claude-sonnet-5-5), streaming, ≤ 3 tool rounds
 │         simulate_price_move → computed server-side with risk.ts
 │         suggest_action      → forwarded to the UI as a button
 └─ lib/positions/
      types.ts   one Position type for every protocol
      risk.ts    tiers + all maths (shared by UI, chat tools, future watcher)
      kamino.ts  Kamino REST adapter (fallback to demo on any failure)
      demo.ts    labelled demo book
```

**Language:** TypeScript everywhere (Next.js 16 route handlers on Node). There are no smart contracts. Argus only reads the chain.

**Design rules behind it:**
- Every protocol maps into one `Position` type, so the UI and the chat never know where data came from.
- All maths lives in pure functions in `risk.ts`, so the slider, the drawer and Claude's tools agree.
- Claude never does arithmetic. It quotes numbers the server computed.
- Secrets (`ANTHROPIC_API_KEY`) are server-only. Empty env vars count as unset.

## Known gaps (in risk order)

1. **"Never sleeps" isn't true yet.** Argus only watches while a tab is open: no background job, no alerts.
2. **`/api/chat` trusts client-sent positions and has no rate limit.** Spam would cost Claude credits.
3. **No caching.** Every tab polls Kamino every 30 s.
4. **Thin data.** The Kamino field mapping is unverified against a live borrow, Kamino positions show "Mixed" with no per-asset liquidation price, Jupiter Lend is demo-only, and prices are demo values.
5. **No tests or logging** for the money maths.

## Upgrade plan

### Phase 1: harden (1–2 days)
- Chat takes `wallet`, not `snapshot`. The server fetches positions itself. Add a rate limit per IP and wallet (Upstash Redis / Vercel KV).
- `ProtocolAdapter { id; fetch(wallet): Promise<Position[]> }` registry, run with `Promise.allSettled`, so one protocol failing never hides the others. Then add the Jupiter Lend adapter.
- Cache positions for each wallet for 15–30 s.
- Prices from Pyth's price service (Hermes). Kamino asset names and per-asset liquidation prices.
- Validate every API response's shape with `zod`. Unit-test `risk.ts`.

### Phase 2: make "never sleeps" true (3–5 days)
- **Supabase Postgres** tables: `watched_wallets`, `alert_rules` (wallet, threshold, channel), `alert_events`, `health_snapshots`.
- **Watcher** every 1–5 min: fetch → compare against rules → send. Vercel's free plan limits scheduled jobs, so use Supabase `pg_cron` / an Edge Function or a small worker.
- Channels: Telegram bot → email (Resend) → web push.
- This unlocks Alerts, Activity, the living favicon and later Radar (see `design/`).

### Phase 3: auto-protect (only after a security review)
- Argus builds normal Kamino repay or deposit transactions, signed under a limited, revocable permission (session key / Squads rule / spending limit). Still TypeScript.
- A custom Anchor (Rust) "guardian" program only if users need on-chain guarantees, and then with an audit first.
- If ML is ever added (predicting volatility or risk), it gets a separate Python/FastAPI service that reads `health_snapshots`. The core stays TypeScript.
