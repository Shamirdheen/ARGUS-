import Link from "next/link";
import "./not-found.css";

/**
 * 404 for every unknown URL. Argus's eye opens, then searches left and right and blinks:
 * a hundred eyes, and none of them can find this page. Motion is CSS-only and switches off
 * under prefers-reduced-motion (the eye simply stays open and centred).
 */
export default function NotFound() {
  return (
    <main className="flex-1 min-h-dvh grid place-items-center px-4 py-16">
      <div className="flex flex-col items-center text-center gap-7 max-w-[560px]">
        <svg viewBox="0 0 400 240" width="240" height="144" aria-hidden="true" className="nf-eye overflow-visible">
          <defs>
            <clipPath id="nf-eye-shape">
              <path d="M20 120 Q200 -10 380 120 Q200 250 20 120Z" />
            </clipPath>
          </defs>
          <g className="nf-lid">
            <path
              d="M20 120 Q200 -10 380 120 Q200 250 20 120Z"
              fill="#1e1711"
              stroke="#efc796"
              strokeWidth={3}
              vectorEffect="non-scaling-stroke"
            />
            <g clipPath="url(#nf-eye-shape)">
            <g className="nf-iris">
              <circle cx="200" cy="120" r="58" fill="#c0551e" stroke="#efc796" strokeWidth={2} vectorEffect="non-scaling-stroke" />
              <circle cx="200" cy="120" r="22" fill="#16110c" />
            </g>
            </g>
          </g>
        </svg>
        <div className="nf-copy flex flex-col gap-3">
          <span className="text-[11px] font-medium uppercase tracking-[0.1em] text-sand-500">404 · Not found</span>
          <h1 className="font-display m-0 text-[26px] md:text-[34px] leading-[1.15] text-sand-100 text-balance">
            A hundred eyes, and none of them can see this page.
          </h1>
          <p className="m-0 text-sm leading-relaxed text-sand-300">The link may be old, or the address mistyped. Your positions are still being watched.</p>
        </div>
        <div className="nf-copy flex gap-2 flex-wrap justify-center" style={{ animationDelay: "250ms" }}>
          <Link href="/app" className="inline-flex min-h-11 items-center px-[18px] bg-sand-200 text-ink-950 text-sm font-medium hover:bg-sand-100">
            Open Argus
          </Link>
          <Link href="/" className="inline-flex min-h-11 items-center px-[18px] border border-ink-700 text-sand-200 text-sm font-medium hover:bg-ink-850">
            Home
          </Link>
        </div>
      </div>
    </main>
  );
}
