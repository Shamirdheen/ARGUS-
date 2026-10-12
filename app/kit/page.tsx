import type { Metadata } from "next";
import { OpeningEye, RiskEye } from "@/components/brand/RiskEye";
import { Button, Card, H1, H2, Health, Label, Stat, Status } from "@/components/ui";
import { TIERS, riskLabel } from "@/lib/positions/risk";
import type { Risk } from "@/lib/positions/types";
import "@/features/shell/app-motion.css";

/**
 * Living component catalogue. Renders the real components, so it can't drift from the code.
 * Internal reference for designers and agents; not linked from the product and not indexed.
 */
export const metadata: Metadata = { title: "Component kit", robots: { index: false, follow: false } };

const SAMPLE_HF: Record<Risk, number> = { safe: 2.7, watch: 1.64, warning: 1.31, critical: 1.07 };
const COLORS = [
  ["terra-500", "#c0551e"], ["terra-400", "#d06f3c"], ["terra-300", "#e0946a"],
  ["ink-950", "#16110c"], ["ink-900", "#1e1711"], ["ink-850", "#271e16"], ["ink-800", "#33271d"], ["ink-700", "#482a16"],
  ["sand-100", "#f6ddb8"], ["sand-200", "#efc796"], ["sand-500", "#a8865f"], ["sand-600", "#7e654a"],
] as const;

function Section({ title, note, delay = 0, children }: { title: string; note?: string; delay?: number; children: React.ReactNode }) {
  return (
    <section className="enter flex flex-col gap-4 border-t border-ink-800 pt-8" style={{ "--d": `${delay}ms` } as React.CSSProperties}>
      <div className="flex flex-col gap-1.5">
        <H2>{title}</H2>
        {note && <p className="m-0 text-[13px] text-sand-500 max-w-[760px]">{note}</p>}
      </div>
      {children}
    </section>
  );
}

