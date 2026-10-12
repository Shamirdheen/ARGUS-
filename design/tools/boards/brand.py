import re
L='logo/'
INK,INK9,INK85,INK8,INK7='#16110C','#1E1711','#271E16','#33271D','#482A16'
T7,T6,T5,T4,T3='#853F19','#A04A1B','#C0551E','#D06F3C','#E0946A'
S1,S2,S3,S5,S6='#F6DDB8','#EFC796','#DEB281','#A8865F','#7E654A'
WATCH,WARN,CRIT='#77BECF','#EFD280','#E8669C'
MONO="'IBM Plex Mono',ui-monospace,monospace"; DISP="Michroma,'Arial Black',sans-serif"
def inner(f):
    s=open(L+f).read(); s=re.sub(r'\swidth="\d+"\sheight="\d+"','',s,count=1)
    return s.replace('<svg ','<svg style="display:block;width:100%;height:auto" ',1)
def eye(state):
    if state=='safe':
        return f'<svg viewBox="0 0 120 64" width="120" height="64" aria-hidden="true"><path d="M8 32 Q60 6 112 32 Q60 52 8 32Z" fill="{S2}"/><path d="M8 32 Q60 20 112 32" fill="none" stroke="{INK}" stroke-width="5"/><circle cx="60" cy="36" r="9" fill="{INK}"/></svg>'
    col={'watch':WATCH,'warning':WARN,'critical':CRIT}[state]; h={'watch':26,'warning':30,'critical':34}[state]; r={'watch':13,'warning':15,'critical':17}[state]
    return f'<svg viewBox="0 0 120 72" width="120" height="72" aria-hidden="true"><path d="M8 36 Q60 {36-h*1.6} 112 36 Q60 {36+h*1.6} 8 36Z" fill="{S2}"/><circle cx="60" cy="36" r="{r}" fill="none" stroke="{col}" stroke-width="5"/><circle cx="60" cy="36" r="{r-7}" fill="{INK}"/></svg>'
lab=lambda t,c=S5: f'<span style="font:400 12px/1.4 {MONO};color:{c}">{t}</span>'
def ramp(name,role,items):
    cells=''.join(f'<div style="display:flex;flex-direction:column;gap:6px"><div style="height:72px;background:{h};border:1px solid {INK8}"></div><span style="font:500 12px/1.2 {MONO};color:{S1}">{n}</span>{lab(h)}</div>' for n,h in items)
    return f'<div style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;gap:12px;align-items:baseline;flex-wrap:wrap"><h3 style="margin:0;font:400 15px/1.2 {DISP};letter-spacing:.06em;text-transform:uppercase;color:{S1}">{name}</h3>{lab(role)}</div><div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px">{cells}</div></div>'
ramps=(ramp('Terracotta','The vase: landing ground, brand, primary actions',[('700',T7),('600',T6),('500 · base',T5),('400',T4),('300',T3)])+
       ramp('Ink','Inside the figure: product ground and surfaces',[('950 · base',INK),('900',INK9),('850',INK85),('800',INK8),('700',INK7)])+
       ramp('Sand','Incised line: text, borders, the safe state',[('100',S1),('200 · base',S2),('300',S3),('500',S5),('600',S6)]))
risk=''.join(f'<div style="display:flex;flex-direction:column;gap:10px;align-items:flex-start">{eye(s)}<span style="font:500 13px/1.3 {MONO};color:{S1};text-transform:uppercase;letter-spacing:.08em">{n}</span>{lab(d)}</div>' for s,n,d in [('safe','Safe · sand','No colour. Resting eye.'),('watch',f'Watch · {WATCH}','Only cool hue in the system.'),('warning',f'Warning · {WARN}','Gold, far lighter than clay.'),('critical',f'Critical · {CRIT}','Hot coral, lighter than terracotta, plus red row tint.')])
rules=[('Black text on terracotta','4.07:1','Headlines and 18px+ bold only. Body copy on terracotta sits on a sand or ink card.'),
       ('Terracotta 500 on ink','4.07:1','Fills, icons and large text only. Links and small text use Terracotta 400 (5.38:1).'),
       ('Primary button','5.38:1','Terracotta 400 fill with ink text in the product; ink fill with sand text on the terracotta landing.'),
       ('Sand 200 on ink','11.86:1','Default text. Sand 500 (5.57:1) for secondary text; Sand 600 only for borders.'),
       ('Critical vs terracotta','1.65:1','Close in lightness, so critical always adds a form cue: tinted row, wide red eye, never colour alone.')]
