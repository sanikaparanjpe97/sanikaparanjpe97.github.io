"""Generate the static site pages from the content below + assets/img/manifest.json.

Usage:  py -3.12 -I tools/build.py <repo_root>

Edit copy here, re-run, commit the regenerated *.html files.
"""
import json
import os
import sys
from html import escape

SITE_URL = "https://sanikaparanjpe97.github.io/"
NAME = "Sanika Paranjpe"

PAGES = [
    ("accessories", "Accessories"),
    ("textile", "Textile"),
    ("apparel", "Apparel"),
]

DOWNLOADS = [
    ("sanika-paranjpe-accessories-portfolio.pdf", "Accessories Design Portfolio", "19 pages"),
    ("sanika-paranjpe-textile-portfolio.pdf", "Textile Design Portfolio", "25 pages"),
    ("sanika-paranjpe-apparel-projects.pdf", "Apparel Projects", "11 pages"),
]

# ---------------------------------------------------------------- content

ACCESSORIES = {
    "slug": "accessories",
    "num": "01",
    "title": "Accessories",
    "eyebrow": "Portfolio 01 · Bags & footwear",
    "lede": "Handbags, footwear and small leather goods, from first proposal to production tech pack: "
            "colourways, materials and construction details for Kat Maconie, Pelicans London, Aranyani "
            "and freelance client EEBAGAA.",
    "groups": [
        {
            "label": "Footwear for Kat Maconie",
            "projects": [
                {
                    "id": "kat-maconie",
                    "title": "Strappy Flats & KAY Sandals",
                    "meta": "Kat Maconie · Colour vibe proposals",
                    "paras": [
                        "Colourway proposals for two Kat Maconie styles. Each takes the colour vibe of an existing "
                        "Kat Maconie shoe, the Strappy Pumps or the Aya sandals, and carries it onto another style, "
                        "with Pantone references and a full specification of materials and construction.",
                        "The strappy flats are slip-on satin flats with gradient stones, mesh detail and a jewelled "
                        "bow on a 10mm covered block heel, in Teal (Rain Forest to Little Boy Blue to Intimate Pink) "
                        "and Coconut Cream (to Intimate Pink to Lichen). The KAY sandal is the bird-motif sandal with "
                        "a tassel and back zip, in gradient glitter from Electric Blue to White and from Molten Lava "
                        "to Light Peach, on a 100mm heel with a silver or golden frame.",
                    ],
                    "keywords": ["Footwear", "Colourways", "Pantone", "Embellishment", "Specifications"],
                    "plates": [
                        ("fw-01", "Strappy flats, Teal colour vibe: render, flat sketch, Pantone colourway and specification"),
                        ("fw-02", "Strappy flats, Coconut Cream colour vibe"),
                        ("fw-03", "KAY sandal, Electric Blue to White colour vibe"),
                        ("fw-04", "KAY sandal, Lava Red to Light Peach colour vibe"),
                        ("fw-05", "Kat Maconie brand imagery"),
                    ],
                },
            ],
        },
        {
            "label": "Freelance work",
            "logo": ("brand/logo-eebagaa.png", "EEBAGAA", ""),
            "projects": [
                {
                    "id": "eebagaa",
                    "title": "Tech Packs for EEBAGAA",
                    "meta": "Freelance · 2024",
                    "paras": [
                        "Technical specifications for four styles: a saddle bag, two totes and a women’s "
                        "backpack. Each pack runs from 3D views through external and internal details, "
                        "materials and trims to the final colourways.",
                    ],
                    "keywords": ["Tech packs", "Colourways", "Construction details"],
                    "plates": [
                        ("acc-03", "Saddle bag and totes: 3D views and colourways"),
                        ("acc-04", "Women’s backpack and Tote Style 2: 3D views and colourways"),
                        ("acc-05", "Women’s backpack: external and internal details, materials, colourways"),
                    ],
                },
            ],
        },
        {
            "label": "Work at Pelicans London",
            "logo": ("brand/logo-pelicans.png", "Pelicans London", ""),
            "projects": [
                {
                    "id": "bmw-alpina",
                    "title": "BMW Alpina CCB",
                    "meta": "Pelicans London",
                    "paras": [
                        "Two families of bags, a top-handle over-the-shoulder bag and a backpack, each in two "
                        "versions. Version A pairs a screen print with quilting inspired by the signature BMW "
                        "M-type grille; Version B uses linear quilting with the classic M-type stripes.",
                        "Details include a detachable dog hook shaped after the BMW kidney grille and a hidden "
                        "phone pocket with RFID card slots.",
                    ],
                    "keywords": ["Co-branding", "Quilting", "Screen print"],
                    "plates": [
                        ("acc-07", "Versions 1A, 1B, 2A and 2B with construction call-outs"),
                        ("acc-08", "Front panels and 3D views"),
                    ],
                },
                {
                    "id": "canvas-bags",
                    "title": "Canvas Bags Collection",
                    "meta": "Pelicans London",
                    "paras": [
                        "A full canvas range: zipped rucksack, satchel, north–south cross-body, messenger, work "
                        "bag, rolled-top rucksack, 24-hour weekender, totes and duffles, on a palette of navy, "
                        "khaki, beige and black with tan or dark-brown trims.",
                        "Print stories for the totes and duffles include block stripes, Kantha-inspired prints, "
                        "botanical and floral prints, and camouflage.",
                    ],
                    "keywords": ["Range building", "Colourways", "Prints"],
                    "plates": [
                        ("acc-09", "Zipped rucksack, satchel, north–south cross-body bag and canvas messenger"),
                        ("acc-10", "Canvas work bag, rolled-top rucksack, 24H weekender and tote bag"),
                        ("acc-11", "Canvas totes: block stripes, Kantha-inspired prints, botanical pattern"),
                        ("acc-12", "Canvas totes in solids and florals; duffles in autumn colours and camouflage"),
                    ],
                },
                {
                    "id": "back-to-school",
                    "title": "Back to School Collection",
                    "meta": "Pelicans London · Kidswear",
                    "paras": [
                        "Printed backpacks in three age bands: pre-schoolers aged 3–5 (transport and rainbows), "
                        "5–7 years (space and butterflies) and 8–12 years (camouflage and flowers), each with a "
                        "coordinated plain back and contrast straps.",
                    ],
                    "keywords": ["Print design", "Kids", "Backpacks"],
                    "plates": [
                        ("acc-13", "Six prints across three age groups, front and back"),
                    ],
                },
                {
                    "id": "leather-tech-pack",
                    "title": "Leather Handbag Tech Pack",
                    "meta": "Pelicans London · Leather Bags Collection 1 · 2024",
                    "paras": [
                        "A small women’s work tote in leather, sized to carry an iPad Pro: leather outer, "
                        "black cotton-drill lining, silver fittings. The six-page pack covers the overview, "
                        "exterior and interior specs, a zipped pouch, an AirPod holder, and how the bag "
                        "converts to a shoulder style.",
                    ],
                    "keywords": ["Leather", "Tech pack", "Specs"],
                    "plates": [
                        ("acc-14", "Overview, exterior, interior, zipped pouch, AirPod holder and shoulder-style specs"),
                    ],
                },
                {
                    "id": "final-products",
                    "title": "Final Products",
                    "meta": "Pelicans London · Samples",
                    "paras": [
                        "A few of the finished, sampled products: canvas tote bags, a men’s chest bag, a barrel "
                        "duffle, a zipped-top backpack, a rolled-top rucksack and a messenger bag.",
                    ],
                    "keywords": ["Sampling", "Production"],
                    "plates": [
                        ("acc-15", "Canvas totes, chest bag, barrel duffle, backpack, rucksack and messenger bag"),
                    ],
                },
            ],
        },
        {
            "label": "Work at Aranyani",
            "logo": ("brand/logo-aranyani.png", "Aranyani", "logo-round"),
            "projects": [
                {
                    "id": "aranyani-slg",
                    "title": "Small Leather Goods, Trims & Surface Development",
                    "meta": "Aranyani · S/S 21",
                    "paras": [
                        "I was responsible for proposals for SLGs, new trims and surface developments for "
                        "capsule collections; a few of those samples are compiled here. I also made design tech "
                        "packs for all of the brand’s SKUs for the production team. That meant studying the "
                        "artisans’ specification requirements and their workflow during production, so the tech "
                        "packs and specs would make the work easier for the craftsmen.",
                        "I assisted stylist Steven Lasalle on the brand’s lifestyle shoot for the S/S 21 season "
                        "at Nahargarh Hotel, Rajasthan. The photographs are outtakes from that shoot. "
                        "Photography: Udo Spreitzenbarth.",
                    ],
                    "keywords": ["SLGs", "Trims", "Surface development", "Styling"],
                    "plates": [
                        ("acc-17", "S/S 21 lifestyle shoot outtakes. Photography: Udo Spreitzenbarth"),
                        ("acc-18", "Small leather goods proposals and surface development"),
                    ],
                },
                {
                    "id": "aranyani-crossbody",
                    "title": "Mini Crossbody Bag Tech Pack",
                    "meta": "Aranyani · AW 20–21",
                    "paras": [
                        "Production-sample tech pack for the Stone Drop mini crossbody bag with a single stone "
                        "ring: colourways, front, side and back measurements, internal pocket details, and "
                        "per-colour material and thread specifications.",
                    ],
                    "keywords": ["Tech pack", "Production sample"],
                    "plates": [
                        ("acc-19", "Colourways, measured drawings and colour specifications"),
                    ],
                },
            ],
        },
    ],
}

