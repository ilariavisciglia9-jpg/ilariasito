/* ================================================================
   ILARIA VISCIGLIA — JS comune (incorporato in ogni pagina)
   - boot loader, header + barra XP, menu mobile
   - comparsa allo scroll, testo che si digita, card che si muovono
   - PC 3D (Three.js) che segue lo scroll e reagisce a mouse / touch
   - assistente AI
   ================================================================ */
(function(){
'use strict';
var doc=document, root=doc.documentElement, W=window;
var reduce=W.matchMedia('(prefers-reduced-motion: reduce)').matches;
var coarse=W.matchMedia('(hover: none)').matches;

/* ---------- BOOT (solo alla prima visita della sessione) ---------- */
var boot=doc.getElementById('boot');
if(boot){
  var seen=false; try{seen=sessionStorage.getItem('iv-boot')==='1';sessionStorage.setItem('iv-boot','1');}catch(e){}
  if(seen||reduce){boot.classList.add('off');}
  else{
    var bi=boot.querySelector('.boot-bar i'),bp=0;
    var bt=setInterval(function(){bp=Math.min(100,bp+18+Math.random()*22);bi.style.width=bp+'%';if(bp>=100){clearInterval(bt);setTimeout(function(){boot.classList.add('off');},120);}},60);
    setTimeout(function(){boot.classList.add('off');},900);
  }
}

/* ---------- HEADER + XP ---------- */
var hdr=doc.querySelector('.hdr'),xp=doc.querySelector('.xp i'),xpb=doc.querySelector('.xp b');
var maxScroll=0;function measureMax(){maxScroll=root.scrollHeight-W.innerHeight;}
W.addEventListener('resize',measureMax);W.addEventListener('load',measureMax);measureMax();
function onScrollUI(){
  var y=W.scrollY,max=maxScroll;
  if(hdr) hdr.classList.toggle('scrolled',y>30);
  var p=max>0?Math.min(1,y/max):0;
  if(xp) xp.style.width=(p*100)+'%';
  if(xpb) xpb.textContent='XP '+Math.round(p*100)+'%';
}
var uiTick=false;W.addEventListener('scroll',function(){if(uiTick)return;uiTick=true;requestAnimationFrame(function(){uiTick=false;onScrollUI();scrollTilt();});},{passive:true});requestAnimationFrame(onScrollUI);

/* ---------- MENU MOBILE ---------- */
var burger=doc.querySelector('.burger');
if(burger){
  burger.addEventListener('click',function(){var o=doc.body.classList.toggle('menu-open');burger.setAttribute('aria-expanded',o?'true':'false');});
  doc.querySelectorAll('.mmenu a').forEach(function(a){a.addEventListener('click',function(){doc.body.classList.remove('menu-open');});});
}

/* ---------- REVEAL ---------- */
if('IntersectionObserver' in W){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}});},{threshold:.12});
  doc.querySelectorAll('.rv').forEach(function(el){io.observe(el);});
}else{doc.querySelectorAll('.rv').forEach(function(el){el.classList.add('visible');});}

/* ---------- TESTO CHE SI DIGITA ---------- */
doc.querySelectorAll('[data-words]').forEach(function(el){
  var words; try{words=JSON.parse(el.getAttribute('data-words'));}catch(e){return;}
  var out=el.querySelector('.tw'),wi=0,ci=0,del=false;
  if(reduce){out.textContent=words[0];return;}
  (function tick(){
    var w=words[wi];
    ci+=del?-1:1; out.textContent=w.slice(0,ci);
    var t=del?35:70;
    if(!del&&ci===w.length){del=true;t=1500;}
    else if(del&&ci===0){del=false;wi=(wi+1)%words.length;t=300;}
    setTimeout(tick,t);
  })();
});

