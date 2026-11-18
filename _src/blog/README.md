# Blog — come funziona

Ogni articolo è un file JSON in questa cartella, chiamato `AAAA-MM-GG-slug.json`.
Dopo aver aggiunto o modificato un articolo:

    python3 _src/cover.py    # crea la copertina in images/blog/<slug>.jpg (solo se manca)
    python3 _src/build.py    # rigenera blog.html, blog/<slug>.html, la home e la sitemap

Un articolo con `date` futura resta nascosto finché non arriva quel giorno (e si rigenera il sito).
Per usare una foto tua al posto della copertina grafica: salvala come `images/blog/<slug>.jpg` (1200x630).

## Campi
- `slug` — indirizzo della pagina (minuscolo, trattini): blog/<slug>.html
- `date` — AAAA-MM-GG
- `category` — una tra: Siti web · SEO e Google · Intelligenza artificiale · E-commerce · Social e ADV · Gestionali e CRM · Strategia digitale
- `service` — servizio da consigliare in fondo: siti-web, ecommerce, dashboard, agente-ai-email, agente-ai-whatsapp, strategia-digitale, campagne-adv
- `title`, `seo_title` (max ~65 caratteri), `desc` (meta description, max ~155 caratteri), `excerpt` (anteprima nelle card)
- `alt` — descrizione dell'immagine
- `minutes` — minuti di lettura
- `body` — HTML dell'articolo (p, h2, h3, ul/ol, blockquote, `<div class='box'>` per i consigli). Attributi con apici singoli.
- `faqs` — lista di [domanda, risposta]
- `image` (facoltativo) — percorso di un'immagine diversa
- `updated` (facoltativo) — data dell'ultimo aggiornamento

## Regole
- Niente prezzi o cifre dei pacchetti.
- Dare del "tu" al lettore, come nel resto del sito.
- Link interni verso le pagine servizio e contatti.html.
- Gli argomenti già usati e quelli da fare sono in `ARGOMENTI.md`.