TEXTILE = {
    "slug": "textile",
    "num": "02",
    "title": "Textile",
    "eyebrow": "Portfolio 02 · Textile design",
    "lede": "Six projects across handwoven, naturally dyed, printed and embroidered textiles, rooted in "
            "research trips and in work with craft communities in Northeast India.",
    "groups": [
        {
            "projects": [
                {
                    "id": "vasudhaiva-kutumbakam",
                    "tag": "#bccc3c",
                    "title": "Vasudhaiva Kutumbakam",
                    "deva": "वसुधैव कुटुम्बकम",
                    "meta": "Collection · Eri silk · Rabha weavers, Loharghat, Assam",
                    "paras": [
                        "Taking Freddy Mamani’s Neo-Andean architecture from Bolivia as its starting point, this "
                        "collection is an intersection of craft, research, cultures and design. It is an attempt "
                        "at mobilising high levels of local skill and tradition to sustain local communities, "
                        "using traditional techniques with a contemporary design approach and making optimal use "
                        "of the fabric crafted by the community.",
                        "The collection is made with handspun, handwoven Eri silk and organic dyes from locally "
                        "available dyestuffs. The women of the Rabha tribe from Loharghat, Assam spun, dyed and "
                        "wove the fabrics. Eri is considered the most sustainable silk, as the moth is not killed "
                        "to extract the fibre, and its cooling property in summer and warmth in winter make the "
                        "garments seasonless.",
                    ],
                    "keywords": ["Eri silk", "Organic dyeing", "Responsible fashion", "Contemporary weaves",
                                 "Zero waste", "Geometric", "Easy silhouettes"],
                    "plates": [
                        ("tex-02", "Concept: Freddy Mamani’s Neo-Andean architecture, and the palette"),
                        ("tex-03", "Organic-dyed swatches, stripe explorations and final stripes"),
                        ("tex-04", "Textile development: handspinning, mordanting, dyeing and warping"),
                        ("tex-05", "Working sketches, fabric on the loom, and the zero-waste flat lay"),
                        ("tex-06", "Range plan"),
                    ],
                },
                {
                    "id": "the-orient",
                    "tag": "#ec4c30",
                    "title": "The Orient",
                    "meta": "Collection · Rabha and Hajong handwoven textiles",
                    "paras": [
                        "A visit to the Rumtek Monastery near Gangtok, Sikkim inspired this collection. The "
                        "neo-traditional theme combines handwoven Indian oriental fabrics with western and "
                        "Japanese silhouettes. The striped patterns formed by the monastery’s columns and "
                        "windows are drawn with the vibrant fabrics of the Hajong tribe, while the traditional "
                        "Rabha fabrics bring intricate borders and overall diamond motifs.",
                        "The ensembles use the Rabha women’s kambung and riphan and the men’s pasra, alongside "
                        "the pathin, the Hajong wrap skirt of symmetric stripes between red bands and thick "
                        "‘chapa’ borders. Plunging western dresses look bolder in the bright patterns; easy "
                        "wide-legged pants are a highlight.",
                    ],
                    "keywords": ["East–West fusion", "Handwoven", "Bold stripes", "Ornamental", "Festive"],
                    "crosslink": ("apparel.html#the-orient", "See the finished ensemble in Apparel →"),
                    "plates": [
                        ("tex-07", "Concept: Rumtek Monastery, Sikkim, and the palette"),
                        ("tex-08", "Rabha and Hajong traditional attire; rendered explorations and flats"),
                        ("tex-09", "Range plan"),
                    ],
                },
                {
                    "id": "sawai",
                    "tag": "#d4a444",
                    "title": "Sawai",
                    "meta": "Print design · Surface pattern",
                    "paras": [
                        "Nahargarh Palace in Sawai Madhopur has some of the most striking mosaic tiles, and "
                        "they inspired this print collection. The muted palette recalls the earthy feeling of "
                        "the misty weather I experienced during my time there.",
                    ],
                    "keywords": ["Mosaic", "Geometric", "Tessellated", "Muted", "Repeat"],
                    "plates": [
                        ("tex-10", "Concept: the mosaic floors and arches of Nahargarh Palace"),
                        ("tex-11", "Print 1 with colourways and an interior mockup"),
                        ("tex-12", "Print 2 with colourways and an interior mockup"),
                        ("tex-13", "Coordinates with colourways and mockups"),
                    ],
                },
                {
                    "id": "blooming-abode",
                    "tag": "#bc3854",
                    "title": "Blooming Abode",
                    "meta": "Print design · Sleepwear",
                    "paras": [
                        "Four flowers were picked for a sleepwear print range: poppy, ruby cinquefoil, bergenia "
                        "and rhododendron. Their shapes are simplified into ditsy, monochromatic prints.",
                    ],
                    "keywords": ["Ditsy prints", "Florals", "Sleepwear"],
                    "plates": [
                        ("tex-14", "The four flowers and the landscape collage"),
                        ("tex-15", "Mood board and palette"),
                        ("tex-16", "Ditsy monochromatic prints"),
                        ("tex-17", "Mockups"),
                    ],
                },
                {
                    "id": "textile-samples",
                    "tag": "#80d0f0",
                    "title": "Textile Samples",
                    "meta": "Weaving · Embroidery · Embellishment",
                    "paras": [
                        "A selection of the embroidery swatches I developed during college, and samples "
                        "prototyped during my internship.",
                    ],
                    "keywords": ["Hand embroidery", "Beadwork", "Weaving"],
                    "plates": [
                        ("tex-18", "Woven and embellished samples"),
                        ("tex-19", "Embroidery swatches"),
                    ],
                },
                {
                    "id": "towards-better-livelihoods",
                    "tag": "#dcb8a8",
                    "title": "Towards Better Livelihoods",
                    "meta": "SBI Youth for India Fellowship · the ant · Chirang, Assam",
                    "paras": [
                        "Documentation of my project under the SBI Youth for India fellowship, in partnership "
                        "with the SBI Foundation and the ant (The Action Northeast Trust): my journey into the "
                        "development sector, working in the thematic areas of traditional crafts and social "
                        "entrepreneurship.",
                        "After a rural-development orientation at Seva Mandir in Udaipur, field visits across "
                        "NGO clusters in Chirang, Assam led to a community of women looking for an alternative "
                        "livelihood. The project set up a safe workspace, regular sewing-training workshops and "
                        "an entrepreneurship awareness workshop with SBI RSETI, and mapped a path from training "
                        "and sampling to market linkages, a joint-liability-group loan and first production.",
                    ],
                    "note": "Faces of community members are blurred to protect their privacy.",
                    "keywords": ["Traditional crafts", "Social entrepreneurship", "Skill development"],
                    "plates": [
                        ("tex-20", "Fellowship context and problem identification"),
                        ("tex-21", "Problem statement synopsis"),
                        ("tex-22", "A safe workspace, training workshops and the SBI RSETI entrepreneurship workshop"),
                        ("tex-23", "Garments made during the training workshops"),
                        ("tex-24", "Project timeline, challenges and sustainability"),
                    ],
                },
            ],
        },
    ],
}