/* ---------- CARD CHE SI MUOVONO (tilt 3D) ---------- */
var tilts=[].slice.call(doc.querySelectorAll('.tilt'));
tilts.forEach(function(el){
  var host=el.closest('.pitem')||el;
  host.addEventListener('pointermove',function(e){
    if(e.pointerType==='touch') return;
    var r=el.getBoundingClientRect(),px=(e.clientX-r.left)/r.width-.5,py=(e.clientY-r.top)/r.height-.5;
    el.classList.add('live');
    el.style.setProperty('--rx',(-py*14).toFixed(2)+'deg');
    el.style.setProperty('--ry',(px*16).toFixed(2)+'deg');
    el.style.setProperty('--mx',((px+.5)*100).toFixed(1)+'%');
    el.style.setProperty('--my',((py+.5)*100).toFixed(1)+'%');
  });
  host.addEventListener('pointerleave',function(){el.classList.remove('live');el.style.setProperty('--rx','0deg');el.style.setProperty('--ry','0deg');});
});
/* su mobile le card si inclinano mentre scrolli */
function scrollTilt(){
  if(!coarse||reduce) return;
  var vh=W.innerHeight;
  var rs=tilts.map(function(el){return el.getBoundingClientRect();}); /* prima tutte le letture… */
  tilts.forEach(function(el,i){ /* …poi tutte le scritture */
    var r=rs[i]; if(r.bottom<0||r.top>vh) return;
    var c=(r.top+r.height/2-vh/2)/(vh/2);
    el.style.setProperty('--rx',(c*10).toFixed(2)+'deg');
    el.style.setProperty('--ry',(Math.sin((r.top/vh)*Math.PI)*6).toFixed(2)+'deg');
  });
}
requestAnimationFrame(scrollTilt);
/* luce che segue il mouse sulle card servizi */
doc.querySelectorAll('.srv').forEach(function(el){
  el.addEventListener('pointermove',function(e){var r=el.getBoundingClientRect();el.style.setProperty('--mx',(e.clientX-r.left)+'px');el.style.setProperty('--my',(e.clientY-r.top)+'px');});
});

/* ---------- FILTRI PORTFOLIO ---------- */
var fl=doc.querySelector('.filters');
if(fl){
  fl.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    fl.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);});
    var f=b.getAttribute('data-f');
    doc.querySelectorAll('.pitem[data-cat]').forEach(function(it){
      it.classList.toggle('hide',f!=='all'&&(' '+it.getAttribute('data-cat')+' ').indexOf(' '+f+' ')<0);
    });
    W.dispatchEvent(new Event('scroll'));
  });
}
/* immagini portfolio: se lo screenshot non carica, resta il segnaposto */
doc.querySelectorAll('.shot img').forEach(function(img){
  function bad(){img.classList.add('err');}
  img.addEventListener('error',bad);
  if(img.complete&&img.naturalWidth===0) bad();
});

/* ================================================================
   PC 3D — Three.js
   Ogni <section data-pc="right|left|center|corner-r|corner-l" data-screen="...">
   decide dove va il computer e cosa mostra lo schermo.
   ================================================================ */
