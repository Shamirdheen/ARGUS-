import sys, os
OUT = sys.argv[2]
which = sys.argv[1]

SHARED_CSS = r"""
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:var(--fb);-webkit-font-smoothing:antialiased}
button{font:inherit;color:inherit;cursor:pointer;background:none;border:0;padding:0}
h1,h2,h3,p{margin:0}
.app{min-height:@@MINH@@px;background:var(--bg);position:relative;overflow:hidden}
.wrap{max-width:1280px;margin:0 auto;padding:24px;display:flex;flex-direction:column;gap:24px;position:relative}
.hdr{position:relative;display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:10px 24px}
.hdr-in{max-width:1280px;width:100%;margin:0 auto;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:8px;font-family:var(--fd);font-weight:800;font-size:18px;letter-spacing:.02em}
.brand .v{font-family:var(--fm);font-size:11px;padding:2px 6px}
.net{font-family:var(--fm);font-size:11px;color:var(--sub);display:flex;align-items:center;gap:6px}
.dot{width:7px;height:7px;border-radius:50%;background:var(--safe);display:inline-block}
.nav{display:flex;gap:4px;flex-wrap:wrap;margin-left:auto}
.tab{min-height:44px;padding:0 12px;font-size:13px;font-weight:600;display:flex;align-items:center;gap:6px;color:var(--sub)}
.badge{font-family:var(--fm);font-size:10px;font-weight:700;padding:1px 5px}
.wallet{min-height:44px;padding:0 12px;display:flex;align-items:center;gap:8px;font-family:var(--fm);font-size:12px}
.launch{min-height:44px;padding:0 16px;font-weight:700;font-size:13px}
.panel{padding:24px;display:flex;flex-direction:column;gap:20px;position:relative}
.eyebrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-family:var(--fm);font-size:11px}
.h1{font-family:var(--fd);font-weight:800;font-size:34px;line-height:1.1;letter-spacing:-.01em;text-wrap:balance}
.lede{color:var(--sub);font-size:14px;line-height:1.5;max-width:620px;text-wrap:pretty}
.hero-top{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:flex-start}
.actions{display:flex;gap:10px;flex-wrap:wrap}
.btn{min-height:44px;padding:0 16px;font-size:13px;font-weight:600;display:flex;align-items:center;gap:8px}
.chips{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.lbl{font-family:var(--fm);font-size:11px;color:var(--sub);text-transform:uppercase;letter-spacing:.06em}
.pchip{min-height:44px;padding:0 14px;display:flex;align-items:center;gap:8px;font-size:13px;font-weight:600}
.pchip small{font-family:var(--fm);font-size:11px;font-weight:500}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(250px,100%),1fr));gap:16px}
.kpi{padding:20px;display:flex;flex-direction:column;gap:10px;position:relative}
.kpi .k-row{display:flex;justify-content:space-between;gap:12px;align-items:flex-end;flex-wrap:wrap}
.num{font-family:var(--fm);font-weight:700;font-size:30px;line-height:1.1;font-variant-numeric:tabular-nums}
.sub{font-size:12px;color:var(--sub);line-height:1.4}
.mono{font-family:var(--fm)}
.neg{color:var(--crit);font-family:var(--fm);font-size:12px;font-weight:700}
.dial{width:168px;aspect-ratio:168/96;border-radius:168px 168px 0 0;background:var(--dial-bg);box-shadow:var(--dial-shadow);border:var(--dial-border);padding:10px 10px 0;flex:none}
.dial svg{display:block;width:100%;height:auto}
.dial .g{fill:none;stroke-width:13}
.g1{stroke:var(--crit)}.g2{stroke:var(--high)}.g3{stroke:var(--warn)}.g4{stroke:var(--watch)}.g5{stroke:var(--safe)}
.needle{stroke:var(--needle)}
.hub-hd{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center}
.hub-ttl{display:flex;flex-direction:column;gap:2px}
.h2{font-family:var(--fd);font-weight:800;font-size:14px;letter-spacing:.06em;text-transform:uppercase}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.stab{min-height:44px;padding:0 12px;font-size:13px;font-weight:600;color:var(--sub);display:flex;align-items:center}
.stress{padding:20px;display:flex;flex-direction:column;gap:18px}
.row-sp{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:baseline}
.presets{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(96px,100%),1fr));gap:10px}
.preset{min-height:44px;font-family:var(--fm);font-size:13px;font-weight:700;background:var(--p-bg);box-shadow:var(--p-shadow);border:var(--p-border);border-radius:var(--p-rad)}
.preset.on{background:var(--p-on-bg);box-shadow:var(--p-on-shadow);color:var(--p-on-ink)}
input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:30px;background:transparent;margin:0;display:block}
input[type=range]::-webkit-slider-runnable-track{height:12px;border-radius:var(--t-rad);background:var(--track-bg);box-shadow:var(--track-shadow);border:var(--t-border)}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:30px;height:30px;margin-top:-10px;border-radius:var(--th-rad);background:var(--thumb-bg);box-shadow:var(--thumb-shadow);border:var(--th-border)}
input[type=range]::-moz-range-track{height:12px;border-radius:var(--t-rad);background:var(--track-bg);box-shadow:var(--track-shadow);border:var(--t-border)}
input[type=range]::-moz-range-thumb{width:30px;height:30px;border-radius:var(--th-rad);background:var(--thumb-bg);box-shadow:var(--thumb-shadow);border:var(--th-border)}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(200px,100%),1fr));gap:12px}
.metric{padding:14px 16px;display:flex;flex-direction:column;gap:6px}
.metric .num{font-size:22px}
.hub-ft{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center;font-size:13px;color:var(--sub)}
.link{font-weight:700;font-size:13px;min-height:44px;display:flex;align-items:center;gap:6px}
.wl-hd{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center}
.scroll{overflow-x:auto}
.tbl{min-width:880px;display:flex;flex-direction:column}
.tr{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1.2fr) minmax(0,1fr) minmax(0,1fr) minmax(0,.8fr) minmax(0,.9fr) minmax(0,1fr);gap:12px;align-items:center;padding:0 16px;min-height:52px;font-size:13px}
.tr.th{min-height:44px;font-family:var(--fm);font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--sub)}
.r{text-align:right;font-family:var(--fm);font-variant-numeric:tabular-nums}
.pos{font-weight:700}
.chip{display:inline-flex;align-items:center;gap:6px;padding:3px 8px;font-family:var(--fm);font-size:11px;font-weight:700;letter-spacing:.04em;justify-self:end}
.tier-warning{--tc:var(--warn)}.tier-watch{--tc:var(--watch)}.tier-safe{--tc:var(--safe)}.tier-high{--tc:var(--high)}.tier-critical{--tc:var(--crit)}
.hf.tier-warning,.hf.tier-watch,.hf.tier-safe,.hf.tier-high,.hf.tier-critical{color:var(--tc);font-weight:700}
.proto{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(110px,100%),1fr));gap:10px}
.pr{padding:10px 12px;min-height:56px;display:flex;flex-direction:column;gap:2px;align-items:center;justify-content:center;text-align:center}
.pr b{font-family:var(--fd);font-size:13px;letter-spacing:.04em}
.pr span{font-size:11px;color:var(--sub)}
.foot{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-family:var(--fm);font-size:11px;color:var(--sub);padding:8px 2px}
"""

