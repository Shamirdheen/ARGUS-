"use client";

import Link from "next/link";
import { RiskEye, OpeningEye } from "@/components/brand/RiskEye";
import { Button, Card, H1, H2, Health, Label, Stat } from "@/components/ui";
import { PositionTable } from "@/features/positions/PositionTable";
import { hfAfterMove, hfText, pct, riskLabel, riskOf, summarise, usd } from "@/lib/positions/risk";
import { usePortfolio } from "./PortfolioProvider";

const SHOCKS = [-10, -25, -40];

export function Overview() {
  const { snapshot, loading, ask, select } = usePortfolio();

  if (loading && !snapshot) return <OpeningEye />;
  if (!snapshot) return <p className="text-sand-500">Argus couldn&apos;t load positions. Refresh to try again.</p>;

  const { positions } = snapshot;
  if (positions.length === 0)
    return (
      <Card className="items-start">
        <H2>Nothing to watch yet</H2>
        <p className="m-0 text-sand-500 text-sm">No open borrows on Kamino or Jupiter Lend for this wallet.</p>
      </Card>
    );

  const s = summarise(positions);
  const worst = s.worst;
  const worstRisk = riskOf(worst.healthFactor);
  const updated = new Date(snapshot.updatedAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div className="flex flex-col gap-2">
          <Label>
            {snapshot.source === "demo" ? "Demo book" : "Your wallet"} · {positions.length} positions · updated {updated}
          </Label>
          <H1>Portfolio risk</H1>
        </div>
        <Button kind="secondary" small onClick={() => ask("Am I safe? Which position needs me first?")}>
          Am I safe?
        </Button>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1.3fr_1fr]">
        <Card className={worstRisk === "critical" ? "!bg-ink-850 !border-terra-700" : ""}>
          <Label>Closest to liquidation</Label>
          <div className="flex items-center gap-5">
            <RiskEye risk={worstRisk} size={96} glow />
            <div className="flex flex-col gap-1 min-w-0">
              <span className="text-sand-100 font-medium truncate">
                {worst.name} · {worst.protocol}
              </span>
              <Health value={worst.healthFactor} className="font-display !font-normal text-[40px] leading-none" />
              <span className="text-[13px] text-sand-500">
                {riskLabel(worstRisk)} · liquidated after a −{pct(worst.distanceToLiquidationPct)} move
              </span>
            </div>
          </div>
          <div className="flex gap-2 flex-wrap">
            <Button small onClick={() => select(worst.id)}>
              Open position
            </Button>
            <Button kind="simulate" small onClick={() => ask(`How do I get ${worst.name} on ${worst.protocol} back above 1.5x?`)}>
              How do I fix it?
            </Button>
          </div>
        </Card>

        <Card>
          <div className="grid grid-cols-2 gap-5">
            <Stat label="Collateral" value={usd(s.collateral)} />
            <Stat label="Debt" value={usd(s.debt)} />
            <Stat label="Net" value={usd(s.net)} />
            <Stat
              label="Needs you"
              value={`${s.counts.critical + s.counts.warning} of ${positions.length}`}
              sub={`${s.counts.critical} act now · ${s.counts.warning} warning`}
            />
          </div>
        </Card>
      </div>

      <section className="flex flex-col gap-3">
        <div className="flex items-baseline justify-between gap-4">
          <H2>If SOL falls</H2>
          <span className="text-[12px] text-sand-500">Assumes all SOL-linked collateral moves together</span>
        </div>
        <div className="grid gap-3 sm:grid-cols-3">
          {SHOCKS.map((m) => {
            const after = positions.map((p) => hfAfterMove(p, m / 100));
            const gone = after.filter((h) => h < 1).length;
            const minHf = Math.min(...after);
            return (
              <button
                key={m}
                type="button"
                onClick={() => ask(`What happens to my positions if SOL drops ${Math.abs(m)}%?`)}
                className="text-left bg-ink-900 border border-ink-800 hover:border-ink-700 p-4 flex flex-col gap-2 cursor-pointer"
              >
                <span className="font-display text-[22px] text-sand-100">
                  −{Math.abs(m)}
                  <span className="font-mono text-[18px] ml-0.5">%</span>
                </span>
                <span className="flex items-center gap-2 text-[13px]">
                  <RiskEye risk={riskOf(minHf)} />
                  <span className={gone ? "text-risk-critical font-medium" : "text-sand-300"}>
                    {gone ? `${gone} liquidated` : "None liquidated"}
                  </span>
                </span>
                <span className="text-[12px] text-sand-500">Lowest health {hfText(Math.max(minHf, 0))}</span>
              </button>
            );
          })}
        </div>
      </section>

      <section className="flex flex-col gap-3">
        <div className="flex items-baseline justify-between gap-4">
          <H2>Positions</H2>
          <Link href="/app/positions" className="text-[13px] text-sand-300 hover:text-sand-100">
            All details →
          </Link>
        </div>
        <PositionTable positions={positions} compact />
      </section>
    </div>
  );
}
