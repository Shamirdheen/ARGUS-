"use client";

import Image from "next/image";
import Link from "next/link";
import { useRef, useState } from "react";
import { RiskEye } from "@/components/brand/RiskEye";
import { Health, Label } from "@/components/ui";
import { demoPositions } from "@/lib/positions/demo";
import { tween, useInViewOnce } from "./MotionRoot";
import { collateralToReach, hfAfterMove, hfText, repayToReach, riskLabel, riskOf } from "@/lib/positions/risk";

/** Three-step landing tutorial. Each step pairs an illustration with a working piece of the real app. */

function StepFrame({
  n,
  img,
  alt,
  title,
  body,
  delay = "0ms",
  children,
}: {
  n: string;
  img: string;
  alt: string;
  title: string;
  body: string;
  delay?: string;
  children: React.ReactNode;
}) {
  return (
    <article data-reveal style={{ "--d": delay } as React.CSSProperties} className="lift flex flex-col border border-ink-800 bg-ink-900 min-w-0">
      <figure className="lean m-0 relative aspect-square bg-terra-500 overflow-hidden">
        <Image src={img} alt={alt} fill sizes="(min-width: 1024px) 33vw, 100vw" className="object-cover" />
        <span className="absolute top-3 left-3 bg-ink-950 text-sand-200 text-[12px] font-medium px-2 py-1">{n}</span>
      </figure>
      <div className="flex flex-col gap-3 p-5 md:p-6 flex-1">
        <h3 className="font-display m-0 text-[20px] leading-[1.2] text-sand-100">{title}</h3>
        <p className="m-0 text-sm leading-relaxed text-sand-300">{body}</p>
        <div className="mt-auto pt-4 border-t border-ink-800">{children}</div>
      </div>
    </article>
  );
}

/** Step 1: drag health down and watch the eye open. */
function ReadTheEye() {
  const [hf, setHf] = useState(2.2);
  const ref = useRef<HTMLDivElement>(null);
  const stop = useRef<(() => void) | void>(undefined);
  const touched = useRef(false);
  // First time it's seen, the eye demonstrates itself: health falls and the lid opens. Any touch hands control over.
  useInViewOnce(ref, () => {
    setTimeout(() => {
      if (!touched.current) stop.current = tween(2.2, 1.05, 2600, setHf);
    }, 600);
  });
  const risk = riskOf(hf);
  return (
    <div ref={ref} className="flex flex-col gap-3">
      <div className="flex items-center justify-between gap-3">
        <span className="flex items-center gap-3">
          <RiskEye risk={risk} size={56} glow />
          <span className="text-[13px] text-sand-200">{riskLabel(risk)}</span>
        </span>
        <Health value={hf} className="text-[18px]" />
      </div>
      <input
        type="range"
        min={0.95}
        max={2.4}
        step={0.01}
        value={hf}
        onChange={(e) => setHf(Number(e.target.value))}
        onPointerDown={() => {
          touched.current = true;
          stop.current?.();
        }}
        aria-label="Health factor"
        className="w-full accent-[#efc796]"
      />
      <span className="text-[12px] text-sand-500">Drag health down. Below 1.00x the protocol can sell your collateral.</span>
    </div>
  );
}

