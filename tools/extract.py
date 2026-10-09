"""Render portfolio PDFs into web images + a manifest.

Usage:  py -3.12 -I tools/extract.py <accessories.pdf> <textile.pdf> <apparel.pdf> <out_dir> [faces.json] [--footwear <kat-maconie.pdf>]

        py -3.12 -I tools/extract.py --redact <textile.pdf> <out.pdf> <faces.json>

faces.json maps textile page numbers to face boxes in PDF points; those are blurred
(the livelihoods project photographs community members who should not be identifiable).
--redact writes a copy of the textile PDF with the same blur, for the public download.

Plates (whole pages) get two sizes: a ~1100px "md" for the page and a full-size
version for the lightbox. Apparel photos are rendered from their placed rectangles
so the web gallery can be laid out in HTML instead of as flat page images.
"""
import io
import json
import os
import sys

import pymupdf
from PIL import Image, ImageFilter

MD_WIDTH = 1100
QUALITY = 82


def pix_to_image(pix):
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def save_webp(im, path):
    im.save(path, "WEBP", quality=QUALITY, method=6)


def trim(im, pad=12):
    """Crop away surrounding white space."""
    gray = im.convert("L").point(lambda v: 255 if v < 245 else 0)
    box = gray.getbbox()
    if not box:
        return im
    x0, y0, x1, y1 = box
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


class Extractor:
    def __init__(self, out_dir):
        self.out = out_dir
        self.manifest = {}

    def plate(self, doc, page_no, key, folder, scale, fix=None):
        page = doc[page_no - 1]
        im = pix_to_image(page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False))
        if fix:
            im = fix(im, scale)
        os.makedirs(os.path.join(self.out, folder), exist_ok=True)
        full = f"{folder}/{key}.webp"
        md = f"{folder}/{key}-md.webp"
        save_webp(im, os.path.join(self.out, full))
        small = im.resize((MD_WIDTH, round(im.height * MD_WIDTH / im.width)), Image.LANCZOS)
        save_webp(small, os.path.join(self.out, md))
        self.manifest[key] = {"src": full, "md": md, "w": im.width, "h": im.height, "mdw": small.width, "mdh": small.height}

    def clip(self, doc, page_no, rect, key, folder, scale, do_trim=False, png=False):
        page = doc[page_no - 1]
        im = pix_to_image(page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), clip=pymupdf.Rect(rect), alpha=False))
        if do_trim:
            im = trim(im)
        os.makedirs(os.path.join(self.out, folder), exist_ok=True)
        ext = "png" if png else "webp"
        rel = f"{folder}/{key}.{ext}"
        if png:
            im.save(os.path.join(self.out, rel), optimize=True)
        else:
            save_webp(im, os.path.join(self.out, rel))
        self.manifest[key] = {"src": rel, "w": im.width, "h": im.height}

    def photos(self, doc, page_no, keys, folder, scale=2.1):
        """Render each placed image on a page, left to right."""
        page = doc[page_no - 1]
        rects = []
        for img in page.get_images(full=True):
            for r in page.get_image_rects(img[0]):
                rects.append(r)
        rects.sort(key=lambda r: r.x0)
        assert len(rects) == len(keys), (page_no, len(rects), keys)
        for r, key in zip(rects, keys):
            self.clip(doc, page_no, r, key, folder, scale)


def blur_regions(regions):
    """Return a plate fix that blurs faces. Regions are in PDF points (x0, y0, x1, y1)."""
    def fix(im, scale):
        for x0, y0, x1, y1 in regions:
            box = tuple(round(v * scale) for v in (x0, y0, x1, y1))
            im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(radius=10 * scale)), box)
        return im
    return fix


def paint_white(regions):
    def fix(im, scale):
        for x0, y0, x1, y1 in regions:
            im.paste((255, 255, 255), tuple(round(v * scale) for v in (x0, y0, x1, y1)))
        return im
    return fix


