export type Protocol = "Kamino" | "Jupiter Lend";

/** Where the user goes to add collateral or repay. Argus never signs; the protocol's own app does. */
export const PROTOCOL_APP_URL: Record<Protocol, string> = {
  Kamino: "https://app.kamino.finance/",
  "Jupiter Lend": "https://jup.ag/lend",
};
export type Risk = "safe" | "watch" | "warning" | "critical";
export type DataSource = "live" | "demo";

/** One lending position, normalised across protocols. All USD values are numbers, not strings. */
export interface Position {
  id: string;
  protocol: Protocol;
  market: string;
  name: string;
  collateralAsset: string;
  collateralUsd: number;
  borrowAsset: string;
  borrowUsd: number;
  healthFactor: number;
  /** Fraction (0–1) of collateral value at which liquidation starts. */
  liquidationLtv: number;
  /** Price of the collateral asset now, and the price where HF hits 1.0. */
  priceUsd: number;
  liquidationPriceUsd: number;
  /** % price fall in the collateral asset before liquidation. */
  distanceToLiquidationPct: number;
  borrowApy: number;
  interestPerDayUsd: number;
}

export interface PortfolioSnapshot {
  wallet: string | null;
  source: DataSource;
  /** Why we are on demo data, if we are. */
  note?: string;
  updatedAt: string;
  positions: Position[];
}
