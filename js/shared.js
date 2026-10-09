/* ═══════════════════════════════════════════
   ILARIA VISCIGLIA — SHARED JS
═══════════════════════════════════════════ */

/* ── CURSOR ── */
const cursor = document.getElementById('cursor');
const ring = document.getElementById('cursor-ring');
let mx = 0, my = 0, rx = 0, ry = 0;
document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cursor.style.left = mx + 'px'; cursor.style.top = my + 'px';
});
function animRing() {
  rx += (mx - rx) * 0.12; ry += (my - ry) * 0.12;
  ring.style.left = rx + 'px'; ring.style.top = ry + 'px';
  requestAnimationFrame(animRing);
}
animRing();
document.querySelectorAll('a, button, input, textarea, select, .srv, .port-card, .work-item, .contact-method').forEach(el => {
  el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
  el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
});

/* ── NAV ── */
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
hamburger?.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  navMenu.classList.toggle('open');
});
navMenu?.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    hamburger.classList.remove('open');
    navMenu.classList.remove('open');
  });
});

/* ── SCROLL REVEAL ── */
const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.08 });
document.querySelectorAll('.reveal, .reveal-l, .reveal-r').forEach(el => revealObserver.observe(el));

/* ── AI AGENT ── */
const SYSTEM_PROMPT = `Sei l'assistente virtuale di Ilaria Visciglia, web designer specializzata in siti interattivi e integrazione AI.

Chi è Ilaria:
- 5 anni di esperienza in web design interattivo e innovativo
- Diploma in grafica pubblicitaria + Master in Web Design (in corso)
- Specializzata in: siti dinamici fuori dalla norma, integrazione AI, agenti virtuali, piattaforme per lavoratori
- Basata a Roma, Italia
- Mission: rendere le aziende vive nel tempo con una presenza digitale continua e di qualità
- Vision: tenere i clienti sempre un passo avanti alla concorrenza

Servizi offerti:
1. Web Design Interattivo — animazioni, microinterazioni, layout fuori dalla norma
2. Integrazione AI e Agenti Virtuali — GPT-4, Claude, DALL-E 3 nei siti web
3. Piattaforme e Dashboard per lavoratori — registrazione, profili, marketplace
4. Sistemi di Booking — calendario sync Airbnb/Google, Stripe, email automatiche
5. E-commerce e Configuratori Interattivi
6. Strategia Digitale — SEO, Google Ads, tracking conversioni

Portfolio completo:
- logovex.com → generatore loghi AI con DALL-E 3 + pagamento Stripe
- emifotoottica.it → ottica con prova virtuale occhiali in realtà aumentata (AR)
- fashionharp.com → piattaforma moda con registrazione utenti, dashboard Supabase
- laperlanera.eu → casa vacanza Roma: booking personalizzato + sincronizzazione Airbnb in tempo reale
- laboratoriwrapping.it → car wrapping con configuratore automatico in sviluppo
- gfmentalcoach.it → sito per mental coach equestre
- consorzioserviziesvilupporoma.it → consorzio servizi Roma
- emiliofranchini.it → sito professionale

Per domande su prezzi: variano in base al progetto e alle funzionalità richieste. Invita sempre a contattare Ilaria via form o email per un preventivo personalizzato. Non inventare prezzi.

Tono: professionale, cordiale, diretto. Rispondi sempre in italiano a meno che l'utente non scriva in un'altra lingua.`;

const bubble = document.getElementById('agent-bubble');
const panel = document.getElementById('agent-panel');
const agentClose = document.getElementById('agent-close');
const agentInput = document.getElementById('agent-input');
const agentSend = document.getElementById('agent-send');
const agentMsgs = document.getElementById('agent-messages');

bubble?.addEventListener('click', () => {
  panel.classList.toggle('open');
  if (panel.classList.contains('open')) agentInput?.focus();
});
agentClose?.addEventListener('click', () => panel.classList.remove('open'));
agentSend?.addEventListener('click', sendAgentMsg);
agentInput?.addEventListener('keydown', e => { if (e.key === 'Enter') sendAgentMsg(); });

let agentHistory = [];

function appendAgentMsg(text, role) {
  const d = document.createElement('div');
  d.className = 'amsg ' + role;
  d.textContent = text;
  agentMsgs.appendChild(d);
  agentMsgs.scrollTop = agentMsgs.scrollHeight;
  return d;
}

async function sendAgentMsg() {
  const text = agentInput.value.trim();
  if (!text) return;
  agentInput.value = '';
  appendAgentMsg(text, 'user');
  agentHistory.push({ role: 'user', content: text });
  const typing = appendAgentMsg('...', 'bot typing');
  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'x-api-key': 'sk-ant-TUA_CHIAVE_QUI',
        // 'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 500,
        system: SYSTEM_PROMPT,
        messages: agentHistory
      })
    });
    const data = await res.json();
    const reply = data.content?.[0]?.text || 'Mi dispiace, si è verificato un errore. Riprova!';
    typing.textContent = reply;
    typing.classList.remove('typing');
    agentHistory.push({ role: 'assistant', content: reply });
  } catch {
    typing.textContent = 'Problema di connessione. Contatta Ilaria direttamente dalla pagina Contatti!';
    typing.classList.remove('typing');
  }
  agentMsgs.scrollTop = agentMsgs.scrollHeight;
}