MARKUP = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>@@TITLE@@</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="@@FONT@@">
<style>
@@CSS@@
</style>
</helmet>
<div class="app">
@@BG@@
@@TOP@@
<header class="hdr">
<div class="hdr-in">
<div class="brand">
<svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><path d="M11 2 L20 19 H2 Z" fill="currentColor"/></svg>
<span>ARGUS</span><span class="v">V2</span>
</div>
<div class="net"><span class="dot"></span>Solana Mainnet · 2,140 TPS · 410ms</div>
<nav class="nav" aria-label="Main navigation">
<sc-for list="{{ tabs }}" as="t" hint-placeholder-count="7">
<button type="button" class="tab {{ t.cls }}">{{ t.label }}<sc-if value="{{ t.alerts }}" hint-placeholder-val="{{ false }}"><span class="badge">3</span></sc-if></button>
</sc-for>
</nav>
<div class="wallet">Demo...3tKG <span>$1843k</span></div>
<button type="button" class="launch">Launch App</button>
</div>
</header>

<main class="wrap">

<section class="panel hero">
<div class="hero-top">
<div style="display:flex;flex-direction:column;gap:12px">
<div class="eyebrow"><span class="eb">Solana Risk Intelligence</span><span style="color:var(--sub)">Pyth Oracle Feeds Active</span></div>
<h1 class="h1">Portfolio Liquidation &amp; Risk Overview</h1>
<p class="lede">Autonomous collateral monitoring and stress testing across Kamino, Marginfi, Drift, Jupiter, and Raydium.</p>
</div>
<div class="actions">
<button type="button" class="btn b-main">Watch 18s Mitigation Demo</button>
<button type="button" class="btn b-alt">Search Wallet</button>
</div>
</div>
<div class="chips">
<span class="lbl">Active Portfolio</span>
<button type="button" class="pchip on">DeFi Whale <small>$1.84M</small></button>
<button type="button" class="pchip">JUP Staker <small>$438K</small></button>
<button type="button" class="pchip">Airdrop Farmer <small>1.07x · $84K</small></button>
<button type="button" class="pchip">Consolidated (All 3)</button>
</div>
</section>

