"""Build design/prototype/argus-prototype.html: the canvas boards stitched into one clickable file.

Usage:  python3 design/tools/build_prototype.py
Reads   design/source/*.dc.html (export of the Claude Design canvas)
Embeds  fonts (node_modules/@fontsource) and the hero image as base64, so the file works offline.

Each board keeps its own markup and inline styles untouched; this script only wraps every board in a
<section>, and appends a small router (prototype.js below) that maps button/link text to screens.
"""
import base64, html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "design" / "source"
OUT = ROOT / "design" / "prototype" / "argus-prototype.html"

# Screen id -> (board file, label). Order = order in the screen picker.
SCREENS = [
    ("landing", "Landing", "Landing · public"),
    ("wallet", "Wallet", "Connect wallet"),
    ("overview", "Overview", "Overview"),
    ("positions", "Positions", "Positions + drawer"),
    ("terminal", "Terminal", "Terminal"),
    ("radar", "Radar", "Risk Radar"),
    ("alerts", "Alerts", "Alerts"),
    ("activity", "Activity", "Activity"),
    ("askbar", "Ask-bar", "Ask Argus · ⌘K bar"),
    ("askpanel", "Ask-panel", "Ask Argus · panel"),
]


def b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def board(name: str) -> tuple[str, str]:
    """Return (css, body) for one board: helmet <style> rules + the markup inside <x-dc>."""
    s = (SRC / f"{name}.dc.html").read_text()
    helmet = re.search(r"<helmet>(.*?)</helmet>", s, re.S)
    css = "\n".join(re.findall(r"<style>(.*?)</style>", helmet.group(1), re.S)) if helmet else ""
    body = re.search(r"<x-dc>(.*?)</x-dc>", s, re.S).group(1)
    body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S)
    return css, body


def main() -> None:
    fonts = ROOT / "node_modules" / "@fontsource"
    hero = "data:image/jpeg;base64," + b64(ROOT / "public" / "brand" / "hero.jpg")
    font_css = (
        f"@font-face{{font-family:Michroma;src:url(data:font/woff2;base64,{b64(fonts / 'michroma/files/michroma-latin-400-normal.woff2')}) format('woff2')}}"
        f"@font-face{{font-family:'IBM Plex Mono';font-weight:400;src:url(data:font/woff2;base64,{b64(fonts / 'ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2')}) format('woff2')}}"
        f"@font-face{{font-family:'IBM Plex Mono';font-weight:500;src:url(data:font/woff2;base64,{b64(fonts / 'ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2')}) format('woff2')}}"
    )
    styles, sections, options = [], [], []
    for sid, file, label in SCREENS:
        css, body = board(file)
        body = re.sub(r'src="/_blob/[0-9a-f]+"', f'src="{hero}"', body)
        styles.append(css)
        sections.append(f'<section class="pt-screen" data-s="{sid}" data-label="{html.escape(label)}" hidden>{body}</section>')
        options.append(f'<option value="{sid}">{html.escape(label)}</option>')

    page = TEMPLATE.replace("/*FONTS*/", font_css).replace("/*BOARDS*/", "\n".join(dict.fromkeys(styles)))
    page = page.replace("<!--SECTIONS-->", "\n".join(sections)).replace("<!--OPTIONS-->", "".join(options))
    page = page.replace("/*JS*/", (pathlib.Path(__file__).parent / "prototype.js").read_text())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Argus prototype</title>
