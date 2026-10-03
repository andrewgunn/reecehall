"""Build the site from site/index.src.html.

Writes:
  site/index.html      standalone page for GitHub Pages / any static host
  build/artifact.html  body-only version for publishing as a Claude artifact
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")

VIDEOS = [
    ("Horsley-Gate", "Horsleygate Lane", "0:48"),
    ("Ecclesall-Road-South-horizontal1", "Ecclesall Road South", "1:30"),
    ("New-Build", "New build", "0:42"),
]

src = open(os.path.join(SITE, "index.src.html"), encoding="utf-8").read()
photos = json.load(open(os.path.join(SITE, "photos.json"), encoding="utf-8"))

src = src.replace(
    "They don't believe in the word “can't”, and the work they do is of exceptional quality and without compromise.”",
    "They don’t believe in the word ‘can’t’ and go about everything with enormous professionalism and efficiency.”",
)

f0, t0, d0 = VIDEOS[0]
vids = (f'<div class="film"><div class="stage" id="stage"><video src="vid/{f0}-720.mp4" poster="vid/{f0}.jpg" muted playsinline preload="none" '
        f'aria-label="Video walk-through: {t0}"></video><button type="button" class="stage-play" aria-label="Play walk-through">'
        f'<span class="ring"><svg><use href="#i-play"/></svg></span><span class="mono">Now showing · <span class="dur">{d0}</span></span><h3>{t0}</h3></button></div>'
        '<ol class="reel" id="reel">')
for i, (f, title, dur) in enumerate(VIDEOS):
    vids += (f'<li><button type="button" data-f="{f}" data-t="{title}" data-d="{dur}" aria-current="{str(i == 0).lower()}">'
             f'<span class="th"><img src="vid/{f}.jpg" alt="" loading="lazy"></span>'
             f'<span class="tx"><b>{title}</b><span>{i + 1:02d} · {dur}</span></span></button></li>')
vids += '</ol></div><p class="film-note mono">No sound · tap any film to play</p>'

body = src.replace("__PHOTOS__", json.dumps(photos, separators=(",", ":"))).replace("__VIDEOS__", vids)
assert "__PHOTOS__" not in body and "__VIDEOS__" not in body

os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
open(os.path.join(ROOT, "build", "artifact.html"), "w", encoding="utf-8").write(body)

head_end = body.index("</style>") + len("</style>")
head, rest = body[:head_end], body[head_end:]
standalone = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="R Hall &amp; Son: family-run builders in Sheffield. Award-winning: Building Renovations Service of the Year, Yorkshire Prestige Awards 2026/27. New builds, extensions and full renovations, roof to cellar.">
<meta property="og:title" content="R Hall &amp; Son · Sheffield builders">
<meta property="og:description" content="New builds, extensions and full renovations across Sheffield.">
<meta property="og:image" content="img/hero.jpg">
<style>:root{{color-scheme:light}}body{{margin:0}}[hidden]{{display:none!important}}</style>
{head}
</head>
<body>
{rest}
</body>
</html>
"""
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(standalone)
print("built site/index.html and build/artifact.html")