def chain(*fixes):
    def fix(im, scale):
        for f in fixes:
            im = f(im, scale)
        return im
    return fix


def extend_backdrop(photo, ratio=3 / 2, feather=56):
    """Place a portrait studio photo on a wider canvas, continuing its seamless backdrop to the sides."""
    import numpy as np
    im = np.asarray(photo.convert("RGB")).astype(np.float32)
    h, w, _ = im.shape
    width = round(h * ratio)
    # Backdrop colour per row from the outer strips, ignoring pixels far from the overall tone (shoes, legs).
    strip = np.concatenate([im[:, :24], im[:, -24:]], axis=1)
    ref = np.median(strip.reshape(-1, 3), axis=0)
    rows = np.full((h, 3), np.nan, dtype=np.float32)
    for y in range(h):
        keep = strip[y][np.linalg.norm(strip[y] - ref, axis=1) < 28]
        if len(keep) > 6:
            rows[y] = np.median(keep, axis=0)
    idx = np.arange(h)
    k = 151
    for c in range(3):
        ok = ~np.isnan(rows[:, c])
        col = np.interp(idx, idx[ok], rows[ok, c])
        rows[:, c] = np.convolve(np.pad(col, k // 2, mode="edge"), np.ones(k) / k, mode="valid")
    canvas = np.repeat(rows[:, None, :], width, axis=1)
    x0 = (width - w) // 2
    alpha = np.ones(w, dtype=np.float32)
    ramp = np.linspace(0, 1, feather) ** 1.5
    alpha[:feather], alpha[-feather:] = ramp, ramp[::-1]
    a = alpha[None, :, None]
    canvas[:, x0:x0 + w] = im * a + canvas[:, x0:x0 + w] * (1 - a)
    grain = np.random.default_rng(7).normal(0, 2.4, canvas.shape).astype(np.float32)
    outside = np.ones(width, dtype=np.float32)
    outside[x0 + feather:x0 + w - feather] = 0
    canvas += grain * outside[None, :, None]
    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))


def embedded_image(doc, page_no, size):
    """The raw embedded image of a given pixel size on a page (avoids the page's display distortion)."""
    page = doc[page_no - 1]
    for img in page.get_images(full=True):
        if (img[2], img[3]) == size:
            return Image.open(io.BytesIO(doc.extract_image(img[0])["image"])).convert("RGB")
    raise ValueError(f"no {size} image on page {page_no}")


def redact_pdf(src, dst, faces):
    """Copy a PDF, rebuilding the pages listed in faces as images with those regions blurred."""
    doc = pymupdf.open(src)
    out = pymupdf.open()
    for i, page in enumerate(doc):
        regions = faces.get(str(i + 1))
        if not regions:
            out.insert_pdf(doc, from_page=i, to_page=i)
            continue
        scale = 1801 / page.rect.width  # native resolution of the page rasters
        fixes = [blur_regions(regions)]
        if i + 1 == 22:
            fixes.append(paint_white([(517, 535, 549, 572)]))
        im = chain(*fixes)(pix_to_image(page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)), scale)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=90)
        new = out.new_page(width=page.rect.width, height=page.rect.height)
        new.insert_image(new.rect, stream=buf.getvalue())
    out.set_metadata(doc.metadata)
    out.save(dst, garbage=3, deflate=True)


