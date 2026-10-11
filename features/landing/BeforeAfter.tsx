"use client";

import { useRef, useState } from "react";
import { RiskEye } from "@/components/brand/RiskEye";
import { Label } from "@/components/ui";
import { riskOf } from "@/lib/positions/risk";
import { tween, useInViewOnce } from "./MotionRoot";

/** 1.18x → 1.31x, played once when it scrolls into view: the number climbs and the eye calms down. */
export function BeforeAfter() {
  const ref = useRef<HTMLDivElement>(null);
  const [after, setAfter] = useState(1.18);

  useInViewOnce(ref, () => {
    setTimeout(() => tween(1.18, 1.31, 1600, setAfter), 500);
  });

  const r = riskOf(after);
  return (
    <div ref={ref} className="flex flex-wrap gap-7 items-center p-6 md:p-9 border border-ink-800 bg-ink-900">
      <div className="flex flex-col gap-1.5">
        <Label>Before</Label>
        <span className="font-display text-[44px] md:text-[56px] leading-none text-risk-warning">1.18x</span>
        <RiskEye risk="critical" size={60} glow />
      </div>
      <span aria-hidden className="text-[40px] text-sand-600">
        →
      </span>
      <div className="flex flex-col gap-1.5">
        <Label>After a $9,000 buffer</Label>
        <span className="font-display text-[44px] md:text-[56px] leading-none text-sand-200 tabular-nums" aria-label="1.31x">
          {after.toFixed(2)}x
        </span>
        <RiskEye risk={r} size={60} glow={r === "critical"} />
      </div>
      <p className="flex-[1_1_300px] min-w-0 m-0 text-sm leading-relaxed text-sand-300">
        Example: a SOL / USDC loan on Kamino at 1.18x survives about a −15% day. Argus shows the exact top-up; at 1.31x the same position survives −24%.
      </p>
    </div>
  );
}
