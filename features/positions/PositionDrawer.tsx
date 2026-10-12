"use client";

import { X } from "@phosphor-icons/react";
import { useCallback, useEffect, useState } from "react";
import { RiskEye } from "@/components/brand/RiskEye";
import { Button, Health, Label, Status } from "@/components/ui";
import { collateralToReach, hfAfterMove, hfText, pct, repayToReach, riskOf, usd } from "@/lib/positions/risk";
import { usePortfolio } from "@/features/portfolio/PortfolioProvider";
import { useExit } from "@/features/shell/useExit";

/** Position detail: numbers, a price rehearsal slider, and the two ways out. */
export function PositionDrawer() {
  const { snapshot, selectedId, select, ask } = usePortfolio();
  const p = snapshot?.positions.find((x) => x.id === selectedId) ?? null;
  // The rehearsal resets whenever a different position is opened.
  const [rehearsal, setRehearsal] = useState({ id: selectedId, move: 0 });
  const move = rehearsal.id === selectedId ? rehearsal.move : 0;
  const setMove = (v: number) => setRehearsal({ id: selectedId, move: v });
  const { leaving, close } = useExit(useCallback(() => select(null), [select]));

  useEffect(() => {
    if (!p) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && close();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [p, close]);

  if (!p) return null;
  const risk = riskOf(p.healthFactor);
  const simHf = hfAfterMove(p, move / 100);
  const simRisk = riskOf(simHf);
  const add = collateralToReach(p, 1.5);
  const repay = repayToReach(p, 1.5);

  const row = (k: string, v: React.ReactNode) => (
    <div className="flex justify-between gap-4 py-2.5 border-t border-ink-800 text-[13px]">
      <span className="text-sand-500">{k}</span>
      <span className="text-sand-100 tabular-nums text-right">{v}</span>
    </div>
  );

  return (
    <div className="fixed inset-0 z-40" role="dialog" aria-modal="true" aria-label={`${p.name} details`}>
      <button
        type="button"
        aria-label="Close"
        className={`${leaving ? "backdrop-out" : "backdrop-in"} absolute inset-0 bg-ink-950/70 cursor-default`}
        onClick={close}
      />
      <aside className={`${leaving ? "panel-out" : "panel-in"} absolute top-0 right-0 bottom-0 w-full max-w-[520px] bg-ink-900 border-l border-ink-700 flex flex-col`}>
        <div className="flex items-start justify-between gap-4 px-5 py-4 border-b border-ink-800">
          <div className="flex flex-col gap-1 min-w-0">
            <Label>
              {p.protocol} · {p.market}
            </Label>
            <span className="font-display text-[20px] text-sand-100 truncate">{p.name}</span>
          </div>
          <button type="button" onClick={close} aria-label="Close" className="min-w-10 min-h-10 grid place-items-center border border-ink-700 text-sand-200 cursor-pointer hover:bg-ink-850">
            <X size={18} weight="light" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-5 py-5 flex flex-col gap-6">
          <div className="flex items-center gap-5">
            <span className="eye-wake" style={{ "--d": "260ms" } as React.CSSProperties}>
              <RiskEye risk={risk} size={84} glow />
            </span>
            <div className="flex flex-col gap-1.5">
              <Label>Health factor</Label>
              <Health value={p.healthFactor} className="font-display !font-normal text-[34px]" />
              <Status risk={risk} />
            </div>
          </div>

          <div>
            {row("Collateral", `${usd(p.collateralUsd)} in ${p.collateralAsset}`)}
            {row("Debt", `${usd(p.borrowUsd)} in ${p.borrowAsset}`)}
            {row("Liquidation LTV", pct(p.liquidationLtv * 100, 0))}
            {p.priceUsd > 0 && row(`${p.collateralAsset} price`, usd(p.priceUsd, 2))}
            {p.liquidationPriceUsd > 0 && row("Liquidation price", usd(p.liquidationPriceUsd, 2))}
            {row("Distance to liquidation", `−${pct(p.distanceToLiquidationPct)}`)}
            {p.borrowApy > 0 && row("Borrow APY", pct(p.borrowApy))}
            {p.interestPerDayUsd > 0 && row("Interest per day", usd(p.interestPerDayUsd, 2))}
          </div>

          <div className="flex flex-col gap-3 p-4 border border-dashed border-sand-600">
            <div className="flex justify-between items-baseline">
              <Label>Rehearse a price move</Label>
              <span className="text-[13px] text-sand-100 tabular-nums">
                {p.collateralAsset} {move > 0 ? "+" : ""}
                {move}%
              </span>
            </div>
            <input
              type="range"
              min={-50}
              max={20}
              step={1}
              value={move}
              onChange={(e) => setMove(Number(e.target.value))}
              aria-label={`${p.collateralAsset} price change`}
              className="w-full accent-[#efc796]"
            />
            <div className="flex items-center justify-between">
              <span className="text-[13px] text-sand-500">Health becomes</span>
              <span className="flex items-center gap-3">
                <RiskEye risk={simRisk} />
                <Health value={simHf} />
              </span>
            </div>
            {simHf < 1 && <p className="msg-in m-0 text-[13px] text-risk-critical">Liquidated at this price.</p>}
          </div>

          {p.healthFactor < 1.5 && (
            <div className="enter flex flex-col gap-3" style={{ "--d": "320ms" } as React.CSSProperties}>
              <Label>Two ways back to 1.50x</Label>
              <div className="grid grid-cols-2 gap-3">
                <div className="border border-ink-700 p-3.5 flex flex-col gap-1">
                  <span className="text-[12px] text-sand-500">Add collateral</span>
                  <span className="text-[17px] font-medium text-sand-100 tabular-nums">{usd(add)}</span>
                </div>
                <div className="border border-ink-700 p-3.5 flex flex-col gap-1">
                  <span className="text-[12px] text-sand-500">Or repay</span>
                  <span className="text-[17px] font-medium text-sand-100 tabular-nums">{usd(repay)}</span>
                </div>
              </div>
              <p className="m-0 text-[12px] text-sand-500">
                Do it on {p.protocol}. Argus is read-only: it never moves your funds.
              </p>
            </div>
          )}
        </div>

        <div className="border-t border-ink-800 px-5 py-4 flex gap-2 flex-wrap">
          <Button
            kind="primary"
            onClick={() => {
              select(null);
              ask(`Walk me through ${p.name} on ${p.protocol}. Health is ${hfText(p.healthFactor)}. What should I do?`);
            }}
          >
            Ask Argus about this
          </Button>
          <Button kind="secondary" onClick={close}>
            Close
          </Button>
        </div>
      </aside>
    </div>
  );
}
