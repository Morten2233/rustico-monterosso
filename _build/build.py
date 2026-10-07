# Baut die statische Verkaufsseite (index.html, en/, it/) aus content.json.
# Aufruf: python _build/build.py  (aus dem Ordner Webseite)
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(ROOT, "_build", "content.json"), encoding="utf-8"))
SITE = "https://rustico-monterosso.com/"
FORM_ENDPOINT = C["form_endpoint"]
TALL = {"02", "06", "07", "10", "12", "15", "16", "19", "25", "26", "27", "28", "29", "30", "31"}
e = html.escape
FLAGS = {
    "de": '<svg class="flag" viewBox="0 0 5 3" aria-hidden="true"><rect width="5" height="1" fill="#000"/><rect y="1" width="5" height="1" fill="#DD0000"/><rect y="2" width="5" height="1" fill="#FFCE00"/></svg>',
    "en": '<svg class="flag" viewBox="0 0 60 30" aria-hidden="true"><clipPath id="uk"><path d="M0,0 v30 h60 v-30 z"/></clipPath><path d="M0,0 v30 h60 v-30 z" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6" clip-path="url(#uk)"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#C8102E" stroke-width="3" clip-path="url(#uk)"/><path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/><path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></svg>',
    "fr": '<svg class="flag" viewBox="0 0 3 2" aria-hidden="true"><rect width="1" height="2" fill="#002654"/><rect x="1" width="1" height="2" fill="#fff"/><rect x="2" width="1" height="2" fill="#CE1126"/></svg>',
    "it": '<svg class="flag" viewBox="0 0 3 2" aria-hidden="true"><rect width="1" height="2" fill="#009246"/><rect x="1" width="1" height="2" fill="#fff"/><rect x="2" width="1" height="2" fill="#CE2B37"/></svg>',
}


