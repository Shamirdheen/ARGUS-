"""Ask Argus — the Claude-powered chat, as a ⌘K command bar + a side panel next to the data.
Rules: every answer ends in a real action; numbers in Plex Mono with the risk eye; never buy/sell advice."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui import *

Y = 13000

def icon(n, size=18, col=S3):
    s = open(os.path.join(ROOT, f'icons/package/assets/light/{n}-light.svg')).read()
    return re.sub(r'<svg[^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="{size}" height="{size}" fill="{col}" aria-hidden="true" style="flex:none">', s, count=1)

def kbd(k):
    return f'<kbd style="font:500 11px {M};color:{S5};border:1px solid {K7};padding:2px 6px">{k}</kbd>'

def ghost_overview():
    """A dimmed slice of the Overview behind the overlays, so the chat is seen in context."""
    rows = [(s, [n, p, hf(s, v), '<span style="display:flex;gap:8px;justify-content:flex-end;align-items:center">' + eye(s, on_fill=(s == 'critical')) + status(s) + '</span>'])
            for n, p, v, s in [('SOL-PERP Cross Margin', 'Drift', '1.04x', 'critical'), ('SOL-USDC Multiply', 'Kamino', '1.31x', 'warning'),
                               ('JitoSOL Leverage Loop', 'Kamino', '1.58x', 'watch'), ('bSOL Core Supply', 'Marginfi', '2.85x', 'safe')]]
    main = (f'<div style="display:flex;flex-direction:column;gap:8px">{label("DeFi Whale · 7 positions")}{h1("Portfolio risk")}</div>'
            f'<div style="border:1px solid {K8}">' + table([('Position', 'left'), ('Protocol', 'left'), ('Health', 'right'), ('Status', 'right')], rows, [2, 1, .7, 1.2]) + '</div>')
    return shell('Overview', main, 'Overview')

# ---------- Board 1: ⌘K command bar ----------
def group(title, items):
    out = f'<div style="padding:10px 0 4px">{label(title)}</div>'
    for i, (ic, text, hint, active) in enumerate(items):
        out += (f'<button type="button" style="display:flex;align-items:center;gap:12px;width:100%;min-height:44px;padding:0 12px;border:0;cursor:pointer;text-align:left;'
                f'background:{K85 if active else "transparent"};{("box-shadow:inset 2px 0 0 "+S2+";") if active else ""}">{icon(ic, 18, S2 if active else S3)}'
                f'<span style="flex:1;font:400 14px {M};color:{S1 if active else S3}">{text}</span><span style="font:400 12px {M};color:{S6}">{hint}</span></button>')
    return out

palette = (f'<div role="dialog" aria-label="Ask Argus" style="width:min(680px,100%);background:{K9};border:1px solid {K7};box-shadow:0 30px 80px #000000AA">'
           f'<div style="display:flex;align-items:center;gap:12px;padding:16px 18px;border-bottom:1px solid {K8}">{eye("watch",26)}'
           f'<label for="ask" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Ask Argus</label>'
           f'<input id="ask" type="text" value="which position breaks first if SOL drops 25%" style="flex:1;min-width:0;min-height:40px;background:transparent;border:0;color:{S1};font:400 16px {M}">{kbd("↵")}</div>'
           f'<div style="padding:6px 8px 12px">'
           + group('Ask', [('flask', 'Which position breaks first if SOL drops 25%?', 'Ask ↵', True),
                           ('pulse', 'Why did my health drop overnight?', '', False),
                           ('coins', 'How much do I need to add to get SOL-PERP to 1.5x?', '', False)])
           + group('Go to', [('crosshair', 'Risk Radar', 'G R', False), ('bell', 'Alerts · 2 unread', 'G A', False), ('chart-line-up', 'Terminal', 'G T', False)])
           + group('Do', [('flask', 'Rehearse a −20% SOL crash', '', False), ('shield-check', 'Arm a watchdog on SOL-PERP', '', False)])
           + f'</div><div style="display:flex;justify-content:space-between;gap:12px;padding:10px 18px;border-top:1px solid {K8};font:400 12px {M};color:{S6}">'
           f'<span>{kbd("↑")} {kbd("↓")} move · {kbd("↵")} ask · {kbd("esc")} close</span><span>Reads your 7 positions · read-only</span></div></div>')
board1 = (f'<div style="position:relative">{ghost_overview()}<div aria-hidden="true" style="position:absolute;inset:0;background:#16110CCC"></div>'
          f'<div style="position:absolute;inset:0;display:flex;justify-content:center;padding:110px 24px">{palette}</div></div>')
write_board('Ask-bar.dc.html', page('Ask Argus command bar', board1, 900), 0, Y, 900, 'Ask Argus · ⌘K bar', fill=True)

# ---------- Board 2: side panel conversation ----------
def you(t):
    return f'<div style="align-self:flex-end;max-width:85%;background:{K85};border:1px solid {K7};padding:12px 14px;font:400 14px/1.55 {M};color:{S1}">{t}</div>'
def argus(inner):
    return (f'<div style="display:flex;gap:12px;align-items:flex-start"><span style="padding-top:2px">{svgfile("logo/final/argus-mark-S-dark.svg","display:block;width:26px;height:auto")}</span>'
            f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:12px">{inner}</div></div>')
rank = [('critical', 'SOL-PERP · Drift', '1.04x → 0.78x', 'liquidated at −15.6%'),
        ('critical', 'SOL-USDC Multiply', '1.31x → 0.98x', 'liquidated at −23.6%'),
        ('critical', 'KMNO Loop', '1.64x → 1.07x', 'survives, barely'),
        ('warning', 'JitoSOL Loop', '1.58x → 1.19x', 'survives')]
rank_html = ''.join(f'<div style="display:grid;grid-template-columns:22px 28px minmax(0,1.4fr) minmax(0,1fr);gap:10px;align-items:center;padding:10px 0;border-top:1px solid {K8}">'
                    f'<span style="font:500 12px {M};color:{S6}">{i+1}</span>{eye(s)}<span style="font:500 13px {M};color:{S1}">{n}</span>'
                    f'<span style="display:flex;flex-direction:column;align-items:flex-end;gap:2px"><span style="font:500 13px {M};color:{T3 if s=="critical" else S2}">{h}</span><span style="font:400 11px {M};color:{S5}">{d}</span></span></div>'
                    for i, (s, n, h, d) in enumerate(rank))
a1 = argus(body('At −25% SOL ($111.62), <b style="color:'+S1+';font-weight:500">two positions are liquidated</b>. SOL-PERP goes first, at −15.6%.', S3)
           + f'<div style="border:1px solid {K8};padding:0 12px">{rank_html}</div>'
           + f'<div style="display:flex;gap:8px;flex-wrap:wrap">{btn("Open in Radar →","secondary",True)}{btn("Rehearse −25%","simulate",True)}</div>'
           + f'<span style="font:400 11px {M};color:{S6}">Based on Pyth SOL/USD $148.82 at slot 312,448,901. Assumes all SOL-based collateral moves together.</span>')
fix = (f'<div style="display:flex;flex-direction:column;gap:10px;padding:14px;border:1px dashed {S6}">'
       f'<div style="display:flex;justify-content:space-between"><span style="font:400 13px {M};color:{S5}">Add to SOL-PERP</span><span style="font:500 18px {M};color:{S1}">$22,700 USDC</span></div>'
       f'<div style="display:flex;justify-content:space-between"><span style="font:400 13px {M};color:{S5}">Health</span><span style="font:500 14px {M};color:{S2}">1.04x → 1.50x</span></div>'
       f'<div style="display:flex;justify-content:space-between"><span style="font:400 13px {M};color:{S5}">Survives SOL down to</span><span style="font:500 14px {M};color:{S2}">$99.20 (−33%)</span></div></div>')
a2 = argus(body('To reach 1.50x you need about <b style="color:'+S1+';font-weight:500">$22,700 USDC</b> more collateral on Drift. A smaller $8,400 gets you to 1.20x, out of the danger zone but not comfortable.', S3)
           + fix + f'<div style="display:flex;gap:8px;flex-wrap:wrap">{btn("Simulate $22,700","simulate",True)}{btn("Open SOL-PERP","secondary",True)}</div>')
thinking = argus(f'<div style="display:flex;gap:10px;align-items:center"><svg viewBox="0 0 400 240" width="30" height="18" aria-hidden="true"><g class="ag-open"><path d="M20 120 Q200 -10 380 120 Q200 250 20 120Z" fill="none" stroke="{S2}" stroke-width="3" vector-effect="non-scaling-stroke"/></g></svg>'
                 f'<span role="status" style="font:400 13px {M};color:{S5}">Argus is looking at Drift funding history…</span></div>')
chips = ''.join(f'<button type="button" style="min-height:36px;padding:0 12px;background:transparent;border:1px solid {K7};color:{S3};font:400 12px {M};cursor:pointer">{c}</button>'
                for c in ['Arm a watchdog at 1.20x', 'What if I repay instead?', 'Explain health factor'])
panel = (f'<aside aria-label="Ask Argus" style="position:absolute;top:0;right:0;bottom:0;width:min(520px,100%);background:{K9};border-left:1px solid {K7};display:flex;flex-direction:column">'
         f'<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px 20px;border-bottom:1px solid {K8}">'
         f'<div style="display:flex;flex-direction:column;gap:4px"><span style="font:400 18px {D};color:{S1}">Ask Argus</span><span style="font:400 12px {M};color:{S5}">Reads your 7 positions · read-only · not financial advice</span></div>'
         f'<button type="button" aria-label="Close" style="min-width:40px;min-height:40px;background:transparent;border:1px solid {K7};color:{S2};font:400 16px {M};cursor:pointer">×</button></div>'
         f'<div style="flex:1;overflow:auto;padding:20px;display:flex;flex-direction:column;gap:22px">'
         f'{you("Which position breaks first if SOL drops 25%?")}{a1}{you("How much to fix SOL-PERP properly?")}{a2}{you("Is Drift funding making it worse?")}{thinking}</div>'
         f'<div style="border-top:1px solid {K8};padding:14px 20px;display:flex;flex-direction:column;gap:10px"><div style="display:flex;gap:8px;flex-wrap:wrap">{chips}</div>'
         f'<div style="display:flex;gap:8px"><label for="q2" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Ask a question</label>'
         f'<input id="q2" type="text" placeholder="Ask about your positions…" style="flex:1;min-width:0;min-height:44px;padding:0 12px;background:{INK};border:1px solid {K7};color:{S1};font:400 14px {M}">{btn("Ask →")}</div></div></aside>')
css = '''@keyframes argusOpen{0%,100%{transform:scaleY(.08)}45%,70%{transform:scaleY(.62)}}
.ag-open{transform-box:fill-box;transform-origin:center;animation:argusOpen 2.4s ease-in-out infinite}
@media (prefers-reduced-motion: reduce){.ag-open{animation:none}}'''
board2 = f'<div style="position:relative;min-height:1180px">{ghost_overview()}<div aria-hidden="true" style="position:absolute;inset:0;background:#16110C99"></div>{panel}</div>'
write_board('Ask-panel.dc.html', page('Ask Argus panel', board2, 1180, css), 1520, Y, 1180, 'Ask Argus · side panel', fill=True)
print('ok')
