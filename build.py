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

vids = '<div class="vids"><div class="vids-head"><h3>Walk-throughs</h3><span class="mono" style="color:#A3A9AD">Tap to play · no sound</span></div>'
for f, title, dur in VIDEOS:
    vids += (f'<figure><video src="vid/{f}-720.mp4" poster="vid/{f}.jpg" controls muted playsinline preload="none" '
             f'aria-label="Video walk-through: {title}"></video><figcaption><b>{title}</b><span>{dur}</span></figcaption></figure>')
vids += "</div>"

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
<meta name="description" content="R Hall &amp; Son: family-run builders in Sheffield. New builds, extensions and full renovations, roof to cellar.">
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
