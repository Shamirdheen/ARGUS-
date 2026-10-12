/* Argus prototype router. The boards are untouched design exports; this file only decides
 * where each link/button goes, by its visible text. One rule list, read top to bottom. */
(() => {
  const screens = [...document.querySelectorAll(".pt-screen")];
  const jump = document.getElementById("pt-jump");
  const toastEl = document.getElementById("pt-toast");
  const trail = [];
  let current = null;

  const text = (el) => (el.getAttribute("aria-label") || el.textContent || "").replace(/\s+/g, " ").trim();

  // [screen or "*", matcher on the element's text, action]. Action: a screen id, "back", "toast:…", "scroll:#id", "seg".
  const RULES = [
    ["*", /^Argus home$/, "landing"],
    ["*", /^Overview$/, "overview"],
    ["*", /^Positions$/, "positions"],
    ["*", /^Terminal$/, "terminal"],
    ["*", /^Radar$/, "radar"],
    ["*", /^Alerts/, "alerts"],
    ["*", /^Activity$/, "activity"],
    ["*", /^Demo…/, "wallet"],
    // Landing
    ["landing", /^How it works$/, "scroll:#how"],
    ["landing", /^Why Argus$/, "scroll:#myth"],
    ["landing", /^FAQ$/, "scroll:#faq"],
    ["landing", /^Docs/, "toast:Docs open in a new tab in the real product."],
    ["landing", /^(Launch app|Scan wallet|Scan a wallet)/, "wallet"],
    // Wallet
    ["wallet", /^(Phantom|Solflare|Backpack|Watch this wallet|Try a demo wallet|Open Overview)/, "overview"],
    ["wallet", /^Copy address$/, "toast:Address copied."],
    ["wallet", /^Stop watching/, "landing"],
    ["wallet", /^×$/, "back"],
    // Overview
    ["overview", /^Review the buffer$/, "positions"],
    ["overview", /^Run a stress test$/, "radar"],
    ["overview", /^All positions/, "positions"],
    ["overview", /(Drift|Kamino|Raydium|Marginfi|Jupiter)\$/, "positions"],
    ["overview", /^(0|−\d+)%$/, "seg"],
    // Positions
    ["positions", /^(All|At risk|Lending|Perps|Pools|Health|Size|Protocol)/, "seg"],
    ["positions", /^×$/, "overview"],
    ["positions", /^Add \$/, "toast:Opens the protocol to sign. Argus never moves funds."],
    ["positions", /^Set alert/, "alerts"],
    // Terminal
    ["terminal", /^\d+x$/, "seg"],
    ["terminal", /^Rehearse/, "radar"],
    // Radar
    ["radar", /^(0|−\d+)%/, "seg"],
    ["radar", /^Plan buffers/, "positions"],
    // Alerts
    ["alerts", /^(All|Unread|Critical|Archived|Health|Price|Oracle drift|Borrow rate|In-app|Telegram|Email)/, "seg"],
    ["alerts", /^(Act now|View)$/, "positions"],
    ["alerts", /^Simulate$/, "radar"],
    ["alerts", /^Snooze/, "toast:Snoozed for 1 hour."],
    ["alerts", /^Arm watchdog$/, "toast:Watchdog armed. Argus will message you below the threshold."],
    // Activity
    ["activity", /^(All|Argus|You|Market|Oracle)$/, "seg"],
    ["activity", /↗$/, "toast:Opens the transaction on Solscan."],
    // Ask bar (⌘K)
    ["askbar", /^(Which position|Why did|How much)/, "askpanel"],
    ["askbar", /^Risk Radar/, "radar"],
    ["askbar", /^Alerts ·/, "alerts"],
    ["askbar", /^Terminal/, "terminal"],
    ["askbar", /^Rehearse/, "radar"],
    ["askbar", /^Arm a watchdog/, "alerts"],
    // Ask panel
    ["askpanel", /^×$/, "back"],
    ["askpanel", /^(Open in Radar|Rehearse)/, "radar"],
    ["askpanel", /^(Simulate \$|Open SOL)/, "positions"],
    ["askpanel", /^Arm a watchdog/, "alerts"],
    ["askpanel", /^(What if|Explain)/, "toast:Argus answers here, streaming, with the next step."],
    ["askpanel", /^Ask/, "toast:Argus answers here, streaming, with the next step."],
  ];

  function actionFor(el, screen) {
    const t = text(el);
    const hit = RULES.find(([s, re]) => (s === "*" || s === screen) && re.test(t));
    return hit ? hit[2] : null;
  }

  function show(id, push = true) {
    const s = screens.find((x) => x.dataset.s === id) || screens[0];
    if (current && push && current !== s.dataset.s) trail.push(current);
    screens.forEach((x) => (x.hidden = x !== s));
    current = s.dataset.s;
    jump.value = current;
    window.scrollTo(0, 0);
    animate(s);
    if (location.hash.slice(1) !== current) location.replace("#" + current);
    markHotspots(s);
  }


  /* ---------- motion ---------- */
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const MOTION = ["pt-rise", "pt-reveal", "pt-seen", "pt-settle", "pt-wake", "pt-glow", "pt-crit", "pt-slide", "pt-drop", "pt-grow", "pt-draw", "pt-ring", "pt-pop", "pt-twinkle"];
  let io;

  // Leave the current screen with a short fade, then show the next one.
  function go(id, push = true) {
    const out = screens.find((x) => x.dataset.s === current);
    if (reduced || !out) return show(id, push);
    out.classList.add("pt-out");
    setTimeout(() => {
      out.classList.remove("pt-out");
      show(id, push);
    }, 150);
  }

  const delay = (el, ms) => el.style.setProperty("--d", ms + "ms");
  const add = (el, cls, ms) => {
    if (ms !== undefined) delay(el, ms);
    el.classList.add(cls);
  };

  // Blocks to stagger: each child of <main>; if a child is a row/grid of cards, its children instead.
  function blocks(root) {
    const out = [];
    for (const child of root.children) {
      const cs = getComputedStyle(child);
      const isRow = child.children.length > 1 && child.children.length <= 8 && (cs.display === "grid" || (cs.display === "flex" && cs.flexDirection === "row"));
      if (isRow) out.push(...child.children);
      else out.push(child);
    }
    return out.slice(0, 36);
  }

  function animate(s) {
    io?.disconnect();
    // Reset anything from the previous visit so revisits animate again.
    s.querySelectorAll("." + MOTION.join(",.")).forEach((el) => el.classList.remove(...MOTION));
    if (reduced) return;
    void s.offsetWidth;

    const main = s.querySelector("main");
    const header = s.querySelector("header");
    if (header) add(header, "pt-rise", 0);

    if (main) {
      blocks(main).forEach((el, i) => add(el, "pt-rise", 60 + i * 55));
    } else if (s.dataset.s === "landing") {
      landing(s);
    } else {
      // Wallet: the three dialogs side by side.
      s.querySelectorAll('[role="dialog"]').forEach((el, i) => add(el, "pt-rise", 80 + i * 140));
    }

    // Panels slide in from the edge they live on; the ⌘K bar drops in.
    s.querySelectorAll("aside").forEach((el) => add(el, "pt-slide"));
    if (s.dataset.s === "askbar") s.querySelectorAll('[role="dialog"]').forEach((el) => add(el, "pt-drop"));

    // Argus opens his eyes: every risk-eye lid starts shut and eases to its real state.
    s.querySelectorAll('g[style*="scaleY"]').forEach((g, i) => add(g, "pt-wake", 300 + Math.min(i, 10) * 70));
    s.querySelectorAll('ellipse[style*="blur"]').forEach((el) => el.classList.add("pt-glow"));

    // Critical rows breathe (the only rows with the terracotta fill).
    s.querySelectorAll('[style*="background:#D06F3C"]').forEach((el) => {
      if (el.children.length >= 3) el.classList.add("pt-crit");
    });

    if (s.dataset.s === "terminal") terminal(s);
    if (s.dataset.s === "radar") radar(s);
  }

  // Terminal: candles grow left→right, liquidation lines draw across.
  function terminal(s) {
    const chart = s.querySelector('svg[aria-label*="candles"]');
    if (!chart) return;
    chart.querySelectorAll("rect").forEach((r, i) => add(r, "pt-grow", 200 + i * 18));
    chart.querySelectorAll("line").forEach((l) => {
      const stroke = (l.getAttribute("stroke") || "").toUpperCase();
      if (stroke === "#33271D" || l.getAttribute("stroke-dasharray")) return; // grid / dashed stay put
      l.setAttribute("pathLength", "1");
      add(l, "pt-draw", 900);
    });
  }

  // Radar: rings expand from the centre, positions pop in, links draw, background stars twinkle.
  function radar(s) {
    const sky = s.querySelector('svg[aria-label*="constellation"]');
    if (!sky) return;
    let ring = 0, dot = 0;
    sky.querySelectorAll("circle").forEach((c) => {
      const r = parseFloat(c.getAttribute("r") || "0");
      if (r <= 1.5) return add(c, "pt-twinkle", Math.round(Math.random() * 3000));
      if (c.getAttribute("fill") === "none") return add(c, "pt-ring", 100 + ring++ * 90);
      add(c, "pt-pop", 600 + dot++ * 70);
    });
    sky.querySelectorAll("line").forEach((l, i) => {
      if (l.getAttribute("stroke-dasharray")) return;
      l.setAttribute("pathLength", "1");
      add(l, "pt-draw", 900 + i * 40);
    });
  }

  // Landing: hero settles, everything below reveals on scroll.
  function landing(s) {
    const hero = s.querySelector("section");
    hero?.querySelector("img")?.classList.add("pt-settle");
    hero?.querySelectorAll("h1, h1 ~ div").forEach((el, i) => add(el, "pt-rise", 150 + i * 200));
    const later = [...s.querySelectorAll("section, footer")].slice(1).flatMap((sec) => {
      const kids = [...sec.firstElementChild?.children || []];
      return kids.length > 1 && kids.length <= 8 ? kids : [sec];
    });
    io = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.isIntersecting && (e.target.classList.add("pt-seen"), io.unobserve(e.target))),
      { rootMargin: "0px 0px -10% 0px" },
    );
    later.forEach((el, i) => {
      add(el, "pt-reveal", (i % 4) * 90);
      io.observe(el);
    });
  }

  function back() {
    go(trail.pop() || "overview", false);
  }

  let toastTimer;
  function toast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add("on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove("on"), 2200);
  }

  // Segmented controls: move the "selected" look (sand fill) from the old button to the clicked one.
  function segment(el) {
    const group = [...el.parentElement.children].filter((c) => c.tagName === el.tagName);
    const active = group.find((c) => /background:\s*#EFC796/i.test(c.getAttribute("style") || ""));
    if (!active || active === el) return;
    const a = active.getAttribute("style"), b = el.getAttribute("style");
    active.setAttribute("style", b);
    el.setAttribute("style", a);
    el.classList.remove("pt-seg");
    void el.offsetWidth;
    el.classList.add("pt-seg");
  }

  function markHotspots(s) {
    s.querySelectorAll("a,button").forEach((el) => {
      const act = actionFor(el, s.dataset.s);
      if (act && act !== "seg") el.setAttribute("data-hot", "");
    });
  }

  document.addEventListener("click", (e) => {
    if (e.target.closest(".pt-bar")) return;
    // Ask overlays: a click on the dimmed backdrop (outside the dialog / panel) closes them.
    if (["askbar", "askpanel", "positions"].includes(current) && e.target.matches('[aria-hidden="true"]') && !e.target.closest('[role="dialog"],aside')) return back();
    if ((current === "askbar" || current === "askpanel") && !e.target.closest('[role="dialog"],aside,a,button')) return back();
    const el = e.target.closest("a,button");
    if (!el) return;
    e.preventDefault();
    const act = actionFor(el, current);
    if (!act) return toast("Not wired in the prototype.");
    if (act === "back") return back();
    if (act === "seg") return segment(el);
    if (act.startsWith("toast:")) return toast(act.slice(6));
    if (act.startsWith("scroll:")) return document.querySelector(`[data-s="${current}"] ${act.slice(7)}`)?.scrollIntoView({ behavior: "smooth" });
    go(act);
  });

  // Forms in the boards (scan wallet, ask) shouldn't reload the page.
  document.addEventListener("submit", (e) => {
    e.preventDefault();
    if (current === "landing") go("wallet");
    if (current === "askpanel") toast("Argus answers here, streaming, with the next step.");
  });

  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      go("askbar");
    }
    if (e.key === "Escape" && current !== "landing") back();
    if (e.key === "Enter" && current === "askbar" && document.activeElement?.id === "ask") go("askpanel");
  });

  jump.addEventListener("change", () => go(jump.value));
  document.getElementById("pt-back").addEventListener("click", back);
  document.getElementById("pt-hot").addEventListener("click", (e) => {
    const on = document.body.classList.toggle("pt-show");
    e.currentTarget.setAttribute("aria-pressed", on);
  });
  window.addEventListener("hashchange", () => {
    const id = location.hash.slice(1);
    if (id && id !== current) show(id);
  });

  show(location.hash.slice(1) || "landing", false);
})();
