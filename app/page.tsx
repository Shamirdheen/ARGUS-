import Image from "next/image";
import Link from "next/link";
import { Health, Label, Status } from "@/components/ui";
import { ScanForm } from "@/features/landing/ScanForm";
import { Tutorial } from "@/features/landing/Tutorial";
import { BeforeAfter } from "@/features/landing/BeforeAfter";
import { MotionRoot } from "@/features/landing/MotionRoot";
import type { CSSProperties } from "react";
import { demoPositions } from "@/lib/positions/demo";
import { byRisk, riskOf } from "@/lib/positions/risk";

const PROOF = [
  { v: "2", l: "lending protocols read at launch", n: "1" },
  { v: "30s", l: "between every look at your positions", n: "2" },
  { v: "0", l: "signatures or keys Argus asks for", n: "3" },
];

const STEPS = [
  { n: "01", t: "Connect", d: "Paste any wallet or connect Phantom, Solflare or Backpack. Read-only: Argus never asks for a signature." },
  { n: "02", t: "Watch", d: "Every position gets an eye. It opens as health falls, from calm ash to bright terracotta." },
  { n: "03", t: "Act early", d: "Before 1.00x, Argus tells you exactly how much to add or repay, and where. You make the move." },
];

const MYTH = [
  {
    n: "I",
    a: "Argus",
    img: "/brand/watch.jpg",
    alt: "Argus, seen from behind with eyes open across his back, keeping watch over a valley of amphorae under orbital rings",
    b: "The hundred-eyed giant set to watch what others could not afford to lose. Some of his eyes were always open.",
    c: "Argus watches every position, every block, all night.",
  },
  {
    n: "II",
    a: "Hermes",
    img: "/brand/hermes.jpg",
    alt: "Hermes playing a reed pipe on a rock while the hundred-eyed giant's eyes droop shut",
    b: "The god of merchants and thieves lulled every one of those eyes to sleep with a slow song, then struck.",
    c: "Calm markets are the song. Liquidation bots are waiting for you to look away.",
  },
  {
    n: "III",
    a: "Premeditatio malorum",
    img: "/brand/stoic.jpg",
    alt: "Argus at a table beside an armillary sphere, rehearsing a wave against a row of amphorae; the first one is already cracking",
    b: "The Stoics rehearsed misfortune before it arrived, so it never arrived as a surprise.",
    c: "Run the crash before it happens. See which position breaks first, and by how much.",
  },
];

const FAQ = [
  { q: "Does Argus need my keys or a signature?", a: "No. Argus reads public on-chain positions. Watching a wallet needs only its address." },
  { q: "Which protocols does it read?", a: "Kamino and Jupiter Lend at launch. More Solana lending markets follow." },
  {
    q: "What happens when a position nears 1.00x?",
    a: "Its eye opens wide, the row turns terracotta, and Argus shows the exact amount to add or repay to get back to 1.50x.",
  },
  { q: "What is Ask Argus?", a: "A chat that reads your positions and answers in numbers: which one breaks first, what a −25% day does, what to do next. Powered by Claude." },
  { q: "Is this financial advice?", a: "No. Argus shows risk and options. Markets can move faster than any alert." },
];

/** Stagger delay for motion.css (`--d`). */
const d = (ms: number) => ({ "--d": `${ms}ms` }) as CSSProperties;

