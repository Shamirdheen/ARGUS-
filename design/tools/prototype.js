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
    s.classList.remove("pt-in");
    void s.offsetWidth;
    s.classList.add("pt-in");
    window.scrollTo(0, 0);
    if (location.hash.slice(1) !== current) location.replace("#" + current);
    markHotspots(s);
  }

  function back() {
    show(trail.pop() || "overview", false);
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
    if ((current === "askbar" || current === "askpanel") && !e.target.closest('[role="dialog"],aside')) return back();
    const el = e.target.closest("a,button");
    if (!el) return;
    e.preventDefault();
    const act = actionFor(el, current);
    if (!act) return toast("Not wired in the prototype.");
    if (act === "back") return back();
    if (act === "seg") return segment(el);
    if (act.startsWith("toast:")) return toast(act.slice(6));
    if (act.startsWith("scroll:")) return document.querySelector(`[data-s="${current}"] ${act.slice(7)}`)?.scrollIntoView({ behavior: "smooth" });
    show(act);
  });

  // Forms in the boards (scan wallet, ask) shouldn't reload the page.
  document.addEventListener("submit", (e) => {
    e.preventDefault();
    if (current === "landing") show("wallet");
    if (current === "askpanel") toast("Argus answers here, streaming, with the next step.");
  });

  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      show("askbar");
    }
    if (e.key === "Escape" && current !== "landing") back();
    if (e.key === "Enter" && current === "askbar" && document.activeElement?.id === "ask") show("askpanel");
  });

  jump.addEventListener("change", () => show(jump.value));
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