def page(lang):
    t = C["t"][lang]
    base = "" if lang == "de" else "../"
    url = SITE if lang == "de" else f"{SITE}{lang}/"
    langs = "".join(
        f'<a href="{base}{"" if l == "de" else l + "/"}" hreflang="{l}"'
        + (' aria-current="true"' if l == lang else "")
        + f">{FLAGS[l]}<span>{l.upper()}</span></a>"
        for l in ("de", "en", "fr", "it")
    )
    alts = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE}{"" if l == "de" else l + "/"}">'
        for l in ("de", "en", "fr", "it")
    )
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in t["facts"])
    intro = "".join(f"<p>{e(p)}</p>" for p in t["intro"])
    dist = "".join(f"<li><span>{e(k)}</span><span>{e(v)}</span></li>" for k, v in t["dist"])
    equip = "".join(f"<li>{e(x)}</li>" for x in t["equip"])
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
    allp = C["photos"] + C["area_photos"]
    photos_js = json.dumps([{"src": f'{base}photos/{p["n"]}.jpg', "alt": p[lang]} for p in allp], ensure_ascii=False)
    off = len(C["photos"])
    area_tiles = "".join(
        f'<button type="button" class="tile" data-i="{off + i}" aria-label="{e(p[lang])}">'
        f'<img src="{base}photos/t_{p["n"]}.jpg" alt="{e(p[lang])}" width="1200" height="1600" loading="lazy"><span>{e(p[lang])}</span></button>'
        for i, p in enumerate(C["area_photos"])
    )
    S = C["seller"]
    L = C["legal"]
    seller_html = (
        f'<section class="seller wrap" id="verkaeufer">'
        f'<img src="{base}{S["photo"]}" alt="{e(S["name"])}" width="200" height="200" loading="lazy">'
        f'<div><h2>{e(S["title"][lang])}</h2>'
        f'<p class="seller-name">{e(S["name"])}<span>{e(S["role"][lang])}</span></p>'
        + "".join(f"<p>{e(x)}</p>" for x in S["text"][lang])
        + "</div></section>"
    )
    foot_links = (
        f'<a href="{base}{lang}/impressum.html" class="flink">{e(L["imprint"][lang])}</a>'
        f'<a href="{base}{lang}/datenschutz.html" class="flink">{e(L["privacy"][lang])}</a>'
    ) if lang != "de" else (
        f'<a href="impressum.html" class="flink">{e(L["imprint"]["de"])}</a>'
        f'<a href="datenschutz.html" class="flink">{e(L["privacy"]["de"])}</a>'
    )

    ld = {
        "@context": "https://schema.org",
        "@type": "Offer",
        "name": t["title"],
        "price": C["price_num"],
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
      <div class="price"><small>{e(t["price"])}</small><strong>{C["price_display"]}</strong></div>
      <a class="visit-cta" href="#kontakt">{e(t["ctaVisit"])} <span aria-hidden="true">→</span></a>
      <button type="button" class="sound-cta" id="soundBtn"><span class="play" aria-hidden="true"><svg width="12" height="14" viewBox="0 0 12 14"><path d="M1 1l10 6-10 6z" fill="currentColor"/></svg></span>{e(t["ctaSound"])}</button>
    </div>
  </div>
</section>

<section class="intro wrap" id="haus">
  <div><h2>{e(t["introTitle"])}</h2><div class="prose">{intro}</div></div>
  <dl class="facts">{facts}</dl>
</section>

<section class="plan wrap" id="grundriss">
  <div class="plan-copy"><h2>{e(t["planTitle"])}</h2><p>{e(t["planText"])}</p><a class="map-link dark" href="{base}grundriss.pdf" target="_blank" rel="noopener">{e(t["planLink"])} ↗</a>
    <h3 class="equip-title">{e(t["equipTitle"])}</h3><ul class="equip">{equip}</ul></div>
  <a class="plan-img" href="{base}grundriss.png" target="_blank" rel="noopener"><img src="{base}grundriss.png" alt="{e(t["planTitle"])}" width="880" height="1260" loading="lazy"></a>
  <figure class="draw"><a href="{base}schnitt.jpg" target="_blank" rel="noopener"><img src="{base}schnitt.jpg" alt="{e(t["drawCap"])}" width="1289" height="752" loading="lazy"></a><figcaption>{e(t["drawCap"])}</figcaption></figure>
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
  <div class="wrap"><img class="wide" src="{base}photos/20.jpg" alt="{e(next(p[lang] for p in C["photos"] if p["n"] == "20"))}" loading="lazy" width="1600" height="1200"></div>
  <div class="wrap area"><h3>{e(t["areaTitle"])}</h3><p>{e(t["areaText"])}</p><div class="area-grid">{area_tiles}</div></div>
</section>

<section class="buy wrap" id="kauf">
  <h2>{e(t["buyTitle"])}</h2><p class="sub">{e(t["buyText"])}</p>
  <ol class="steps">{steps}</ol>
</section>

{seller_html}

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
<div class="mbar" id="mbar"><div><small>{e(t["price"])}</small><strong>{C["price_display"]}</strong></div><a href="#kontakt">{e(t["ctaVisit"])} →</a></div>
<footer class="foot"><div class="wrap"><span>{e(t["footer"])}</span><span class="flinks">{foot_links}</span><a href="#top" aria-label="top">↑</a></div></footer>

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


for lang in ("de", "en", "fr", "it"):
    d = ROOT if lang == "de" else os.path.join(ROOT, lang)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(lang))
print("ok")


