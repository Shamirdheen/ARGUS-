import { demoPositions } from "@/lib/positions/demo";
import { kaminoPositions } from "@/lib/positions/kamino";
import type { PortfolioSnapshot } from "@/lib/positions/types";

const BASE58 = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;

export async function GET(request: Request) {
  const wallet = new URL(request.url).searchParams.get("wallet");
  const now = new Date().toISOString();

  if (!wallet || !BASE58.test(wallet)) {
    return Response.json({ wallet: null, source: "demo", updatedAt: now, positions: demoPositions() } satisfies PortfolioSnapshot);
  }

  const kamino = await kaminoPositions(wallet);
  if (kamino && kamino.length > 0) {
    return Response.json({ wallet, source: "live", updatedAt: now, positions: kamino } satisfies PortfolioSnapshot);
  }

  return Response.json({
    wallet,
    source: "demo",
    note: kamino === null ? "Couldn't reach Kamino. Showing the demo book." : "No open borrows on Kamino for this wallet. Showing the demo book.",
    updatedAt: now,
    positions: demoPositions(),
  } satisfies PortfolioSnapshot);
}
