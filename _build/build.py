# Baut die statische Verkaufsseite (index.html, en/, it/) aus content.json.
# Aufruf: python _build/build.py  (aus dem Ordner Webseite)
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(ROOT, "_build", "content.json"), encoding="utf-8"))
SITE = "https://morten2233.github.io/rustico-monterosso/"
FORM_ENDPOINT = C["form_endpoint"]
TALL = {"02", "06", "07", "10", "12", "15", "16", "19"}
e = html.escape


def page(lang):
    t = C["t"][lang]
    base = "" if lang == "de" else "../"
    url = SITE if lang == "de" else f"{SITE}{lang}/"
    langs = "".join(
        f'<a href="{base}{"" if l == "de" else l + "/"}" hreflang="{l}"'
        + (' aria-current="true"' if l == lang else "")
        + f">{l.upper()}</a>"
        for l in ("de", "en", "it")
    )
    alts = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE}{"" if l == "de" else l + "/"}">'
        for l in ("de", "en", "it")
    )
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in t["facts"])
    intro = "".join(f"<p>{e(p)}</p>" for p in t["intro"])
    dist = "".join(f"<li><span>{e(k)}</span><span>{e(v)}</span></li>" for k, v in t["dist"])
    steps = "".join(
        f"<li><span class=\"num\">{i + 1}</span><h3>{e(k)}</h3><p>{e(v)}</p></li>"
        for i, (k, v) in enumerate(t["steps"])
    )
    tiles = "".join(
        f'<button type="button" class="tile" data-i="{i}" aria-label="{e(a)}">'
        f'<img src="{base}photos/t_{n}.jpg" alt="{e(a)}" width="{1200 if n in TALL else 1600}" '
        f'height="{1600 if n in TALL else 1200}" loading="lazy"><span>{e(a)}</span></button>'
        for i, (n, a) in enumerate((p["n"], p[lang]) for p in C["photos"])
    )
    photos_js = json.dumps([{"src": f'{base}photos/{p["n"]}.jpg', "alt": p[lang]} for p in C["photos"]], ensure_ascii=False)
    ld = {
        "@context": "https://schema.org",
        "@type": "Offer",
        "name": t["title"],
        "price": "165000",
        "priceCurrency": "EUR",
        "url": url,
        "image": SITE + "og.jpg",
        "itemOffered": {
            "@type": "House",
            "name": t["title"],
            "floorSize": {"@type": "QuantitativeValue", "value": 50, "unitCode": "MTK"},
            "numberOfRooms": 2,
            "address": {"@type": "PostalAddress", "addressLocality": "Monterosso al Mare", "addressRegion": "SP", "addressCountry": "IT"},
        },
    }
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["metaTitle"])}</title>
<meta name="description" content="{e(t["metaDesc"])}">
<link rel="canonical" href="{url}">{alts}
<meta property="og:type" content="website">
<meta property="og:title" content="{e(t["metaTitle"])}">
<meta property="og:description" content="{e(t["metaDesc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{base}poster-quer.jpg" as="image" media="(min-aspect-ratio: 1/1)">
<link rel="stylesheet" href="{base}fonts.css">
<link rel="stylesheet" href="{base}style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="bar" id="bar">
  <a class="brand" href="#top"><img src="{base}favicon.svg" alt="" width="30" height="30"><span>Rustico Soviore</span></a>
  <nav class="links"><a href="#haus">{e(t["nav"]["house"])}</a><a href="#bilder">{e(t["nav"]["photos"])}</a><a href="#lage">{e(t["nav"]["location"])}</a><a href="#kauf">{e(t["nav"]["buy"])}</a></nav>
  <div class="right"><div class="langs" aria-label="Sprache / Language">{langs}</div><a class="head-cta" href="#kontakt">{e(t["nav"]["contact"])}</a></div>
</header>
<main>
<section class="hero" id="top">
  <picture><source media="(max-aspect-ratio: 1/1)" srcset="{base}poster-hoch.jpg"><img class="hero-media" src="{base}poster-quer.jpg" alt=""></picture>
  <video class="hero-media" id="bgvideo" poster="{base}poster-quer.jpg" muted loop playsinline preload="none" aria-hidden="true" data-wide="{base}video/hero-quer.mp4" data-tall="{base}video/hero-hoch.mp4" data-sound-wide="{base}video/rundgang-quer.mp4" data-sound-tall="{base}video/rundgang-hoch.mp4"></video>
  <div class="hero-shade"></div>
  <div class="hero-inner wrap">
    <p class="eyebrow">{e(t["eyebrow"])}</p>
    <h1>{e(t["title"])}</h1>
    <p class="lead">{e(t["lead"])}</p>
    <div class="hero-row">
      <div class="price"><small>{e(t["price"])}</small><strong>165.000 €</strong></div>
      <a class="visit-cta" href="#kontakt">{e(t["ctaVisit"])} <span aria-hidden="true">→</span></a>
      <button type="button" class="sound-cta" id="soundBtn"><span class="play" aria-hidden="true"><svg width="12" height="14" viewBox="0 0 12 14"><path d="M1 1l10 6-10 6z" fill="currentColor"/></svg></span>{e(t["ctaSound"])}</button>
    </div>
  </div>