/** Step 2: rehearse a SOL move on a demo loan and see the two ways back. */
function RehearseTheCrash() {
  const p = demoPositions().find((x) => x.id === "demo-kmn-msol-usdt")!;
  const [move, setMove] = useState(-30);
  const after = { ...p, healthFactor: hfAfterMove(p, move / 100), collateralUsd: p.collateralUsd * (1 + move / 100) };
  const r = riskOf(after.healthFactor);
  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between gap-3 text-[13px]">
        <span className="text-sand-300">
          {p.name} · SOL {move > 0 ? "+" : ""}
          {move}%
        </span>
        <span className="flex items-center gap-2">
          <RiskEye risk={r} />
          <Health value={after.healthFactor} />
        </span>
      </div>
      <input
        type="range"
        min={-70}
        max={10}
        step={1}
        value={move}
        onChange={(e) => setMove(Number(e.target.value))}
        aria-label="SOL price change"
        className="w-full accent-[#efc796]"
      />
      {after.healthFactor < 1.5 ? (
        <span className="text-[12px] text-sand-300">
          {after.healthFactor < 1 ? "Liquidated. " : ""}Back to 1.50x: add{" "}
          <b className="font-medium text-sand-100">${Math.round(collateralToReach(after, 1.5)).toLocaleString()}</b> or repay{" "}
          <b className="font-medium text-sand-100">${Math.round(repayToReach(after, 1.5)).toLocaleString()}</b>.
        </span>
      ) : (
        <span className="text-[12px] text-sand-500">Comfortable at this price. Drag further.</span>
      )}
    </div>
  );
}

/** Step 3: what an Ask Argus answer looks like. Static; the real one lives in the app. */
function AskPreview() {
  const p = demoPositions().find((x) => x.id === "demo-kmn-sol-usdc")!;
  const add = Math.round(collateralToReach(p, 1.5) / 10) * 10;
  return (
    <div className="flex flex-col gap-2.5 text-[13px]">
      <div className="self-end bg-ink-850 border border-ink-700 px-3 py-2 text-sand-100">Which breaks first if SOL drops 25%?</div>
      <p className="m-0 text-sand-300 leading-relaxed">
        <b className="font-medium text-sand-100">SOL / USDC on Kamino</b> goes first: {hfText(p.healthFactor)} falls to {hfText(hfAfterMove(p, -0.25))}. Add ${add.toLocaleString()} to get it to 1.50x.
      </p>
      <div className="flex items-center justify-between gap-3">
        <Link href="/app" className="text-sand-200 hover:text-sand-100 underline underline-offset-4">
          Try it in the app →
        </Link>
        <kbd className="text-[11px] text-sand-500 border border-ink-700 px-1.5 py-px">⌘K</kbd>
      </div>
    </div>
  );
}

export function Tutorial() {
  return (
    <section id="tutorial" className="mx-auto max-w-[1360px] w-full px-4 md:px-6 py-16 md:py-20 flex flex-col gap-8">
      <div data-reveal className="flex flex-col gap-3 max-w-[760px]">
        <Label className="!text-terra-400">A short tutorial</Label>
        <h2 className="font-display m-0 text-[28px] md:text-[40px] leading-[1.1] text-sand-100">Three things Argus teaches you.</h2>
        <p className="m-0 text-[15px] leading-relaxed text-sand-300">Each one works right here, on a demo position. Try them before you connect anything.</p>
      </div>
      <div className="grid gap-4 lg:grid-cols-3">
        <StepFrame
          n="01"
          img="/brand/tut-eye.jpg"
          alt="Argus raising a hand toward three eyes: one nearly closed, one half open, one wide open and glowing"
          title="Read the eye"
          body="Every position gets an eye. Calm and half-shut when it's safe, wide open and glowing when it needs you. No colours to decode."
        >
          <ReadTheEye />
        </StepFrame>
        <StepFrame
          n="02"
          delay="140ms"
          img="/brand/tut-dial.jpg"
          alt="Argus turning a bronze wheel while the water level in a tall vessel falls toward a marked notch"
          title="Rehearse the crash"
          body="Move the price before the market does. Argus shows how far health falls and the exact amount that gets you back to 1.50x."
        >
          <RehearseTheCrash />
        </StepFrame>
        <StepFrame
          n="03"
          delay="280ms"
          img="/brand/tut-ask.jpg"
          alt="Argus at his laptop, the screen showing a rising line and a gauge"
          title="Ask in plain words"
          body="Press ⌘K and ask anything about your positions. Argus answers in numbers and ends with the one thing to do next."
        >
          <AskPreview />
        </StepFrame>
      </div>
    </section>
  );
}
