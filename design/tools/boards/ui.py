"""Argus UI kit for canvas artboards — one source for every screen, so primitives stay identical.
Locked system: dark only · Mono-2 (terracotta = danger) · Michroma + IBM Plex Mono."""
import re, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK,K9,K85,K8,K7 = '#16110C','#1E1711','#271E16','#33271D','#482A16'
S1,S2,S3,S5,S6 = '#F6DDB8','#EFC796','#DEB281','#A8865F','#7E654A'
T3,T4,T5,T7 = '#E0946A','#D06F3C','#C0551E','#853F19'
M = "'IBM Plex Mono',ui-monospace,monospace"; D = "Michroma,sans-serif"
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Michroma&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">'

def svgfile(path, style):
    s = open(os.path.join(ROOT, path)).read()
    s = re.sub(r'\swidth="\d+"\sheight="\d+"', '', s, count=1)
    s = re.sub(r'<rect width="\d+" height="\d+" fill="#(16110C|C0551E)"/>', '', s)
    return s.replace('<svg ', f'<svg style="{style}" ', 1)

LOCK = lambda h=28: svgfile('logo/final/argus-lockup-dark.svg', f'display:block;height:{h}px;width:auto')

# ---- risk ----
HF_COL = {'critical': INK, 'warning': T3, 'watch': S2, 'safe': S5}
def eye(state, w=22, on_fill=False, glow=False):
    o = {'safe': .32, 'watch': .55, 'warning': .78, 'critical': 1}[state]
    i = {'safe': .6, 'watch': .8, 'warning': .95, 'critical': 1.05}[state]
    lid = INK if on_fill else {'safe': S6, 'watch': S2, 'warning': T3, 'critical': T3}[state]
    iris = INK if on_fill else {'safe': 'none', 'watch': 'none', 'warning': T5, 'critical': T3}[state]
    g = '<ellipse cx="200" cy="120" rx="160" ry="80" fill="#C0551E" opacity=".45" style="filter:blur(22px)"></ellipse>' if glow else ''
    return (f'<svg viewBox="0 0 400 240" width="{w}" height="{round(w*.6)}" aria-hidden="true" style="flex:none">{g}'
            f'<g style="transform-box:fill-box;transform-origin:center;transform:scaleY({o})"><path d="M20 120 Q200 -10 380 120 Q200 250 20 120Z" fill="{INK if w>40 else "none"}" stroke="{lid}" stroke-width="2.4" vector-effect="non-scaling-stroke"></path></g>'
            f'<circle cx="200" cy="120" r="64" fill="{iris}" stroke="{lid}" stroke-width="2" vector-effect="non-scaling-stroke" style="transform-box:fill-box;transform-origin:center;transform:scale({i})"></circle></svg>')
def status(state):
    return {'critical': f'<span style="font:500 12px/1 {M};padding:6px 9px;color:{T4};background:{INK}">Act now</span>',
            'warning': f'<span style="font:500 13px {M};color:{T3}">Warning</span>',
            'watch': f'<span style="font:400 13px {M};color:{S2}">Watch</span>', 'safe': ''}[state]
def hf(state, v, size=14):
    deco = 'text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px;' if state == 'warning' else ''
    return f'<span style="font:500 {size}px {M};color:{HF_COL[state]};{deco}font-variant-numeric:tabular-nums">{v}</span>'

# ---- primitives ----
def btn(label, kind='primary', small=False):
    h = 36 if small else 44
    st = {'primary': f'background:{S2};color:{INK};border:1px solid {S2}',
          'secondary': f'background:transparent;color:{S2};border:1px solid {K7}',
          'simulate': f'background:transparent;color:{S2};border:1px dashed {S6}',
          'danger': f'background:{T4};color:{INK};border:1px solid {T4}',
          'ghost': f'background:transparent;color:{S3};border:1px solid transparent'}[kind]
    return f'<button type="button" style="min-height:{h}px;padding:0 {14 if small else 18}px;{st};font:500 {13 if small else 14}px {M};cursor:pointer">{label}</button>'
def label(t, c=S5): return f'<span style="font:500 11px {M};letter-spacing:.1em;text-transform:uppercase;color:{c}">{t}</span>'
def h1(t): return f'<h1 style="margin:0;font:400 34px/1.1 {D};color:{S1}">{t}</h1>'
def h2(t): return f'<h2 style="margin:0;font:400 17px/1.2 {D};letter-spacing:.06em;color:{S1}">{t.upper()}</h2>'
def body(t, c=S3, size=14): return f'<p style="margin:0;font:400 {size}px/1.6 {M};color:{c}">{t}</p>'
def card(inner, pad=22, bg=K9, extra=''): return f'<div style="background:{bg};border:1px solid {K8};padding:{pad}px;display:flex;flex-direction:column;gap:14px;min-width:0;{extra}">{inner}</div>'
def stat(lbl, val, sub='', vc=S1, big=False):
    f = f"400 34px/1 {D}" if big else f"500 22px/1 {M}"
    return f'<div style="display:flex;flex-direction:column;gap:6px;min-width:0">{label(lbl)}<span style="font:{f};color:{vc};font-variant-numeric:tabular-nums">{val}</span>{("<span style=\"font:400 12px "+M+";color:"+S5+"\">"+sub+"</span>") if sub else ""}</div>'