def main():
    if sys.argv[1] == "--redact":
        with open(sys.argv[4], encoding="utf-8") as f:
            redact_pdf(sys.argv[2], sys.argv[3], json.load(f))
        print("wrote", sys.argv[3])
        return
    args = sys.argv[1:]
    footwear_pdf = None
    if "--footwear" in args:
        i = args.index("--footwear")
        footwear_pdf = args[i + 1]
        del args[i:i + 2]
    acc_pdf, tex_pdf, app_pdf, out_dir = args[:4]
    faces = {}
    if len(args) > 4:
        with open(args[4], encoding="utf-8") as f:
            faces = json.load(f)
    ex = Extractor(out_dir)

    # Accessories: vector pages render sharper; pages built from rasters stay at 2x.
    acc = pymupdf.open(acc_pdf)
    raster_pages = {3, 4, 5, 17, 18, 19}
    for p in [3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19]:
        ex.plate(acc, p, f"acc-{p:02d}", "accessories", 2.0 if p in raster_pages else 2.5)
    ex.clip(acc, 2, (200, 440, 642, 590), "logo-eebagaa", "brand", 3, do_trim=True, png=True)
    ex.clip(acc, 6, (200, 440, 642, 590), "logo-pelicans", "brand", 3, do_trim=True, png=True)
    ex.clip(acc, 16, (370, 415, 472, 515), "logo-aranyani", "brand", 3, do_trim=True, png=True)

    # Textile: every page is already a single 2x raster.
    tex = pymupdf.open(tex_pdf)
    for p in range(2, 25):
        fixes = []
        if str(p) in faces:
            fixes.append(blur_regions(faces[str(p)]))
        if p == 22:
            fixes.append(paint_white([(517, 535, 549, 572)]))  # stray black box beside the logos
        ex.plate(tex, p, f"tex-{p:02d}", "textile", 2.0, fix=chain(*fixes) if fixes else None)

    # Apparel: lift the photographs out of each page.
    app = pymupdf.open(app_pdf)
    layout = {
        1: ["app-saadgi-front", "app-saadgi-back"],
        2: ["app-export-1", "app-export-2"],
        3: ["app-export-3", "app-export-4"],
        4: ["app-indian-1", "app-indian-2"],
        5: ["app-surface-1", "app-surface-2"],
        6: ["app-personal-1", "app-personal-2"],
        7: ["app-surface-3", "app-surface-4"],
        8: ["app-crochet-1", "app-crochet-2"],
        9: ["app-orient-1", "app-orient-2"],
        10: ["app-kaftaan-1", "app-kaftaan-2"],
        11: ["app-other-tote", "app-other-pattern"],
    }
    for p, keys in layout.items():
        ex.photos(app, p, keys, "apparel")

    # Footwear presentation for Kat Maconie (kept outside the repo: the source PDF is ~140 MB).
    # Its sandals photo (page 5) becomes the accessories cover; without it, the saddle-bag colourways are used.
    if footwear_pdf:
        fw = pymupdf.open(footwear_pdf)
        for p in range(1, fw.page_count + 1):
            ex.plate(fw, p, f"fw-{p:02d}", "accessories", 2.5)
        # The PDF shows this 416×624 photo stretched ~20% wide; use the raw image, backdrop extended to 3:2.
        cover = extend_backdrop(embedded_image(fw, 5, (416, 624)))
        os.makedirs(os.path.join(out_dir, "covers"), exist_ok=True)
        cover.save(os.path.join(out_dir, "covers", "cover-accessories.webp"), "WEBP", quality=92, method=6)
        ex.manifest["cover-accessories"] = {"src": "covers/cover-accessories.webp", "w": cover.width, "h": cover.height}
    else:
        ex.clip(acc, 3, (440, 50, 842, 298), "cover-accessories", "covers", 4)

    # Covers for the home page and the link-preview image.
    ex.clip(tex, 14, (186, 174, 818, 601), "cover-textile", "covers", 2)
    og = Image.new("RGB", (1200, 630), (246, 244, 239))
    panels = [os.path.join(out_dir, ex.manifest[k]["src"]) for k in ("cover-accessories", "cover-textile", "app-orient-1")]
    for i, path in enumerate(panels):
        im = Image.open(path).convert("RGB")
        w, h = 400, 630
        s = max(w / im.width, h / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        x, y = (im.width - w) // 2, (im.height - h) // 2
        og.paste(im.crop((x, y, x + w, y + h)), (i * 400, 0))
    og.save(os.path.join(out_dir, "og.jpg"), quality=85)

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(ex.manifest, f, indent=1)
    print(len(ex.manifest), "images")


if __name__ == "__main__":
    main()