export default function Kit() {
  return (
    <main className="mx-auto max-w-[1280px] px-4 md:px-8 py-12 flex flex-col gap-10">
      <div className="enter flex flex-col gap-2">
        <Label>Argus v2 · live components · rules in docs/DESIGN.md</Label>
        <H1>Component kit</H1>
      </div>

      <Section delay={60} title="Colour" note="Three colours, two surfaces. No other hues anywhere, charts included.">
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3">
          {COLORS.map(([n, hex], i) => (
            <div key={n} className="enter flex flex-col gap-1.5" style={{ "--d": `${120 + i * 30}ms` } as React.CSSProperties}>
              <div className="h-14 border border-ink-800" style={{ background: hex }} />
              <span className="text-[12px] text-sand-100">{n}</span>
              <span className="text-[11px] text-sand-500">{hex}</span>
            </div>
          ))}
        </div>
      </Section>

      <Section delay={120} title="Type" note="Michroma speaks (titles, headings, one hero number). IBM Plex Mono works (everything else).">
        <div className="flex flex-col gap-3">
          <span className="font-display text-[56px] leading-[1.05] text-sand-100">A hundred eyes</span>
          <H1>Portfolio risk</H1>
          <H2>Active positions</H2>
          <span className="font-display text-[40px] text-risk-warning">1.31x</span>
          <p className="m-0 text-[15px] leading-relaxed text-sand-200 max-w-[640px]">
            Argus never sleeps. It watches every Solana position and tells you what to do before the liquidators do.
          </p>
          <Label>Health factor</Label>
          <span className="text-[14px] tabular-nums text-sand-200">$1,842,500 · −3.21% · 1.31x</span>
        </div>
      </Section>

      <Section delay={180} title="Buttons" note="Primary: one per view. Simulate: anything hypothetical. Danger: only for acting on a risky position.">
        <div className="flex flex-wrap gap-3">
          <Button>Primary</Button>
          <Button kind="secondary">Secondary</Button>
          <Button kind="simulate">Simulate</Button>
          <Button kind="danger">Danger</Button>
          <Button kind="ghost">Ghost</Button>
          <Button disabled>Disabled</Button>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button small>Primary small</Button>
          <Button kind="secondary" small>Secondary small</Button>
          <Button kind="simulate" small>Simulate small</Button>
        </div>
      </Section>

      <Section delay={240} title="Risk tiers" note="Lightness, weight, the eye and a word. Never hue alone. Critical is the only row that changes background.">
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {TIERS.map(({ risk, min }) => {
            const crit = risk === "critical";
            return (
              <div key={risk} className={`p-4 border flex flex-col gap-3 ${crit ? "bg-risk-critical border-risk-critical" : "bg-ink-900 border-ink-800"}`}>
                <span className={`text-[12px] ${crit ? "text-ink-950" : "text-sand-500"}`}>
                  {riskLabel(risk)} · {crit ? "< 1.20x" : `≥ ${min.toFixed(2)}x`}
                </span>
                <div className="flex items-center justify-between">
                  <Health value={SAMPLE_HF[risk]} onFill={crit} className="text-[18px]" />
                  <Status risk={risk} onFill={crit} />
                </div>
              </div>
            );
          })}
        </div>
      </Section>

      <Section delay={300} title="Risk eye" note="Lid and iris ease over 600 ms; critical glows and pulses. Sizes 22 (rows), 56–60 (cards), 84–96 (hero).">
        <div className="flex flex-wrap items-end gap-10">
          {(["safe", "watch", "warning", "critical"] as Risk[]).map((r, i) => (
            <div key={r} className="eye-wake flex flex-col items-center gap-3" style={{ "--d": `${500 + i * 120}ms` } as React.CSSProperties}>
              <RiskEye risk={r} size={96} glow />
              <div className="flex items-end gap-3">
                <RiskEye risk={r} size={56} />
                <RiskEye risk={r} />
              </div>
              <span className="text-[12px] text-sand-500">{riskLabel(r)}</span>
            </div>
          ))}
        </div>
      </Section>

      <Section delay={360} title="Cards and stats">
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <Label>Closest to liquidation</Label>
            <div className="flex items-center gap-4">
              <RiskEye risk="warning" size={72} />
              <Health value={1.31} className="font-display !font-normal text-[34px]" />
            </div>
          </Card>
          <Card>
            <div className="grid grid-cols-2 gap-5">
              <Stat label="Collateral" value="$240,330" />
              <Stat label="Debt" value="$137,400" />
              <Stat label="Net" value="$102,930" />
              <Stat label="Needs you" value="3 of 5" sub="1 act now · 2 warning" />
            </div>
          </Card>
        </div>
      </Section>

      <Section delay={480} title="Motion" note="Product motion classes (features/shell/app-motion.css). Hover the card; the eye below woke when this page loaded.">
        <div className="grid gap-4 md:grid-cols-3">
          <div className="lift bg-ink-900 border border-ink-800 p-5 flex flex-col gap-2 cursor-default">
            <span className="text-sand-100 text-sm">.lift</span>
            <span className="text-[12px] text-sand-500">Hover affordance for clickable cards</span>
          </div>
          <div className="bg-ink-900 border border-ink-800 p-5 flex flex-col gap-2">
            <span className="flex items-center gap-2 text-sand-100 text-sm">
              <span aria-hidden className="heartbeat size-1.5 rounded-full bg-sand-200" /> .heartbeat
            </span>
            <span className="text-[12px] text-sand-500">Argus is watching (30 s refresh)</span>
          </div>
          <div className="bg-ink-900 border border-ink-800 p-5 flex flex-col gap-2">
            <span className="caret text-sand-100 text-sm">.caret</span>
            <span className="text-[12px] text-sand-500">The streaming answer in Ask Argus</span>
          </div>
        </div>
      </Section>

      <Section delay={420} title="States" note="Loading uses the opening eye. Empty and error copy name what happened (see docs/DESIGN.md, Voice).">
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <Label>Loading</Label>
            <OpeningEye />
          </Card>
          <Card>
            <Label>Empty</Label>
            <span className="text-sand-100">Nothing to watch yet.</span>
            <span className="text-[13px] text-sand-500">No open borrows on Kamino or Jupiter Lend for this wallet.</span>
          </Card>
          <Card>
            <Label>Error</Label>
            <span className="text-risk-warning text-[14px]">Argus lost sight for a moment. Try again.</span>
          </Card>
        </div>
      </Section>
    </main>
  );
}