# --- Rechtsseiten: Impressum und Datenschutzerklaerung je Sprache ---
LEGAL_TXT = {
    "de": {
        "imp_h": "Impressum",
        "imp": [
            ("Angaben gemäß § 5 DDG", "{owner}<br>{street}<br>{city}<br>{country}<br>E-Mail: {email}"),
            ("Verantwortlich für den Inhalt", "{owner}, Anschrift wie oben"),
            ("Art des Angebots", "Diese Seite ist ein privates Verkaufsangebot für eine einzelne Immobilie. Es handelt sich nicht um ein gewerbliches Angebot und nicht um eine Maklertätigkeit."),
            ("Streitbeilegung", "Zur Teilnahme an einem Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle sind wir nicht verpflichtet und nicht bereit."),
        ],
        "pri_h": "Datenschutzerklärung",
        "pri": [
            ("Verantwortlicher", "{owner}<br>{street}<br>{city}<br>{country}<br>E-Mail: {email}"),
            ("Aufruf der Seite", "Die Seite wird über GitHub Pages bereitgestellt (GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). Beim Aufruf überträgt Ihr Browser technisch notwendige Daten wie IP-Adresse, Datum und Uhrzeit, die GitHub in Server-Protokollen speichert. Rechtsgrundlage ist unser berechtigtes Interesse am sicheren Betrieb der Seite (Art. 6 Abs. 1 lit. f DSGVO)."),
            ("Kontaktformular", "Ihre Angaben aus dem Formular werden über den Dienst FormSubmit (formsubmit.co) per E-Mail an uns weitergeleitet und nur zur Beantwortung Ihrer Anfrage verwendet. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b und f DSGVO. Wir löschen die Daten, sobald die Anfrage erledigt ist."),
            ("Schriften", "Die Schriften werden von unserem eigenen Server geladen, es besteht keine Verbindung zu Google Fonts."),
            ("Keine Cookies, keine Statistik", "Die Seite setzt keine Cookies und verwendet keine Analyse- oder Werbedienste."),
            ("Ihre Rechte", "Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch sowie ein Beschwerderecht bei einer Datenschutz-Aufsichtsbehörde."),
        ],
        "back": "Zurück zur Startseite",
    },
    "en": {
        "imp_h": "Legal notice",
        "imp": [
            ("Provider", "{owner}<br>{street}<br>{city}<br>{country}<br>E-mail: {email}"),
            ("Responsible for the content", "{owner}, address as above"),
            ("Type of offer", "This page is a private sale offer for a single property. It is not a commercial offer and not an estate agency service."),
            ("Dispute resolution", "We are not obliged and not willing to take part in dispute resolution proceedings before a consumer arbitration board."),
        ],
        "pri_h": "Privacy policy",
        "pri": [
            ("Controller", "{owner}<br>{street}<br>{city}<br>{country}<br>E-mail: {email}"),
            ("Visiting this page", "The page is hosted on GitHub Pages (GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). Your browser transmits technically necessary data such as IP address, date and time, which GitHub stores in server logs. Legal basis: our legitimate interest in operating the site securely (Art. 6(1)(f) GDPR)."),
            ("Contact form", "The details you enter are forwarded to us by e-mail through the service FormSubmit (formsubmit.co) and used only to answer your enquiry. Legal basis: Art. 6(1)(b) and (f) GDPR. We delete the data once your enquiry has been dealt with."),
            ("Fonts", "Fonts are served from our own server; there is no connection to Google Fonts."),
            ("No cookies, no tracking", "This site sets no cookies and uses no analytics or advertising services."),
            ("Your rights", "You have the right to access, rectification, erasure, restriction of processing, data portability and objection, as well as the right to lodge a complaint with a supervisory authority."),
        ],
        "back": "Back to the home page",
    },
    "fr": {
        "imp_h": "Mentions légales",
        "imp": [
            ("Éditeur", "{owner}<br>{street}<br>{city}<br>{country}<br>E-mail : {email}"),
            ("Responsable du contenu", "{owner}, adresse ci-dessus"),
            ("Nature de l'offre", "Cette page est une offre de vente entre particuliers pour un seul bien. Il ne s'agit ni d'une offre commerciale ni d'une activité d'agence immobilière."),
            ("Règlement des litiges", "Nous ne sommes pas tenus de participer à une procédure de règlement des litiges devant un organisme de médiation et n'y sommes pas disposés."),
        ],
        "pri_h": "Politique de confidentialité",
        "pri": [
            ("Responsable du traitement", "{owner}<br>{street}<br>{city}<br>{country}<br>E-mail : {email}"),
            ("Consultation du site", "Le site est hébergé par GitHub Pages (GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis). Votre navigateur transmet des données techniques nécessaires telles que l'adresse IP, la date et l'heure, que GitHub conserve dans des journaux. Base légale : notre intérêt légitime à exploiter le site en toute sécurité (art. 6, par. 1, point f, RGPD)."),
            ("Formulaire de contact", "Vos données sont transmises par e-mail via le service FormSubmit (formsubmit.co) et utilisées uniquement pour répondre à votre demande. Base légale : art. 6, par. 1, points b et f, RGPD. Les données sont supprimées une fois la demande traitée."),
            ("Polices", "Les polices sont chargées depuis notre propre serveur, sans connexion à Google Fonts."),
            ("Pas de cookies, pas de statistiques", "Ce site ne dépose aucun cookie et n'utilise aucun service d'analyse ou de publicité."),
            ("Vos droits", "Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation du traitement, de portabilité et d'opposition, ainsi que du droit d'introduire une réclamation auprès d'une autorité de contrôle."),
        ],
        "back": "Retour à l'accueil",
    },
    "it": {
        "imp_h": "Note legali",
        "imp": [
            ("Titolare del sito", "{owner}<br>{street}<br>{city}<br>{country}<br>E-mail: {email}"),
            ("Responsabile dei contenuti", "{owner}, indirizzo come sopra"),
            ("Tipo di offerta", "Questa pagina è un offerta di vendita tra privati per un singolo immobile. Non si tratta di un offerta commerciale né di attività di agenzia immobiliare."),
            ("Risoluzione delle controversie", "Non siamo obbligati né disponibili a partecipare a procedure di conciliazione davanti a un organismo di risoluzione delle controversie dei consumatori."),
        ],
        "pri_h": "Informativa sulla privacy",
        "pri": [
            ("Titolare del trattamento", "{owner}<br>{street}<br>{city}<br>{country}<br>E-mail: {email}"),
            ("Visita del sito", "Il sito è ospitato su GitHub Pages (GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). Il browser trasmette dati tecnicamente necessari come indirizzo IP, data e ora, che GitHub conserva nei log del server. Base giuridica: il nostro legittimo interesse al funzionamento sicuro del sito (art. 6, par. 1, lett. f, GDPR)."),
            ("Modulo di contatto", "I dati inseriti vengono inoltrati via e-mail tramite il servizio FormSubmit (formsubmit.co) e utilizzati solo per rispondere alla sua richiesta. Base giuridica: art. 6, par. 1, lett. b ed f, GDPR. I dati vengono cancellati una volta evasa la richiesta."),
            ("Caratteri", "I caratteri sono caricati dal nostro server, senza collegamento a Google Fonts."),
            ("Nessun cookie, nessuna statistica", "Il sito non utilizza cookie né servizi di analisi o pubblicità."),
            ("I suoi diritti", "Ha diritto di accesso, rettifica, cancellazione, limitazione del trattamento, portabilità e opposizione, nonché di presentare reclamo a un autorità di controllo."),
        ],
        "back": "Torna alla pagina iniziale",
    },
}


