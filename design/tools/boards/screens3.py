"""Risk Radar (constellation), Alerts, Activity — built from the shared Argus UI kit."""
import sys, math, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui import *

Y0 = 11400

# ---------- Risk Radar: positions as stars, distance from the core = distance from liquidation ----------
C = 360
def radius(hf):
    return 46 + (min(hf, 2.6) - 1.0) / 1.6 * 270 if hf >= 1 else 46 * hf ** 3
def tier(hf):
    return 'critical' if hf < 1.2 else 'warning' if hf < 1.5 else 'watch' if hf < 2 else 'safe'

# (name, protocol, health now, health at -20% SOL, collateral $k, angle)
POS = [('SOL-PERP', 'Drift', 1.04, 0.83, 185, 200), ('SOL-USDC Multiply', 'Kamino', 1.31, 1.05, 820, 250),
       ('JitoSOL Loop', 'Kamino', 1.58, 1.26, 410, 290), ('KMNO Loop', 'Kamino', 1.64, 1.15, 64, 320),
       ('CLMM Range', 'Raydium', 1.72, 1.38, 95, 40), ('bSOL Supply', 'Marginfi', 2.85, 2.28, 190, 120),
       ('JLP Pool', 'Jupiter', 9.9, 9.9, 120, 160)]

svg = '<svg viewBox="0 0 720 720" width="100%" role="img" aria-label="Risk constellation at a 20 percent SOL drop: SOL-PERP falls inside the liquidation core" style="display:block;max-width:720px">'
random.seed(3)
svg += ''.join(f'<circle cx="{random.uniform(20,700):.0f}" cy="{random.uniform(20,700):.0f}" r="{random.choice([.8,1,1.3])}" fill="{S6}" opacity=".6"/>' for _ in range(90))
for ring in [1.2, 1.5, 2.0, 2.5]:
    dash = 'stroke-dasharray="3 6"' if ring in (1.5, 2.0) else ''
    svg += (f'<circle cx="{C}" cy="{C}" r="{radius(ring):.1f}" fill="none" stroke="{T7 if ring == 1.2 else K7}" stroke-width="1" {dash}/>'
            f'<text x="{C+4}" y="{C-radius(ring)-6:.1f}" fill="{S6}" font-family="IBM Plex Mono" font-size="12">{ring:.1f}x</text>')
svg += f'<circle cx="{C}" cy="{C}" r="46" fill="{T5}" opacity=".9"/><text x="{C}" y="{C+4}" text-anchor="middle" fill="{INK}" font-family="IBM Plex Mono" font-size="12" font-weight="500">1.00x</text>'

pts = {}
for name, proto, h_now, h_st, size, ang in POS:
    a = math.radians(ang)
    x0, y0 = C + radius(h_now) * math.cos(a), C + radius(h_now) * math.sin(a)
    x1, y1 = C + radius(h_st) * math.cos(a), C + radius(h_st) * math.sin(a)
    pts[name] = (x1, y1)
    svg += f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="3" fill="none" stroke="{S6}"/><line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{S6}" stroke-dasharray="2 4"/>'
for a_, b_ in [('SOL-PERP', 'SOL-USDC Multiply'), ('SOL-USDC Multiply', 'JitoSOL Loop'), ('JitoSOL Loop', 'bSOL Supply'), ('SOL-USDC Multiply', 'CLMM Range')]:
    (xa, ya), (xb, yb) = pts[a_], pts[b_]
    svg += f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{S3}" stroke-width="1" opacity=".5"/>'
for name, proto, h_now, h_st, size, ang in POS:
    x, y = pts[name]; t = tier(h_st); rr = 4 + math.sqrt(size) / 3.2
    col = {'critical': T3, 'warning': T5, 'watch': S2, 'safe': S5}[t]
    if t == 'critical':
        svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr*2.6:.1f}" fill="{T5}" opacity=".35" style="filter:blur(6px)"/>'
    svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{INK if t == "watch" else col}" stroke="{col}" stroke-width="2"/>'
    right = x < C + 150
    lab = f'{name} · {"∞" if h_st > 9 else f"{h_st:.2f}x"}'
    svg += (f'<text x="{(x+rr+8) if right else (x-rr-8):.1f}" y="{y+4:.1f}" text-anchor="{"start" if right else "end"}" '
            f'fill="{S1 if t in ("critical","warning") else S3}" font-family="IBM Plex Mono" font-size="13">{lab}</text>')
svg += '</svg>'

