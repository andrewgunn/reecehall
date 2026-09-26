# R Hall & Son website

Website and brand refresh concept for R Hall & Son Developments Ltd, Sheffield.

- `site/index.src.html`: the page source (edit this)
- `site/photos.json`: photo captions, alt text and gallery tags
- `site/img/`, `site/vid/`: optimised photos and 720p videos
- `build.py`: builds `site/index.html` (standalone) and `build/artifact.html` (Claude artifact)

```sh
python3 build.py
```

Pushing to `main` deploys `site/` to GitHub Pages.