function initPC(){
  var canvas=doc.getElementById('pc3d');
  if(!canvas) return;
  if(!W.THREE){canvas.remove();return;}
  var T=W.THREE,renderer;
  try{renderer=new T.WebGLRenderer({canvas:canvas,antialias:!coarse,alpha:true,powerPreference:'high-performance'});}
  catch(e){canvas.remove();return;}
  renderer.setPixelRatio(Math.min(W.devicePixelRatio||1,coarse?1.25:1.75));
  renderer.setClearColor(0x000000,0);

  var scene=new T.Scene();
  var cam=new T.PerspectiveCamera(35,1,.1,100); cam.position.set(0,0,10);

  scene.add(new T.AmbientLight(0x7c8cff,.55));
  var lc=new T.PointLight(0x38f2ff,1.6,40); lc.position.set(-5,3,6); scene.add(lc);
  var lp=new T.PointLight(0xff3fd1,1.3,40); lp.position.set(5,-2,5); scene.add(lp);
  var dl=new T.DirectionalLight(0xffffff,.7); dl.position.set(2,5,8); scene.add(dl);

  var pc=new T.Group(); scene.add(pc);
  var body=new T.MeshStandardMaterial({color:0x161b2e,metalness:.55,roughness:.38});
  var body2=new T.MeshStandardMaterial({color:0x0f1322,metalness:.4,roughness:.5});
  var edge=new T.LineBasicMaterial({color:0x38f2ff,transparent:true,opacity:.65});
  function box(w,h,d,mat,x,y,z,parent,noEdge){
    var m=new T.Mesh(new T.BoxGeometry(w,h,d),mat); m.position.set(x,y,z);
    if(!noEdge) m.add(new T.LineSegments(new T.EdgesGeometry(m.geometry),edge));
    (parent||pc).add(m); return m;
  }
  /* monitor */
  var mon=new T.Group(); mon.position.y=.55; pc.add(mon);
  box(3.4,2.2,.18,body,0,0,0,mon);
  box(2.3,1.45,.36,body2,0,-.05,-.25,mon);
  var led=new T.Mesh(new T.BoxGeometry(.08,.03,.02),new T.MeshBasicMaterial({color:0xb8ff3c})); led.position.set(1.45,-1.02,.1); mon.add(led);
  /* schermo con texture disegnata in canvas */
  var sc=doc.createElement('canvas'); sc.width=640; sc.height=400;
  var g=sc.getContext('2d');
  var tex=new T.CanvasTexture(sc); if(T.sRGBEncoding) tex.encoding=T.sRGBEncoding;
  var scr=new T.Mesh(new T.PlaneGeometry(3.12,1.95),new T.MeshBasicMaterial({map:tex,toneMapped:false}));
  scr.position.z=.092; mon.add(scr);
  var glow=new T.Mesh(new T.PlaneGeometry(3.9,2.6),new T.MeshBasicMaterial({color:0x38f2ff,transparent:true,opacity:.08,depthWrite:false}));
  glow.position.z=-.5; mon.add(glow);
  /* piede */
  box(.3,.7,.2,body,0,-.95,-.12);
  box(1.5,.08,.85,body,0,-1.32,-.05);
  /* tastiera con tasti che si illuminano */
  var kb=new T.Group(); kb.position.set(0,-1.34,1.35); kb.rotation.x=.1; pc.add(kb);
  box(3,.09,1,body,0,0,0,kb);
  var keys=[],kg=new T.BoxGeometry(.19,.07,.19);
  for(var r=0;r<4;r++)for(var c=0;c<12;c++){
    var km=new T.MeshStandardMaterial({color:0x232b48,emissive:0x000000,metalness:.3,roughness:.6});
    var k=new T.Mesh(kg,km); k.position.set(-1.21+c*.22,.075,-.33+r*.22); kb.add(k); keys.push({m:k,mat:km,t:0});
  }
  box(1.2,.07,.19,body2,0,.075,.55,kb,true);
  /* mouse */
  box(.26,.09,.4,body,1.95,-1.32,1.4);

  /* oggetti che fluttuano (voxel / wireframe) */
  var floaters=[],cols=[0x38f2ff,0xff3fd1,0xb8ff3c,0xffc23d];
  var geos=[new T.BoxGeometry(.32,.32,.32),new T.OctahedronGeometry(.28),new T.TetrahedronGeometry(.3),new T.TorusGeometry(.22,.06,8,20)];
  var nF=W.innerWidth<860?10:20;
  for(var i=0;i<nF;i++){
    var col=cols[i%cols.length],wire=i%3===0;
    var mat=wire?new T.MeshBasicMaterial({color:col,wireframe:true,transparent:true,opacity:.55})
                :new T.MeshStandardMaterial({color:col,emissive:col,emissiveIntensity:.35,metalness:.3,roughness:.4});
    var f=new T.Mesh(geos[i%geos.length],mat);
    var ang=Math.random()*Math.PI*2,rad=4+Math.random()*4;
    f.userData={x:Math.cos(ang)*rad*1.4,y:(Math.random()-.5)*10,z:-2-Math.random()*6,s:.5+Math.random()*1.1,
      rx:(Math.random()-.5)*.02,ry:(Math.random()-.5)*.02,ph:Math.random()*6,depth:.4+Math.random()*1.2};
    f.scale.setScalar(f.userData.s); scene.add(f); floaters.push(f);
  }

  /* ---------- schermo: modalità ---------- */
  var C={bg:'#060914',cyan:'#38f2ff',pink:'#ff3fd1',lime:'#b8ff3c',amber:'#ffc23d',txt:'#e8eeff',dim:'#56628a'};
  var mode='boot',modeT=0,hoverMode=null,hoverUntil=0;
  var TITLES={boot:'ilaria_os.exe',about:'player_1.sav',mission:'mission.txt',crm:'crm_clienti.app',dash:'dashboard.app',ai:'agente_ai.bot',
    code:'sito_web.html',shop:'ecommerce.shop',portfolio:'portfolio.lvl',start:'press_start',seo:'seo_google.log',ads:'campagne_ads.app',pay:'pagamenti.app',mail:'email_ai.bot'};
  var code=['<section class="hero">','  <h1>Soluzioni digitali</h1>','  <p>per aziende e agenzie</p>','</section>','const crm = new CRM({','  clienti: true, dashboard: true','});','await agenteAI.rispondi(msg);','stripe.checkout({ rate: 3 });','export default sitoSuMisura;'];
  function rr(x,y,w,h,r,fill){g.beginPath();g.moveTo(x+r,y);g.arcTo(x+w,y,x+w,y+h,r);g.arcTo(x+w,y+h,x,y+h,r);g.arcTo(x,y+h,x,y,r);g.arcTo(x,y,x+w,y,r);g.closePath();g.fillStyle=fill;g.fill();}
  function txt(s,x,y,size,col,font){g.font=(font||'600 ')+size+'px "JetBrains Mono",monospace';g.fillStyle=col;g.fillText(s,x,y);}
  function drawScreen(t){
    var m=(hoverMode&&t<hoverUntil)?hoverMode:mode;
    var lt=(t-modeT)/1000;
    g.fillStyle=C.bg;g.fillRect(0,0,640,400);
    /* barra finestra */
    g.fillStyle='#0e1428';g.fillRect(0,0,640,34);
    ['#ff5f57','#febc2e','#28c840'].forEach(function(c,i){g.beginPath();g.arc(20+i*20,17,6,0,7);g.fillStyle=c;g.fill();});
    txt(TITLES[m]||m,90,22,14,C.dim);
    txt(new Date().toTimeString().slice(0,5),580,22,13,C.dim);
    var k=t/1000;
    if(m==='boot'){
      txt('ILARIA_OS  v.2026',30,80,26,C.cyan,'700 ');
      txt('> soluzioni digitali per aziende',30,125,17,C.txt);
      txt('> CRM · dashboard · siti · agenti AI',30,155,17,C.txt);
      txt('> web designer · Roma',30,185,17,C.lime);
      var p=Math.min(1,lt/2.2);g.strokeStyle=C.cyan;g.lineWidth=2;g.strokeRect(30,230,580,26);
      for(var i=0;i<Math.floor(p*36);i++){g.fillStyle=i%2?C.cyan:'#2bc6d1';g.fillRect(34+i*16,234,13,18);}
      txt(p<1?'caricamento '+Math.round(p*100)+'%':'pronta. premi START ▶',30,295,16,p<1?C.dim:C.pink);
    }else if(m==='about'){
      rr(30,60,150,150,16,'#141c38');g.fillStyle=C.cyan;g.font='700 64px "Chakra Petch",sans-serif';g.fillText('IV',60,160);
      txt('NOME   Ilaria Visciglia',210,85,17,C.txt);txt('CLASSE Web Designer & Dev',210,115,17,C.txt);txt('BASE   Roma, Italia',210,145,17,C.txt);txt('LIVELLO 5+ anni',210,175,17,C.lime);
      [['DESIGN',.95,C.cyan],['CODICE',.9,C.pink],['AI',.88,C.lime],['STRATEGIA',.8,C.amber]].forEach(function(s,i){
        var y=245+i*34; txt(s[0],30,y+14,14,C.dim); g.strokeStyle='#2a3561';g.strokeRect(160,y,440,18);
        var w=Math.min(s[1],lt*.6+i*.02)*436;g.fillStyle=s[2];g.fillRect(162,y+2,Math.max(0,w),14);
      });
    }else if(m==='mission'){
      txt('MISSION',30,90,30,C.pink,'700 ');
      var lines=['Rendere le aziende vive nel tempo:','rendimento continuo, presenza online','che si distingue e tecnologia che','lavora per loro 24 ore su 24.'];
      var chars=Math.floor(lt*40),used=0;
      lines.forEach(function(l,i){var s=l.slice(0,Math.max(0,chars-used));used+=l.length;txt(s,30,150+i*36,19,C.txt);});
      if(Math.floor(k*2)%2) {g.fillStyle=C.lime;g.fillRect(30,300,12,20);}
    }else if(m==='crm'){
      txt('CLIENTI',30,72,20,C.cyan,'700 ');rr(470,52,140,28,8,'#13204a');txt('+ nuovo',500,72,14,C.cyan);
      var rows=[['Studio Rossi','attivo',C.lime],['B&B Roma','preventivo',C.amber],['Agenzia Nova','attivo',C.lime],['Ottica Emi','follow-up',C.pink],['Hotel Sole','attivo',C.lime]];
      var hl=Math.floor(k*1.2)%rows.length;
      rows.forEach(function(r,i){var y=100+i*52; if(i===hl) rr(24,y-6,592,44,8,'#142048');
        g.beginPath();g.arc(48,y+16,12,0,7);g.fillStyle=['#38f2ff','#ff3fd1','#b8ff3c','#ffc23d','#8b7cff'][i];g.fill();
        txt(r[0],72,y+22,17,C.txt);txt('€ '+(1200+i*730),300,y+22,16,C.dim);
        rr(450,y+2,130,26,13,'rgba(255,255,255,.06)');txt(r[1],465,y+21,14,r[2]);});
    }else if(m==='dash'||m==='ads'){
      var kp=m==='ads'?[['CLICK','8.2k'],['CPC','€0,41'],['LEAD','+212']]:[['VENDITE','€48k'],['ORDINI','1.284'],['CRESCITA','+32%']];
      kp.forEach(function(x,i){rr(24+i*204,50,192,74,10,'#111a38');txt(x[0],40+i*204,78,13,C.dim);txt(x[1],40+i*204,110,26,[C.cyan,C.pink,C.lime][i],'700 ');});
      for(var b=0;b<12;b++){var h=40+Math.abs(Math.sin(k*1.4+b*.7))*130;g.fillStyle=b%3===0?C.pink:C.cyan;g.globalAlpha=.85;g.fillRect(40+b*48,370-h,30,h);}
      g.globalAlpha=1;g.strokeStyle=C.lime;g.lineWidth=3;g.beginPath();
      for(var j=0;j<=12;j++){var yy=300-Math.sin(k+j*.6)*30-j*8;j?g.lineTo(40+j*48,yy):g.moveTo(40,yy);} g.stroke();
    }else if(m==='ai'||m==='mail'){
      var msgs=m==='mail'?[['user','Avete disponibilità sabato?'],['bot','Sì! Sabato dalle 9 alle 13. Prenoto?'],['user','Perfetto, grazie'],['bot','Fatto ✓ Riceverai una conferma.']]
        :[['user','Ciao, siete aperti domenica?'],['bot','Ciao! Domenica 10-18. Vuoi prenotare?'],['user','Sì, per 2 persone'],['bot','Prenotato ✓ A domenica!']];
      var n=Math.min(msgs.length,Math.floor(lt/1.1)+1);
      for(var q=0;q<n;q++){var mm=msgs[q],y2=60+q*76,isB=mm[0]==='bot';g.font='500 17px "JetBrains Mono",monospace';var w2=g.measureText(mm[1]).width+36;
        rr(isB?24:616-w2,y2,w2,52,14,isB?'#13244a':C.cyan);txt(mm[1],(isB?24:616-w2)+18,y2+32,17,isB?C.txt:'#04050a','500 ');}
      if(n<msgs.length&&Math.floor(k*3)%2){txt('sta scrivendo…',30,380,14,C.dim);}
      if(lt>6) modeT=performance.now();
    }else if(m==='code'){
      var off=Math.floor(k*1.5)%code.length;
      for(var l2=0;l2<9;l2++){var line=code[(l2+off)%code.length];txt(String(l2+1).padStart(2,'0'),24,72+l2*36,15,C.dim);
        var cc=/^const|^await|^export|^stripe/.test(line)?C.pink:/</.test(line)?C.cyan:C.txt;txt(line,70,72+l2*36,17,cc);}
      if(Math.floor(k*2)%2){g.fillStyle=C.lime;g.fillRect(70,72+8*36-16,10,20);}
    }else if(m==='shop'||m==='pay'){
      if(m==='pay'){
        rr(40,70,300,180,18,'#1a2350');txt('CARTA',64,110,16,C.dim);txt('•••• 4242',64,170,26,C.txt,'700 ');txt('IV CLIENT',64,220,15,C.dim);
        txt('PAGA IN 3 RATE',370,110,18,C.lime,'700 ');
        ['Klarna · 3 rate','Carta','Apple / Google Pay'].forEach(function(s,i){rr(370,130+i*52,240,40,10,i===Math.floor(k)%3?'#1d3a6b':'#111a38');txt(s,388,156+i*52,16,C.txt);});
        txt('✓ pagamento sicuro',40,300,17,C.lime);
      }else{
        for(var p2=0;p2<6;p2++){var x=24+(p2%3)*204,y3=50+Math.floor(p2/3)*170;rr(x,y3,192,156,12,'#111a38');
          rr(x+12,y3+12,168,90,8,['#38f2ff','#ff3fd1','#b8ff3c','#ffc23d','#8b7cff','#38f2ff'][p2]);g.globalAlpha=.25;g.fillStyle='#000';g.fillRect(x+12,y3+12,168,90);g.globalAlpha=1;
          txt('prodotto '+(p2+1),x+14,y3+126,14,C.txt);txt('€ '+(19+p2*10),x+14,y3+146,14,C.lime);}
        rr(530,8,90,22,11,C.pink);txt('🛒 '+(1+Math.floor(k)%9),548,24,13,'#04050a');
      }
    }else if(m==='portfolio'){
      var sites=['logovex.com','inpostsocial.com','fashionharp.com','laperlanera.eu'];var s2=sites[Math.floor(k/2)%sites.length];
      rr(24,48,592,30,8,'#111a38');txt('https://'+s2,40,69,15,C.cyan);
      rr(24,92,592,290,10,'#0d1430');
      txt('LIVELLO COMPLETATO',150,180,26,C.lime,'700 ');txt(s2,150+((290-s2.length*9)/2),225,22,C.txt);
      for(var st=0;st<3;st++){g.fillStyle=C.amber;g.font='38px sans-serif';g.fillText('★',230+st*50,300);}
    }else if(m==='seo'){
      rr(40,60,560,52,26,'#111a38');txt('web designer roma',70,93,19,C.txt);g.fillStyle=C.cyan;g.beginPath();g.arc(565,86,12,0,7);g.fill();
      ['ilariavisciglia.it — Web Designer a Roma','risultato 2','risultato 3'].forEach(function(s,i){var y4=150+i*70;rr(40,y4,560,56,10,i?'#0d1430':'#15306a');txt((i+1)+'.',58,y4+35,18,i?C.dim:C.lime,'700 ');txt(s,90,y4+35,16,i?C.dim:C.txt);});
    }else if(m==='start'){
      g.fillStyle=C.cyan;g.font='700 54px "Chakra Petch",sans-serif';var tw='GAME ON';g.fillText(tw,320-g.measureText(tw).width/2,170);
      if(Math.floor(k*2)%2){g.font='20px "Press Start 2P",monospace';g.fillStyle=C.lime;var ps='PRESS START';g.fillText(ps,320-g.measureText(ps).width/2,250);}
      txt('info@ilariavisciglia.it',190,330,18,C.pink);
    }
    /* scanline sullo schermo */
    g.globalAlpha=.08;g.fillStyle='#000';for(var s3=34;s3<400;s3+=3)g.fillRect(0,s3,640,1);g.globalAlpha=1;
    tex.needsUpdate=true;
  }

  /* ---------- posizioni ---------- */
  var secs=[].slice.call(doc.querySelectorAll('[data-pc]'));
  var cur={x:3,y:0,s:.8,ry:0},tgt={x:3,y:0,s:.8,ry:0},spin=0,spinT=0,side='right';
  var mouse={x:0,y:0,tx:0,ty:0},energy=0,lastY=W.scrollY;
  function visW(){var h=2*cam.position.z*Math.tan(cam.fov*Math.PI/360);return{w:h*cam.aspect,h:h};}
  function place(kind){
    var v=visW(),mob=W.innerWidth<860,o;
    if(mob){
      switch(kind){
        case 'left':o={x:-v.w*.2,y:v.h*.27,s:.36,ry:.5};break;
        case 'right':o={x:v.w*.2,y:v.h*.27,s:.36,ry:-.5};break;
        case 'center':o={x:0,y:v.h*.22,s:.4,ry:0};break;
        case 'corner-l':o={x:-v.w*.28,y:v.h*.34,s:.24,ry:.6};break;
        case 'hero':o={x:0,y:v.h*.21,s:.48,ry:-.25};break;
        default:o={x:v.w*.28,y:v.h*.34,s:.24,ry:-.6};
      }
    }else{
      var sc2=Math.min(1,v.w/14);
      switch(kind){
        case 'left':o={x:-v.w*.29,y:-.1,s:.82*sc2,ry:.45};break;
        case 'right':o={x:v.w*.29,y:-.1,s:.82*sc2,ry:-.45};break;
        case 'hero':o={x:v.w*.31,y:-.1,s:.9*sc2,ry:-.38};break;
        case 'center':o={x:0,y:v.h*.19,s:.6*sc2,ry:0};break;
        case 'corner-l':o={x:-v.w*.38,y:v.h*.2,s:.42*sc2,ry:.5};break;
        default:o={x:v.w*.38,y:v.h*.2,s:.42*sc2,ry:-.5};
      }
    }
    return o;
  }
  var activeSec=null;
  function pickSection(){
    var mid=W.innerHeight*.5,best=null;
    for(var i=0;i<secs.length;i++){var r=secs[i].getBoundingClientRect();if(r.top<=mid&&r.bottom>=mid){best=secs[i];break;}}
    if(!best&&secs.length) best=W.scrollY<50?secs[0]:secs[secs.length-1];
    if(best&&best!==activeSec){
      var prevX=tgt.x;activeSec=best;
      var kind=best.getAttribute('data-pc')||'right';
      var o=place(kind);tgt.x=o.x;tgt.y=o.y;tgt.s=o.s;tgt.ry=o.ry;
      var nm=best.getAttribute('data-screen');if(nm&&nm!==mode){mode=nm;modeT=performance.now();}
      if(Math.abs(o.x-prevX)>.5&&!reduce) spinT+=(o.x>prevX?-1:1)*Math.PI*2; /* giro completo quando cambia lato */
      energy=1;
    }
  }
  function resize(){
    var w=W.innerWidth,h=W.innerHeight;
    renderer.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix();
    if(activeSec){var o=place(activeSec.getAttribute('data-pc')||'right');tgt.x=o.x;tgt.y=o.y;tgt.s=o.s;tgt.ry=o.ry;}
  }
  W.addEventListener('resize',resize);resize();pickSection();spin=spinT=0;
  cur.x=tgt.x;cur.y=tgt.y-3;cur.s=tgt.s;cur.ry=tgt.ry;
  W.addEventListener('scroll',function(){pickSection();var d=Math.abs(W.scrollY-lastY);lastY=W.scrollY;energy=Math.min(1,energy+d*.004);},{passive:true});

  /* mouse / touch / giroscopio: il computer guarda verso di te */
  W.addEventListener('pointermove',function(e){mouse.tx=e.clientX/W.innerWidth*2-1;mouse.ty=e.clientY/W.innerHeight*2-1;energy=Math.min(1,energy+.03);},{passive:true});
  W.addEventListener('touchmove',function(e){var t0=e.touches[0];if(!t0)return;mouse.tx=t0.clientX/W.innerWidth*2-1;mouse.ty=t0.clientY/W.innerHeight*2-1;},{passive:true});
  W.addEventListener('deviceorientation',function(e){if(e.gamma==null)return;mouse.tx=Math.max(-1,Math.min(1,e.gamma/30));mouse.ty=Math.max(-1,Math.min(1,(e.beta-45)/30));},{passive:true});
  /* passando sopra (o toccando) un elemento con data-screen, lo schermo cambia e la tastiera "scrive" */
  doc.querySelectorAll('[data-hover-screen]').forEach(function(el){
    function on(){hoverMode=el.getAttribute('data-hover-screen');hoverUntil=performance.now()+4000;modeT=performance.now();energy=1;}
    el.addEventListener('pointerenter',on);el.addEventListener('touchstart',on,{passive:true});
    el.addEventListener('pointerleave',function(){hoverUntil=performance.now()+600;});
  });

  var running=true,frame=0;
  doc.addEventListener('visibilitychange',function(){running=!doc.hidden;if(running){lastT=0;requestAnimationFrame(loop);}});
  function lerp(a,b,t){return a+(b-a)*t;}
  var lastT=0;
  var lastDraw=0;
  function loop(t){
    if(!running) return;
    /* su telefono 30 fotogrammi al secondo: fluido ma consuma metà */
    if(coarse&&t-lastDraw<31){requestAnimationFrame(loop);return;}
    lastDraw=t;
    frame++;
    var dt=Math.min(.1,lastT?(t-lastT)/1000:.016);lastT=t;
    var e=reduce?1:1-Math.pow(.94,dt*60),es=reduce?1:1-Math.pow(.955,dt*60),em=1-Math.pow(.92,dt*60);
    mouse.x=lerp(mouse.x,mouse.tx,em);mouse.y=lerp(mouse.y,mouse.ty,em);
    cur.x=lerp(cur.x,tgt.x,e);cur.y=lerp(cur.y,tgt.y,e);cur.s=lerp(cur.s,tgt.s,e);cur.ry=lerp(cur.ry,tgt.ry,e);
    spin=lerp(spin,spinT,es);
    var bob=reduce?0:Math.sin(t*.0012)*.12;
    pc.position.set(cur.x,cur.y+bob,0);pc.scale.setScalar(cur.s);
    pc.rotation.y=cur.ry+spin+mouse.x*.45+(reduce?0:Math.sin(W.scrollY*.002)*.12);
    pc.rotation.x=.08+mouse.y*.18;
    pc.rotation.z=reduce?0:Math.sin(t*.0009)*.03;
    /* tasti */
    energy*=.97;
    if(!reduce&&Math.random()<.08+energy*.5){var kk=keys[(Math.random()*keys.length)|0];kk.t=1;}
    keys.forEach(function(kk){if(kk.t>0){kk.t*=.9;var c=kk.t;kk.mat.emissive.setRGB(.22*c,.95*c,1*c);kk.m.position.y=.075-.03*c;}});
    led.material.color.setHex(Math.floor(t/500)%2?0xb8ff3c:0x2a4410);
    glow.material.opacity=.06+energy*.14;
    lc.intensity=1.4+energy*1.2;
    /* fluttuanti: si muovono con lo scroll (parallasse) */
    var sy=W.scrollY*.0035;
    floaters.forEach(function(f,i){var u=f.userData;
      f.position.set(u.x+Math.sin(t*.0004+u.ph)*.4+mouse.x*u.depth*.5,((u.y+sy*u.depth+15)%14)-7+Math.cos(t*.0005+u.ph)*.3,u.z);
      f.rotation.x+=u.rx*(1+energy*3);f.rotation.y+=u.ry*(1+energy*3);});
    if(frame%2===0) drawScreen(t);
    renderer.render(scene,cam);
    if(!reduce) requestAnimationFrame(loop);
  }
  /* aspetta i font per lo schermo, poi parte */
  var go=function(){requestAnimationFrame(loop);canvas.classList.add('ready');};
  if(doc.fonts&&doc.fonts.ready) doc.fonts.ready.then(go); else go();
  if(reduce){setInterval(function(){drawScreen(performance.now());renderer.render(scene,cam);},1000);}
}
/* VELOCITÀ: la libreria 3D (600 KB) si scarica solo quando l'utente interagisce o dopo 6 secondi,
   così la pagina si apre subito. */
