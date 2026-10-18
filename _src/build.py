#!/usr/bin/env python3
"""Genera tutte le pagine del sito con CSS e JS incorporati.
Uso:  python3 _src/build.py   (dalla cartella del repo)
La cartella _src non viene pubblicata da GitHub Pages (inizia con "_")."""
import json, os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_src')
CSS = open(os.path.join(SRC, 'style.css'), encoding='utf-8').read()
JS = open(os.path.join(SRC, 'app.js'), encoding='utf-8').read()
SITE = 'https://www.ilariavisciglia.it/'
TODAY = '2026-10-16'

ICON = {
 'web':  '<path d="M3 5h18v11H3z"/><path d="M8 20h8M12 16v4"/>',
 'shop': '<path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
 'crm':  '<rect x="3" y="3" width="7" height="8" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="15" width="7" height="6" rx="1"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'chat': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/>',
 'seo':  '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 6 6"/><path d="M8 12l2-2 2 1 2-3"/>',
 'ads':  '<path d="M3 10v4l11 5V5z"/><path d="M14 9a3 3 0 0 1 0 6M6 14v4"/>',
 'pay':  '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h4"/>',
 'mailc':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'wa':   '<path d="M5 19l1.3-3.6A8 8 0 1 1 9 18.3z"/><path d="M9 9.5c.5 2 2 3.6 4 4.3l1.2-1.1 1.8.8-.4 1.6c-3.6.3-7.3-3.3-7-7l1.6-.4.8 1.8z"/>',
 'ig':   '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
 'bot':  '<rect x="4" y="7" width="16" height="12" rx="3"/><path d="M12 3v4M9 12h.01M15 12h.01M9 16h6"/>',
}
def ico(k, size=None):
    s = f' width="{size}" height="{size}"' if size else ''
    return f'<svg viewBox="0 0 24 24"{s} fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'

