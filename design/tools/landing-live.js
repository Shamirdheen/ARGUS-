/* Runs inside the prototype's landing frame (the real built landing page, without React).
 * Restores what React did on that page: scroll reveals, the two tutorial sliders, the
 * 1.18x → 1.31x count-up and the scan box. Links tell the prototype where to go next.
 * Maths mirror lib/positions/risk.ts; the eye mirrors components/brand/RiskEye.tsx. */
(() => {
  const go = (id) => parent.postMessage({ argusGo: id }, "*");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- risk tiers + eye (same numbers as the app) ----
  const tier = (hf) => (hf >= 2 ? "safe" : hf >= 1.5 ? "watch" : hf >= 1.2 ? "warning" : "critical");
  const LABEL = { safe: "Safe", watch: "Watch", warning: "Warning", critical: "Act now" };
  const OPEN = { safe: 0.32, watch: 0.55, warning: 0.78, critical: 1 };
  const IRIS = { safe: 0.6, watch: 0.8, warning: 0.95, critical: 1.05 };
  const LID = { safe: "#7e654a", watch: "#efc796", warning: "#e0946a", critical: "#e0946a" };
  const FILL = { safe: "none", watch: "none", warning: "#c0551e", critical: "#e0946a" };
  const HF_CLASS = {
    safe: "text-risk-safe",
    watch: "text-risk-watch",
    warning: "text-risk-warning underline decoration-2 underline-offset-4",
    critical: "text-risk-critical",
  };
  function paintEye(svg, risk) {
    const lid = svg.querySelector(".risk-eye-lid"), iris = svg.querySelector(".risk-eye-iris");
    if (!lid || !iris) return;
    lid.style.transform = `scaleY(${OPEN[risk]})`;
    lid.querySelector("path").setAttribute("stroke", LID[risk]);
    iris.style.transform = `scale(${IRIS[risk]})`;
    iris.setAttribute("stroke", LID[risk]);
    iris.setAttribute("fill", FILL[risk]);
  }
  const usd = (n) => "$" + Math.round(n).toLocaleString("en-US");
  function tween(from, to, ms, set) {
    if (reduced) return set(to);
    const t0 = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - t0) / ms);
      set(from + (to - from) * (1 - Math.pow(1 - t, 3)));
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
  const onceInView = (el, fn) => {
    const io = new IntersectionObserver(([e]) => e.isIntersecting && (io.disconnect(), fn()), { threshold: 0.4 });
    io.observe(el);
  };

  // ---- scroll reveals (MotionRoot) ----
  const io = new IntersectionObserver(
    (es) => es.forEach((e) => e.isIntersecting && (e.target.setAttribute("data-in", ""), io.unobserve(e.target))),
    { rootMargin: "0px 0px -12% 0px", threshold: 0.12 },
  );
  document.querySelectorAll("[data-reveal]").forEach((el) => (reduced ? el.setAttribute("data-in", "") : io.observe(el)));
  // Fast scrolls or anchor jumps can skip past a section without it ever "intersecting":
  // anything already above the bottom of the screen counts as seen.
  addEventListener(
    "scroll",
    () => {
      document.querySelectorAll("[data-reveal]:not([data-in])").forEach((el) => {
        if (el.getBoundingClientRect().top < innerHeight) el.setAttribute("data-in", "");
      });
    },
    { passive: true },
  );

  // ---- tutorial 01: read the eye ----
  const hfIn = document.querySelector('input[aria-label="Health factor"]');
  if (hfIn) {
    const box = hfIn.parentElement, row = box.firstElementChild;
    const svg = row.querySelector("svg"), word = row.querySelector("span > span"), num = row.lastElementChild;
    let touched = false;
    const set = (hf) => {
      const r = tier(hf);
      hfIn.value = hf;
      paintEye(svg, r);
      word.textContent = LABEL[r];
      num.textContent = hf.toFixed(2) + "x";
      num.className = `font-medium tabular-nums text-[18px] ${HF_CLASS[r]}`;
    };
    hfIn.addEventListener("input", () => ((touched = true), set(+hfIn.value)));
    onceInView(box, () => setTimeout(() => !touched && tween(2.2, 1.05, 2600, (v) => !touched && set(v)), 600));
  }

  // ---- tutorial 02: rehearse the crash (demo mSOL / USDT loan) ----
  const solIn = document.querySelector('input[aria-label="SOL price change"]');
  if (solIn) {
    const P = { col: 54300, debt: 16100, ltv: 0.8 };
    const hf0 = (P.col * P.ltv) / P.debt;
    const box = solIn.parentElement, row = box.firstElementChild, note = box.lastElementChild;
    const label = row.firstElementChild, svg = row.querySelector("svg"), num = row.lastElementChild.lastElementChild;
    const set = (m) => {
      const hf = hf0 * (1 + m / 100), col = P.col * (1 + m / 100), r = tier(hf);
      label.textContent = `mSOL / USDT · SOL ${m > 0 ? "+" : ""}${m}%`;
      paintEye(svg, r);
      num.textContent = hf.toFixed(2) + "x";
      num.className = `font-medium tabular-nums ${HF_CLASS[r]}`;
      if (hf < 1.5) {
        const add = Math.max(0, (1.5 * P.debt) / P.ltv - col), repay = Math.max(0, P.debt - (col * P.ltv) / 1.5);
        note.className = "text-[12px] text-sand-300";
        note.innerHTML = `${hf < 1 ? "Liquidated. " : ""}Back to 1.50x: add <b class="font-medium text-sand-100">${usd(add)}</b> or repay <b class="font-medium text-sand-100">${usd(repay)}</b>.`;
      } else {
        note.className = "text-[12px] text-sand-500";
        note.textContent = "Comfortable at this price. Drag further.";
      }
    };
    solIn.addEventListener("input", () => set(+solIn.value));
  }

  // ---- before / after count-up ----
  const after = document.querySelector('[aria-label="1.31x"]');
  if (after) {
    const svg = after.parentElement.querySelector("svg");
    onceInView(after, () =>
      setTimeout(() => tween(1.18, 1.31, 1600, (v) => ((after.textContent = v.toFixed(2) + "x"), paintEye(svg, tier(v)))), 500),
    );
  }

  // ---- scan box + links → the rest of the prototype ----
  document.addEventListener("submit", (e) => {
    e.preventDefault();
    const v = e.target.querySelector("input")?.value.trim();
    if (v && !/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(v)) {
      const hint = e.target.querySelector("span:last-child");
      if (hint) {
        hint.textContent = "That doesn't look like a Solana address.";
        hint.className = "text-[12px] text-risk-warning";
      }
      return;
    }
    go("wallet");
  });
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (!a) return;
    const href = a.getAttribute("href") || "";
    if (href.startsWith("#")) return; // in-page anchors (How it works, FAQ…) scroll normally
    e.preventDefault();
    if (/Try it in the app/.test(a.textContent)) return go("askbar");
    if (href === "/") return scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    go("wallet"); // Launch app, Scan a wallet →
  });
  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      go("askbar");
    }
  });
})();