SCEN = [('0%', '$148.82'), ('−10%', '$133.94'), ('−20%', '$119.06'), ('−30%', '$104.17'), ('−40%', '$89.29'), ('−50%', '$74.41')]
segs = ('<div role="group" aria-label="SOL drawdown" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid ' + K7 + '">' + ''.join(
    f'<button type="button" style="min-height:56px;border:0;border-right:1px solid {K8};border-bottom:1px solid {K8};cursor:pointer;font:500 13px {M};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;'
    f'{("background:"+S2+";color:"+INK) if a == "−20%" else ("background:transparent;color:"+S3)}"><span>{a}</span><span style="font:400 11px {M};opacity:.8">{b}</span></button>' for a, b in SCEN) + '</div>')
BRK = [('critical', 'SOL-PERP · Drift', 'liquidated at −15.6%'), ('critical', 'SOL-USDC Multiply', '1.05x'), ('critical', 'KMNO Loop', '1.15x'),
       ('warning', 'JitoSOL Loop', '1.26x'), ('warning', 'CLMM Range', '1.38x')]
brk = ''.join(f'<div style="display:flex;gap:10px;align-items:center;padding:10px 0;border-top:1px solid {K8}">{eye(s)}<span style="font:500 13px {M};color:{S1};flex:1">{n}</span>'
              f'<span style="font:400 12px {M};color:{T3 if s == "critical" else S5}">{d}</span></div>' for s, n, d in BRK)
side = card(f'{label("Rehearse a SOL drawdown")}<span style="font:400 44px/1 {D};color:{T3}">−20%</span>{segs}'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">{stat("Liquidated","1 of 7","",T3)}{stat("Capital lost","$185,000")}</div>'
            f'<div style="display:flex;flex-direction:column">{label("Under this scenario")}{brk}</div><div style="display:flex;gap:10px;flex-wrap:wrap">{btn("Plan buffers for −20%","simulate")}</div>')
main = (f'<div style="display:flex;flex-direction:column;gap:8px">{label("Premeditatio malorum")}{h1("Risk Radar")}'
        f'{body("Every position is a star. The closer it falls to the terracotta core, the closer it is to liquidation. Hollow circles show where each star sits today; lines join positions that move together.",S5,13)}</div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start"><div style="flex:999 1 640px;min-width:0;display:flex;justify-content:center;background:#0E0B08;border:1px solid {K8};padding:20px">{svg}</div>'
        f'<div style="flex:1 1 340px;min-width:0">{side}</div></div>')
write_board('Radar.dc.html', page('Argus Risk Radar', shell('Radar', main, 'Radar'), 1220), 6080, Y0, 1220, 'Risk Radar · constellation', fill=True)

# ---------- Alerts: inbox + watchdog rules ----------
AL = [('critical', '2 min', 'SOL-PERP Cross Margin', 'Health fell to 1.04x. Add $8,400 USDC to return to 1.30x.', True),
      ('warning', '14 min', 'SOL-USDC Multiply', 'Crossed below your 1.35x watchdog.', True),
      ('watch', '1 h', 'Pyth SOL/USD', 'Oracle confidence widened to ±$0.04 for 40s.', False),
      ('watch', '3 h', 'JitoSOL Leverage Loop', 'Borrow rate rose to 11.2% APY.', False)]
inbox = ''
for s, t, n, msg, unread in AL:
    crit = s == 'critical'
    dotc = INK if crit else S2
    unread_dot = f' <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:{dotc};margin-left:6px"></span>' if unread else ''
    actions = (btn('Act now', 'primary', True) if crit else btn('View', 'secondary', True)) + ('' if crit else btn('Simulate', 'simulate', True)) + btn('Snooze 1h', 'ghost', True)
    inbox += (f'<div style="display:flex;gap:14px;align-items:flex-start;padding:16px 18px;border-top:1px solid {T4 if crit else K8};background:{T4 if crit else "transparent"}">'
              f'<span style="padding-top:3px">{eye(s,26,on_fill=crit)}</span><div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:6px">'
              f'<div style="display:flex;justify-content:space-between;gap:10px"><span style="font:500 14px {M};color:{INK if crit else S1}">{n}{unread_dot}</span><span style="font:400 12px {M};color:{INK if crit else S6}">{t}</span></div>'
              f'<span style="font:400 13px/1.5 {M};color:{INK if crit else S3}">{msg}</span><div style="display:flex;gap:8px;flex-wrap:wrap">{actions}</div></div></div>')
RULES = [('SOL-USDC Multiply', 'Health below 1.35x', 'In-app · [CHANNEL]', True), ('SOL-PERP Cross Margin', 'Health below 1.20x', 'In-app · [CHANNEL]', True),
         ('All positions', 'Oracle drift over 0.3%', 'In-app', True), ('JitoSOL Leverage Loop', 'Borrow rate over 10%', 'In-app', False)]