rule_rows=''.join(f'<div style="display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.5fr) minmax(0,3fr);gap:16px;padding:14px 0;border-top:1px solid {INK8};font:400 13px/1.5 {MONO};color:{S2}"><span style="color:{S1}">{a}</span><span style="color:{T4}">{b}</span><span>{c}</span></div>' for a,b,c in rules)
meander=f'<svg viewBox="0 0 240 24" preserveAspectRatio="none" style="display:block;width:100%;height:24px" aria-hidden="true"><defs><pattern id="mk" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M2 22 V2 H22 V18 H8 V8 H16 V14" fill="none" stroke="{T5}" stroke-width="2.4"/></pattern></defs><rect width="240" height="24" fill="url(#mk)"/></svg>'
H2=lambda t: f'<h2 style="margin:0;font:400 20px/1.2 {DISP};letter-spacing:.06em;text-transform:uppercase;color:{S1}">{t}</h2>'
html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Argus brand v1</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=Michroma&amp;display=swap">
<style>
body{{margin:0;background:{INK}}}
</style>
</helmet>
<div style="width:1440px;box-sizing:border-box;background:{INK};color:{S2};display:flex;flex-direction:column;font-family:{MONO}">
<section style="position:relative;height:810px;background:{T5};overflow:hidden">
<img src="/_blob/51ef131de4d834c39e92992568c4e468" alt="Argus, a black-figure giant covered in eyes, typing on a laptop beneath orbital rings" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
<div style="position:relative;padding:72px;display:flex;flex-direction:column;gap:24px;max-width:640px">
<div style="width:320px">{inner('argus-lockup-terracotta.svg')}</div>
<h1 style="margin:0;font:400 64px/1.02 {DISP};letter-spacing:.02em;color:{INK}">A hundred eyes on your collateral.</h1>
<p style="margin:0;font:500 20px/1.5 {MONO};color:{INK};max-width:460px">Argus never sleeps. It watches every Solana position and acts before the liquidators do.</p>
</div>
</section>
<div style="padding:72px;display:flex;flex-direction:column;gap:56px">
<header style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:flex-end">
<div style="display:flex;flex-direction:column;gap:10px"><span style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:{T4}">Brand v1 · colour system from the illustration</span>{H2('Three colours, two surfaces')}</div>
<p style="margin:0;max-width:520px;font-size:14px;line-height:1.6;color:{S3}">Every value is sampled from the hero image. Terracotta is the vase: landing and brand. Ink is inside the figure: the product. Sand is the incised line: text and borders everywhere.</p>
</header>
{meander}
{ramps}
{meander}
<section style="display:flex;flex-direction:column;gap:20px">{H2('Risk eyes')}<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px">{risk}</div></section>
<section style="display:flex;flex-direction:column;gap:8px">{H2('Contrast rules')}<div>{rule_rows}</div></section>
{meander}
<section style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px">
<div style="grid-column:span 2;display:flex;flex-direction:column;gap:24px">{inner('argus-lockup-terracotta.svg')}{inner('argus-lockup-dark.svg')}{inner('argus-lockup-light.svg')}</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;align-content:start">{inner('argus-mark-terracotta.svg')}{inner('argus-mark-dark.svg')}<div style="background:{S2}">{inner('argus-mark-mono.svg')}</div><div style="display:flex;align-items:center;justify-content:center;gap:16px;border:1px solid {INK8}"><div style="width:32px">{inner('argus-mark-terracotta.svg')}</div><div style="width:16px">{inner('argus-mark-terracotta.svg')}</div></div></div>
</section>
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":2780}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''
open('root/project/Brand.dc.html','w').write(html); print(len(html))