# ------------------------------------------------------------------ SERVIZI
SERVICES = [
 dict(slug='siti-web', name='Siti Web su misura', short='Siti Web', code='MOD_01 // WEB', screen='code', icon='web',
  title='Creazione Siti Web a Roma | Web Designer Freelance — Ilaria Visciglia',
  desc='Web designer freelance a Roma: siti web su misura, landing page e siti aziendali scritti a mano, veloci e ottimizzati per Google. Preventivo gratuito.',
  h1='Il tuo sito web,<br><span class="grad">scritto su misura.</span>',
  intro='Landing page e siti aziendali fino a 5 pagine: ogni progetto è scritto a mano, pensato per il tuo settore e ottimizzato per farti trovare su Google.',
  card='Siti aziendali e landing page scritti a mano, veloci, animati e pronti per Google.',
  how=['Non parto da un modello pronto: ogni sito è scritto a mano, pensato sul tuo settore, sui tuoi obiettivi e su come i tuoi clienti ti cercano online.',
       'Che tu abbia bisogno di una landing page per lanciare un prodotto o di un sito aziendale completo, il risultato è un progetto veloce, responsive e pronto a farti trovare su Google con le parole giuste.'],
  feats=[('Design su misura','Nessun template: layout, colori e animazioni nascono dal tuo brand.'),('Google & SEO','Struttura tecnica corretta, meta tag, dati strutturati e parole chiave del tuo settore.'),
         ('Modulo contatti + WhatsApp','Le richieste arrivano direttamente alla tua email o in chat.'),('Privacy & cookie','Banner cookie e policy conformi al GDPR, già configurati.'),
         ('Velocità','Codice pulito e immagini leggere: il sito si apre in un attimo, anche da mobile.'),('Fino a 100 modifiche','Lo rivediamo insieme finché non è esattamente come lo vuoi.')],
  forwho='aziende, professionisti, agenzie, attività locali che vogliono farsi trovare su Google',
  faqs=[('Quante pagine posso avere?','Si parte da una landing page (una pagina singola ad alta conversione) fino a un sito completo di 5 pagine, con la possibilità di aggiungerne altre in base alle tue esigenze.'),
        ('Il sito sarà ottimizzato per i motori di ricerca?','Sì, ogni sito include l\'ottimizzazione Google & SEO di base: struttura tecnica corretta, velocità di caricamento e contenuti pensati per essere trovati.'),
        ('Fai anche il restyling di un sito esistente?','Sì: posso rifare grafica e struttura di un sito già online, mantenendo dominio e posizionamento e migliorando velocità e SEO.'),
        ('Quanto costa un sito web?','Il prezzo dipende dal numero di pagine e dalle funzionalità richieste. Scrivimi per raccontarmi il tuo progetto e ricevere un preventivo su misura, gratuito e senza impegno.')]),
 dict(slug='dashboard', name='CRM, Dashboard & Piattaforme', short='CRM & Dashboard', code='MOD_02 // CRM', screen='crm', icon='crm',
  title='CRM e Dashboard su Misura a Roma | Gestionali per Aziende — Ilaria Visciglia',
  desc='Sviluppo CRM, gestionali e dashboard su misura a Roma per aziende e agenzie: clienti, preventivi, dati in tempo reale, aree riservate e pannelli di amministrazione.',
  h1='CRM e dashboard<br><span class="grad">costruiti sulla tua azienda.</span>',
  intro='Clienti, preventivi, prenotazioni, dati e report in un unico posto: progetto CRM, gestionali e piattaforme su misura per aziende e agenzie, non un software generico da adattare.',
  card='Gestionali, CRM e dashboard con i dati della tua azienda in tempo reale, aree riservate e ruoli.',
  how=['Molte aziende lavorano ancora tra fogli Excel, email e messaggi sparsi. Un CRM su misura mette tutto in ordine: anagrafiche clienti, trattative, preventivi, scadenze e promemoria, con le schermate che servono davvero al tuo team.',
       'Per chi ha bisogno di più di un sito vetrina costruisco piattaforme complete: registrazione utenti, aree riservate, ruoli e permessi, pannelli di amministrazione e dashboard con grafici e KPI aggiornati in tempo reale.'],
  feats=[('CRM clienti','Anagrafiche, trattative, preventivi, storico e promemoria in un unico pannello.'),('Dashboard in tempo reale','KPI, grafici e report per vedere subito come va l\'azienda.'),
         ('Registrazione e accesso','Login sicuro, recupero password, aree riservate per clienti o collaboratori.'),('Ruoli e permessi','Ognuno vede solo quello che gli serve: admin, staff, clienti.'),
         ('Pannello di amministrazione','Gestisci contenuti e dati senza competenze tecniche.'),('Integrazioni','Pagamenti Stripe, email, WhatsApp, calendari e API di terze parti.')],
  forwho='aziende, agenzie, studi professionali, strutture ricettive, team che vogliono digitalizzare i processi',
  faqs=[('Perché un CRM su misura e non uno già pronto?','I CRM generici costringono ad adattare il tuo lavoro al software. Uno su misura segue i tuoi processi, ha solo le funzioni che ti servono e cresce insieme all\'azienda, senza canoni per utente.'),
        ('Che differenza c\'è con un sito normale?','Un sito vetrina mostra informazioni a tutti i visitatori. Una piattaforma permette agli utenti di registrarsi e accedere a un\'area personale, con dati e funzionalità dedicate a ciascuno.'),
        ('Posso gestire i contenuti da sola dopo il lancio?','Sì, la piattaforma viene consegnata con un pannello di amministrazione pensato per essere usato senza competenze tecniche.'),
        ('Quanto costa una piattaforma su misura?','Il prezzo dipende dalla complessità delle funzionalità richieste. Scrivimi per raccontarmi il tuo progetto e ricevere un preventivo su misura, gratuito e senza impegno.')]),
 dict(slug='ecommerce', name='E-commerce', short='E-commerce', code='MOD_03 // SHOP', screen='shop', icon='shop',
  title='Creazione E-commerce a Roma | Negozi Online su Misura — Ilaria Visciglia',
  desc='Realizzazione e-commerce su misura a Roma: catalogo prodotti, carrello, pagamenti sicuri anche a rate e ottimizzazione SEO. Il tuo negozio online pronto a vendere.',
  h1='Il tuo negozio online,<br><span class="grad">pronto a vendere.</span>',
  intro='Un e-commerce completo, su misura per i tuoi prodotti: catalogo, carrello, pagamenti sicuri e tutto quello che serve per iniziare a vendere online.',
  card='Negozi online su misura con catalogo, carrello, pagamenti sicuri e gestione ordini semplice.',
  how=['Un e-commerce non è solo un catalogo con un carrello: è uno strumento di vendita che deve essere veloce, chiaro e facile da gestire ogni giorno.',
       'Costruisco negozi online su misura per i tuoi prodotti, con pagamenti sicuri, gestione ordini semplice e una struttura pensata fin dall\'inizio per essere trovata su Google.'],
  feats=[('Catalogo su misura','Schede prodotto, varianti, categorie e filtri pensati per i tuoi articoli.'),('Carrello e pagamenti','Stripe: carte, Apple Pay, Google Pay e possibilità di pagamento a rate.'),
         ('Gestione ordini','Notifiche email automatiche e un pannello semplice per seguire ogni ordine.'),('SEO e-commerce','Schede prodotto ottimizzate per comparire su Google.'),
         ('Foto prodotti','Servizio fotografico professionale per presentare al meglio quello che vendi.'),('Fino a 100 modifiche','Lo rifiniamo insieme fino al lancio.')],
  forwho='negozi, artigiani, brand e aziende che vogliono vendere online',
  faqs=[('Che sistema di pagamento usate?','I pagamenti vengono gestiti tramite Stripe, una delle piattaforme più sicure e diffuse al mondo, che supporta carte, wallet digitali e più valute. Si può attivare anche il pagamento a rate.'),
        ('Posso gestire da sola i prodotti dopo il lancio?','Sì, il negozio viene consegnato con un pannello semplice da usare per aggiungere prodotti, modificare prezzi e seguire gli ordini.'),
        ('Quanto costa un e-commerce?','Il prezzo dipende dal numero di prodotti e dalle funzionalità richieste. Scrivimi per raccontarmi il tuo progetto e ricevere un preventivo su misura, gratuito e senza impegno.')]),
 dict(slug='agente-ai-email', name='Agente AI per Email', short='Agente AI Email', code='MOD_04 // MAIL', screen='mail', icon='mail',
  title='Assistente AI per Email a Roma | Automazione Email Aziendale — Ilaria Visciglia',
  desc='Un agente AI che legge, risponde e gestisce le email della tua azienda al posto tuo, anche in più lingue. Realizzazione e attivazione a Roma.',
  h1='Un assistente che risponde<br><span class="grad">alle email al posto tuo.</span>',
  intro='Un agente AI addestrato sulla tua attività, che legge, risponde e gestisce la posta in arrivo — anche quando tu non sei disponibile.',
  card='Un agente AI addestrato sulla tua attività che risponde alle email, anche in più lingue.',
  how=['Ogni email che resta senza risposta è un cliente che aspetta, o che si rivolge altrove. Un agente AI addestrato sulla tua attività legge i messaggi in arrivo e risponde in modo naturale, coerente con il tuo tono e le tue informazioni.',
       'Non è una risposta automatica generica: è un assistente che conosce i tuoi servizi, i tuoi orari e le domande più frequenti dei tuoi clienti.'],
  feats=[('Assistente su misura','Addestrato su servizi, orari, prezzi indicativi e FAQ della tua attività.'),('Risposte automatiche','Risposte naturali, con il tuo tono di voce.'),
         ('Multilingua','Risponde ai clienti stranieri nella loro lingua.'),('Sempre attivo','Anche di notte, nei weekend e quando sei in ferie.'),
         ('Attivazione rapida','Si collega alla casella che usi già.'),('Il controllo resta a te','Puoi scegliere quali email gestisce e rivedere le risposte.')],
  forwho='aziende, B&B, studi professionali e attività che ricevono molte email ogni giorno',
  faqs=[('L\'agente può gestire davvero le mie email?','Sì, viene addestrato sulle informazioni della tua attività (servizi, prezzi indicativi, orari, domande frequenti) e risponde in modo coerente con il tuo tono.'),
        ('Posso rivedere le risposte prima che partano?','Si può impostare in diversi modi, in base alle tue preferenze: ne parliamo insieme in fase di consulenza.'),
        ('Quanto costa attivare l\'assistente email?','Il costo di realizzazione e attivazione è fisso, mentre eventuali costi mensili di gestione (crediti AI, collegamenti) vengono concordati in consulenza. Scrivimi per un preventivo.')]),
 dict(slug='agente-ai-whatsapp', name='Agente AI per WhatsApp', short='Agente AI WhatsApp', code='MOD_05 // CHAT', screen='ai', icon='chat',
  title='Assistente AI per WhatsApp a Roma | Chatbot WhatsApp Business — Ilaria Visciglia',
  desc='Un agente AI sul WhatsApp Business della tua attività che risponde ai clienti 24 ore su 24, anche in più lingue. Realizzazione e attivazione a Roma.',
  h1='Un assistente AI su WhatsApp,<br><span class="grad">sempre attivo.</span>',
  intro='Un agente AI sul numero WhatsApp della tua attività, che risponde ai clienti 24 ore su 24 — anche di notte, nei weekend, in vacanza.',
  card='Risponde ai clienti sul tuo WhatsApp Business 24 ore su 24 e raccoglie le richieste.',
  how=['Su WhatsApp i clienti si aspettano una risposta rapida. Un agente AI sul numero della tua attività risponde alle domande più frequenti, raccoglie le richieste e resta attivo anche quando tu non lo sei.',
       'È addestrato sui tuoi servizi e sul tuo tono di voce, così chi scrive riceve sempre una risposta coerente, anche fuori orario.'],
  feats=[('Sul tuo numero','Si collega al WhatsApp Business della tua attività.'),('Sempre attivo','24 ore su 24, 7 giorni su 7.'),('Risponde alle FAQ','Orari, servizi, prezzi indicativi, come raggiungerti.'),
         ('Multilingua','Parla con i clienti stranieri nella loro lingua.'),('Raccoglie richieste','Prenotazioni e contatti vengono raccolti e inoltrati a te.'),('Il controllo resta a te','Puoi intervenire in chat quando vuoi.')],
  forwho='attività locali, centri estetici, B&B, ristoranti, studi medici e chiunque riceva tanti messaggi',
  faqs=[('Serve WhatsApp Business?','Sì, l\'assistente si collega al numero WhatsApp Business della tua attività. Se non lo hai ancora, ti guido nella configurazione.'),
        ('Può gestire anche gli ordini o le prenotazioni?','Può raccogliere le richieste e indirizzarle correttamente; per automazioni più complesse (come un booking completo) se ne parla in consulenza.'),
        ('Quanto costa attivare l\'assistente WhatsApp?','Il costo di realizzazione e attivazione è fisso, mentre eventuali costi mensili di gestione (crediti AI, collegamenti) vengono concordati in consulenza. Scrivimi per un preventivo.')]),
 dict(slug='strategia-digitale', name='Strategia Digitale & SEO', short='Strategia & SEO', code='MOD_06 // SEO', screen='seo', icon='seo',
  title='Strategia Digitale e SEO a Roma | Consulenza per Aziende — Ilaria Visciglia',
  desc='SEO tecnica, tracking delle conversioni e ottimizzazione continua: una strategia digitale su misura per far crescere la tua azienda a Roma e in tutta Italia.',
  h1='Un ecosistema digitale,<br><span class="grad">non solo un sito.</span>',
  intro='SEO tecnica, tracking avanzato e ottimizzazione continua: la strategia giusta per farti trovare online e trasformare i visitatori in clienti.',
  card='Audit SEO, tracking delle conversioni e report chiari per farti trovare su Google.',
  how=['Un bel sito non basta se nessuno lo trova. La strategia digitale mette insieme SEO tecnica, tracking delle conversioni e monitoraggio costante, per capire davvero cosa funziona e cosa va migliorato.',
       'Non è un intervento una tantum: è un lavoro continuo, con report periodici che ti mostrano i risultati in modo chiaro, senza tecnicismi.'],
  feats=[('Audit SEO tecnico','Analisi completa di cosa frena il tuo sito su Google.'),('Google Ads','Setup e ottimizzazione delle campagne di ricerca.'),('Tracking conversioni','Google Tag Manager e GA4 per misurare contatti e vendite.'),
         ('Report mensili','Risultati chiari, senza tecnicismi.'),('Ottimizzazione continua','Miglioramenti mese dopo mese sui dati reali.'),('Analisi competitor','Cosa fanno i concorrenti e come superarli.')],
  forwho='aziende che hanno già un sito ma non arrivano clienti da Google',
  faqs=[('In quanto tempo si vedono i risultati della SEO?','La SEO è un lavoro nel tempo: i primi segnali si vedono in genere dopo qualche settimana, i risultati più solidi dopo alcuni mesi di lavoro costante.'),
        ('Serve anche se ho già un sito?','Sì, l\'audit tecnico si può fare su un sito già esistente per individuare cosa sta frenando il posizionamento su Google.'),
        ('Quanto costa la strategia digitale?','Dipende dagli obiettivi e dal livello di intervento richiesto. Scrivimi per raccontarmi la tua situazione e ricevere un preventivo su misura, gratuito e senza impegno.')]),
 dict(slug='campagne-adv', name='Campagne Google & Meta Ads', short='Campagne ADV', code='MOD_07 // ADS', screen='ads', icon='ads',
  title='Campagne Google Ads e Meta Ads a Roma | Gestione ADV — Ilaria Visciglia',
  desc='Gestione di campagne Google Ads e Meta Ads a Roma: audience mirate, budget ottimizzato e report chiari per portare clienti reali alla tua azienda.',
  h1='Campagne ads<br><span class="grad">pensate per convertire.</span>',
  intro='Campagne Google Ads e Meta Ads impostate, seguite e ottimizzate passo dopo passo: audience mirate, budget sotto controllo e risultati misurabili, non solo click.',
  card='Campagne Google e Meta impostate e ottimizzate per portarti clienti reali, non solo click.',
  how=['Una campagna ADV ben fatta non punta solo ai click: punta a portarti le persone giuste, pronte a diventare clienti. Imposto e gestisco campagne su Google Ads e Meta Ads a partire da un\'analisi reale del tuo pubblico e dei tuoi obiettivi.',
       'Non è un intervento una tantum: è un lavoro continuo di ottimizzazione, con report periodici che ti mostrano i risultati in modo chiaro, senza tecnicismi.'],
  feats=[('Google Ads','Intercetti chi sta già cercando i tuoi servizi.'),('Meta Ads','Facebook e Instagram per farti conoscere da nuovi clienti.'),('Targeting','Audience costruite sul tuo cliente ideale.'),
         ('Tracking conversioni','Sai quanti contatti e vendite porta ogni euro investito.'),('Report mensili','Numeri chiari e cosa faremo il mese dopo.'),('Ottimizzazione continua','Budget spostato su ciò che funziona davvero.')],
  forwho='aziende e attività che vogliono contatti e vendite in tempi brevi',
  faqs=[('In quanto tempo si vedono i risultati delle campagne ADV?','A differenza della SEO, le campagne a pagamento portano traffico da subito: i primi dati utili si vedono già nelle prime settimane, poi si ottimizza in base ai risultati reali.'),
        ('Meglio Google Ads o Meta Ads?','Dipende da cosa vendi e da chi cerchi: Google Ads intercetta chi sta già cercando attivamente, Meta Ads costruisce interesse verso chi ancora non ti conosce. Spesso la combinazione dei due dà i risultati migliori.'),
        ('Quanto costa gestire una campagna ADV?','Dipende dal budget pubblicitario, dai canali scelti (Google, Meta o entrambi) e dal livello di gestione richiesto. Scrivimi per raccontarmi la tua situazione e ricevere un preventivo su misura, gratuito e senza impegno.')]),
]
SVC = {s['slug']: s for s in SERVICES}

