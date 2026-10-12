"""Living favicon spec + voice & copy guide boards."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui import *

# ---------- Favicon: the risk eye, simplified to two shapes so it survives 16px ----------
def fav(state, px):
    """Ink rounded square, sand lid, iris carries the state. Critical inverts to a terracotta tile."""
    crit = state == 'critical'
    tile = T4 if crit else INK
    o = {'safe': .34, 'watch': .55, 'warning': .8, 'critical': 1}[state]
    lid = INK if crit else S2
    iris = {'safe': 'none', 'watch': 'none', 'warning': T5, 'critical': INK}[state]
    sw = 3 if px <= 16 else 2.4
    return (f'<svg viewBox="0 0 32 32" width="{px}" height="{px}" aria-hidden="true" style="flex:none"><rect width="32" height="32" rx="7" fill="{tile}"/>'
            f'<g style="transform-box:fill-box;transform-origin:center;transform:scaleY({o})"><path d="M4 16 Q16 5 28 16 Q16 27 4 16Z" fill="none" stroke="{lid}" stroke-width="{sw}"/></g>'
            f'<circle cx="16" cy="16" r="{3.2 + 2.6*o:.1f}" fill="{iris}" stroke="{lid}" stroke-width="{sw*0.8:.1f}"/></svg>')

STATES = [('safe', 'Safe', 'Worst position ≥ 2.0x', 'Argus · 7 positions'),
          ('watch', 'Watch', '1.5–2.0x', 'Argus · 1.58x'),
          ('warning', 'Warning', '1.2–1.5x', '1.31x · Argus'),
          ('critical', 'Critical', '< 1.2x', '(!) 1.04x · Act now')]
grid = '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px">'
for s, name, rng, tab in STATES:
    grid += card(f'<div style="display:flex;gap:14px;align-items:flex-end">{fav(s,64)}{fav(s,32)}{fav(s,16)}</div>'
                 f'<span style="font:500 14px {M};color:{S1}">{name}</span><span style="font:400 12px {M};color:{S5}">{rng}</span>'
                 f'<div style="display:flex;gap:8px;align-items:center;padding:8px 10px;background:{K85};border:1px solid {K8}">{fav(s,16)}<span style="font:400 12px {M};color:{S2};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{tab}</span></div>', 18)
grid += '</div>'

def tabbar():
    tabs = [('critical', '(!) 1.04x · Act now'), (None, 'Kamino · Multiply'), (None, 'Drift · Trade'), (None, 'X')]
    out = f'<div style="display:flex;gap:2px;background:#0E0B08;padding:8px 8px 0">'
    for i, (s, t) in enumerate(tabs):
        icon = fav(s, 16) if s else f'<span style="width:16px;height:16px;background:{K7};display:inline-block;border-radius:3px"></span>'
        out += (f'<div style="display:flex;gap:8px;align-items:center;padding:9px 12px;min-width:170px;background:{K9 if i == 0 else K85};border:1px solid {K8};border-bottom:0">'
                f'{icon}<span style="font:400 12px {M};color:{S2 if i == 0 else S5}">{t}</span></div>')
    return out + '</div>'

RULES = [('Which position drives it', 'The single worst health factor across the watched wallet. Never an average: an average hides the position that is about to break.'),
         ('When it changes', 'Getting worse: immediately. Getting better: only after 60 seconds at the new tier, so a wick does not make the tab flicker.'),
         ('Tab title', 'Always carries the number, so state never depends on colour: “(!) 1.04x · Act now”. Safe tabs say “Argus · 7 positions”.'),
         ('No animation', 'Favicons cannot pulse reliably across browsers. Critical is shown by inverting the whole tile to terracotta instead.'),
         ('No wallet', 'Landing, docs and logged-out pages use the static 13-dot Hundred mark.'),
         ('Sizes', 'Dynamic: SVG icon, regenerated per tier. Static fallbacks: 16, 32 and 48 px PNG, 180 px apple-touch-icon (Hundred, never the risk eye). Test Safari separately: SVG favicon support there has been inconsistent.')]
rules = ''.join(f'<div style="display:grid;grid-template-columns:220px minmax(0,1fr);gap:16px;padding:14px 0;border-top:1px solid {K8}"><span style="font:500 13px {M};color:{S1}">{a}</span><span style="font:400 13px/1.6 {M};color:{S3}">{b}</span></div>' for a, b in RULES)
code = ('<pre style="margin:0;padding:18px;background:#0E0B08;border:1px solid ' + K8 + ';overflow:auto;font:400 12px/1.6 ' + M + ';color:' + S3 + '">'
        '// One function, one job: worst health factor in, favicon + title out.\n'
        'const tierOf = (hf) =&gt; hf &lt; 1.2 ? "critical" : hf &lt; 1.5 ? "warning" : hf &lt; 2 ? "watch" : "safe";\n\n'
        'export function setLivingFavicon(worstHf, positionCount) {\n'
        '  const tier = tierOf(worstHf);\n'
        '  document.querySelector(\'link[rel="icon"]\').href = `/favicon/${tier}.svg`;\n'
        '  document.title = tier === "critical" ? `(!) ${worstHf.toFixed(2)}x · Act now`\n'
        '    : tier === "safe" ? `Argus · ${positionCount} positions`\n'
        '    : `${worstHf.toFixed(2)}x · Argus`;\n'
        '}\n// Ship 4 static SVGs (one per tier) instead of drawing at runtime: simpler, cacheable.'
        '</pre>')
main = (f'<div style="max-width:1360px;margin:0 auto;padding:56px 24px;display:flex;flex-direction:column;gap:26px">'
        f'<div style="display:flex;flex-direction:column;gap:8px">{label("Living favicon · spec",T4)}{h1("The tab is a risk indicator.")}'
        f'{body("Even when Argus is a background tab, its icon shows the state of your worst position. Two shapes only, so it reads at 16 px.",S5,13)}</div>'
        f'{grid}<div style="display:flex;flex-direction:column;gap:8px">{label("In a real tab bar")}{tabbar()}</div>'
        f'<div>{rules}</div><div style="display:flex;flex-direction:column;gap:8px">{label("Implementation")}{code}</div></div>')
write_board('Favicon.dc.html', page('Argus living favicon', main, 1640), 1520, 8600, 1640, 'Living favicon · spec', fill=True)

# ---------- Voice & copy ----------
PRINCIPLES = [('Calm when fine, loud only when not.', 'Healthy states get one quiet line. Words get shorter and more direct as risk rises.'),
              ('Say the number and the fix.', 'Every warning names the position, the health factor, and the exact action: “Add $14,200 USDC to return to 1.50x.”'),
              ('Myth is seasoning, not sauce.', 'Mythic language belongs to brand moments: landing, loading, empty states, the Radar. Never in a critical alert.'),
              ('Never promise what Argus cannot do.', 'No “guaranteed”, no “never get liquidated”, no “risk-free”. Argus watches and warns; markets still move.')]
pr = ''.join(f'<div style="display:flex;flex-direction:column;gap:8px;padding:20px;border:1px solid {K8};background:{K9}"><span style="font:400 16px/1.3 {D};color:{S1}">{a}</span>{body(b,S3,13)}</div>' for a, b in PRINCIPLES)
VOCAB = [('Argus watches', '“Argus is watching 7 positions.”', 'our AI, the bot, the system'),
         ('Hermes · the lull', 'Landing and long-form only: quiet markets are when liquidations surprise people.', 'never in product UI or alerts'),
         ('Rehearse the crash', 'The stress test, the −20% simulation, the Radar scenarios.', 'backtest, scenario analysis'),
         ('Watchdog', 'An alert rule the user arms.', 'trigger, rule, notification'),
         ('Buffer', 'Collateral added to move a position away from liquidation.', 'top-up, save, rescue'),
         ('Opening his eyes', 'Loading only: “Argus is opening his eyes…”', 'Loading…, Please wait'),
         ('Act now', 'The critical label. Only for health below 1.2x.', 'URGENT!!, Danger, Rekt')]
vocab = ''.join(f'<div style="display:grid;grid-template-columns:200px minmax(0,1.6fr) minmax(0,1fr);gap:16px;padding:12px 0;border-top:1px solid {K8}"><span style="font:500 13px {M};color:{S1}">{a}</span><span style="font:400 13px/1.55 {M};color:{S3}">{b}</span><span style="font:400 13px/1.55 {M};color:{S6};text-decoration:line-through">{c}</span></div>' for a, b, c in VOCAB)
TIERS = [('safe', 'Safe', 'Argus is watching. All 7 positions are above 1.5x.'),
         ('watch', 'Watch', 'JitoSOL Loop is at 1.58x. Borrow rate rose to 11.2%.'),
         ('warning', 'Warning', 'SOL-USDC Multiply is at 1.31x. Add $14,200 USDC to return to 1.50x.'),
         ('critical', 'Critical', '1.04x on SOL-PERP. Add $8,400 USDC now.')]
tiers = ''.join(f'<div style="display:grid;grid-template-columns:44px 120px minmax(0,1fr);gap:14px;align-items:center;padding:14px 16px;border-top:1px solid {T4 if s=="critical" else K8};background:{T4 if s=="critical" else "transparent"}">{eye(s,30,on_fill=(s=="critical"))}<span style="font:500 13px {M};color:{INK if s=="critical" else S1}">{n}</span><span style="font:{"500" if s=="critical" else "400"} 14px/1.5 {M};color:{INK if s=="critical" else S3}">{t}</span></div>' for s, n, t in TIERS)
DOS = [('Add $14,200 collateral', 'Proceed'), ('1.31x · 20.4% above liquidation', 'Your position is at moderate risk'),
       ('Argus lost sight of Pyth for 12 seconds.', 'Error 503: oracle unavailable'), ('Nothing to watch yet.', 'No data found'),
       ('SOL-PERP is at 1.04x. Add $8,400 USDC now.', '🚨 URGENT!! Your position is about to get REKT!'), ('Argus watches and warns.', 'Never get liquidated again.')]
dos = ''.join(f'<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;padding:12px 0;border-top:1px solid {K8}"><span style="font:400 13px/1.5 {M};color:{S1}">✓ {a}</span><span style="font:400 13px/1.5 {M};color:{S6}">✕ {b}</span></div>' for a, b in DOS)
FMT = [('Health factor', '1.31x · two decimals · ∞ when no debt'), ('Money', '$1,842,500 · $8.4k only in tight cards'), ('Change', '−20.4% · true minus sign, always signed'),
       ('Addresses', '7xKX…3tKG · 4 + 4 characters'), ('Time', '2 min, 14 min, 1 h · absolute time in Activity'), ('Case', 'Sentence case everywhere; caps only for 11px labels')]
fmt = ''.join(f'<div style="display:grid;grid-template-columns:160px minmax(0,1fr);gap:16px;padding:10px 0;border-top:1px solid {K8}"><span style="font:500 13px {M};color:{S1}">{a}</span><span style="font:400 13px {M};color:{S3}">{b}</span></div>' for a, b in FMT)
main = (f'<div style="max-width:1360px;margin:0 auto;padding:56px 24px;display:flex;flex-direction:column;gap:30px">'
        f'<div style="display:flex;flex-direction:column;gap:8px">{label("Voice & copy",T4)}{h1("How Argus speaks.")}{body("A watchman, not a hype man: precise, calm, and never louder than the situation.",S5,13)}</div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:16px">{pr}</div>'
        f'<section style="display:flex;flex-direction:column;gap:8px">{h2("Tone by risk")}<div style="border:1px solid {K8};border-top:0">{tiers}</div></section>'
        f'<section style="display:flex;flex-direction:column;gap:8px">{h2("Vocabulary")}<div style="display:grid;grid-template-columns:200px minmax(0,1.6fr) minmax(0,1fr);gap:16px;padding:8px 0">{label("Say")}{label("How")}{label("Not")}</div>{vocab}</section>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(460px,100%),1fr));gap:28px">'
        f'<section style="display:flex;flex-direction:column;gap:8px">{h2("Do / don&#39;t")}{dos}</section>'
        f'<section style="display:flex;flex-direction:column;gap:8px">{h2("Formats")}{fmt}</section></div></div>')
write_board('Voice.dc.html', page('Argus voice and copy', main, 1900), 3040, 8600, 1900, 'Voice & copy', fill=True)
print('ok')