<section class="kpis" aria-label="Portfolio summary">
<div class="kpi card k1">
<span class="lbl">Total Portfolio Value</span>
<span class="num">$1,842,500</span>
<span class="neg">-3.21% <span style="font-weight:500">($41,820 24h)</span></span>
</div>
<div class="kpi card k2">
<span class="lbl">Aggregate Health Factor</span>
<div class="k-row">
<div style="display:flex;flex-direction:column;gap:6px">
<span class="num hfbig">1.38x</span>
<span class="sub">Liq at 1.00x · Controlled leverage buffer</span>
</div>
<div class="dial" role="img" aria-label="Health factor gauge at 1.38x, warning band">
<svg viewBox="0 0 200 118" aria-hidden="true">
<path class="g g1" d="M20 100 A80 80 0 0 1 180 100" pathLength="100" stroke-dasharray="7 93" stroke-dashoffset="0"/>
<path class="g g2" d="M20 100 A80 80 0 0 1 180 100" pathLength="100" stroke-dasharray="19 81" stroke-dashoffset="-8"/>
<path class="g g3" d="M20 100 A80 80 0 0 1 180 100" pathLength="100" stroke-dasharray="21 79" stroke-dashoffset="-28"/>
<path class="g g4" d="M20 100 A80 80 0 0 1 180 100" pathLength="100" stroke-dasharray="19 81" stroke-dashoffset="-50"/>
<path class="g g5" d="M20 100 A80 80 0 0 1 180 100" pathLength="100" stroke-dasharray="29 71" stroke-dashoffset="-70"/>
<line class="needle" x1="100" y1="100" x2="75.7" y2="38.6" stroke-width="3.5" stroke-linecap="round"/>
<circle class="hubc" cx="100" cy="100" r="8"/>
<text x="20" y="116" text-anchor="middle" font-size="9" class="tk">1.0</text>
<text x="180" y="116" text-anchor="middle" font-size="9" class="tk">2.0</text>
</svg>
</div>
</div>
</div>
<div class="kpi card k3">
<span class="lbl">Debt Liabilities</span>
<span class="num">$577,500</span>
<span class="sub">Against $1,420,000 collateral</span>
</div>
<div class="kpi card k4">
<span class="lbl">Active Alerts &amp; Watchdogs</span>
<span class="num">2 <span class="sub" style="font-weight:500">(0 Critical · 2 Warning)</span></span>
<span class="sub">Continuous Pyth oracle monitoring</span>
</div>
</section>

<section class="panel hub">
<div class="hub-hd">
<div class="hub-ttl">
<h2 class="h2">Risk Intelligence Hub</h2>
<span class="sub">Interactive tools to stress test, calculate liquidation thresholds, and verify safeguards</span>
</div>
<div class="tabs">
<button type="button" class="stab on">Stress Simulator</button>
<button type="button" class="stab">Liq Calculator</button>
<button type="button" class="stab">Diagnosis &amp; Actions</button>
<button type="button" class="stab">18s Demo Video</button>
</div>
</div>
<div class="stress card">
<div class="hub-ttl">
<h3 class="h2">Stress Test Controller</h3>
<span class="sub">Toggle simulated SOL market drawdown scenarios to project real-time liquidation health</span>
</div>
<div class="row-sp"><span class="sub">Simulated Drawdown Preset</span><span class="lbl">SOL Spot: $148.82</span></div>
<div class="presets">
<sc-for list="{{ presets }}" as="p" hint-placeholder-count="7">
<button type="button" class="preset {{ p.cls }}">{{ p.label }}</button>
</sc-for>
</div>
<div style="display:flex;flex-direction:column;gap:8px">
<div class="row-sp"><label class="sub" for="dd">Continuous Drawdown Slider</label><span class="mono" style="font-size:12px;font-weight:700">0% (Baseline Spot)</span></div>
<input id="dd" type="range" min="0" max="50" value="0" aria-label="Simulated SOL drawdown percent">
</div>
<div class="metrics">
<div class="metric tile"><span class="lbl">Projected Health Factor</span><span class="num hfbig">1.38x</span></div>
<div class="metric tile"><span class="lbl">Liquidated Positions</span><span class="num">0 / 6 <span class="sub" style="font-weight:500">safe</span></span></div>
<div class="metric tile"><span class="lbl">Capital at Immediate Risk</span><span class="num">$0</span></div>
<div class="metric tile"><span class="lbl">Stress Test Rating</span><span class="num" style="font-size:16px">NORMAL MONITORING</span></div>
</div>
</div>
<div class="hub-ft">
<span>Drawdown selections dynamically recalculate projected health factors in the table below.</span>
<button type="button" class="link">Deep Protocol Radar →</button>
</div>
</section>

<section class="panel wl">
<div class="wl-hd">
<div class="hub-ttl">
<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><h2 class="h2">Active Positions Watchlist</h2><span class="cnt">6 positions</span></div>
<span class="sub">Select any row to inspect health breakdown or simulate collateral top-ups</span>
</div>
<div class="tabs">
<button type="button" class="stab on">All</button>
<button type="button" class="stab">At Risk</button>
<button type="button" class="stab">Lending</button>
<button type="button" class="stab">Pools</button>
<button type="button" class="link">All Details →</button>
</div>
</div>
<div class="scroll">
<div class="tbl">
<div class="tr th"><span>Position</span><span>Protocol</span><span class="r">Supplied</span><span class="r">Borrowed</span><span class="r">Health Factor</span><span class="r">Liq Distance</span><span style="justify-self:end">Risk Tier</span></div>
<sc-for list="{{ rows }}" as="r" hint-placeholder-count="6">
<div class="tr body">
<span class="pos">{{ r.name }}</span><span>{{ r.proto }}</span><span class="r">{{ r.sup }}</span><span class="r">{{ r.bor }}</span>
<span class="r hf tier-{{ r.tier }}">{{ r.hf }}</span><span class="r">{{ r.dist }}</span>
<span class="chip tier-{{ r.tier }}">{{ r.label }}</span>
</div>
</sc-for>
</div>
</div>
</section>

