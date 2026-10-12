"""Landing v2 — rebuilt on patterns stolen from Inspo's reference components:
form-led hero (input is the action), annotated stats (footnoted sources), numbered triplet (big mono ordinals),
before/after stat (movement, not magnitude), workbench (copy left, real UI right), native <details> FAQ with +/−,
statement footer (one big sentence, quiet sign-off)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui import *

IMG = '/_blob/51ef131de4d834c39e92992568c4e468'
lock_t = svgfile('logo/final/argus-lockup-terracotta.svg', 'display:block;height:30px;width:auto')
mark_big = svgfile('logo/final/argus-mark-L-terracotta.svg', 'display:block;width:100%;height:auto')
nav = ''.join(f'<a href="#{h}" style="min-height:44px;display:flex;align-items:center;padding:0 10px;font:500 13px {M};color:{INK};text-decoration:none">{n}</a>'
              for n, h in [('How it works', 'how'), ('Why Argus', 'myth'), ('FAQ', 'faq'), ('Docs ↗', 'docs')])

# Annotated stats: every number carries a footnote naming its source ("according to what?")
STATS = [('[COLLATERAL WATCHED]', 'collateral under watch', '1'), ('9', 'Solana protocols read', '2'), ('[N]', 'wallets watching today', '1')]
stats = ''.join(f'<div style="background:{INK};border:1px solid {K7};padding:22px;display:flex;flex-direction:column;gap:8px;min-width:0">'
                f'<span style="font:400 30px/1 {D};color:{S1}">{v}<sup style="font:400 12px {M};color:{T4};margin-left:4px">{n}</sup></span>'
                f'<span style="font:400 13px/1.5 {M};color:{S5}">{l}</span></div>' for v, l, n in STATS)
notes = body('¹ Live from the Argus indexer. ² Kamino, Marginfi, Drift, Jupiter, Raydium, Meteora, Orca, Sanctum, Phoenix.', S6, 12)

MYTH = [('Argus', 'The hundred-eyed giant set to watch what others could not afford to lose. Some of his eyes were always open.', 'Argus watches every position, every block, all night.'),
        ('Hermes', 'The god of merchants and thieves lulled every one of those eyes to sleep with a slow song, then struck.', 'Calm markets are the song. Liquidation bots are waiting for you to look away.'),
        ('Premeditatio malorum', 'The Stoics rehearsed misfortune before it arrived, so it never arrived as a surprise.', 'Run the crash before it happens. See which position breaks first, and by how much.')]
myth = ''.join(f'<article style="display:flex;flex-direction:column;gap:14px;padding:28px;border:1px solid {K8};background:{K9};min-width:0">'
               f'<h3 style="margin:0;font:400 22px/1.2 {D};color:{S1}">{a}</h3>{body(b,S3)}<p style="margin:0;font:500 14px/1.6 {M};color:{S1};border-top:1px solid {K8};padding-top:14px">{c}</p></article>' for a, b, c in MYTH)

# Numbered triplet: variety from type, not layout
STEPS = [('01', 'Connect', 'Paste any wallet or connect Phantom, Solflare, Backpack. Read-only: Argus never asks for a signature.'),
         ('02', 'Watch', 'Every position gets an eye. It opens as health falls, from calm ash to bright terracotta.'),
         ('03', 'Act early', 'Before 1.0x, Argus tells you exactly what to add, where, and how much. [DECIDE: approve vs automatic]')]
steps = ''.join(f'<div style="display:flex;flex-direction:column;gap:14px;min-width:0;padding-top:18px;border-top:1px solid {K7}">'
                f'<span style="font:400 64px/1 {M};color:{T4}">{n}</span><h3 style="margin:0;font:400 20px/1.2 {D};color:{S1}">{t}</h3>{body(d,S3)}</div>' for n, t, d in STEPS)

# Before / after: movement, not magnitude
before_after = (f'<div style="display:flex;flex-wrap:wrap;gap:28px;align-items:center;padding:36px;border:1px solid {K8};background:{K9}">'
                f'<div style="display:flex;flex-direction:column;gap:6px">{label("Before")}<span style="font:400 56px/1 {D};color:{T3}">1.18x</span>{eye("critical",60,glow=True)}</div>'
                f'<span aria-hidden="true" style="font:400 40px {M};color:{S6}">→</span>'
                f'<div style="display:flex;flex-direction:column;gap:6px">{label("After a $9,000 buffer")}<span style="font:400 56px/1 {D};color:{S2}">1.31x</span>{eye("watch",60)}</div>'
                f'<div style="flex:1 1 300px;min-width:0">{body("SOL-USDC Multiply on Kamino, 19:30 today. Argus flagged it at 1.18x and showed the exact top-up. Survives a −20% day instead of a −8% one. [EXAMPLE: replace with a real user story]",S3)}</div></div>')

# Workbench: copy left, the real interface right
ROWS = [('SOL-PERP Cross Margin', 'Drift', '1.04x', 'critical'), ('SOL-USDC Multiply', 'Kamino', '1.31x', 'warning'),
        ('JitoSOL Leverage Loop', 'Kamino', '1.58x', 'watch'), ('bSOL Core Supply', 'Marginfi', '2.85x', 'safe')]
rows = [(s, [n, p, hf(s, v), '<span style="display:flex;gap:8px;justify-content:flex-end;align-items:center">' + eye(s, on_fill=(s == 'critical')) + status(s) + '</span>']) for n, p, v, s in ROWS]
workbench = (f'<div style="border:1px solid {K7};background:{K9}"><div style="display:flex;justify-content:space-between;padding:12px 18px;border-bottom:1px solid {K8}">'
             f'<span style="font:400 15px {D};color:{S1}">POSITIONS</span><span style="font:400 12px {M};color:{S5}">aggregate 1.38x</span></div>'
             + table([('Position', 'left'), ('Protocol', 'left'), ('Health', 'right'), ('Status', 'right')], rows, [2, 1, .7, 1.2]) + '</div>')

# FAQ: native <details>, typographic +/−
FAQ = [('Does Argus need my keys or a signature?', 'No. Argus reads public on-chain positions. Watching a wallet needs only its address.'),
       ('Which protocols does it read?', 'Kamino, Marginfi, Drift, Jupiter, Raydium, Meteora, Orca, Sanctum and Phoenix. [CONFIRM list for v2]'),
       ('What happens when a position nears 1.0x?', 'Its eye opens wide, the row turns terracotta, the browser tab changes, and Argus shows the exact amount to add. [DECIDE: approve vs automatic]'),
       ('Is this financial advice?', 'No. Argus shows risk and options. Markets can move faster than any alert.'),
       ('What does it cost?', '[PRICING]')]
faq_css = 'details>summary{list-style:none;cursor:pointer}details>summary::-webkit-details-marker{display:none}details[open] .pm::after{content:"−"}.pm::after{content:"+"}'
faq = ''.join(f'<details style="border-top:1px solid {K8}"><summary style="display:flex;justify-content:space-between;gap:16px;align-items:center;min-height:56px;padding:8px 0;font:500 15px {M};color:{S1}">{q}<span class="pm" aria-hidden="true" style="font:400 22px {M};color:{S3}"></span></summary>'
              f'<div style="padding:0 0 20px;max-width:760px">{body(a,S3)}</div></details>' for q, a in FAQ)

inner = f'''
<section style="position:relative;background:{T5};overflow:hidden">
<img src="{IMG}" alt="Argus, a black-figure giant covered in eyes, working at a laptop under orbital rings" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:right center">
<div style="position:relative;max-width:1360px;margin:0 auto;padding:0 24px">
<header style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:14px 0">
<a href="#" aria-label="Argus home" style="display:flex;align-items:center;min-height:44px">{lock_t}</a>
<nav aria-label="Main" style="display:flex;flex-wrap:wrap;margin-left:auto">{nav}</nav>
<a href="#" style="min-height:44px;display:flex;align-items:center;padding:0 18px;background:{INK};color:{S2};font:500 14px {M};text-decoration:none">Launch app</a>
</header>
<div style="min-height:640px;display:flex;flex-direction:column;justify-content:center;gap:28px;padding:48px 0 140px;max-width:620px">
<h1 style="margin:0;font:400 60px/1.04 {D};letter-spacing:.01em;color:{INK};text-wrap:balance">A hundred eyes on your collateral.</h1>
<div style="background:{INK};padding:22px;display:flex;flex-direction:column;gap:14px;max-width:560px">
<p style="margin:0;font:400 15px/1.6 {M};color:{S2}">Paste a Solana wallet. Argus reads every lending and perps position and shows which one breaks first.</p>
<form style="display:flex;gap:8px;flex-wrap:wrap" onsubmit="return false">
<label for="w" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Solana wallet address</label>
<input id="w" type="text" placeholder="Wallet address or .sol name" style="flex:1 1 260px;min-height:44px;padding:0 14px;background:{K9};border:1px solid {K7};color:{S1};font:400 14px {M}">
<button type="submit" style="min-height:44px;padding:0 20px;background:{S2};color:{INK};border:0;font:500 14px {M};cursor:pointer">Scan wallet →</button>
</form>
<span style="font:400 12px {M};color:{S5}">Read-only. No signature, no keys.</span>
</div></div></div></section>

<section aria-label="Proof" style="max-width:1360px;margin:-84px auto 0;padding:0 24px;position:relative;display:flex;flex-direction:column;gap:10px">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:16px">{stats}</div>{notes}</section>

<section id="how" style="max-width:1360px;margin:0 auto;padding:110px 24px 40px;display:flex;flex-direction:column;gap:32px">
<div style="display:flex;flex-direction:column;gap:12px">{label("How it works",T4)}<h2 style="margin:0;font:400 40px/1.1 {D};color:{S1}">See it first. Fix it early.</h2></div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:32px">{steps}</div></section>

<section style="max-width:1360px;margin:0 auto;padding:40px 24px">{before_after}</section>

<section style="max-width:1360px;margin:0 auto;padding:60px 24px;display:flex;flex-wrap:wrap;gap:48px;align-items:center">
<div style="flex:1 1 380px;min-width:0;display:flex;flex-direction:column;gap:14px">{label("The real interface",T4)}<h2 style="margin:0;font:400 32px/1.15 {D};color:{S1}">Calm when you&#39;re fine. Loud only when you&#39;re not.</h2>
{body("Healthy positions fade back. Only the one that needs you turns terracotta. No dashboards full of red, no alerts for things that don&#39;t matter.",S3)}</div>
<div style="flex:1.3 1 520px;min-width:0">{workbench}</div></section>

<section id="myth" style="max-width:1360px;margin:0 auto;padding:80px 24px 40px;display:flex;flex-direction:column;gap:32px">
<div style="display:flex;flex-direction:column;gap:12px;max-width:760px">{label("Why the name",T4)}<h2 style="margin:0;font:400 40px/1.1 {D};color:{S1}">Named after the watchman who never slept.</h2>
{body("Liquidations don&#39;t happen to people who are watching. They happen at 3 a.m., during a quiet market, to the one position nobody checked.",S3,15)}</div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:16px">{myth}</div></section>

<section id="faq" style="max-width:1360px;margin:0 auto;padding:60px 24px 100px;display:flex;flex-wrap:wrap;gap:48px">
<div style="flex:1 1 300px;min-width:0">{h2("Questions")}</div><div style="flex:3 1 600px;min-width:0;border-bottom:1px solid {K8}">{faq}</div></section>

<footer style="background:{T5};overflow:hidden">
<div style="max-width:1360px;margin:0 auto;padding:90px 24px 0;display:flex;flex-wrap:wrap;gap:40px;align-items:flex-end;justify-content:space-between">
<div style="display:flex;flex-direction:column;gap:22px;flex:1 1 520px;min-width:0">
<p style="margin:0;font:400 52px/1.05 {D};color:{INK};text-wrap:balance">Argus never sleeps. Now neither does your collateral.</p>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a href="#" style="min-height:48px;display:flex;align-items:center;padding:0 22px;background:{INK};color:{S2};font:500 15px {M};text-decoration:none">Scan a wallet →</a></div></div>
<div style="width:170px;flex:none">{mark_big}</div></div>
<div aria-hidden="true" style="font:400 clamp(120px,22vw,320px)/.78 {D};color:{INK};letter-spacing:-.02em;white-space:nowrap;padding:40px 0 0 12px;margin-bottom:-.12em">ΛRGUS</div>
<div style="background:{INK};padding:16px 24px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;font:400 12px {M};color:{S6}"><span>ΛRGUS · Solana liquidation intelligence</span><span>Not financial advice · [LEGAL LINKS]</span></div>
</footer>'''
html = page('Argus landing', inner, 4300, faq_css)
write_board('Landing.dc.html', html, -1560, 7000, 4300, 'Landing · v2', fill=True)
print('ok')
