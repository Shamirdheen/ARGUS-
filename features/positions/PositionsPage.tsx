"use client";

import { OpeningEye } from "@/components/brand/RiskEye";
import { H1, Label } from "@/components/ui";
import { usePortfolio } from "@/features/portfolio/PortfolioProvider";
import { PositionTable } from "./PositionTable";

export function PositionsPage() {
  const { snapshot, loading } = usePortfolio();
  if (loading && !snapshot) return <OpeningEye />;
  const positions = snapshot?.positions ?? [];
  return (
    <div className="flex flex-col gap-6">
      <div className="enter flex flex-col gap-2">
        <Label>Kamino · Jupiter Lend · sorted by risk</Label>
        <H1>Positions</H1>
      </div>
      <PositionTable positions={positions} />
      <p className="enter m-0 text-[12px] text-sand-500" style={{ "--d": "500ms" } as React.CSSProperties}>
        Health = liquidation-weighted collateral ÷ debt. Below 1.00x the protocol can liquidate. Tiers: Safe ≥ 2.00x · Watch ≥ 1.50x · Warning ≥ 1.20x · Act now below.
      </p>
    </div>
  );
}
