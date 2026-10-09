# Sanika Paranjpe — Design Portfolio

Static portfolio site for accessories, textile and apparel work, served by GitHub Pages at
**https://sanikaparanjpe97.github.io/**.

## Structure

```
index.html            home: intro, the three portfolios, PDF downloads
accessories.html      EEBAGAA (freelance), Pelicans London, Aranyani
textile.html          six textile projects
apparel.html          nine apparel projects
assets/css/site.css   all styles
assets/js/site.js     header + image lightbox (click to open, arrows/swipe, click or Z to zoom)
assets/img/           images rendered from the PDFs (+ manifest.json with sizes)
files/                the original PDF portfolios, linked as downloads
tools/                scripts that regenerate images and pages
```

No build step is needed to serve the site; the HTML is committed.

## Updating

Copy lives in `tools/build.py`. Edit it, then regenerate the pages:

```
py -3.12 -I tools/build.py .
```

If a PDF changes, replace it in `files/` and re-render the images first:

```
py -3.12 -m pip install pymupdf pillow
py -3.12 -I tools/extract.py files/sanika-paranjpe-accessories-portfolio.pdf files/sanika-paranjpe-textile-portfolio.pdf files/sanika-paranjpe-apparel-projects.pdf assets/img tools/faces.json
py -3.12 -I tools/build.py .
```

`tools/faces.json` lists face regions (PDF points) that are blurred on the livelihoods project pages,
so community members are not identifiable on the public site. The textile PDF in `files/` is a
redacted copy made with `tools/extract.py --redact <original.pdf> files/sanika-paranjpe-textile-portfolio.pdf tools/faces.json`.

Preview locally with `py -3.12 -m http.server` and open http://localhost:8000.