APPAREL = {
    "slug": "apparel",
    "num": "03",
    "title": "Apparel",
    "eyebrow": "Portfolio 03 · Apparel projects",
    "lede": "Ensembles built from the handwoven textiles of Northeast India (Khasi, Jaintia, Rabha, Hajong "
            "and Assamese taant), alongside surface development and export-house sampling.",
    "groups": [
        {
            "projects": [
                {
                    "id": "saadgi",
                    "title": "Saadgi",
                    "meta": "Ensemble",
                    "paras": ["An ensemble combining traditional Khasi and Jaintia tribal fabrics."],
                    "photos": [("app-saadgi-front", "Front"), ("app-saadgi-back", "Back")],
                },
                {
                    "id": "export-house",
                    "title": "Export House Internship",
                    "meta": "Internship samples",
                    "paras": ["Samples developed during an export-house internship: work on knits, floral machine "
                              "embroidery and lace fabrics."],
                    "photos": [("app-export-1", "Style 1"), ("app-export-2", "Style 2"),
                               ("app-export-3", "Style 3"), ("app-export-4", "Style 4")],
                },
                {
                    "id": "indian-wear",
                    "title": "Indian Wear Project",
                    "meta": "Occasion wear",
                    "paras": ["Inspired by the Taj Mahal’s reflection in the Yamuna: the whites sit beneath a "
                              "blue sheer lace."],
                    "photos": [("app-indian-1", ""), ("app-indian-2", "")],
                },
                {
                    "id": "surface-development",
                    "title": "Surface Development",
                    "meta": "Tie-dye · Hand embroidery · Embellishment",
                    "paras": ["Tie-dye, hand embroidery and embellishments: a deconstructed-denim bralette with "
                              "denim capris, and a jacket worked with surface design details."],
                    "photos": [("app-surface-1", "Denim deconstruction bralette with denim capris"),
                               ("app-surface-2", "Surface design details on the jacket"),
                               ("app-surface-3", "Surface design details on the jacket"),
                               ("app-surface-4", "Surface design details on the jacket")],
                },
                {
                    "id": "personal-project",
                    "title": "Personal Project",
                    "meta": "Ensemble",
                    "paras": ["An ensemble combining taant and tribal Assamese fabrics."],
                    "photos": [("app-personal-1", ""), ("app-personal-2", "")],
                },
                {
                    "id": "surface-design",
                    "title": "Surface Design Project",
                    "meta": "Crochet · Mirrorwork · Stitchwork",
                    "paras": ["Crochet, mirrorwork, cross stitches and double running stitches."],
                    "photos": [("app-crochet-1", "Style 1"), ("app-crochet-2", "Style 2")],
                },
                {
                    "id": "the-orient",
                    "title": "The Orient",
                    "meta": "Ensemble · Rabha and Hajong textiles",
                    "paras": ["An ensemble combining Rabha and Hajong tribal textiles: the finished piece from the "
                              "textile collection of the same name."],
                    "crosslink": ("textile.html#the-orient", "See the textile development →"),
                    "photos": [("app-orient-1", ""), ("app-orient-2", "")],
                },
                {
                    "id": "kaftaan",
                    "title": "Kaftaan Project",
                    "meta": "Surface exploration",
                    "paras": ["Surface explorations with the human brain as a theme."],
                    "photos": [("app-kaftaan-1", "Style 1"), ("app-kaftaan-2", "Style 2")],
                },
                {
                    "id": "other-projects",
                    "title": "Other Projects",
                    "meta": "Craft · Pattern making",
                    "paras": ["A small tote built from two traditional bamboo kulas, and an exercise in creative "
                              "pattern making."],
                    "photos": [("app-other-tote", "Small tote constructed from two traditional bamboo ‘kulas’"),
                               ("app-other-pattern", "Creative pattern making: trapezium tessellation")],
                },
            ],
        },
    ],
}