def field(lid, lab, ph='', value='', suffix=''):
    return (f'<div style="display:flex;flex-direction:column;gap:6px;min-width:0"><label for="{lid}" style="font:500 12px {M};color:{S3}">{lab}</label>'
            f'<div style="display:flex;align-items:center;border:1px solid {K7};background:{INK}"><input id="{lid}" type="text" placeholder="{ph}" value="{value}" style="flex:1;min-width:0;min-height:44px;padding:0 12px;background:transparent;border:0;color:{S1};font:400 14px {M}">'
            f'{("<span style=\"padding:0 12px;font:400 13px "+M+";color:"+S5+"\">"+suffix+"</span>") if suffix else ""}</div></div>')
def seg(options, active):
    return '<div role="group" style="display:flex;flex-wrap:wrap;border:1px solid '+K7+'">'+''.join(
        f'<button type="button" style="min-height:40px;flex:1 1 auto;padding:0 14px;font:500 13px {M};cursor:pointer;border:0;{("background:"+S2+";color:"+INK) if o==active else ("background:transparent;color:"+S3)}">{o}</button>' for o in options)+'</div>'

# ---- table ----
def table(cols, rows, widths):
    """cols: [(title, align)], rows: [(state, [cells])]; cells are HTML. Critical rows invert to terracotta."""
    gt = ' '.join(f'minmax(0,{w}fr)' for w in widths)
    g = f'display:grid;grid-template-columns:{gt};gap:12px;align-items:center;padding:13px 18px'
    head = f'<div style="{g};font:500 11px {M};letter-spacing:.08em;text-transform:uppercase;color:{S5}">' + ''.join(f'<span style="text-align:{a}">{t}</span>' for t, a in cols) + '</div>'
    out = head
    for state, cells in rows:
        crit = state == 'critical'
        out += f'<div style="{g};border-top:1px solid {T4 if crit else K8};background:{T4 if crit else "transparent"};color:{INK if crit else S2}">' + ''.join(
            f'<span style="text-align:{cols[i][1]};{"justify-self:end;" if cols[i][1]=="right" else ""}font:{"500" if i==0 else "400"} 14px {M};color:{(INK if crit else (S1 if i==0 else S5))};min-width:0">{c}</span>' for i, c in enumerate(cells)) + '</div>'
    return out

# ---- app shell ----
NAV = ['Overview', 'Positions', 'Terminal', 'Radar', 'Alerts', 'Activity']
def shell(active, main_html, title):
    nav = ''.join(f'<a href="#" style="min-height:44px;display:flex;align-items:center;padding:0 12px;font:500 13px {M};text-decoration:none;color:{S1 if n==active else S5};{"box-shadow:inset 0 -2px 0 "+S2+";" if n==active else ""}">{n}{(" <span style=\"margin-left:6px;font:500 11px "+M+";padding:2px 5px;background:"+T4+";color:"+INK+"\">2</span>") if n=="Alerts" else ""}</a>' for n in NAV)
    return f'''<header style="border-bottom:1px solid {K8}"><div style="max-width:1360px;margin:0 auto;padding:10px 24px;display:flex;flex-wrap:wrap;gap:16px;align-items:center">
<a href="#" aria-label="Argus home" style="display:flex;align-items:center;min-height:44px">{LOCK()}</a>
<nav aria-label="Main" style="display:flex;flex-wrap:wrap;margin-left:16px">{nav}</nav>
<div style="margin-left:auto;display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span style="display:flex;gap:8px;align-items:center;font:400 12px {M};color:{S5};padding:0 12px;min-height:36px;border:1px solid {K8}"><span style="width:6px;height:6px;background:{S2};border-radius:50%"></span>slot 312,448,901</span>{btn("Demo…3tKG","secondary",True)}</div></div></header>
<main style="max-width:1360px;margin:0 auto;padding:32px 24px 64px;display:flex;flex-direction:column;gap:28px">{main_html}</main>'''

def page(title, inner, height, extra_css='', script_body='renderVals() { return {}; }'):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
body{{margin:0;background:{INK}}}
a{{color:{S2}}}a:hover{{color:{S1}}}
{extra_css}
</style>
</helmet>
<div style="min-height:100vh;background:{INK};color:{S2};font-family:{M}">
{inner}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":{height}}}}}'>
class Component extends DCLogic {{
{script_body}
}}
</script>
</body>
</html>
'''

def write_board(fname, html, x, y, h, title, fill=True, interactive=False):
    open(os.path.join(ROOT, 'root/project', fname), 'w').write(html)
    p = os.path.join(ROOT, 'root/project/canvas.json'); c = json.load(open(p))
    e = {"x": x, "y": y, "w": 1440, "h": h, "title": title}
    if fill: e["expand"] = "fill"
    if interactive: e["is_interactive"] = True
    c['boards'][fname] = e
    if fname not in c['order']: c['order'].append(fname)
    json.dump(c, open(p, 'w'), indent=2)