def legal_page(lang, kind):
    L = C["legal"]
    T = LEGAL_TXT[lang]
    base = "" if lang == "de" else "../"
    head = T["imp_h"] if kind == "imprint" else T["pri_h"]
    rows = T["imp"] if kind == "imprint" else T["pri"]
    vals = {
        "owner": L["owner"], "street": L["street"], "city": L["city"],
        "country": L["country"][lang], "email": L["email"],
    }
    body = "".join("<h2>" + e(h) + "</h2><p>" + b.format(**vals) + "</p>" for h, b in rows)
    home = "./" if lang == "de" else "./"
    return (
        '<!doctype html>\n<html lang="' + lang + '">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + e(head) + " \u00b7 Rustico Soviore</title>\n"
        '<meta name="robots" content="noindex">\n'
        '<link rel="icon" href="' + base + 'favicon.svg" type="image/svg+xml">\n'
        '<link rel="stylesheet" href="' + base + 'fonts.css">\n'
        '<link rel="stylesheet" href="' + base + 'style.css">\n'
        "</head>\n<body>\n"
        '<main class="legal wrap">\n<h1>' + e(head) + "</h1>\n" + body +
        '<p class="back"><a href="' + home + '">\u2190 ' + e(T["back"]) + "</a></p>\n"
        "</main>\n</body>\n</html>\n"
    )


for lang in ("de", "en", "fr", "it"):
    d = ROOT if lang == "de" else os.path.join(ROOT, lang)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "impressum.html"), "w", encoding="utf-8").write(legal_page(lang, "imprint"))
    open(os.path.join(d, "datenschutz.html"), "w", encoding="utf-8").write(legal_page(lang, "privacy"))
print("rechtsseiten ok")