PORTFOLIOS = [ACCESSORIES, TEXTILE, APPAREL]

# ---------------------------------------------------------------- rendering

# Fonts are self-hosted (tools/fonts.py); preload the two faces every page renders first.
PRELOAD_FONTS = ["bodoni-moda-normal-latin.woff2", "inter-normal-latin.woff2"]

PLATE_SIZES = "(min-width: 1240px) 760px, (min-width: 900px) 62vw, calc(100vw - 32px)"


def e(s):
    return escape(s, quote=True)


class Builder:
    def __init__(self, root):
        self.root = root
        with open(os.path.join(root, "assets/img/manifest.json"), encoding="utf-8") as f:
            self.m = json.load(f)

    def img_attrs(self, key, md=False):
        v = self.m[key]
        if md:
            return (f'src="assets/img/{v["md"]}" srcset="assets/img/{v["md"]} {v["mdw"]}w, '
                    f'assets/img/{v["src"]} {v["w"]}w" width="{v["mdw"]}" height="{v["mdh"]}"')
        return f'src="assets/img/{v["src"]}" width="{v["w"]}" height="{v["h"]}"'

    # -- frame

    def head(self, title, desc, path, body_class, extra=""):
        url = SITE_URL + path
        preloads = "\n".join(f'<link rel="preload" href="assets/fonts/{f}" as="font" type="font/woff2" crossorigin>'
                             for f in PRELOAD_FONTS)
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f7f5f0">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
{preloads}
<link rel="stylesheet" href="assets/css/fonts.css">{extra}
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./">{NAME}</a>
    <nav class="nav" aria-label="Portfolios">
{self.nav(path)}
    </nav>
  </div>
