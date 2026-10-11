import type { Position, Risk } from "./types";

/** UI tiers. The chat prompt uses the same thresholds. */
export const TIERS: { risk: Risk; min: number; label: string }[] = [
  { risk: "safe", min: 2.0, label: "Safe" },
  { risk: "watch", min: 1.5, label: "Watch" },
  { risk: "warning", min: 1.2, label: "Warning" },
  { risk: "critical", min: 0, label: "Act now" },
];

export function riskOf(hf: number): Risk {
  for (const t of TIERS) if (hf >= t.min) return t.risk;
  return "critical";
}

export const riskLabel = (r: Risk) => TIERS.find((t) => t.risk === r)!.label;

const ORDER: Record<Risk, number> = { critical: 0, warning: 1, watch: 2, safe: 3 };
export const byRisk = (a: Position, b: Position) =>
  ORDER[riskOf(a.healthFactor)] - ORDER[riskOf(b.healthFactor)] || a.healthFactor - b.healthFactor;

/** Health factor after the collateral asset moves by `pct` (e.g. -0.25). Borrow assumed stable. */
export function hfAfterMove(p: Position, pct: number) {
  return p.healthFactor * (1 + pct);
}

/** Collateral (USD) needed to bring a position to `target` HF. */
export function collateralToReach(p: Position, target: number) {
  const needed = (target * p.borrowUsd) / p.liquidationLtv - p.collateralUsd;
  return Math.max(0, needed);
}

/** Debt (USD) to repay to bring a position to `target` HF. */
export function repayToReach(p: Position, target: number) {
  const maxDebt = (p.collateralUsd * p.liquidationLtv) / target;
  return Math.max(0, p.borrowUsd - maxDebt);
}

export function summarise(positions: Position[]) {
  const collateral = positions.reduce((s, p) => s + p.collateralUsd, 0);
  const debt = positions.reduce((s, p) => s + p.borrowUsd, 0);
  const worst = [...positions].sort(byRisk)[0];
  const counts = { safe: 0, watch: 0, warning: 0, critical: 0 } as Record<Risk, number>;
  positions.forEach((p) => counts[riskOf(p.healthFactor)]++);
  return { collateral, debt, net: collateral - debt, worst, counts };
}

export const usd = (n: number, digits = 0) =>
  n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: digits, minimumFractionDigits: digits });
export const hfText = (n: number) => `${n.toFixed(2)}x`;
export const pct = (n: number, digits = 1) => `${n.toFixed(digits)}%`;
