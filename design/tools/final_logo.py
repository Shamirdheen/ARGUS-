# Argus "Hundred" — final logo set.
# Three optical sizes of the same golden-spiral mark, so it stays crisp from billboard to 16px favicon.
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
T,K,S='#C0551E','#16110C','#EFC796'
GA=math.pi*(3-math.sqrt(5))          # golden angle, 137.5°

def spiral(n, R, dmin, dmax, eye_i, eye_scale, dot, eye):
    """n dots on a Vogel spiral inside radius R. Dot radius grows from dmin to dmax outward.
    eye_i = which dot is the terracotta 'eye on you'."""
    out=''; c=100
    k=(R-dmax)/math.sqrt(n)          # spacing so the outermost dot sits fully inside R
    for i in range(1,n+1):
        r=k*math.sqrt(i); a=i*GA
        x,y=c+r*math.cos(a),c+r*math.sin(a)
        d=dmin+(dmax-dmin)*(i/n)
        if i==eye_i: out+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{d*eye_scale:.2f}" fill="{eye}"/>'
        else: out+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{d:.2f}" fill="{dot}"/>'
    return out
# optical sizes: (dots, min r, max r, eye index, eye scale)
SIZES={'L':(100,1.7,4.6,63,1.75),'M':(34,3.6,8.2,21,1.5),'S':(13,7.5,12.5,8,1.35)}

def mark(size='L', disc=K, dot=S, eye=T, R=92):
    n,a,b,ei,es=SIZES[size]
    body=f'<circle cx="100" cy="100" r="{R+4}" fill="{disc}"/>' if disc else ''
    return body+spiral(n,R-4,a,b,ei,es,dot,eye)

def svg(w,h,body,bg=None,label='Argus'):
    r=f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">{r}{body}</svg>'

# Wordmark: Michroma, with the A replaced by a Greek lambda (Λ) drawn to the same stroke weight.
def wordmark(size=64, track=0.2):
    f=TTFont('fontsource-michroma-5.3.0/files/michroma-latin-400-normal.woff'); gs=f.getGlyphSet(); cm=f.getBestCmap(); s=size/f['head'].unitsPerEm
    bp=BoundsPen(gs); gs[cm[ord('R')]].draw(bp); cap=bp.bounds[3]*s
    # measure R's vertical stem to match the lambda's stroke
    stem=size*0.118; aw=gs[cm[ord('A')]].width*s
    x=0; parts=[]
    for ch in 'ARGUS':
        if ch=='A':
            parts.append(f'<path d="M{x+stem*0.55:.2f},0 L{x+aw/2:.2f},{-cap+stem*0.62:.2f} L{x+aw-stem*0.55:.2f},0" fill="none" stroke="currentColor" stroke-width="{stem:.2f}" stroke-linejoin="miter" stroke-miterlimit="10"/>')
            x+=aw+track*size; continue
        p=SVGPathPen(gs); gs[cm[ord(ch)]].draw(p)
        parts.append(f'<path fill="currentColor" transform="translate({x:.2f},0) scale({s:.5f},{-s:.5f})" d="{p.getCommands()}"/>'); x+=gs[cm[ord(ch)]].width*s+track*size
    return ''.join(parts), x-track*size, cap

WM,WW,CAP=wordmark()
def lockup_h(fg,bg,disc,dot,eye,name):
    m=120; gap=36; pad=44; W=round(pad+m+gap+WW+pad); H=180
    body=f'<g transform="translate({pad},{(H-m)/2}) scale({m/200})">{mark("M",disc,dot,eye)}</g>'
    body+=f'<g color="{fg}" transform="translate({pad+m+gap},{H/2+CAP/2:.2f})">{WM}</g>'
    open('final/'+name,'w').write(svg(W,H,body,bg))
def lockup_v(fg,bg,disc,dot,eye,name):
    W=round(WW+120); H=420; m=220
    body=f'<g transform="translate({(W-m)/2},{50}) scale({m/200})">{mark("L",disc,dot,eye)}</g>'
    body+=f'<g color="{fg}" transform="translate({(W-WW)/2:.2f},{50+m+50+CAP:.2f})">{WM}</g>'
    open('final/'+name,'w').write(svg(W,H,body,bg))

# Lockups: on terracotta (the vase), on ink (the product), on sand (paper/print)
lockup_h(K,T,K,S,T,'argus-lockup-terracotta.svg')
lockup_h(S,K,None,S,T,'argus-lockup-dark.svg')
lockup_h(K,S,K,S,T,'argus-lockup-light.svg')
lockup_v(K,T,K,S,T,'argus-stacked-terracotta.svg')
lockup_v(S,K,None,S,T,'argus-stacked-dark.svg')
# Marks at each optical size
for sz in 'LMS':
    open(f'final/argus-mark-{sz}-terracotta.svg','w').write(svg(200,200,mark(sz),T))
    open(f'final/argus-mark-{sz}-dark.svg','w').write(svg(200,200,mark(sz,None,S,T),K))
    open(f'final/argus-mark-{sz}-mono.svg','w').write(svg(200,200,mark(sz,None,K,K)))
# App icon: terracotta rounded square, ink seal
icon=f'<rect width="200" height="200" rx="44" fill="{T}"/><g transform="translate(22 22) scale(.78)">{mark("M")}</g>'
open('final/argus-app-icon.svg','w').write(svg(200,200,icon))
print('wordmark width',round(WW))