</header>
<main id="main">
"""

    def nav(self, path):
        out = []
        for slug, label in PAGES:
            cur = ' aria-current="page"' if path == f"{slug}.html" else ""
            out.append(f'      <a href="{slug}.html"{cur}>{label}</a>')
        return "\n".join(out)

    def foot(self):
        return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 {NAME}. All work shown is by {NAME} unless credited.</span>
    <a href="#main">Back to top ↑</a>
  </div>
</footer>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""

    # -- pieces

    def plate(self, key, caption, title):
        v = self.m[key]
        return (f'<figure class="plate"><a href="assets/img/{v["src"]}" data-lightbox data-caption="{e(caption)}">'
                f'<img {self.img_attrs(key, md=True)} sizes="{PLATE_SIZES}" alt="{e(title)}: {e(caption)}" '
                f'loading="lazy" decoding="async"></a><figcaption>{e(caption)}</figcaption></figure>')

    def photo(self, key, caption, title):
        v = self.m[key]
        alt = f"{title}: {caption}" if caption else f"{title}, photographed look"
        cap = f"<figcaption>{e(caption)}</figcaption>" if caption else ""
        return (f'<figure class="photo"><a href="assets/img/{v["src"]}" data-lightbox data-caption="{e(caption or title)}">'
                f'<img {self.img_attrs(key)} alt="{e(alt)}" loading="lazy" decoding="async"></a>{cap}</figure>')

    def project(self, p, num, level):
        tag_style = f' style="--tag:{p["tag"]}"' if p.get("tag") else ""
        deva = f'<span class="deva" lang="hi">{e(p["deva"])}</span>' if p.get("deva") else ""
        paras = "\n".join(f"      <p>{e(t)}</p>" for t in p.get("paras", []))
        note = f'\n      <p class="meta">{e(p["note"])}</p>' if p.get("note") else ""
        kws = ""
        if p.get("keywords"):
            kws = '\n      <ul class="keywords">' + "".join(f"<li>{e(k)}</li>" for k in p["keywords"]) + "</ul>"
        cross = ""
        if p.get("crosslink"):
            href, text = p["crosslink"]
            cross = f'\n      <a class="crosslink" href="{href}">{e(text)}</a>'
        if p.get("plates"):
            media = '<div class="plates">\n      ' + "\n      ".join(
                self.plate(k, c, p["title"]) for k, c in p["plates"]) + "\n    </div>"
        else:
            media = '<div class="photos">\n      ' + "\n      ".join(
                self.photo(k, c, p["title"]) for k, c in p["photos"]) + "\n    </div>"
        return f"""  <section class="project" id="{p["id"]}"{tag_style}>
    <div class="project-text">
      <span class="tag">{num}</span>
      <h{level} class="project-title">{e(p["title"])}{deva}</h{level}>
      <p class="meta">{e(p["meta"])}</p>
{paras}{note}{kws}{cross}
    </div>
    {media}
  </section>
