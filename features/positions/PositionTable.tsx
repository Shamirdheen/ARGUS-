"use client";

import { CaretRight } from "@phosphor-icons/react";
import { cx, Health, Status } from "@/components/ui";
import { byRisk, pct, riskOf, usd } from "@/lib/positions/risk";
import type { Position } from "@/lib/positions/types";
import { usePortfolio } from "@/features/portfolio/PortfolioProvider";

export function PositionTable({ positions, compact = false }: { positions: Position[]; compact?: boolean }) {
  const { select } = usePortfolio();
  const rows = [...positions].sort(byRisk);

  return (
    <div className="relative border border-ink-800 overflow-x-auto">
      <table className="w-full text-[13px] border-collapse min-w-[640px]">
        <thead>
          <tr className="text-left text-[11px] uppercase tracking-[0.1em] text-sand-500">
            <th className="font-medium px-4 py-3">Position</th>
            <th className="font-medium px-4 py-3">Protocol</th>
            {!compact && <th className="font-medium px-4 py-3 text-right">Collateral</th>}
            {!compact && <th className="font-medium px-4 py-3 text-right">Debt</th>}
            <th className="font-medium px-4 py-3 text-right">To liquidation</th>
            <th className="font-medium px-4 py-3 text-right">Health</th>
            <th className="font-medium px-4 py-3 text-right">Status</th>
            <th className="w-10" aria-hidden />
          </tr>
        </thead>
        <tbody>
          {rows.map((p) => {
            const r = riskOf(p.healthFactor);
            const crit = r === "critical";
            return (
              <tr
                key={p.id}
                onClick={() => select(p.id)}
                className={cx(
                  "border-t cursor-pointer transition-colors",
                  crit ? "bg-risk-critical text-ink-950 border-risk-critical hover:bg-terra-300" : "border-ink-800 hover:bg-ink-850",
                  r === "safe" && "text-sand-500",
                )}
              >
                <td className="px-4 py-3.5">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      select(p.id);
                    }}
                    className={cx("font-medium text-left cursor-pointer", crit ? "text-ink-950" : r === "safe" ? "text-sand-300" : "text-sand-100")}
                  >
                    {p.name}
                  </button>
                  <div className={cx("text-[11px]", crit ? "text-ink-800" : "text-sand-500")}>{p.market}</div>
                </td>
                <td className="px-4 py-3.5">{p.protocol}</td>
                {!compact && <td className="px-4 py-3.5 text-right tabular-nums">{usd(p.collateralUsd)}</td>}
                {!compact && <td className="px-4 py-3.5 text-right tabular-nums">{usd(p.borrowUsd)}</td>}
                <td className="px-4 py-3.5 text-right tabular-nums">−{pct(p.distanceToLiquidationPct)}</td>
                <td className="px-4 py-3.5 text-right">
                  <Health value={p.healthFactor} onFill={crit} />
                </td>
                <td className="px-4 py-3.5">
                  <div className="flex justify-end">
                    <Status risk={r} onFill={crit} />
                  </div>
                </td>
                <td className="pr-3 text-right">
                  <CaretRight size={14} weight="light" aria-hidden />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