(function(){
  var started=false,EV=['pointermove','pointerdown','touchstart','scroll','keydown','wheel'];
  function start(){
    if(started) return; started=true;
    EV.forEach(function(e){W.removeEventListener(e,start);});
    if(W.THREE){initPC();return;}
    var sc=doc.createElement('script');sc.src='js/three.min.js';sc.async=true;sc.onload=initPC;
    sc.onerror=function(){var c=doc.getElementById('pc3d');if(c)c.remove();};
    doc.head.appendChild(sc);
  }
  function arm(){
    EV.forEach(function(e){W.addEventListener(e,start,{passive:true});});
    setTimeout(start,6000);
  }
  if(doc.readyState==='complete') arm(); else W.addEventListener('load',arm);
})();

/* ================================================================
   ASSISTENTE AI (risposte automatiche, nessun dato inviato a server)
   ================================================================ */
var bub=doc.getElementById('ai-bub'),panel=doc.getElementById('ai-panel');
if(bub&&panel){
  var inp=doc.getElementById('ai-input'),box2=doc.getElementById('ai-msgs');
  bub.addEventListener('click',function(){panel.classList.toggle('open');if(panel.classList.contains('open'))inp.focus();});
  doc.getElementById('ai-close').addEventListener('click',function(){panel.classList.remove('open');});
  function add(text,role){var d=doc.createElement('div');d.className='amsg '+role;d.textContent=text;box2.appendChild(d);box2.scrollTop=box2.scrollHeight;return d;}
  function send(){
    var t=inp.value.trim();if(!t)return;inp.value='';add(t,'user');var ty=add('…','bot');
    setTimeout(function(){
      var q=t.toLowerCase(),rep='Grazie per il messaggio! Per una risposta precisa scrivi a Ilaria: info@ilariavisciglia.it oppure su WhatsApp al +39 329 148 9983. Il preventivo è gratuito.';
      if(/prezz|cost|quanto|preventiv/.test(q)) rep='Ogni progetto è su misura, quindi il costo dipende da cosa ti serve. Scrivi a info@ilariavisciglia.it o su WhatsApp (+39 329 148 9983) per un preventivo gratuito.';
      else if(/rate|klarna|scalapay|pagament|pagare/.test(q)) rep='Puoi pagare online in modo sicuro, anche in 3 rate. Puoi pagare in 3 rate con Klarna o con carta dalla pagina Pagamenti online.';
      else if(/crm|gestional|dashboard|piattaform|portale|area riservata/.test(q)) rep='Ilaria progetta CRM, gestionali e dashboard su misura: clienti, preventivi, prenotazioni e dati della tua azienda in un unico posto. Guarda la pagina Servizi o scrivile per parlarne.';
      else if(/ecommerce|e-commerce|negozio|shop/.test(q)) rep='Realizzo e-commerce su misura, veloci e ottimizzati per Google, con pagamenti sicuri. Vai alla pagina E-commerce o richiedi un preventivo.';
      else if(/whatsapp|email|mail|\bai\b|intelligenza|assistente|agente|chatbot/.test(q)) rep='Ilaria crea agenti AI per WhatsApp ed email che rispondono ai tuoi clienti 24 ore su 24, addestrati sulla tua attività.';
      else if(/sito|web|landing|restyling/.test(q)) rep='Siti web su misura, scritti a mano e ottimizzati per Google, per aziende e professionisti a Roma e in tutta Italia. Scrivimi per un preventivo gratuito!';
      else if(/portfolio|lavori|progetti|esempi/.test(q)) rep='Nel portfolio trovi progetti come LogoVex (loghi con l\'AI) e InPostSocial (social media manager con l\'AI), oltre a siti, e-commerce e booking.';
      else if(/ciao|salve|buongiorno|buonasera/.test(q)) rep='Ciao! 👋 Dimmi pure: siti web, CRM e dashboard, e-commerce o agenti AI?';
      ty.textContent=rep;
    },550);
  }
  doc.getElementById('ai-send').addEventListener('click',send);
  inp.addEventListener('keydown',function(e){if(e.key==='Enter')send();});
}
})();