"""

    def portfolio_page(self, pf, nxt):
        path = f'{pf["slug"]}.html'
        desc = pf["lede"]
        out = [self.head(f'{pf["title"]} · {NAME}', f'{pf["title"]} portfolio of {NAME}. {desc}', path,
                         f'page-{pf["slug"]}')]

        projects = [p for g in pf["groups"] for p in g["projects"]]
        index = "\n".join(f'        <li><a href="#{p["id"]}"><b>{i:02d}</b>{e(p["title"])}</a></li>'
                          for i, p in enumerate(projects, 1))
        out.append(f"""<div class="wrap">
  <section class="page-hero">
    <span class="tag">{pf["num"]}</span>
    <p class="eyebrow">{e(pf["eyebrow"])}</p>
    <h1>{e(pf["title"])}</h1>
    <p class="lede">{e(pf["lede"])}</p>
    <nav class="index" aria-label="Projects">
      <ol>
{index}
      </ol>
    </nav>
  </section>
""")
        n = 0
        for g in pf["groups"]:
            level = 2
            if g.get("label"):
                level = 3
                img = ""
                if g.get("logo"):
                    logo, alt, cls = g["logo"]
                    lv = self.m[os.path.splitext(os.path.basename(logo))[0]]
                    cls_attr = f' class="{cls}"' if cls else ""
                    img = (f'\n    <img src="assets/img/{logo}" width="{lv["w"]}" height="{lv["h"]}" '
                           f'alt="{e(alt)}"{cls_attr}>')
                out.append(f"""  <div class="group-head">{img}
    <h2>{e(g["label"])}</h2>
  </div>