rules = ''.join(
    f'<div style="display:flex;justify-content:space-between;gap:12px;align-items:center;padding:14px 0;border-top:1px solid {K8}"><div style="display:flex;flex-direction:column;gap:3px;min-width:0">'
    f'<span style="font:500 13px {M};color:{S1}">{n}</span><span style="font:400 12px {M};color:{S5}">{c} · {ch}</span></div>'
    f'<button type="button" role="switch" aria-checked="{"true" if on else "false"}" aria-label="Watchdog for {n}" style="flex:none;width:52px;min-height:30px;border:1px solid {S2 if on else K7};background:{S2 if on else "transparent"};position:relative;cursor:pointer">'
    f'<span style="position:absolute;top:4px;{"right" if on else "left"}:4px;width:20px;height:20px;background:{INK if on else S6}"></span></button></div>' for n, c, ch, on in RULES)
newrule = card(f'{h2("New watchdog")}<div style="display:grid;gap:14px">{field("np","Position","","SOL-USDC Multiply")}'
               f'<div style="display:flex;flex-direction:column;gap:6px">{label("Watch")}{seg(["Health","Price","Oracle drift","Borrow rate"],"Health")}</div>'
               f'{field("nt","Alert when below","","1.25","x")}<div style="display:flex;flex-direction:column;gap:6px">{label("Notify")}{seg(["In-app","Telegram","Email"],"In-app")}</div></div>'
               f'{btn("Arm watchdog")}<span style="font:400 12px {M};color:{S6}">[CONFIRM which notification channels v2 supports]</span>')
main = (f'<div style="display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:flex-end"><div style="display:flex;flex-direction:column;gap:8px">{label("2 unread")}{h1("Alerts")}</div>{seg(["All","Unread 2","Critical","Archived"],"All")}</div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start"><div style="flex:999 1 620px;min-width:0;border:1px solid {K8};border-top:0">{inbox}</div>'
        f'<div style="flex:1 1 360px;min-width:0;display:flex;flex-direction:column;gap:20px">{card(h2("Watchdogs")+"<div>"+rules+"</div>")}{newrule}</div></div>')
write_board('Alerts.dc.html', page('Argus Alerts', shell('Alerts', main, 'Alerts'), 1260), 7600, Y0, 1260, 'Alerts + watchdogs', fill=True)

# ---------- Activity: day-grouped log ----------
def dot(c):
    return f'<span aria-hidden="true" style="width:8px;height:8px;background:{c};display:inline-block;flex:none;margin-top:6px"></span>'
DAYS = [('Today', [('22:41', 'Argus', 'critical', 'SOL-PERP fell to 1.04x. Alert sent; buffer of $8,400 suggested.', None),
                   ('22:12', 'You', 'watch', 'Ran a −20% rehearsal. 1 of 7 positions breaks.', None),
                   ('21:58', 'Oracle', 'watch', 'Pyth and Switchboard SOL prices diverged 0.4% for 40s.', None),
                   ('19:30', 'You', 'safe', 'Added 9,000 USDC collateral to SOL-USDC Multiply. 1.18x → 1.31x.', '5Kx9…qL2a')]),
        ('Yesterday', [('23:05', 'Market', 'watch', '$2.1M of SOL longs liquidated on Drift within 60s.', None),
                       ('14:20', 'Argus', 'safe', 'Started watching 7xKX…3tKG. 7 positions across 5 protocols.', None),
                       ('14:19', 'You', 'safe', 'Connected Phantom.', None)])]
ACTOR = {'Argus': T3, 'You': S2, 'Oracle': S5, 'Market': S5}
log = ''
for day, events in DAYS:
    log += f'<div style="display:flex;flex-direction:column"><div style="padding:18px 0 10px">{label(day)}</div>'
    for t, actor, s, text, tx in events:
        link = f'<a href="#" style="font:400 12px {M};white-space:nowrap">{tx} ↗</a>' if tx else '<span></span>'
        log += (f'<div style="display:grid;grid-template-columns:64px 90px minmax(0,1fr) auto;gap:14px;align-items:start;padding:14px 0;border-top:1px solid {K8}">'
                f'<span style="font:400 12px {M};color:{S6};padding-top:2px">{t}</span><span style="display:flex;gap:8px;align-items:flex-start;font:500 13px {M};color:{ACTOR[actor]}">{dot(ACTOR[actor])}{actor}</span>'
                f'<span style="font:400 14px/1.55 {M};color:{S1 if s == "critical" else S3}">{text}</span>{link}</div>')
    log += '</div>'
main = (f'<div style="display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:flex-end"><div style="display:flex;flex-direction:column;gap:8px">{label("Everything Argus saw, and everything you did")}{h1("Activity")}</div>{seg(["All","Argus","You","Market","Oracle"],"All")}</div>'
        f'<div style="max-width:980px">{log}</div>{body("Transactions open on Solscan. [DECIDE: approve vs automatic — today Argus only suggests; you sign.]",S6,12)}')
write_board('Activity.dc.html', page('Argus Activity', shell('Activity', main, 'Activity'), 1120), 9120, Y0, 1120, 'Activity', fill=True)
print('ok')