# ------------------------------------------------------------------ PORTFOLIO
def shot(domain):
    # IMMAGINE PORTFOLIO: screenshot automatico del sito (servizio gratuito WordPress mShots).
    # Per usare una tua immagine: metti il file in images/portfolio/ e sostituisci l'URL.
    return 'https://s0.wp.com/mshots/v1/' + urllib.parse.quote('https://' + domain + '/', safe='') + '?w=1280&h=800'

PROJECTS = [
 dict(d='logovex.com', cat='ai', label='Progetto AI', tags=['AI · OpenAI','Stripe','Node.js','Railway'],
      text='Piattaforma per generare loghi con l\'intelligenza artificiale: l\'utente descrive il suo brand, paga con Stripe e riceve in pochi secondi un logo professionale. Backend Node.js su Railway e consegna automatica via email.'),
 dict(d='inpostsocial.com', cat='ai piattaforme', label='SaaS AI', tags=['AI Social Manager','Meta API','Supabase','Stripe'],
      text='AI social media manager: crea post, immagini e reel con l\'intelligenza artificiale e li pubblica su Instagram e Facebook. Piani in abbonamento con Stripe, login e dashboard utente su Supabase.'),
 dict(d='fashionharp.com', cat='piattaforme', label='Piattaforma', tags=['Supabase Auth','Dashboard','Profili'],
      text='Piattaforma moda completa: editoriali, runway coverage, registrazione utenti con dashboard personale, profili professionali e gestione file.'),
 dict(d='laperlanera.eu', cat='booking', label='Booking', tags=['Airbnb Sync','Stripe','Prezzi dinamici'],
      text='Casa vacanza a Roma con sistema di prenotazione custom: calendario sincronizzato con Airbnb, prezzi stagionali, pagamenti Stripe e notifiche email automatiche.'),
 dict(d='emifotoottica.it', cat='corporate', label='Ottica', tags=['Prova virtuale','SEO locale'],
      text='Sito per un\'ottica a Roma con prova virtuale degli occhiali direttamente dal browser, senza app da scaricare.'),
 dict(d='laboratoriwrapping.it', cat='corporate', label='Sito 3D', tags=['Three.js','Animazioni allo scroll'],
      text='Sito energico per un\'azienda di car wrapping, con una sezione 3D allo scroll e un\'auto da personalizzare con i colori del wrapping.'),
 dict(d='vucandles.com', cat='ecommerce', label='E-commerce', tags=['Bilingue IT/EN','Catalogo'],
      text='E-commerce di candele artigianali, bilingue italiano e inglese: catalogo curato, acquisto semplice e un\'atmosfera calda fin dalla prima schermata.'),
 dict(d='gfmentalcoach.it', cat='corporate', label='Personal brand', tags=['Personal Brand','Design raffinato'],
      text='Sito professionale per una mental coach specializzata nel mondo equestre: design raffinato che comunica autorevolezza.'),
 dict(d='consorzioserviziesvilupporoma.it', cat='corporate', label='Istituzionale', tags=['B2B','Multi-servizi'],
      text='Sito istituzionale per un consorzio di servizi a Roma, con una struttura chiara per comunicare credibilità e servizi a un pubblico B2B.'),
 dict(d='emiliofranchini.com', cat='corporate', label='Professionista', tags=['Personal Brand'],
      text='Sito su misura per un professionista, pensato per valorizzare l\'identità del brand e la presenza online nel suo settore.'),
]

def pitem(p, big=False, i=0):
    tags = ''.join(f'<span>{t}</span>' for t in p['tags'])
    name = p['d'].split('.')[0]
    delay = f' d{(i % 3) + 1}' if i else ''
    return f'''<article class="pitem rv{delay}" data-cat="{p['cat']}">
  <div class="float"><a class="tilt shot" href="https://{p['d']}" target="_blank" rel="noopener" data-hover-screen="portfolio" aria-label="Apri {p['d']}">
    <div class="bar-top"><i></i><i></i><i></i><span>https://{p['d']}</span></div>
    <span class="badge">{p['label']}</span>
    <div class="img"><img src="{shot(p['d'])}" alt="Anteprima del sito {p['d']}" loading="lazy" width="1280" height="800"><div class="ph">{name}</div></div>
    <div class="glare"></div>
  </a></div>
  <div class="pmeta">
    <a class="site" href="https://{p['d']}" target="_blank" rel="noopener">{p['d']} <span aria-hidden="true">↗</span></a>
    <div class="tags">{tags}</div>
    <p>{p['text']}</p>
  </div>
</article>'''

# ------------------------------------------------------------------ PARTI COMUNI
NAV = [('chi-sono.html', 'Chi sono'), ('servizi.html', 'Servizi'), ('portfolio.html', 'Portfolio'), ('contatti.html', 'Contatti')]
FONTS = 'https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Manrope:wght@400;500;600;700&family=Press+Start+2P&display=swap'

LD_BUSINESS = {
 "@context": "https://schema.org", "@type": "ProfessionalService",
 "name": "Ilaria Visciglia — Web Designer a Roma", "image": SITE + "images/photo2.jpg", "url": SITE,
 "email": "info@ilariavisciglia.it", "telephone": "+393291489983", "priceRange": "€€",
 "description": "Web designer freelance a Roma: soluzioni digitali per aziende e agenzie — siti web, CRM, dashboard, e-commerce e agenti AI.",
 "address": {"@type": "PostalAddress", "addressLocality": "Roma", "addressRegion": "RM", "addressCountry": "IT"},
 "areaServed": [{"@type": "City", "name": "Roma"}, {"@type": "Country", "name": "Italia"}],
 "sameAs": ["https://www.instagram.com/iladesign_web"],
 "vatID": "IT18671571000",
 "founder": {"@type": "Person", "name": "Ilaria Visciglia", "jobTitle": "Web Designer & Developer freelance"},
 "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s['name']}} for s in SERVICES],
}

def head(title, desc, path, extra_ld=None, og_img='images/photo2.jpg', robots='index, follow'):
    url = SITE + ('' if path == 'index.html' else path)
    lds = [LD_BUSINESS] if path == 'index.html' else []
    lds += extra_ld or []
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in lds)
    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<!-- Iubenda Cookie Banner -->
<script type="text/javascript">
var _iub = _iub || [];
_iub.csConfiguration = {{"siteId":4001214,"cookiePolicyId":51717720,"storage":{{"useSiteId":true}}}};
_iub.csLangConfiguration = {{"it":{{"cookiePolicyId":51717720}}}};
</script>
<script type="text/javascript" src="https://cs.iubenda.com/autoblocking/4001214.js"></script>
<script type="text/javascript" src="//cdn.iubenda.com/cs/gpp/stub.js"></script>
<script type="text/javascript" src="//cdn.iubenda.com/cs/iubenda_cs.js" charset="UTF-8" async></script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="author" content="Ilaria Visciglia">
<meta name="geo.region" content="IT-RM">
<meta name="geo.placename" content="Roma">
<meta name="theme-color" content="#05060b">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}{og_img}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Ilaria Visciglia — Web Designer a Roma">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}{og_img}">
<link rel="icon" type="image/png" href="images/logo-cropped.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<script>document.documentElement.classList.add('js');</script>
<style>
{CSS}
</style>
{ld}</head>'''

def header(active):
    links = ''.join(f'<a href="{h}"{" class=\"on\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    mlinks = ''.join(f'<a href="{h}"{" class=\"on\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<body>
<div class="boot" id="boot" aria-hidden="true"><div class="boot-in"><p>&gt; avvio ilaria_os…</p><div class="boot-bar"><i></i></div></div></div>
<canvas id="pc3d" aria-hidden="true"></canvas>
<header class="hdr">
  <div class="hdr-in">
    <a class="logo" href="/" aria-label="Ilaria Visciglia — Home"><span class="logo-badge">IV</span><span>ilaria.visciglia<small>web designer · Roma</small></span></a>
    <nav class="nav" aria-label="Menu principale">{links}</nav>
    <a class="btn" href="contatti.html" data-hover-screen="start">▶ Preventivo</a>
    <button class="burger" aria-label="Apri il menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
  <div class="xp"><i></i><b>XP 0%</b></div>
</header>
<nav class="mmenu" aria-label="Menu mobile">
  <span class="hud">Pausa · Menu</span>
  <a href="/"{" class=\"on\"" if active == "index.html" else ""}>Home</a>{mlinks}
  <a class="btn" href="contatti.html">▶ Richiedi un preventivo</a>
</nav>
<main>'''