</section>

<section class="intro wrap" id="haus">
  <div><h2>{e(t["introTitle"])}</h2><div class="prose">{intro}</div></div>
  <dl class="facts">{facts}</dl>
</section>

<section class="gallery" id="bilder">
  <div class="wrap">
    <div class="gal-head"><h2>{e(t["photosTitle"])}</h2><p>{e(t["photosNote"])}</p></div>
    <div class="masonry">{tiles}</div>
  </div>
</section>

<section class="loc" id="lage">
  <div class="wrap loc-grid">
    <div><h2>{e(t["locTitle"])}</h2><p>{e(t["locText"])}</p><a class="map-link" href="{C["maps_url"]}" target="_blank" rel="noopener noreferrer">{e(t["mapLink"])} ↗</a></div>
    <ul class="dist">{dist}</ul>
  </div>
  <div class="wrap"><img class="wide" src="{base}photos/20.jpg" alt="{e(C["photos"][19][lang])}" loading="lazy" width="1600" height="1200"></div>
</section>

<section class="buy wrap" id="kauf">
  <h2>{e(t["buyTitle"])}</h2><p class="sub">{e(t["buyText"])}</p>
  <ol class="steps">{steps}</ol>
</section>

<section class="contact" id="kontakt">
  <img class="contact-bg" src="{base}photos/18.jpg" alt="" loading="lazy">
  <div class="contact-shade"></div>
  <div class="wrap contact-grid">
    <div class="contact-copy"><h2>{e(t["formTitle"])}</h2><p>{e(t["formText"])}</p></div>
    <form id="form" class="card" novalidate>
      <div class="fields">
        <label>{e(t["fName"])}<input name="name" required minlength="2" maxlength="120" autocomplete="name"></label>
        <label>{e(t["fEmail"])}<input name="email" type="email" required maxlength="200" autocomplete="email"></label>
        <label class="full">{e(t["fPhone"])}<input name="phone" type="tel" maxlength="60" autocomplete="tel"></label>
        <label class="full">{e(t["fMsg"])}<textarea name="message" required minlength="5" maxlength="4000" rows="4">{e(t["fMsgDefault"])}</textarea></label>
        <input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
      </div>
      <p class="privacy">{e(t["fPrivacy"])}</p>
      <p class="err" id="formErr" role="alert" hidden>{e(t["fErr"])}</p>
      <button class="submit" type="submit"><span class="prog" aria-hidden="true"></span><span class="lbl" data-send="{e(t["fSend"])}" data-sending="{e(t["fSending"])}">{e(t["fSend"])}</span></button>
      <div class="ok" id="formOk" hidden><strong>✓</strong><p>{e(t["fOk"])}</p></div>
    </form>
  </div>
</section>
</main>
<footer class="foot"><div class="wrap"><span>{e(t["footer"])}</span><a href="#top" aria-label="top">↑</a></div></footer>

<div class="modal" id="videoModal" hidden><div class="modal-in"><button type="button" class="close" data-close>{e(t["close"])} ✕</button><video id="modalVideo" controls playsinline></video></div></div>
<div class="modal lb" id="lightbox" hidden>
  <div class="lb-top"><span id="lbCap"></span><button type="button" class="close" data-close>{e(t["close"])} ✕</button></div>
  <div class="lb-stage"><button type="button" class="nav prev" aria-label="‹">‹</button><img id="lbImg" alt=""><button type="button" class="nav next" aria-label="›">›</button></div>
</div>
<script>window.PHOTOS={photos_js};window.FORM_ENDPOINT={json.dumps(FORM_ENDPOINT)};window.LANG={json.dumps(lang)};</script>
<script src="{base}app.js" defer></script>
</body>
</html>
"""


for lang in ("de", "en", "it"):
    d = ROOT if lang == "de" else os.path.join(ROOT, lang)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(lang))
print("ok")