export default function Landing() {
  const book = demoPositions().sort(byRisk).slice(0, 4);

  return (
    <>
      <MotionRoot />
      <section className="relative bg-terra-500 overflow-hidden">
        <Image
          src="/brand/hero.jpg"
          alt="Argus, a black-figure giant covered in eyes, working at a laptop under orbital rings"
          fill
          priority
          sizes="100vw"
          className="hero-art object-cover object-[70%_center] opacity-40 md:opacity-100"
        />
        <div className="relative mx-auto max-w-[1360px] px-4 md:px-6">
          <header className="flex items-center gap-3 py-3.5">
            <Link href="/" aria-label="Argus home" className="min-h-11 flex items-center">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src="/brand/argus-lockup-terracotta.svg" alt="Argus" width={105} height={30} className="h-[30px] w-auto" />
            </Link>
            {/* Links share the button's dark bar so they stay legible over the hero art at any width. */}
            <div className="ml-auto flex items-center bg-ink-950">
              <nav aria-label="Main" className="hidden md:flex pl-2 border-r border-sand-200/15">
                {[
                  ["How it works", "#how"],
                  ["Why Argus", "#myth"],
                  ["FAQ", "#faq"],
                ].map(([n, h]) => (
                  <a key={h} href={h} className="min-h-11 flex items-center px-2.5 text-[13px] font-medium text-sand-200/80 hover:text-sand-200 hover:underline">
                    {n}
                  </a>
                ))}
              </nav>
              <Link href="/app" className="min-h-11 flex items-center px-[18px] bg-ink-950 text-sand-200 text-sm font-medium hover:bg-ink-900">
                Launch app
              </Link>
            </div>
          </header>
          <div className="min-h-[560px] md:min-h-[640px] flex flex-col justify-center gap-7 pt-12 pb-36 max-w-[620px]">
            <h1 className="font-display m-0 text-[38px] md:text-[60px] leading-[1.04] tracking-[0.01em] text-ink-950 text-balance">
              <span className="hero-line"><span style={d(100)}>A hundred</span></span>
              <span className="hero-line"><span style={d(220)}>eyes on your</span></span>
              <span className="hero-line"><span style={d(340)}>collateral.</span></span>
            </h1>
            <div className="hero-fade bg-ink-950 p-[22px] flex flex-col gap-3.5 max-w-[560px]" style={d(650)}>
              <p className="m-0 text-[15px] leading-relaxed text-sand-200">
                Argus never sleeps. Paste a Solana wallet and it shows which lending position breaks first, and what to do before the liquidators do.
              </p>
              <ScanForm />
            </div>
          </div>
        </div>
      </section>

      <section aria-label="Proof" className="relative mx-auto max-w-[1360px] w-full px-4 md:px-6 -mt-[84px] flex flex-col gap-2.5">
        <div className="grid gap-4 sm:grid-cols-3">
          {PROOF.map((s, i) => (
            <div key={s.l} data-reveal style={d(900 + i * 120)} className="bg-ink-950 border border-ink-700 p-[22px] flex flex-col gap-2">
              <span className="font-display text-[30px] leading-none text-sand-100">
                {s.v}
                <sup className="font-mono text-[12px] text-terra-400 ml-1">{s.n}</sup>
              </span>
              <span className="text-[13px] leading-normal text-sand-500">{s.l}</span>
            </div>
          ))}
        </div>
        <p className="m-0 text-[12px] text-sand-600">¹ Kamino and Jupiter Lend. ² The app refreshes every 30 seconds while open. ³ Watching needs only a public address.</p>
      </section>

      <section id="how" className="mx-auto max-w-[1360px] w-full px-4 md:px-6 pt-24 md:pt-28 pb-10 flex flex-col gap-8">
        <div data-reveal className="flex flex-col gap-3">
          <Label className="!text-terra-400">How it works</Label>
          <h2 className="font-display m-0 text-[28px] md:text-[40px] leading-[1.1] text-sand-100">See it first. Fix it early.</h2>
        </div>
        <div className="grid gap-8 md:grid-cols-3">
          {STEPS.map((s, i) => (
            <div key={s.n} data-reveal style={d(i * 140)} className="flex flex-col gap-3.5 pt-[18px] border-t border-ink-700">
              <span className="text-[64px] leading-none text-terra-400">{s.n}</span>
              <h3 className="font-display m-0 text-[20px] leading-[1.2] text-sand-100">{s.t}</h3>
              <p className="m-0 text-sm leading-relaxed text-sand-300">{s.d}</p>
            </div>
          ))}
        </div>
      </section>

      <section aria-label="Night watch" className="relative my-10 md:my-16 bg-terra-500 overflow-hidden">
        <div className="relative aspect-[2/1] max-h-[640px] w-full">
          <Image src="/brand/frieze.jpg" alt="A night sky of open eyes joined by constellation lines that rise and fall like a price chart" fill sizes="100vw" className="sky-drift object-cover" />
        </div>
        <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink-950/90 via-ink-950/40 to-transparent">
          <div className="mx-auto max-w-[1360px] px-4 md:px-6 pt-24 pb-6 md:pb-10 flex flex-wrap items-end justify-between gap-4">
            <p data-reveal className="font-display m-0 text-[22px] md:text-[36px] leading-[1.1] text-sand-100 max-w-[720px] text-balance">
              Every block. Every position. All night.
            </p>
            <span className="text-[12px] text-sand-300">One eye per position. It opens as health falls.</span>
          </div>
        </div>
      </section>

      <Tutorial />

      <section data-reveal className="mx-auto max-w-[1360px] w-full px-4 md:px-6 py-10">
        <BeforeAfter />
      </section>

      <section className="mx-auto max-w-[1360px] w-full px-4 md:px-6 py-14 flex flex-wrap gap-12 items-center">
        <div data-reveal className="flex-[1_1_380px] min-w-0 flex flex-col gap-3.5">
          <Label className="!text-terra-400">The real interface</Label>
          <h2 className="font-display m-0 text-[24px] md:text-[32px] leading-[1.15] text-sand-100">Calm when you&apos;re fine. Loud only when you&apos;re not.</h2>
          <p className="m-0 text-sm leading-relaxed text-sand-300">
            Healthy positions fade back. Only the one that needs you turns terracotta. No dashboards full of red, no alerts for things that don&apos;t matter.
          </p>
        </div>
        <div data-reveal style={d(150)} className="relative flex-[1.3_1_520px] min-w-0 border border-ink-700 bg-ink-900 overflow-x-auto">
          <div className="flex justify-between px-[18px] py-3 border-b border-ink-800">
            <span className="font-display text-[15px] text-sand-100">POSITIONS</span>
            <span className="text-[12px] text-sand-500">Demo book</span>
          </div>
          <table className="w-full text-[13px] border-collapse min-w-[480px]">
            <tbody>
              {book.map((p, i) => {
                const r = riskOf(p.healthFactor);
                const crit = r === "critical";
                return (
                  <tr key={p.id} data-reveal style={d(350 + i * 110)} className={crit ? "bg-risk-critical text-ink-950" : r === "safe" ? "text-sand-500 border-t border-ink-800" : "border-t border-ink-800"}>
                    <td className={`px-4 py-3.5 font-medium ${crit ? "" : "text-sand-100"}`}>{p.name}</td>
                    <td className="px-4 py-3.5">{p.protocol}</td>
                    <td className="px-4 py-3.5 text-right">
                      <Health value={p.healthFactor} onFill={crit} />
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="flex justify-end">
                        <Status risk={r} onFill={crit} />
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section id="myth" className="mx-auto max-w-[1360px] w-full px-4 md:px-6 pt-20 pb-10 flex flex-col gap-8">
        <div data-reveal className="flex flex-col gap-3 max-w-[760px]">
          <Label className="!text-terra-400">Why the name</Label>
          <h2 className="font-display m-0 text-[28px] md:text-[40px] leading-[1.1] text-sand-100">Named after the watchman who never slept.</h2>
          <p className="m-0 text-[15px] leading-relaxed text-sand-300">
            Liquidations don&apos;t happen to people who are watching. They happen at 3 a.m., during a quiet market, to the one position nobody checked.
          </p>
        </div>
        <div className="flex flex-col gap-16 md:gap-24 pt-4">
          {MYTH.map((m, i) => (
            <article key={m.a} data-reveal="group" className={`grid gap-8 md:gap-14 items-center md:grid-cols-[1.35fr_1fr] ${i % 2 ? "md:[&>figure]:order-2 md:grid-cols-[1fr_1.35fr]" : ""}`}>
              <figure data-wipe className="lean m-0 relative aspect-[16/9] overflow-hidden border border-ink-800 bg-terra-500">
                <Image src={m.img} alt={m.alt} fill sizes="(min-width: 768px) 58vw, 100vw" className="object-cover" />
              </figure>
              <div data-reveal style={d(300)} className="flex flex-col gap-4 min-w-0">
                <span className="font-display text-[15px] tracking-[0.2em] text-terra-400">{m.n}</span>
                <h3 className="font-display m-0 text-[26px] md:text-[32px] leading-[1.15] text-sand-100">{m.a}</h3>
                <p className="m-0 text-[15px] leading-relaxed text-sand-300">{m.b}</p>
                <p className="m-0 text-[15px] font-medium leading-relaxed text-sand-100 border-t border-ink-700 pt-4">{m.c}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section id="faq" className="mx-auto max-w-[1360px] w-full px-4 md:px-6 pt-14 pb-24 flex flex-wrap gap-12">
        <div className="flex-[1_1_300px] min-w-0">
          <h2 className="font-display m-0 text-[17px] tracking-[0.06em] text-sand-100">QUESTIONS</h2>
        </div>
        <div className="flex-[3_1_600px] min-w-0 border-b border-ink-800">
          {FAQ.map((f) => (
            <details key={f.q} className="group border-t border-ink-800">
              <summary className="flex justify-between gap-4 items-center min-h-14 py-2 text-[15px] font-medium text-sand-100 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                {f.q}
                <span aria-hidden className="text-[22px] text-sand-500 group-open:hidden">
                  +
                </span>
                <span aria-hidden className="text-[22px] text-sand-500 hidden group-open:inline">
                  −
                </span>
              </summary>
              <p className="m-0 pb-5 max-w-[760px] text-sm leading-relaxed text-sand-300">{f.a}</p>
            </details>
          ))}
        </div>
      </section>

      <footer className="bg-terra-500 overflow-hidden">
        <div className="mx-auto max-w-[1360px] px-4 md:px-6 pt-20 md:pt-24 flex flex-wrap gap-10 items-end justify-between">
          <div data-reveal className="flex flex-col gap-5 flex-[1_1_520px] min-w-0">
            <p className="font-display m-0 text-[32px] md:text-[52px] leading-[1.05] text-ink-950 text-balance">Argus never sleeps. Now neither does your collateral.</p>
            <div>
              <Link href="/app" className="inline-flex min-h-12 items-center px-[22px] bg-ink-950 text-sand-200 text-[15px] font-medium hover:bg-ink-900">
                Scan a wallet →
              </Link>
            </div>
          </div>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/brand/argus-mark-L-terracotta.svg" alt="" width={170} height={170} className="mark-breathe w-[120px] md:w-[170px] h-auto" />
        </div>
        <div aria-hidden data-reveal style={d(200)} className="font-display text-ink-950 leading-[0.78] tracking-[-0.02em] whitespace-nowrap pt-10 pl-3 -mb-[0.12em] text-[clamp(96px,22vw,320px)]">
          ΛRGUS
        </div>
        <div className="bg-ink-950 px-4 md:px-6 py-4 flex flex-wrap justify-between gap-3 text-[12px] text-sand-600">
          <span>ΛRGUS · Solana liquidation intelligence</span>
          <span>Read-only · Not financial advice</span>
        </div>
      </footer>
    </>
  );
}