def footer(extra_js=''):
    svc = ''.join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    return f'''</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div>
        <a class="logo" href="/"><span class="logo-badge">IV</span><span>ilaria.visciglia<small>web designer · Roma</small></span></a>
        <p>Web designer freelance a Roma. Soluzioni digitali per aziende e agenzie: siti web, CRM, dashboard, e-commerce e agenti AI.</p>
        <p class="mono" style="font-size:14px;color:var(--muted)">P.IVA 18671571000</p>
      </div>
      <div><h4>MENU</h4><ul><li><a href="/">Home</a></li>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}<li><a href="pagamenti.html">Pagamenti online</a></li></ul></div>
      <div><h4>SERVIZI</h4><ul>{svc}</ul></div>
      <div><h4>CONTATTI</h4><ul>
        <li><a href="mailto:info@ilariavisciglia.it">info@ilariavisciglia.it</a></li>
        <li><a href="https://wa.me/393291489983" target="_blank" rel="noopener">WhatsApp +39 329 148 9983</a></li>
        <li><a href="https://www.instagram.com/iladesign_web" target="_blank" rel="noopener">Instagram @iladesign_web</a></li>
        <li><span style="color:var(--muted);font-size:15.5px">Roma, Italia · anche da remoto</span></li></ul></div>
    </div>
    <div class="ftr-bot">
      <span>© 2026 Ilaria Visciglia — Web Designer &amp; Developer — Roma, Italia</span>
      <span><a href="https://www.iubenda.com/privacy-policy/51717720" class="iubenda-white iubenda-noiframe iubenda-embed" title="Privacy Policy">Privacy Policy</a><a href="https://www.iubenda.com/privacy-policy/51717720/cookie-policy" class="iubenda-white iubenda-noiframe iubenda-embed" title="Cookie Policy">Cookie Policy</a></span>
    </div>
  </div>
</footer>
<button class="ai-bub" id="ai-bub" aria-label="Apri l'assistente">{ico('bot')}</button>
<div class="ai-panel" id="ai-panel" role="dialog" aria-label="Assistente di Ilaria">
  <div class="ai-head"><span class="logo-badge">IV</span><div><b>Assistente di Ilaria</b><small>● online ora</small></div><button id="ai-close" aria-label="Chiudi">✕</button></div>
  <div class="ai-msgs" id="ai-msgs"><div class="amsg bot">Ciao! 👋 Sono l'assistente virtuale di Ilaria. Chiedimi di siti web, CRM e dashboard, e-commerce, agenti AI o pagamenti a rate.</div></div>
  <div class="ai-in"><input id="ai-input" type="text" placeholder="Scrivi un messaggio…" aria-label="Messaggio"><button id="ai-send" aria-label="Invia">→</button></div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
{JS}
</script>
{extra_js}
<script type="text/javascript">(function (w,d) {{var loader = function () {{var s = d.createElement("script"), tag = d.getElementsByTagName("script")[0]; s.src="https://cdn.iubenda.com/iubenda.js"; tag.parentNode.insertBefore(s,tag);}}; if(w.addEventListener){{w.addEventListener("load", loader, false);}}else if(w.attachEvent){{w.attachEvent("onload", loader);}}else{{w.onload = loader;}}}})(window, document);</script>
</body>
</html>
'''

def srv_card(s, i):
    return f'''<a class="srv rv d{(i % 3) + 1}" href="{s['slug']}.html" data-hover-screen="{s['screen']}">
  <span class="lvl">{s['code'].split(' ')[0]}</span>
  <span class="ico">{ico(s['icon'])}</span>
  <h3>{s['name']}</h3>
  <p>{s['card']}</p>
  <span class="more">Scopri di più →</span>
</a>'''