<style>
/*FONTS*/
/*BOARDS*/
body{margin:0;background:#16110C}
.pt-screen[hidden]{display:none!important}
/* hotspots: everything that goes somewhere */
[data-hot]{cursor:pointer}
body.pt-show [data-hot]{outline:2px dashed #C0551E;outline-offset:2px}
[data-hot]:hover{outline:2px solid #C0551E;outline-offset:2px}
/* prototype bar (not part of the design) */
.pt-bar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:9999;display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:center;
  max-width:calc(100% - 24px);padding:8px 10px;background:#0E0B08;border:1px solid #482A16;box-shadow:0 12px 40px #000A;font:500 12px 'IBM Plex Mono',ui-monospace,monospace;color:#EFC796}
.pt-bar select,.pt-bar button{font:inherit;color:#EFC796;background:#1E1711;border:1px solid #482A16;min-height:32px;padding:0 10px;cursor:pointer}
.pt-bar button[aria-pressed=true]{background:#EFC796;color:#16110C}
.pt-bar span{color:#A8865F}
.pt-toast{position:fixed;left:50%;bottom:76px;z-index:9999;background:#EFC796;color:#16110C;font:500 13px 'IBM Plex Mono',monospace;padding:10px 14px;max-width:calc(100% - 24px);opacity:0;transition:opacity .25s,transform .3s cubic-bezier(.2,.8,.2,1)}
.pt-toast.on{opacity:1}
/* ---- motion (same language as the app: one easing, calm, meaningful) ---- */
.pt-screen a,.pt-screen button{transition:background-color .2s ease,color .2s ease,border-color .2s ease,transform .2s cubic-bezier(.2,.8,.2,1)}
@media (prefers-reduced-motion: no-preference){
  .pt-out{animation:pt-out .16s ease both}
  .pt-rise{animation:pt-rise .6s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,0ms)}
  .pt-reveal{opacity:0;transform:translateY(26px);transition:opacity .9s cubic-bezier(.2,.8,.2,1) var(--d,0ms),transform .9s cubic-bezier(.2,.8,.2,1) var(--d,0ms)}
  .pt-reveal.pt-seen{opacity:1;transform:none}
  .pt-settle{animation:pt-settle 2.4s cubic-bezier(.2,.8,.2,1) both}
  .pt-wake{transform-box:fill-box;transform-origin:center;animation:pt-wake 1s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,250ms)}
  .pt-glow{animation:pt-glow 1.6s ease-in-out infinite}
  .pt-crit{animation:pt-crit 2.4s ease-in-out infinite}
  .pt-slide{animation:pt-slide .5s cubic-bezier(.2,.8,.2,1) both;animation-delay:.12s}
  .pt-drop{animation:pt-drop .45s cubic-bezier(.2,.8,.2,1) both;animation-delay:.1s}
  .pt-grow{transform-box:fill-box;transform-origin:50% 100%;animation:pt-grow .5s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,0ms)}
  .pt-draw{stroke-dasharray:1;stroke-dashoffset:1;animation:pt-draw 1.2s cubic-bezier(.6,0,.2,1) forwards;animation-delay:var(--d,600ms)}
  .pt-ring{transform-box:view-box;transform-origin:center;animation:pt-ring 1.1s cubic-bezier(.2,.8,.2,1) both;animation-delay:var(--d,0ms)}
  .pt-pop{transform-box:fill-box;transform-origin:center;animation:pt-pop .55s cubic-bezier(.2,1.4,.4,1) both;animation-delay:var(--d,0ms)}
  .pt-twinkle{animation:pt-twinkle 3.2s ease-in-out infinite;animation-delay:var(--d,0ms)}
  .pt-seg{animation:pt-seg .3s cubic-bezier(.2,.8,.2,1)}
  .pt-screen [data-hot]:hover{transform:translateY(-1px)}
  .pt-screen button:active{transform:scale(.97)}
}
@keyframes pt-out{to{opacity:0}}
@keyframes pt-rise{from{opacity:0;transform:translateY(16px)}}
@keyframes pt-settle{from{transform:scale(1.06);opacity:.5}}
@keyframes pt-wake{from{transform:scaleY(.04)}}
@keyframes pt-glow{0%,100%{opacity:.35}50%{opacity:.95}}
@keyframes pt-crit{0%,100%{filter:none}50%{filter:brightness(1.12)}}
@keyframes pt-slide{from{transform:translateX(100%)}}
@keyframes pt-drop{from{opacity:0;transform:translateY(-14px) scale(.98)}}
@keyframes pt-grow{from{transform:scaleY(0);opacity:0}}
@keyframes pt-draw{to{stroke-dashoffset:0}}
@keyframes pt-ring{from{transform:scale(.3);opacity:0}}
@keyframes pt-pop{from{transform:scale(0);opacity:0}}
@keyframes pt-twinkle{0%,100%{opacity:.25}50%{opacity:.9}}
@keyframes pt-seg{from{transform:scale(.94)}}
.pt-toast{transform:translate(-50%,8px)}.pt-toast.on{transform:translate(-50%,0)}
@media (prefers-reduced-motion: reduce){.pt-toast{transition:none}}
</style>
</head>
<body>
<!--SECTIONS-->
<div class="pt-bar" role="toolbar" aria-label="Prototype controls">
  <strong style="font-family:Michroma,sans-serif;letter-spacing:.08em">ΛRGUS</strong><span>prototype</span>
  <select id="pt-jump" aria-label="Go to screen"><!--OPTIONS--></select>
  <button type="button" id="pt-back" aria-label="Back">←</button>
  <button type="button" id="pt-hot" aria-pressed="false">Show clickable</button>
  <span>⌘K ask · Esc back</span>
</div>
<div class="pt-toast" id="pt-toast" role="status" aria-live="polite"></div>
<script>
/*JS*/
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
