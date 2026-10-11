import type { Position } from "./types";

/**
 * Kamino adapter — reads obligations from Kamino's public REST API.
 * Untested against the live API from the build sandbox (network blocked there):
 * every field is read defensively, and any failure returns null so the caller falls back to demo.
 */
const API = process.env.KAMINO_API_URL || "https://api.kamino.finance";
const MAIN_MARKET = "7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF";

type Stats = Record<string, string | number | undefined>;
const num = (v: unknown) => (v === undefined || v === null || v === "" ? NaN : Number(v));

export async function kaminoPositions(wallet: string): Promise<Position[] | null> {
  try {
    const res = await fetch(`${API}/kamino-market/${MAIN_MARKET}/users/${wallet}/obligations`, {
      headers: { accept: "application/json" },
      signal: AbortSignal.timeout(6000),
    });
    if (!res.ok) return null;
    const data = (await res.json()) as unknown;
    if (!Array.isArray(data)) return null;

    const out: Position[] = [];
    for (const o of data as { obligationAddress?: string; refreshedStats?: Stats }[]) {
      const s = o.refreshedStats ?? {};
      const collateralUsd = num(s.userTotalDeposit);
      const borrowUsd = num(s.userTotalBorrow);
      if (!(borrowUsd > 0) || !(collateralUsd > 0)) continue; // supply-only: no liquidation risk
      const liqLimit = num(s.borrowLiquidationLimit);
      const adjBorrow = num(s.userTotalBorrowBorrowFactorAdjusted);
      const liquidationLtv = num(s.liquidationLtv) || (liqLimit > 0 ? liqLimit / collateralUsd : 0.85);
      const healthFactor =
        liqLimit > 0 && adjBorrow > 0 ? liqLimit / adjBorrow : (collateralUsd * liquidationLtv) / borrowUsd;
      if (!Number.isFinite(healthFactor)) continue;
      out.push({
        id: o.obligationAddress ?? `kamino-${out.length}`,
        protocol: "Kamino",
        market: "Main Market",
        name: `Kamino obligation ${(o.obligationAddress ?? "").slice(0, 4)}…`,
        collateralAsset: "Mixed",
        collateralUsd,
        borrowAsset: "Mixed",
        borrowUsd,
        healthFactor,
        liquidationLtv,
        priceUsd: 0,
        liquidationPriceUsd: 0,
        distanceToLiquidationPct: (1 - 1 / healthFactor) * 100,
        borrowApy: 0,
        interestPerDayUsd: 0,
      });
    }
    return out;
  } catch {
    return null;
  }
}
