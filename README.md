# Ilaria Visciglia — Sito WOW Edition 🔥

## Funzionalità Speciali

- **Cursore custom** dorato con ring animato
- **Preloader cinematico** con contatore
- **Particle field interattivo** sul background dell'hero (reagisce al mouse)
- **Big typography** decorativa
- **Marquee animato** con tecnologie
- **Bento grid portfolio** con hover effects
- **Scroll reveal** su tutti gli elementi
- **Agente AI** in basso a destra
- **Noise texture overlay** per profondità
- **Form di contatto** integrato nella pagina

## Setup API Key Agente

Nel file `index.html`, cerca:
```javascript
headers: { 'Content-Type': 'application/json' },
```
E aggiungi:
```javascript
headers: {
  'Content-Type': 'application/json',
  'x-api-key': 'sk-ant-TUA_CHIAVE',
  'anthropic-version': '2023-06-01'
},
```

## Come aprire in locale

```bash
# Python
python -m http.server 8080

# Node.js
npx serve .
```

Poi vai su: http://localhost:8080

## Email Form

Per ricevere le email dal form, aggiungi Formspree:
- Registrati su formspree.io
- Sostituisci la riga `<form class="cta-form"` con:
  `<form action="https://formspree.io/f/TUOCODICE" method="POST">`
- Rimuovi lo script del form (document.getElementById('cta-form').addEventListener)