<section style="display:flex;flex-direction:column;gap:10px">
<span class="lbl">Monitored Solana Protocols</span>
<div class="proto">
<sc-for list="{{ protos }}" as="x" hint-placeholder-count="9">
<div class="pr card"><b>{{ x.code }}</b><span>{{ x.name }}</span></div>
</sc-for>
</div>
</section>

<footer class="foot"><span><b style="color:var(--ink)">ARGUS V2</b> — Autonomous Solana DeFi Risk Intelligence Terminal</span><span>Pyth / Switchboard Feeds Synced · Mainnet-beta: 2,140 TPS · v2.4.0</span></footer>
</main>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1440,"height":@@MINH@@}}'>
class Component extends DCLogic {
renderVals() {
const labels = ['Features','Overview','Terminal','Positions','Risk Radar','Alerts','Activity'];
return {
tabs: labels.map((l) => ({ label: l, cls: l === 'Overview' ? 'on' : '', alerts: l === 'Alerts' })),
presets: ['0% Spot','-10%','-15%','-20%','-25%','-35%','-50%'].map((l, i) => ({ label: l, cls: i === 0 ? 'on' : '' })),
rows: [
{ name:'SOL-USDC Multiply', proto:'Kamino Lend', sup:'$820,000', bor:'$512,000', hf:'1.31x', dist:'-20.4%', tier:'warning', label:'WARNING' },
{ name:'JitoSOL Leverage Loop', proto:'Kamino Lend', sup:'$410,000', bor:'$270,850', hf:'1.58x', dist:'-21.6%', tier:'watch', label:'WATCH' },
{ name:'bSOL Core Supply', proto:'Marginfi', sup:'$190,000', bor:'$22,000', hf:'2.85x', dist:'-76.1%', tier:'safe', label:'SAFE' },
{ name:'SOL-PERP Cross Margin', proto:'Drift Protocol', sup:'$185,000', bor:'$126,500', hf:'1.46x', dist:'-23.8%', tier:'warning', label:'WARNING' },
{ name:'JLP Liquidity Pool', proto:'Jupiter Perps', sup:'$120,000', bor:'$0', hf:'∞', dist:'Safe', tier:'safe', label:'SAFE' },
{ name:'SOL-USDC CLMM Range', proto:'Raydium CLMM', sup:'$95,000', bor:'$0', hf:'1.72x', dist:'-16.0%', tier:'watch', label:'WATCH' }
],
protos: [
{ code:'KMNO', name:'Kamino Finance' },{ code:'MRGN', name:'Marginfi' },{ code:'DRIFT', name:'Drift Protocol' },
{ code:'JUP', name:'Jupiter' },{ code:'RAY', name:'Raydium' },{ code:'MET', name:'Meteora' },
{ code:'ORCA', name:'Orca' },{ code:'CLOUD', name:'Sanctum' },{ code:'PHX', name:'Phoenix' }
]
};
}
}
</script>
</body>
</html>
"""

# ---------------- THEMES ----------------
THEMES = {}

THEMES['A'] = dict(
 title="Overview — A Raw brutalism", minh=1720,
 font="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap",
 top="", bg="",
 css=r"""
