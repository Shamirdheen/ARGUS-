import type { Position, Protocol } from "./types";

/** Reference prices for the demo book. Labelled "Demo" everywhere it shows. */
export const DEMO_PRICES: Record<string, number> = { SOL: 148.82, JitoSOL: 176.4, JupSOL: 162.1, JLP: 4.61, mSOL: 181.3 };

function make(
  id: string,
  protocol: Protocol,
  market: string,
  collateralAsset: string,
  collateralUsd: number,
  borrowAsset: string,
  borrowUsd: number,
  liquidationLtv: number,
  borrowApy: number,
): Position {
  const healthFactor = (collateralUsd * liquidationLtv) / borrowUsd;
  const priceUsd = DEMO_PRICES[collateralAsset] ?? 1;
  return {
    id,
    protocol,
    market,
    name: `${collateralAsset} / ${borrowAsset}`,
    collateralAsset,
    collateralUsd,
    borrowAsset,
    borrowUsd,
    healthFactor,
    liquidationLtv,
    priceUsd,
    liquidationPriceUsd: priceUsd / healthFactor,
    distanceToLiquidationPct: (1 - 1 / healthFactor) * 100,
    borrowApy,
    interestPerDayUsd: (borrowUsd * borrowApy) / 100 / 365,
  };
}

export function demoPositions(): Position[] {
  return [
    make("demo-kmn-sol-usdc", "Kamino", "Main Market", "SOL", 42_180, "USDC", 33_400, 0.85, 7.9),
    make("demo-kmn-jito-sol", "Kamino", "JitoSOL Multiply", "JitoSOL", 96_550, "SOL", 61_900, 0.9, 6.2),
    make("demo-jup-jlp-usdc", "Jupiter Lend", "JLP Vault", "JLP", 28_400, "USDC", 14_200, 0.82, 9.4),
    make("demo-jup-jupsol-sol", "Jupiter Lend", "JupSOL Vault", "JupSOL", 18_900, "SOL", 11_800, 0.92, 5.1),
    make("demo-kmn-msol-usdt", "Kamino", "Main Market", "mSOL", 54_300, "USDT", 16_100, 0.8, 8.3),
  ];
}