""")
            for p in g["projects"]:
                n += 1
                out.append(self.project(p, f"{n:02d}", level))

        nslug, nlabel, nsmall = nxt
        out.append(f"""  <nav class="next" aria-label="Next">
    <a href="{nslug}"><small>{e(nsmall)}</small><strong>{e(nlabel)} <span class="arrow">→</span></strong></a>
    <a class="more" href="#main">Back to top <span>↑</span></a>
  </nav>
</div>
""")
        out.append(self.foot())
        self.write(path, "".join(out))

    def home(self):
        sizes = {}
        for fname, _, _ in DOWNLOADS:
            sizes[fname] = os.path.getsize(os.path.join(self.root, "files", fname)) / 1e6
        desc = (f"{NAME} is a designer working across handbags and accessories, textiles and apparel. "
                "Portfolio of work for Kat Maconie, Pelicans London, Aranyani and EEBAGAA, handwoven textile collections "
                "and apparel projects.")
        out = [self.head(f"{NAME} · Accessories, Textile & Apparel Designer", desc, "", "page-home")]

        chapters = [
            ("accessories.html", "01", "var(--accessories)", "Accessories",
             "Tech packs, colourways and collections for Kat Maconie, Pelicans London, Aranyani and freelance "
             "client EEBAGAA, from embellished sandals and canvas rucksacks to leather totes and small leather goods.",
             ["Kat Maconie Footwear", "EEBAGAA", "BMW Alpina CCB", "Canvas Bags", "Back to School", "Aranyani SLGs"],
             f'<img {self.img_attrs("cover-accessories")} alt="Kat Maconie embellished block-heel sandals arranged '
             f'around a model’s feet on a beige backdrop" loading="eager" fetchpriority="high">'),
            ("textile.html", "02", "var(--textile)", "Textile",
             "Handspun Eri silk dyed with turmeric, indigo and onion peel; prints drawn from palace mosaics "
             "and mountain flowers; embroidery samples; and a fellowship building livelihoods in Assam.",
             [p["title"] for p in TEXTILE["groups"][0]["projects"]],
             f'<img {self.img_attrs("cover-textile")} alt="Blooming Abode: layered landscape collage with '
             f'printed hills and flowers" loading="lazy">'),
            ("apparel.html", "03", "var(--apparel)", "Apparel",
             "Ensembles in Khasi, Jaintia, Rabha, Hajong and Assamese handwoven fabrics, with surface "
             "development, export-house sampling and pattern-making experiments.",
             ["Saadgi", "Indian Wear", "Surface Development", "The Orient", "Kaftaan"],
             f'<img {self.img_attrs("app-orient-1")} alt="The Orient ensemble, look 1" loading="lazy">'
             f'<img {self.img_attrs("app-orient-2")} alt="The Orient ensemble, look 2" loading="lazy">'),
        ]
        ch_html = []
        for href, num, color, title, text, items, media in chapters:
            lis = "".join(f"<li>{e(i)}</li>" for i in items)
            ch_html.append(f"""    <a class="chapter" href="{href}" style="--tag:{color}">
      <div class="chapter-media">{media}</div>
      <div>
        <span class="tag chapter-num">{num}</span>
        <h2>{title}</h2>
        <p>{e(text)}</p>
        <ul>{lis}</ul>
        <span class="more">View portfolio <span>→</span></span>
      </div>
    </a>""")

        dls = "\n".join(
            f'      <a class="dl" href="files/{f}" download><span><strong>{e(t)}</strong>'
            f'<small>PDF · {pages} · {sizes[f]:.1f} MB</small></span><span aria-hidden="true">↓</span></a>'
            for f, t, pages in DOWNLOADS)

        out.append(f"""<section class="hero wrap">
  <p class="eyebrow">Design Portfolio</p>
  <h1>Sanika<br><em>Paranjpe</em></h1>
  <p class="lede">Designer working across handbags &amp; accessories, textiles and apparel: from tech packs
  and colourways to handwoven, naturally dyed cloth made with craft communities in Northeast India.</p>
  <ul class="disciplines">
    <li><i style="background:var(--accessories)"></i>Accessories</li>
    <li><i style="background:var(--textile)"></i>Textile</li>
    <li><i style="background:var(--apparel)"></i>Apparel</li>
  </ul>
  <div class="worked">
    <div><strong>Pelicans London</strong>Bag collections &amp; tech packs</div>
    <div><strong>Aranyani</strong>SLGs, trims &amp; tech packs</div>
    <div><strong>EEBAGAA</strong>Freelance tech packs</div>
    <div><strong>SBI Youth for India</strong>Fellow, with the ant, Assam</div>
  </div>
</section>

<section class="chapters wrap" aria-label="Portfolios">
{chr(10).join(ch_html)}
</section>

<section class="downloads">
  <div class="wrap">
    <h2>Download the portfolios</h2>
    <p>The original PDF portfolios, for print or offline viewing.</p>
    <div class="dl-list">
{dls}
    </div>
  </div>
</section>
""")
        out.append(self.foot())
        self.write("index.html", "".join(out))

    def write(self, rel, text):
        with open(os.path.join(self.root, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("wrote", rel)


def main():
    b = Builder(sys.argv[1])
    b.home()
    b.portfolio_page(ACCESSORIES, ("textile.html", "Textile", "Next portfolio"))
    b.portfolio_page(TEXTILE, ("apparel.html", "Apparel", "Next portfolio"))
    b.portfolio_page(APPAREL, ("./", "Home", "Back to"))


if __name__ == "__main__":
    main()