:root{--bg:#E8E6DF;--panel:#F3F1EA;--ink:#111111;--sub:#4a4842;--line:#111111;
--fd:'IBM Plex Mono',ui-monospace,monospace;--fb:'IBM Plex Mono',ui-monospace,monospace;--fm:'IBM Plex Mono',ui-monospace,monospace;
--safe:#0a6b36;--watch:#0b4fa8;--warn:#8f4a00;--high:#a8350a;--crit:#b00000;--needle:#111;
--dial-bg:radial-gradient(circle at 30% 15%,#ffffff 0%,#d9d6cd 55%,#bdb9ad 100%);
--dial-shadow:inset 0 2px 3px rgba(255,255,255,.95),inset 0 -4px 8px rgba(0,0,0,.28),0 3px 0 #111;--dial-border:2px solid #111;
--p-bg:#F3F1EA;--p-shadow:3px 3px 6px #c3c0b6,-3px -3px 6px #ffffff;--p-border:1px solid #111;--p-rad:0;
--p-on-bg:#e2dfd5;--p-on-shadow:inset 3px 3px 6px #b5b2a7,inset -3px -3px 6px #fbfaf6;--p-on-ink:#111;
--track-bg:#dedbd1;--track-shadow:inset 2px 2px 4px #b0ada2,inset -2px -2px 4px #fff;--t-rad:0;--t-border:1px solid #111;
--thumb-bg:linear-gradient(145deg,#fdfcf8,#cfccc1);--thumb-shadow:2px 3px 5px rgba(0,0,0,.35),inset 1px 1px 2px #fff;--th-rad:0;--th-border:2px solid #111}
.hdr{background:var(--bg);border-bottom:2px solid #111}
.brand .v{background:#111;color:#E8E6DF}
.tab{border:1px solid transparent;text-transform:uppercase;font-size:12px;letter-spacing:.04em}
.tab.on{background:#111;color:#E8E6DF}
.badge{background:#b00000;color:#fff}
.wallet{border:1px solid #111;background:var(--panel)}
.launch{background:#111;color:#E8E6DF;border:1px solid #111;text-transform:uppercase;letter-spacing:.04em}
.panel,.card{background:var(--panel);border:1px solid #111}
.panel{padding:0}
.panel>*{margin-left:24px;margin-right:24px}
.panel>:first-child{margin-top:24px}
.panel>:last-child{margin-bottom:24px}
.hub>.hub-hd{margin:0;padding:12px 24px;background:#111;color:#E8E6DF}
.hub>.hub-hd .sub,.hub>.hub-hd .stab{color:#cfccc2}
.hub>.hub-hd .stab.on{background:#E8E6DF;color:#111}
.hub .hub-hd .h2{color:#E8E6DF}
.hub>.hub-ft{margin-bottom:24px}
.hub{padding-bottom:0}
.hub>.hub-hd+.stress{margin-top:0}
.eb{background:#111;color:#E8E6DF;padding:2px 8px;text-transform:uppercase;letter-spacing:.05em}
.h1{font-size:34px;text-transform:uppercase;letter-spacing:-.02em}
.btn{border:1px solid #111;text-transform:uppercase;letter-spacing:.03em;font-size:12px}
.b-main{background:#111;color:#E8E6DF}
.b-alt{background:var(--panel)}
.pchip{border:1px solid #111;background:var(--panel)}
.pchip.on{background:#111;color:#E8E6DF}
.kpis{gap:0;border:1px solid #111;background:var(--panel)}
.kpis .kpi{border:0;border-right:1px solid #111}
.kpis .kpi:last-child{border-right:0}
.kpi .num{font-size:30px}
.stab{text-transform:uppercase;font-size:12px;letter-spacing:.04em}
.stab.on{background:#111;color:#E8E6DF}
.stress{background:var(--bg)}
.tile{background:var(--panel);border:1px solid #111}
.cnt{font-size:11px;border:1px solid #111;padding:2px 8px}
.link{border-bottom:2px solid #111;align-self:center;text-transform:uppercase;font-size:12px;letter-spacing:.04em}
.tr{border-top:1px solid #111}
.tr.th{background:#111;color:#E8E6DF;border-top:0}
.tbl{border:1px solid #111}
.tr.body:hover{background:#E8E6DF}
.chip{border:1px solid var(--tc);color:var(--tc);background:transparent}
.chip.tier-warning{background:var(--warn);color:#fff}
.pr{border:1px solid #111;background:var(--panel)}
.proto{gap:0;border:1px solid #111}
.proto .pr{border:0;border-right:1px solid #111}
.proto .pr:last-child{border-right:0}
.hubc{fill:#111}.tk{fill:#111;font-family:'IBM Plex Mono',monospace}
"""
)

THEMES['B'] = dict(
 title="Overview — B Neobrutalism", minh=1760,
 font="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=DM+Mono:wght@400;500&display=swap",
 top="", bg="",
 css=r"""
:root{--bg:#F4EEE3;--panel:#FFFDF6;--ink:#1A1410;--sub:#4f4438;--line:#1A1410;
--fd:'Space Grotesk',system-ui,sans-serif;--fb:'Space Grotesk',system-ui,sans-serif;--fm:'DM Mono',ui-monospace,monospace;
--safe:#0f7a3d;--watch:#0b62b5;--warn:#a85500;--high:#b8380b;--crit:#c01212;--needle:#1A1410;
--dial-bg:radial-gradient(circle at 35% 20%,#fffdf6 0%,#efe6d2 70%);
--dial-shadow:4px 4px 0 #1A1410,inset 3px 3px 8px rgba(255,255,255,.9),inset -3px -5px 10px rgba(26,20,16,.18);--dial-border:3px solid #1A1410;
--p-bg:#FFFDF6;--p-shadow:3px 3px 0 #1A1410;--p-border:2px solid #1A1410;--p-rad:8px;
--p-on-bg:#ece3cf;--p-on-shadow:inset 3px 3px 7px rgba(26,20,16,.35),inset -2px -2px 5px rgba(255,255,255,.8);--p-on-ink:#1A1410;
--track-bg:#e6dcc6;--track-shadow:inset 3px 3px 6px rgba(26,20,16,.35),inset -2px -2px 4px rgba(255,255,255,.9);--t-rad:8px;--t-border:2px solid #1A1410;
--thumb-bg:linear-gradient(145deg,#fffdf6,#e7dcc3);--thumb-shadow:3px 3px 0 #1A1410,inset 2px 2px 3px #fff;--th-rad:50%;--th-border:3px solid #1A1410}
.hdr{background:var(--panel);border-bottom:3px solid #1A1410}
.brand .v{background:#1A1410;color:#FFFDF6;border-radius:6px}
.tab{border:2px solid transparent;border-radius:8px}
.tab.on{background:#1A1410;color:#FFFDF6;box-shadow:3px 3px 0 #8b7a66}
.badge{background:#c01212;color:#fff;border:2px solid #1A1410;border-radius:6px}
.wallet{border:2px solid #1A1410;border-radius:8px;background:#FFFDF6;box-shadow:3px 3px 0 #1A1410}
.launch{background:#1A1410;color:#FFFDF6;border:2px solid #1A1410;border-radius:8px;box-shadow:3px 3px 0 #8b7a66}
.panel,.card{background:var(--panel);border:3px solid #1A1410;border-radius:12px;box-shadow:6px 6px 0 #1A1410}
.kpi.card,.metric.tile,.pr.card{box-shadow:4px 4px 0 #1A1410}
.stress.card{box-shadow:none;border-width:2px;background:var(--bg)}
.tile{background:#FFFDF6;border:2px solid #1A1410;border-radius:10px;box-shadow:3px 3px 0 #1A1410}
.eb{background:#1A1410;color:#FFFDF6;padding:3px 10px;border-radius:6px;font-weight:700}
.h1{font-size:40px;letter-spacing:-.025em}
.btn{border:2px solid #1A1410;border-radius:8px;box-shadow:3px 3px 0 #1A1410}
.b-main{background:#1A1410;color:#FFFDF6;box-shadow:3px 3px 0 #8b7a66}
.b-alt{background:#FFFDF6}
.pchip{border:2px solid #1A1410;border-radius:999px;background:#FFFDF6}
.pchip.on{background:#1A1410;color:#FFFDF6}
.stab{border:2px solid transparent;border-radius:8px}
.stab.on{background:#1A1410;color:#FFFDF6}
.cnt{font-family:var(--fm);font-size:11px;border:2px solid #1A1410;border-radius:6px;padding:1px 8px;background:#F4EEE3}
.link{text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:4px;text-decoration-color:#1A1410}
.tr{border-top:2px solid #1A1410}
.tr.th{border-top:0;border-bottom:3px solid #1A1410;background:#F4EEE3;color:#1A1410;font-weight:500;border-radius:8px 8px 0 0}
.tr.body:hover{background:#F4EEE3}
.chip{background:var(--tc);color:#fff;border:2px solid #1A1410;border-radius:6px}
.chip.tier-watch,.chip.tier-warning,.chip.tier-safe{color:#fff}
.hubc{fill:#1A1410}.tk{fill:#1A1410;font-family:'DM Mono',monospace}
.h2{font-weight:700}
"""
)

THEMES['C'] = dict(
 title="Overview — C Flat + glass layers", minh=1720,
 font="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap",
 top="",
 bg='<div style="position:absolute;left:8%;top:40px;width:520px;height:520px;border-radius:50%;background:#10b981;opacity:.28;filter:blur(110px)"></div><div style="position:absolute;right:4%;top:560px;width:460px;height:460px;border-radius:50%;background:#fbbf24;opacity:.18;filter:blur(120px)"></div>',
 css=r"""
:root{--bg:#15161a;--panel:#20232a;--ink:#f3efe8;--sub:#b2aba0;--line:#323742;
--fd:'Plus Jakarta Sans',system-ui,sans-serif;--fb:'Plus Jakarta Sans',system-ui,sans-serif;--fm:'JetBrains Mono',ui-monospace,monospace;
--safe:#34d399;--watch:#38bdf8;--warn:#fbbf24;--high:#fb923c;--crit:#f87171;--needle:#f3efe8;
--dial-bg:linear-gradient(145deg,#232730,#1a1d23);
--dial-shadow:8px 8px 16px #0c0d10,-6px -6px 14px #2a2f3a,inset 1px 1px 2px rgba(255,255,255,.05);--dial-border:0;
--p-bg:#20232a;--p-shadow:5px 5px 10px #0f1013,-4px -4px 9px #2b303a;--p-border:0;--p-rad:12px;
--p-on-bg:#1a1d23;--p-on-shadow:inset 4px 4px 8px #0c0d10,inset -3px -3px 7px #2a2f3a;--p-on-ink:#34d399;
--track-bg:#181a1f;--track-shadow:inset 3px 3px 6px #0b0c0f,inset -2px -2px 5px #2a2f3a;--t-rad:999px;--t-border:0;
--thumb-bg:linear-gradient(145deg,#2c313b,#1d2027);--thumb-shadow:4px 4px 8px #0b0c0f,-2px -2px 6px #323845,inset 1px 1px 1px rgba(255,255,255,.12);--th-rad:50%;--th-border:0}
.glass{background:rgba(32,35,42,.55);backdrop-filter:blur(18px) saturate(140%);-webkit-backdrop-filter:blur(18px) saturate(140%);border:1px solid rgba(255,255,255,.14);box-shadow:0 18px 50px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.12)}
.hdr{background:rgba(21,22,26,.55);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid rgba(255,255,255,.1)}
.brand .v{background:#10b981;color:#06281d;border-radius:5px;font-weight:700}
.tab{border-radius:10px}
.tab.on{background:rgba(255,255,255,.1);color:var(--ink)}
.badge{background:rgba(248,113,113,.18);color:#f87171;border:1px solid rgba(248,113,113,.4);border-radius:5px}
.wallet{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:10px}
.launch{background:#10b981;color:#06281d;border-radius:10px}
.panel,.card{background:var(--panel);border:1px solid var(--line);border-radius:16px}
.hub{background:rgba(32,35,42,.5);backdrop-filter:blur(22px) saturate(150%);-webkit-backdrop-filter:blur(22px) saturate(150%);border:1px solid rgba(255,255,255,.16);box-shadow:0 24px 60px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.14)}
.hub .stress.card{background:rgba(15,16,19,.45);border:1px solid rgba(255,255,255,.08)}
.eb{color:#34d399;background:rgba(16,185,129,.14);border:1px solid rgba(52,211,153,.35);border-radius:999px;padding:3px 10px}
.btn{border-radius:10px}
.b-main{background:#10b981;color:#06281d}
.b-alt{background:rgba(255,255,255,.06);border:1px solid var(--line)}
.pchip{border-radius:10px;background:rgba(255,255,255,.04);border:1px solid var(--line)}
.pchip.on{border-color:#34d399;color:#34d399;background:rgba(16,185,129,.1)}
.stab{border-radius:10px}
.stab.on{background:rgba(255,255,255,.1);color:var(--ink)}
.tile{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:12px}
.cnt{font-family:var(--fm);font-size:11px;background:rgba(255,255,255,.08);border-radius:6px;padding:2px 8px}
.link{color:#34d399}
.tr{border-top:1px solid var(--line)}
.tr.th{border-top:0}
.tr.body:hover{background:rgba(255,255,255,.04)}
.chip{color:var(--tc);background:color-mix(in srgb,var(--tc) 14%,transparent);border:1px solid color-mix(in srgb,var(--tc) 45%,transparent);border-radius:6px}
.hubc{fill:#f3efe8}.tk{fill:#b2aba0;font-family:'JetBrains Mono',monospace}
.kpi .num,.metric .num{color:var(--ink)}
.hfbig{color:var(--warn)!important}
"""
)

THEMES['D'] = dict(
 title="Overview — D Maximalism", minh=2040,
 font="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Space+Mono:wght@400;700&display=swap",
 top=('<div class="tick" aria-hidden="true"><div class="tick-in">'
      + ''.join('<span>SOL-USDC MULTIPLY 1.31x ▲ WARNING</span><span class="sp">✦</span><span>JLP POOL ∞ SAFE</span><span class="sp">✦</span><span>SOL SPOT $148.82</span><span class="sp">✦</span><span>PYTH FEEDS SYNCED</span><span class="sp">✦</span><span>0 / 6 LIQUIDATED</span><span class="sp">✦</span>' for _ in range(3))
      + '</div></div>'),
 bg='<div class="dots"></div>',
 css=r"""
:root{--bg:#FFE9A8;--panel:#FFFFFF;--ink:#14102B;--sub:#3a3358;--line:#14102B;
--fd:'Bricolage Grotesque',system-ui,sans-serif;--fb:'Bricolage Grotesque',system-ui,sans-serif;--fm:'Space Mono',ui-monospace,monospace;
--safe:#0b6b3a;--watch:#1747d6;--warn:#8a4300;--high:#b3300a;--crit:#c0120c;--needle:#14102B;
--dial-bg:radial-gradient(circle at 30% 15%,#fff3b0 0%,#ffcf3f 55%,#e0a200 100%);
--dial-shadow:6px 6px 0 #14102B,inset 0 3px 4px rgba(255,255,255,.8),inset 0 -6px 10px rgba(120,70,0,.45);--dial-border:3px solid #14102B;
--p-bg:#fff;--p-shadow:3px 3px 0 #14102B;--p-border:3px solid #14102B;--p-rad:999px;
--p-on-bg:#C6F432;--p-on-shadow:inset 3px 4px 0 rgba(20,16,43,.35);--p-on-ink:#14102B;
--track-bg:#14102B;--track-shadow:inset 0 3px 5px rgba(0,0,0,.6);--t-rad:999px;--t-border:3px solid #14102B;
--thumb-bg:radial-gradient(circle at 30% 25%,#fff,#ff8fd1 60%,#e0529f);--thumb-shadow:3px 3px 0 #14102B,inset 0 -3px 5px rgba(120,0,70,.35);--th-rad:50%;--th-border:3px solid #14102B}
.dots{position:absolute;inset:0;background-image:radial-gradient(#14102B 1.4px,transparent 1.6px);background-size:22px 22px;opacity:.14;pointer-events:none}
.tick{background:#14102B;color:#C6F432;font-family:var(--fm);font-size:12px;font-weight:700;overflow:hidden;white-space:nowrap;border-bottom:3px solid #14102B;position:relative}
.tick-in{display:inline-flex;gap:28px;padding:9px 0;animation:mq 40s linear infinite}
.sp{color:#FF8FD1}
@keyframes mq{from{transform:translateX(0)}to{transform:translateX(-33.33%)}}
.hdr{background:#FFFFFF;border-bottom:4px solid #14102B}
.brand{font-size:24px;font-weight:800}
.brand .v{background:#FF4D2E;color:#fff;border:2px solid #14102B;border-radius:6px;transform:rotate(-5deg)}
.tab{border-radius:999px;border:2px solid transparent;font-weight:800}
.tab.on{background:#C6F432;border-color:#14102B;color:#14102B;box-shadow:3px 3px 0 #14102B}
.badge{background:#FF4D2E;color:#fff;border:2px solid #14102B;border-radius:999px}
.wallet{background:#FF8FD1;border:3px solid #14102B;border-radius:999px;box-shadow:3px 3px 0 #14102B;color:#14102B;font-weight:700}
.launch{background:#14102B;color:#C6F432;border-radius:999px;box-shadow:3px 3px 0 #2D5BFF}
.panel,.card{border:4px solid #14102B;border-radius:20px;background:#fff}
.hero{background:#2D5BFF;color:#fff;box-shadow:10px 10px 0 #14102B;overflow:hidden}
.hero .lede,.hero .lbl{color:#e8edff}
.hero:after{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;background:repeating-radial-gradient(circle,#FF8FD1 0 8px,#2D5BFF 8px 18px);opacity:.9;pointer-events:none}
.hero-top,.chips{position:relative;z-index:1}
.eb{background:#C6F432;color:#14102B;border:2px solid #14102B;padding:3px 10px;border-radius:999px;font-weight:700;transform:rotate(-2deg);display:inline-block}
.hero .eyebrow span:last-child{color:#fff}
.h1{font-size:60px;line-height:.98;letter-spacing:-.035em;font-weight:800;max-width:760px}
.btn{border:3px solid #14102B;border-radius:999px;box-shadow:4px 4px 0 #14102B;font-weight:800}
.b-main{background:#C6F432;color:#14102B}
.b-alt{background:#fff;color:#14102B}
.pchip{border:3px solid #14102B;border-radius:999px;background:#fff;color:#14102B;font-weight:800}
.pchip.on{background:#FF8FD1;box-shadow:3px 3px 0 #14102B}
.kpis{gap:20px}
.kpi.card{box-shadow:7px 7px 0 #14102B}
.k1{background:#C6F432}.k2{background:#FFB020;grid-column:span 2}.k3{background:#FF8FD1}.k4{background:#fff}
.kpi .lbl{color:#14102B;font-weight:700}
.kpi .sub{color:#14102B}
.num{font-weight:700}
.k2 .hfbig{font-family:var(--fd);font-weight:800;font-size:110px;line-height:.9;letter-spacing:-.05em}
.k1 .num,.k3 .num{font-size:34px}
.hub{background:#14102B;color:#fff;box-shadow:10px 10px 0 #FF4D2E}
.hub .h2,.hub .sub,.hub .lbl{color:#fff}
.hub .sub{color:#d6d1f0}
.hub .stress.card{background:#fff;border:4px solid #C6F432;color:#14102B}
.hub .stress .h2,.hub .stress .sub,.hub .stress .lbl{color:#14102B}
.hub .stress .sub{color:#3a3358}
.hub .tile{background:#FFE9A8;border:3px solid #14102B;color:#14102B}
.hub .tile .lbl{color:#14102B}
.hub .stab{color:#fff;border-radius:999px;border:2px solid #fff}
.hub .stab.on{background:#C6F432;color:#14102B;border-color:#C6F432}
.hub .hub-ft,.hub .link{color:#fff}
.hub .link{color:#C6F432;text-decoration:underline;text-decoration-thickness:3px}
.h2{font-size:18px;font-weight:800}
.tile{border-radius:14px}
.wl{box-shadow:10px 10px 0 #14102B;background:#fff}
.cnt{background:#14102B;color:#C6F432;font-family:var(--fm);font-size:11px;font-weight:700;padding:3px 10px;border-radius:999px}
.stab{border-radius:999px;border:2px solid transparent;font-weight:800}
.wl .stab.on{background:#14102B;color:#C6F432}
.link{text-decoration:underline;text-decoration-thickness:3px}
.tr{border-top:3px solid #14102B}
.tr.th{border-top:0;background:#14102B;color:#C6F432;border-radius:10px}
.tr.body:nth-child(odd){background:#FFF6D6}
.tr.body:hover{background:#FFD1EC}
.chip{background:var(--tc);color:#fff;border:2px solid #14102B;border-radius:999px;font-size:12px;padding:4px 12px;transform:rotate(-2deg)}
.chip.tier-warning{background:#FFB020;color:#14102B}
.chip.tier-watch{background:#2D5BFF}
.chip.tier-safe{background:#C6F432;color:#14102B}
.pr{border-radius:14px;box-shadow:4px 4px 0 #14102B}
.proto .pr:nth-child(3n+1){background:#C6F432}.proto .pr:nth-child(3n+2){background:#FF8FD1}.proto .pr:nth-child(3n){background:#fff}
.pr span{color:#14102B}
.foot{color:#14102B;font-weight:700}
.hubc{fill:#14102B}.tk{fill:#14102B;font-family:'Space Mono',monospace;font-weight:700}
.g{stroke-width:15!important}
.dial{width:210px}
"""
)

t = THEMES[which]
css = (SHARED_CSS + t['css']).replace('@@MINH@@', str(t['minh']))
html = (MARKUP.replace('@@CSS@@', css).replace('@@TITLE@@', t['title']).replace('@@FONT@@', t['font'])
        .replace('@@BG@@', t['bg']).replace('@@TOP@@', t['top']).replace('@@MINH@@', str(t['minh'])))
os.makedirs(os.path.join(OUT, 'project'), exist_ok=True)
name = {'A':'Raw-brutalism','B':'Neobrutalism','C':'Flat-glass','D':'Maximalism'}[which] + '.dc.html'
if which == 'A': name = 'Artboard-oo62.dc.html'
open(os.path.join(OUT, 'project', name), 'w').write(html)
print(name, len(html))