def faq_html(faqs):
    return '<div class="faq">' + ''.join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs) + '</div>'

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def crumbs(*items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def cta(title='Pronta a passare<br>al <span class="grad">prossimo livello</span>?', text='Raccontami la tua idea: ti rispondo entro 24 ore con un preventivo gratuito e senza impegno.'):
    return f'''<section class="sec cta-big" data-pc="center" data-screen="start">
  <div class="wrap rv">
    <span class="hud pink">Player 2 · pronto?</span>
    <h2 class="glitch">{title}</h2>
    <p class="lead">{text}</p>
    <div class="btns"><a class="btn" href="contatti.html" data-hover-screen="start">▶ Iniziamo il progetto</a><a class="btn ghost" href="https://wa.me/393291489983" target="_blank" rel="noopener">Scrivimi su WhatsApp</a></div>
    <span class="press">PRESS START</span>
  </div>
</section>'''

STEPS = [('01', 'Discovery & analisi', 'Ascolto la tua idea, analizzo il settore e la concorrenza. Capisco cosa ti distingue prima ancora di aprire un editor.'),
         ('02', 'Concept & design', 'Prototipo visivo, palette, tipografia, layout: vedi com\'è il progetto prima di scrivere una riga di codice.'),
         ('03', 'Sviluppo & test', 'Codice pulito e ottimizzato, testato su tutti i dispositivi, con ogni funzionalità integrata con cura.'),
         ('04', 'Lancio & supporto', 'Pubblicazione, dominio, monitoraggio dopo il lancio. Non ti lascio sola dopo la consegna.')]
def steps_html():
    return '<div class="steps">' + ''.join(f'<div class="step rv d{i % 3 + 1}"><b>STAGE {n}</b><h3>{t}</h3><p>{d}</p></div>' for i, (n, t, d) in enumerate(STEPS)) + '</div>'

pages = {}

# ================================================================== HOME
home_srv = ''.join(srv_card(s, i) for i, s in enumerate(SERVICES))
pages['index.html'] = head(
  'Web Designer Roma | Soluzioni Digitali per Aziende — CRM, Dashboard, Siti e AI',
  'Ilaria Visciglia, web designer freelance a Roma: soluzioni digitali per aziende e agenzie. Siti web su misura, CRM, dashboard, e-commerce e agenti AI. Preventivo gratuito.',
  'index.html', [{"@context": "https://schema.org", "@type": "WebSite", "name": "Ilaria Visciglia — Web Designer a Roma", "url": SITE}]
) + header('index.html') + f'''
<!-- ===== 1. BANNER ANIMATO ===== -->
<section class="hero" data-pc="hero" data-screen="boot">
  <div class="hero-floor" aria-hidden="true"></div>
  <div class="wrap">
    <div class="half">
      <span class="hud rv">Player 1 · Web designer freelance · Roma</span>
      <h1 class="rv d1"><span class="h1-kicker">Web designer a Roma</span>Soluzioni digitali <span class="grad">per aziende e agenzie</span></h1>
      <div class="typer rv d2" data-words='["CRM su misura","dashboard aziendali","siti web che convertono","agenti AI 24/7","e-commerce","piattaforme e gestionali"]'>&gt; creo <span class="tw">CRM su misura</span><span class="cur"></span></div>
      <p class="lead rv d2">Sono Ilaria, <strong>web designer a Roma</strong>. Progetto e sviluppo siti web, CRM, dashboard e agenti AI che fanno lavorare meglio la tua azienda: codice scritto a mano, zero template.</p>
      <div class="btns rv d3">
        <a class="btn" href="contatti.html" data-hover-screen="start">▶ Inizia un progetto</a>
        <a class="btn ghost" href="portfolio.html" data-hover-screen="portfolio">Guarda il portfolio</a>
      </div>
      <div class="stats rv d3">
        <div class="stat"><b>5+</b><span>ANNI</span></div>
        <div class="stat"><b>10+</b><span>PROGETTI</span></div>
        <div class="stat"><b>AI</b><span>READY</span></div>
      </div>
    </div>
  </div>
  <div class="scroll-hint" aria-hidden="true">SCROLL<i></i></div>
</section>

<!-- ===== 2. CHI SONO ===== -->
<section class="sec" id="chi-sono" data-pc="right" data-screen="about">
  <div class="wrap">
    <div class="half" style="max-width:700px">
      <span class="hud rv">Lvl 01 · Chi sono</span>
      <div class="player m-panel">
        <div class="pcard-photo rv"><img src="images/photo2.jpg" alt="Ilaria Visciglia, web designer freelance a Roma" width="1023" height="1423" loading="lazy"><span class="scan"></span><span class="tag">PLAYER_1<br>ILARIA V.</span></div>
        <div class="rv d1">
          <h2>Ciao, sono <span class="grad">Ilaria.</span></h2>
          <p>Sono una <strong>freelance web designer</strong> e sviluppatrice di Roma. Vengo dalla grafica pubblicitaria e da un master in web design: da oltre 5 anni unisco estetica e codice per costruire strumenti digitali che lavorano davvero per le aziende.</p>
          <p>Parli direttamente con chi progetta e scrive il tuo sito, il tuo CRM o il tuo agente AI: nessun passaggio inutile, nessun template.</p>
          <div class="bars">
            <div class="bar">DESIGN<i style="--w:95%"></i></div>
            <div class="bar">CODICE<i style="--w:90%;--c:var(--pink)"></i></div>
            <div class="bar">AI<i style="--w:88%;--c:var(--lime)"></i></div>
            <div class="bar">STRATEGIA<i style="--w:82%;--c:var(--amber)"></i></div>
          </div>
          <div class="btns"><a class="btn ghost" href="chi-sono.html" data-hover-screen="about">La mia storia →</a></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ===== 3. MISSION ===== -->
<section class="sec" data-pc="left" data-screen="mission">
  <div class="wrap">
    <div class="half r m-panel">
      <span class="hud pink rv">Lvl 02 · Mission</span>
      <h2 class="rv d1">La mia <span class="grad">missione</span></h2>
      <p class="quote rv d1">Rendere le aziende vive nel tempo: rendimento continuo, una presenza online che si distingue davvero e tecnologia che lavora per loro 24 ore su 24.</p>
      <p class="rv d2" style="margin-top:22px">Ogni progetto nasce per risolvere un problema concreto: farti trovare su Google, togliere lavoro ripetitivo al tuo team, trasformare i visitatori in clienti. Il digitale come alleato, non come costo.</p>
    </div>
  </div>
</section>

<!-- ===== 4. SERVIZI (assaggio) ===== -->
<section class="sec" data-pc="corner-r" data-screen="crm">
  <div class="wrap">
    <span class="hud rv">Lvl 03 · Servizi</span>
    <h2 class="rv d1" style="max-width:900px">Scegli il tuo <span class="grad">power-up</span> digitale</h2>
    <p class="lead rv d2">Dal sito web al CRM su misura, dalla dashboard all'agente AI: tutto quello che serve alla tua azienda per crescere online, costruito da zero.</p>
    <div class="srv-grid">{home_srv}</div>
    <div class="btns rv"><a class="btn ghost" href="servizi.html">Tutti i servizi nel dettaglio →</a></div>
  </div>
</section>

<!-- ===== 5. PORTFOLIO (progetti AI) ===== -->
<section class="sec" data-pc="corner-l" data-screen="portfolio">
  <div class="wrap">
    <span class="hud pink rv">Lvl 04 · Portfolio</span>
    <h2 class="rv d1">Livelli <span class="grad">completati</span></h2>
    <p class="lead rv d2">Due piattaforme con intelligenza artificiale progettate, sviluppate e gestite da me: dal design al backend, fino ai pagamenti.</p>
    <div class="port-grid">{pitem(PROJECTS[0])}{pitem(PROJECTS[1], i=1)}</div>
    <div class="btns rv"><a class="btn ghost" href="portfolio.html" data-hover-screen="portfolio">Vedi tutti i progetti →</a></div>
  </div>
</section>

<!-- ===== 6. FRASE FINALE ===== -->
{cta('Il tuo business merita<br>un <span class="grad">upgrade</span>.', 'Smetti di inseguire la concorrenza: costruiamo insieme gli strumenti digitali che la lasciano indietro. Preventivo gratuito, risposta entro 24 ore.')}
''' + footer()

# ================================================================== CHI SONO
TL = [('2019', 'Diploma in Grafica Pubblicitaria', 'Le fondamenta: composizione visiva, tipografia, comunicazione del brand. Qui ho capito che l\'estetica non è decorazione: è comunicazione.'),
      ('2020', 'Master in Web Design', 'Il salto tecnico: HTML, CSS, JavaScript avanzato, Node.js. La grafica incontra il codice e tutto cambia prospettiva.'),
      ('2021', 'I primi siti fuori dalla norma', 'La specializzazione nel web design interattivo: animazioni avanzate e layout che rompono le aspettative.'),
      ('2022', 'Piattaforme per i professionisti', 'Nasce FashionHarp: registrazione utenti, dashboard, profili. Il web diventa uno strumento di lavoro, non solo una vetrina.'),
      ('2024', 'AI e agenti virtuali', 'L\'intelligenza artificiale entra in ogni progetto: nasce LogoVex, il generatore di loghi con l\'AI, e i primi agenti per email e WhatsApp.'),
      ('2026', 'Soluzioni digitali per aziende', 'CRM, dashboard, piattaforme SaaS come InPostSocial e siti 3D immersivi: il prossimo livello è già in costruzione.')]
tl = ''.join(f'<div class="tl-item rv"><span class="y">{y}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for y, t, d in TL)
SKILLS = [('web', 'Design & Frontend', 'Interfacce animate, layout fuori dagli schemi, tipografia ricercata. Ogni pixel ha uno scopo.', ['HTML/CSS', 'JavaScript', 'Three.js', 'Figma']),
          ('crm', 'CRM & Piattaforme', 'Gestionali, dashboard e aree riservate con login, ruoli e dati in tempo reale.', ['Supabase', 'Dashboard', 'Auth', 'Ruoli']),
          ('bot', 'Intelligenza Artificiale', 'Agenti virtuali su misura, generazione di testi e immagini, automazioni.', ['OpenAI', 'Claude API', 'Chatbot', 'Automazioni']),
          ('pay', 'Pagamenti & Commerce', 'Checkout, abbonamenti, webhook, booking e pagamenti a rate.', ['Stripe', 'Klarna', 'Booking', 'E-commerce']),
          ('seo', 'Backend & Integrazioni', 'Node.js, API REST, database, deploy su Railway e Render.', ['Node.js', 'REST API', 'Railway', 'Webhook']),
          ('ads', 'Strategia Digitale', 'SEO tecnica, Google Ads, tracking delle conversioni per massimizzare il ritorno.', ['SEO', 'Google Ads', 'GA4', 'Meta Ads'])]
skills = ''.join(f'<div class="srv rv d{i % 3 + 1}" data-hover-screen="{["code","crm","ai","pay","dash","seo"][i]}"><span class="ico">{ico(k)}</span><h3>{t}</h3><p>{d}</p><div class="chips">{"".join(f"<span class=chip>{c}</span>" for c in cs)}</div></div>' for i, (k, t, d, cs) in enumerate(SKILLS))
pages['chi-sono.html'] = head(
  'Chi Sono | Ilaria Visciglia — Freelance Web Designer a Roma',
  'Ilaria Visciglia, freelance web designer e sviluppatrice a Roma: grafica pubblicitaria, master in web design, oltre 5 anni di siti, CRM, dashboard e agenti AI per aziende.',
  'chi-sono.html', [crumbs(('Home', ''), ('Chi sono', 'chi-sono.html')),
   {"@context": "https://schema.org", "@type": "Person", "name": "Ilaria Visciglia", "jobTitle": "Web Designer & Developer freelance", "url": SITE + "chi-sono.html", "image": SITE + "images/photo1.jpg", "address": {"@type": "PostalAddress", "addressLocality": "Roma", "addressCountry": "IT"}, "sameAs": ["https://www.instagram.com/iladesign_web"]}],
  og_img='images/photo1.jpg'
) + header('chi-sono.html') + f'''
<section class="hero" data-pc="right" data-screen="about">
  <div class="wrap">
    <div class="half" style="max-width:700px">
      <span class="hud rv">Profilo giocatore · Chi sono</span>
      <div class="player m-panel">
        <div class="pcard-photo rv"><img src="images/photo1.jpg" alt="Ilaria Visciglia, freelance web designer a Roma" width="1023" height="1427"><span class="scan"></span><span class="tag">PLAYER_1<br>ROMA · IT</span></div>
        <div class="rv d1">
          <h1 style="font-size:clamp(2.2rem,4.4vw,3.8rem)">Sono <span class="grad">Ilaria Visciglia</span></h1>
          <p class="lead">Web designer e sviluppatrice freelance a Roma. Da oltre 5 anni creo siti web, CRM, dashboard e agenti AI per aziende, agenzie e professionisti.</p>
          <p>Non mi accontento del "funziona": voglio che ogni progetto stupisca, converta e resti impresso a chi lo usa.</p>
          <div class="chips"><span class="chip">Roma, Italia</span><span class="chip">Web Designer</span><span class="chip">Developer</span><span class="chip">AI Integrator</span><span class="chip">Master in Web Design</span></div>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="sec" data-pc="left" data-screen="code">
  <div class="wrap"><div class="half r">
    <span class="hud pink rv">Storia · Livelli superati</span>
    <h2 class="rv">Da dove vengo, <span class="grad">dove vado.</span></h2>
    <div class="tl">{tl}</div>
  </div></div>
</section>
<section class="sec" data-pc="corner-r" data-screen="dash">
  <div class="wrap">
    <span class="hud rv">Inventario · Competenze</span>
    <h2 class="rv">Quello che <span class="grad">so fare.</span></h2>
    <div class="srv-grid">{skills}</div>
  </div>
</section>
<section class="sec" data-pc="right" data-screen="mission">
  <div class="wrap"><div class="half mv">
    <div class="panel corners rv"><span class="hud pink">Mission</span><p class="quote">Rendere le aziende vive nel tempo, con un rendimento continuo, una presenza online che si distingue davvero e tecnologia che lavora per loro 24 ore su 24.</p></div>
    <div class="panel corners rv d1"><span class="hud">Vision</span><p class="quote">Rendere i miei clienti sempre un passo avanti alla concorrenza: in un web che evolve ogni giorno, non basta stare al passo, bisogna guidare.</p></div>
  </div></div>
</section>
<section class="sec" data-pc="corner-l" data-screen="crm">
  <div class="wrap">
    <span class="hud rv">Perché scegliermi</span>
    <h2 class="rv">Non sono una web agency. <span class="grad">Sono meglio.</span></h2>
    <div class="grid4" style="margin-top:40px">
      <div class="step rv"><b>✦</b><h3>Artigianalità digitale</h3><p>Ogni progetto scritto a mano, nessun template. Codice pulito e tutto tuo.</p></div>
      <div class="step rv d1"><b>◈</b><h3>Approccio AI-native</h3><p>L'intelligenza artificiale non è un optional: è parte del mio modo di lavorare.</p></div>
      <div class="step rv d2"><b>◉</b><h3>Visione a lungo termine</h3><p>Costruisco asset digitali che crescono e producono nel tempo.</p></div>
      <div class="step rv d3"><b>⬡</b><h3>Comunicazione diretta</h3><p>Risposte entro 24 ore, aggiornamenti costanti, nessuna sorpresa finale.</p></div>
    </div>
  </div>
</section>
{cta()}
''' + footer()

# ================================================================== SERVIZI (hub dettagliato)
blocks = ''
for i, s in enumerate(SERVICES):
    side = 'right' if i % 2 == 0 else 'left'
    cls = 'half' if side == 'right' else 'half r'
    lis = ''.join(f'<li><span><strong>{t}</strong> — {d}</span></li>' for t, d in s['feats'])
    blocks += f'''
<section class="sec tight" id="{s['slug']}" data-pc="{side}" data-screen="{s['screen']}">
  <div class="wrap"><div class="{cls}">
    <div class="panel corners rv">
      <span class="hud{' pink' if i % 2 else ''}">{s['code']}</span>
      <h2 style="font-size:clamp(1.9rem,3.4vw,2.8rem)">{s['name']}</h2>
      <p>{s['intro']}</p>
      <p>{s['how'][0]}</p>
      <ul style="margin-top:18px">{lis}</ul>
      <p class="for">PER CHI È → <b>{s['forwho']}</b></p>
      <div class="btns" style="margin-top:24px"><a class="btn" href="{s['slug']}.html" data-hover-screen="{s['screen']}">Scopri il servizio →</a><a class="btn ghost" href="contatti.html">Preventivo</a></div>
    </div>
  </div></div>
</section>'''
toc = ''.join(f'<a href="#{s["slug"]}">{s["short"]}</a>' for s in SERVICES)
pages['servizi.html'] = head(
  'Servizi | Soluzioni Digitali per Aziende a Roma — Siti Web, CRM, AI | Ilaria Visciglia',
  'Tutti i servizi di Ilaria Visciglia, web designer a Roma: siti web su misura, CRM e dashboard, e-commerce, agenti AI per email e WhatsApp, SEO e campagne Google e Meta Ads.',
  'servizi.html', [crumbs(('Home', ''), ('Servizi', 'servizi.html')),
   {"@context": "https://schema.org", "@type": "ItemList", "name": "Servizi digitali per aziende",
    "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s['name'], "url": SITE + s['slug'] + '.html'} for i, s in enumerate(SERVICES)]}]
) + header('servizi.html') + f'''
<section class="hero" data-pc="hero" data-screen="dash">
  <div class="wrap"><div class="half m-panel">
    <span class="hud rv">Seleziona il tuo modulo · Servizi</span>
    <h1 class="rv d1">Soluzioni digitali <span class="grad">per aziende a Roma</span></h1>
    <p class="lead rv d2">Sette servizi, un'unica regola: niente template. Siti web, CRM, dashboard, e-commerce e agenti AI progettati intorno a come lavora davvero la tua azienda o la tua agenzia.</p>
    <div class="toc rv d3">{toc}</div>
  </div></div>
</section>
{blocks}
<section class="sec" data-pc="corner-r" data-screen="code">
  <div class="wrap">
    <span class="hud rv">Come lavoro</span>
    <h2 class="rv">Il mio <span class="grad">processo</span></h2>
    {steps_html()}
  </div>
</section>
{cta()}
''' + footer()

# ================================================================== PORTFOLIO
pf = ''.join(pitem(p, i=i) for i, p in enumerate(PROJECTS))
pages['portfolio.html'] = head(
  'Portfolio | Siti Web, Piattaforme e Progetti AI — Ilaria Visciglia Web Designer Roma',
  'Portfolio di Ilaria Visciglia, web designer a Roma: LogoVex e InPostSocial (piattaforme AI), siti web, e-commerce, booking e piattaforme su misura per aziende.',
  'portfolio.html', [crumbs(('Home', ''), ('Portfolio', 'portfolio.html')),
   {"@context": "https://schema.org", "@type": "ItemList", "name": "Portfolio progetti",
    "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": "https://" + p['d']} for i, p in enumerate(PROJECTS)]}]
) + header('portfolio.html') + f'''
<section class="hero" style="min-height:76vh" data-pc="hero" data-screen="portfolio">
  <div class="wrap"><div class="half m-panel">
    <span class="hud rv">Selezione livelli · Portfolio</span>
    <h1 class="rv d1">Il mio <span class="grad">portfolio</span></h1>
    <p class="lead rv d2">Piattaforme AI, siti web, e-commerce e sistemi di prenotazione: ogni progetto è una sfida risolta con design su misura e tecnologia al servizio degli obiettivi del cliente.</p>
  </div></div>
</section>
<section class="sec" style="padding-top:40px" data-pc="corner-l" data-screen="portfolio">
  <div class="wrap">
    <div class="filters rv" role="group" aria-label="Filtra i progetti">
      <button class="on" data-f="all">Tutti</button><button data-f="ai">AI</button><button data-f="piattaforme">Piattaforme</button><button data-f="ecommerce">E-commerce</button><button data-f="booking">Booking</button><button data-f="corporate">Siti aziendali</button>
    </div>
    <div class="port-grid three">{pf}</div>
  </div>
</section>
{cta('Il prossimo livello<br>potrebbe essere <span class="grad">il tuo</span>.')}
''' + footer()

# ================================================================== CONTATTI (stesso form EmailJS)
CONTACT_FAQ = [('Quanto tempo richiede realizzare un sito?', 'Dipende dalla complessità: un sito professionale di 5-6 pagine richiede in genere 3-4 settimane. Piattaforme più complesse, CRM o progetti con AI possono richiedere 6-10 settimane.'),
  ('Offri assistenza dopo la consegna?', 'Sì. Non ti lascio sola dopo il lancio: supporto post-consegna per fix e aggiornamenti, con possibilità di accordi continuativi per la manutenzione.'),
  ('Posso integrare l\'AI nel mio sito esistente?', 'Assolutamente sì. Agenti virtuali e funzionalità AI possono essere aggiunti a siti esistenti senza rifare tutto da zero.'),
  ('Posso pagare online o a rate?', 'Sì: puoi pagare online in modo sicuro con carta e, quando disponibile, anche in 3 rate. Trovi i dettagli nella pagina Pagamenti online.'),
  ('Lavori anche con clienti fuori Roma?', 'Certo. Lavoro da remoto con clienti in tutta Italia e all\'estero: le videochiamate sostituiscono perfettamente gli incontri in presenza.'),
  ('Il preventivo è gratuito?', 'Sì, il preventivo iniziale è gratuito e senza impegno. Ti mando una proposta dettagliata entro 48 ore dalla ricezione del brief.')]
FORM_JS = r'''<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
<script>
/* FORM PREVENTIVI — le richieste arrivano a contatto@ilariavisciglia.it */
const FORM_TO = 'contatto@ilariavisciglia.it';
/* EmailJS: conferma automatica al cliente + riserva se FormSubmit non risponde */
const EJS_SERVICE   = 'service_q85tkn6';
const EJS_TEMPLATE  = 'template_iu8dbft';
const EJS_TEMPLATE2 = 'template_40bt12h';
const EJS_KEY       = 'rtvzkUWVS33mOUt0R';
if (window.emailjs) emailjs.init({ publicKey: EJS_KEY });

document.querySelectorAll('.pill').forEach(function(p){
  p.addEventListener('click', function(){
    document.querySelectorAll('.pill').forEach(function(x){ x.classList.remove('active'); });
    p.classList.add('active');
    document.getElementById('f-budget').value = p.dataset.v;
  });
});
/* tipo progetto da link (es. contatti.html?tipo=CRM) */
(function(){ var t = new URLSearchParams(location.search).get('tipo'); if (!t) return;
  var s = document.getElementById('f-tipo'); [].forEach.call(s.options, function(o){ if (o.value.toLowerCase().indexOf(t.toLowerCase()) > -1) s.value = o.value; }); })();

document.getElementById('contact-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const nome      = document.getElementById('f-nome').value.trim();
  const cognome   = document.getElementById('f-cognome').value.trim();
  const email     = document.getElementById('f-email').value.trim();
  const tipo      = document.getElementById('f-tipo').value;
  const budget    = document.getElementById('f-budget').value;
  const messaggio = document.getElementById('f-messaggio').value.trim();
  const btn = document.getElementById('form-btn'), btnText = document.getElementById('btn-text'), spinner = document.getElementById('btn-spinner');
  btn.disabled = true; btnText.textContent = 'Invio in corso...'; spinner.style.display = 'inline-block';
  document.getElementById('form-ok').style.display = 'none';
  document.getElementById('form-err').style.display = 'none';
  try {
    /* 1) Richiesta a contatto@ilariavisciglia.it tramite FormSubmit (destinatario fissato qui nel codice) */
    let inviato = false;
    try {
      const r = await fetch('https://formsubmit.co/ajax/' + FORM_TO, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          _subject: 'Nuova richiesta di preventivo — ' + nome + ' ' + cognome,
          _template: 'table', _captcha: 'false', _replyto: email,
          Nome: nome + ' ' + cognome, Email: email, 'Tipo di progetto': tipo, Budget: budget, Messaggio: messaggio
        })
      });
      const j = await r.json().catch(function(){ return {}; });
      inviato = r.ok && String(j.success) !== 'false';
      if (!inviato) console.warn('FormSubmit:', j.message || r.status);
    } catch (e1) { console.warn('FormSubmit non raggiungibile:', e1); }
    /* 2) Riserva: EmailJS verso lo stesso indirizzo */
    if (!inviato) {
      if (!window.emailjs) throw new Error('Invio non riuscito');
      await emailjs.send(EJS_SERVICE, EJS_TEMPLATE, {
        from_name: `${nome} ${cognome}`, from_email: email, tipo_progetto: tipo, budget: budget, messaggio: messaggio, to_email: FORM_TO
      });
    }
    /* 3) Conferma automatica al cliente (se fallisce, la richiesta è comunque arrivata) */
    try {
      if (window.emailjs) await emailjs.send(EJS_SERVICE, EJS_TEMPLATE2, { from_name: nome, from_email: email, to_email: email, tipo_progetto: tipo, budget: budget });
    } catch (e2) { console.warn('Conferma al cliente non inviata:', e2); }
    document.getElementById('form-ok').style.display = 'block';
    this.reset();
    document.querySelectorAll('.pill').forEach(function(p){ p.classList.remove('active'); });
    document.getElementById('f-budget').value = 'Non specificato';
    document.getElementById('form-ok').scrollIntoView({ behavior: 'smooth', block: 'center' });
  } catch (err) {
    console.error('Errore invio form:', err);
    document.getElementById('form-err').style.display = 'block';
    document.getElementById('form-err').scrollIntoView({ behavior: 'smooth', block: 'center' });
  } finally {
    btn.disabled = false; btnText.textContent = 'Invia il messaggio →'; spinner.style.display = 'none';
  }
});
</script>'''
TIPI = ['Sito Web Nuovo', 'CRM / Gestionale / Dashboard', 'Integrazione AI / Agente Virtuale', 'E-commerce', 'Sistema di Booking / Prenotazioni', 'Piattaforma o Area Riservata', 'Restyling Sito Esistente', 'Strategia Digitale / SEO', 'Campagne Google & Meta Ads', 'Altro']
opts = ''.join(f'<option value="{t}">{t}</option>' for t in TIPI)
pills = ''.join(f'<button type="button" class="pill" data-v="{b}">{b}</button>' for b in ['< €1.000', '€1.000 – €3.000', '€3.000 – €6.000', '> €6.000', 'Da definire'])
pages['contatti.html'] = head(
  'Contatti | Preventivo Gratuito Web Designer Roma — Ilaria Visciglia',
  'Contatta Ilaria Visciglia, web designer freelance a Roma: preventivo gratuito per siti web, CRM, dashboard, e-commerce e agenti AI. Risposta entro 24 ore.',
  'contatti.html', [crumbs(('Home', ''), ('Contatti', 'contatti.html')), faq_ld(CONTACT_FAQ)]
) + header('contatti.html') + f'''
<section class="hero" style="align-items:flex-start" data-pc="corner-r" data-screen="mail">
  <div class="wrap">
    <span class="hud rv">Nuova partita · Contatti</span>
    <h1 class="rv d1" style="max-width:900px">Parliamo del <span class="grad">tuo progetto.</span></h1>
    <div class="contact-grid" style="margin-top:40px">
      <div class="rv d1 m-panel">
        <p class="lead">Che tu abbia un progetto definito o stia ancora esplorando le possibilità, scrivimi: analizziamo insieme le tue esigenze e costruiamo la soluzione più adatta.</p>
        <span class="avail">Disponibile per nuovi progetti — rispondo entro 24h</span>
        <div class="cmethods">
          <a class="cmethod" href="mailto:info@ilariavisciglia.it" data-hover-screen="mail"><span class="ico">{ico('mailc')}</span><span><strong>Email</strong><span>info@ilariavisciglia.it</span></span></a>
          <a class="cmethod" href="https://wa.me/393291489983" target="_blank" rel="noopener" data-hover-screen="ai"><span class="ico">{ico('wa')}</span><span><strong>WhatsApp</strong><span>+39 329 148 9983</span></span></a>
          <a class="cmethod" href="https://www.instagram.com/iladesign_web" target="_blank" rel="noopener"><span class="ico">{ico('ig')}</span><span><strong>Instagram</strong><span>@iladesign_web</span></span></a>
          <a class="cmethod" href="pagamenti.html" data-hover-screen="pay"><span class="ico">{ico('pay')}</span><span><strong>Pagamenti online</strong><span>Carta o in 3 rate con Klarna</span></span></a>
        </div>
      </div>
      <div class="panel corners rv d2">
        <h2 style="font-size:1.8rem;margin-bottom:20px">Raccontami il tuo <span class="grad">progetto</span></h2>
        <div class="fmsg ok" id="form-ok">✦ Messaggio inviato! Ti rispondo entro 24 ore lavorative. Nel frattempo puoi esplorare il <a href="portfolio.html" style="color:var(--cyan)">portfolio</a>.</div>
        <div class="fmsg err" id="form-err">✕ Ops, qualcosa è andato storto. Puoi scrivermi direttamente a <a href="mailto:contatto@ilariavisciglia.it" style="color:var(--cyan)">contatto@ilariavisciglia.it</a></div>
        <form id="contact-form" class="form">
          <div class="frow">
            <div class="field"><label for="f-nome">Nome *</label><input id="f-nome" type="text" required autocomplete="given-name"></div>
            <div class="field"><label for="f-cognome">Cognome *</label><input id="f-cognome" type="text" required autocomplete="family-name"></div>
          </div>
          <div class="field"><label for="f-email">Email *</label><input id="f-email" type="email" required autocomplete="email"></div>
          <div class="field"><label for="f-tipo">Tipo di progetto</label><select id="f-tipo"><option value="Non specificato">Seleziona una categoria...</option>{opts}</select></div>
          <div class="field"><label>Budget indicativo</label><div class="pills">{pills}</div><input type="hidden" id="f-budget" value="Non specificato"></div>
          <div class="field"><label for="f-messaggio">Descrivi il tuo progetto *</label><textarea id="f-messaggio" required></textarea></div>
          <button class="btn" id="form-btn" type="submit" data-hover-screen="mail"><span id="btn-text">Invia il messaggio →</span><span class="spin" id="btn-spinner"></span></button>
        </form>
      </div>
    </div>
  </div>
</section>
<section class="sec" data-pc="left" data-screen="ai">
  <div class="wrap"><div class="half r">
    <span class="hud pink rv">FAQ · Domande frequenti</span>
    <h2 class="rv">Hai domande? <span class="grad">Ho risposte.</span></h2>
    {faq_html(CONTACT_FAQ)}
  </div></div>
</section>
''' + footer(FORM_JS)

# ================================================================== PAGAMENTI
PAY_FAQ = [('Il pagamento online è sicuro?', 'Sì: il pagamento avviene sulla pagina protetta di Stripe, uno dei sistemi di pagamento più sicuri al mondo. I dati della carta non transitano mai da questo sito.'),
  ('Come funziona il pagamento in 3 rate con Klarna?', 'Inserisci l\'importo del preventivo, scegli Klarna come metodo di pagamento e segui i passaggi: l\'importo viene diviso in 3 rate, senza interessi se paghi alle scadenze. L\'approvazione dipende da Klarna.'),
  ('Posso pagare anche tutto subito?', 'Sì: nella stessa pagina di pagamento puoi scegliere carta, Apple Pay o Google Pay e saldare in un\'unica soluzione.'),
  ('Dove trovo l\'importo da pagare?', 'L\'importo è quello indicato nel preventivo o nella fattura che ti ho inviato. Se hai ricevuto un link di pagamento personale, usa direttamente quello.'),
  ('Riceverò la fattura?', 'Sì, dopo il pagamento ricevi la ricevuta via email e la fattura.')]
PAY_JS = r'''<script>
/* ============================================================
   PAGAMENTO: link di pagamento Stripe (account Ilaria Visciglia).
   Sulla pagina Stripe il cliente inserisce l'importo del preventivo
   e sceglie Klarna (3 rate), carta, Apple Pay o Google Pay.
   Per cambiare link basta sostituire l'indirizzo qui sotto.
   ============================================================ */
const PAY_LINKS = {
  klarna: 'https://buy.stripe.com/9B64gyelg1BmdNIfkg00001'   // PAGAMENTO — Stripe Payment Link
};
document.querySelectorAll('[data-pay]').forEach(function(b){
  var k = b.getAttribute('data-pay'), url = PAY_LINKS[k];
  if (url) { b.href = url; b.target = '_blank'; b.rel = 'noopener'; }
  else { b.href = 'mailto:info@ilariavisciglia.it?subject=' + encodeURIComponent('Richiesta link di pagamento — ' + b.getAttribute('data-name')); }
});
</script>'''
pages['pagamenti.html'] = head(
  'Pagamenti Online e in 3 Rate con Klarna | Ilaria Visciglia Web Designer Roma',
  'Paga online in modo sicuro i servizi di Ilaria Visciglia, web designer a Roma: in 3 rate con Klarna oppure con carta, Apple Pay e Google Pay.',
  'pagamenti.html', [crumbs(('Home', ''), ('Pagamenti', 'pagamenti.html')), faq_ld(PAY_FAQ)]
) + header('pagamenti.html') + f'''
<section class="hero" style="min-height:78vh" data-pc="hero" data-screen="pay">
  <div class="wrap"><div class="half m-panel">
    <span class="hud rv">Shop · Pagamenti online</span>
    <h1 class="rv d1" style="font-size:clamp(2.4rem,5.4vw,4.8rem)">Paga online, <span class="grad">anche in 3 rate.</span></h1>
    <p class="lead rv d2">Salda il tuo progetto in modo sicuro e dividilo in 3 rate con Klarna. Se preferisci, nella stessa pagina puoi pagare tutto subito con carta, Apple Pay o Google Pay.</p>
    <div class="btns rv d3"><a class="btn pink" data-pay="klarna" data-name="Klarna" href="contatti.html" data-hover-screen="pay">▶ Paga ora</a></div>
  </div></div>
</section>
<section class="sec" style="padding-top:30px" data-pc="corner-l" data-screen="pay">
  <div class="wrap">
    <div class="grid2">
      <div class="panel corners pay-card rv"><span class="hud pink">3 rate · senza interessi</span><span class="logo-pay">Klarna</span><p>Dividi l'importo del preventivo in 3 rate. Il pagamento avviene sulla pagina sicura di Stripe: scegli Klarna e segui i passaggi.</p><p>Preferisci saldare subito? Sulla stessa pagina trovi anche carta, Apple Pay e Google Pay.</p><a class="btn pink" data-pay="klarna" data-name="Klarna" href="contatti.html" data-hover-screen="pay">Paga con Klarna →</a></div>
      <div class="panel corners rv d1"><span class="hud">Come funziona</span>
        <div class="tl" style="margin-top:6px">
          <div class="tl-item" style="grid-template-columns:60px 1fr;padding:18px"><span class="y">01</span><div><h3>Clicca "Paga"</h3><p>Si apre la pagina di pagamento protetta di Stripe.</p></div></div>
          <div class="tl-item" style="grid-template-columns:60px 1fr;padding:18px"><span class="y">02</span><div><h3>Inserisci l'importo</h3><p>Scrivi la cifra indicata nel preventivo che hai ricevuto.</p></div></div>
          <div class="tl-item" style="grid-template-columns:60px 1fr;padding:18px"><span class="y">03</span><div><h3>Scegli Klarna o carta</h3><p>Conferma: ricevi subito la ricevuta via email.</p></div></div>
        </div>
      </div>
    </div>
    <p class="note rv">Il pagamento rateale è soggetto all'approvazione di Klarna. Hai ricevuto un link personale? Usa direttamente quello.</p>
  </div>
</section>
<section class="sec" data-pc="right" data-screen="pay">
  <div class="wrap"><div class="half">
    <span class="hud pink rv">FAQ · Pagamenti</span>
    <h2 class="rv">Domande sui <span class="grad">pagamenti</span></h2>
    {faq_html(PAY_FAQ)}
  </div></div>
</section>
''' + footer(PAY_JS)

# ================================================================== PAGINE SERVIZIO
for s in SERVICES:
    pups = ''.join(f'<div class="pup rv d{i % 3 + 1}"><h4>{t}</h4><p>{d}</p></div>' for i, (t, d) in enumerate(s['feats']))
    others = [o for o in SERVICES if o['slug'] != s['slug']][:3]
    if s['slug'] in ('agente-ai-email', 'agente-ai-whatsapp'):
        others = [SVC['agente-ai-whatsapp' if s['slug'] == 'agente-ai-email' else 'agente-ai-email'], SVC['dashboard'], SVC['siti-web']]
    oc = ''.join(srv_card(o, i) for i, o in enumerate(others))
    ld = [crumbs(('Home', ''), ('Servizi', 'servizi.html'), (s['name'], s['slug'] + '.html')), faq_ld(s['faqs']),
          {"@context": "https://schema.org", "@type": "Service", "name": s['name'], "description": s['desc'], "areaServed": "Roma, Italia",
           "provider": {"@type": "ProfessionalService", "name": "Ilaria Visciglia — Web Designer a Roma", "url": SITE}}]
    pages[s['slug'] + '.html'] = head(s['title'], s['desc'], s['slug'] + '.html', ld) + header('servizi.html') + f'''
<section class="hero" data-pc="hero" data-screen="{s['screen']}">
  <div class="wrap"><div class="half m-panel">
    <span class="hud rv"><a href="servizi.html">Servizi</a> · {s['code']}</span>
    <h1 class="rv d1" style="font-size:clamp(2.2rem,4.6vw,4rem)">{s['h1']}</h1>
    <p class="lead rv d2">{s['intro']}</p>
    <div class="btns rv d3"><a class="btn" href="contatti.html" data-hover-screen="start">▶ Richiedi un preventivo</a><a class="btn ghost" href="portfolio.html" data-hover-screen="portfolio">Guarda il portfolio</a></div>
  </div></div>
</section>
<section class="sec" data-pc="left" data-screen="{s['screen']}">
  <div class="wrap"><div class="half r m-panel">
    <span class="hud pink rv">Come funziona</span>
    <h2 class="rv">{s['name']} <span class="grad">a Roma</span> e in tutta Italia</h2>
    <p class="rv">{s['how'][0]}</p>
    <p class="rv">{s['how'][1]}</p>
    <p class="for rv mono" style="margin-top:20px;font-size:14px;color:var(--muted)">PER CHI È → <b style="color:var(--lime);font-weight:500">{s['forwho']}</b></p>
  </div></div>
</section>
<section class="sec" data-pc="corner-r" data-screen="{s['screen']}">
  <div class="wrap">
    <span class="hud rv">Power-up inclusi</span>
    <h2 class="rv">Cosa <span class="grad">ottieni</span></h2>
    <div class="pups">{pups}</div>
  </div>
</section>
<section class="sec" data-pc="right" data-screen="{s['screen']}">
  <div class="wrap"><div class="half">
    <span class="hud pink rv">FAQ</span>
    <h2 class="rv">Quello che ti stai <span class="grad">chiedendo</span></h2>
    {faq_html(s['faqs'])}
  </div></div>
</section>
<section class="sec tight" data-pc="corner-l" data-screen="crm">
  <div class="wrap">
    <span class="hud rv">Altri moduli</span>
    <h2 class="rv">Potrebbero interessarti <span class="grad">anche</span></h2>
    <div class="srv-grid">{oc}</div>
  </div>
</section>
{cta('Hai un progetto?<br><span class="grad">Parliamone adesso.</span>')}
''' + footer()

# ------------------------------------------------------------------ scrittura
for name, html in pages.items():
    with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
        f.write(html)

order = ['', 'servizi.html', 'siti-web.html', 'dashboard.html', 'ecommerce.html', 'agente-ai-email.html', 'agente-ai-whatsapp.html',
         'strategia-digitale.html', 'campagne-adv.html', 'portfolio.html', 'chi-sono.html', 'contatti.html', 'pagamenti.html']
prio = {'': '1.0', 'servizi.html': '0.9', 'portfolio.html': '0.8', 'chi-sono.html': '0.7', 'contatti.html': '0.7', 'pagamenti.html': '0.4'}
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in order:
    sm += f'  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{prio.get(u, "0.9")}</priority>\n  </url>\n'
sm += '</urlset>\n'
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sm)
print('OK', len(pages), 'pagine')
