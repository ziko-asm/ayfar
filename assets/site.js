(function(){
  var root = document.documentElement, body = document.body;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  function store(k, v){ try{ if(v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); }catch(e){ return null; } }
  window.AYFAR = {reduce:reduce, fine:fine, store:store};

  /* ---------- language ---------- */
  function setLang(l){
    root.setAttribute('data-lang', l); root.setAttribute('lang', l);
    document.querySelectorAll('[data-set-lang]').forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.setLang === l)); });
    var t = document.querySelector('meta[name="title-' + l + '"]');
    if(t) document.title = t.content;
    var lbl = document.querySelector('.cur-ring .lbl');
    if(lbl) lbl.textContent = l === 'az' ? 'AÇ' : l === 'ru' ? 'ОТКР' : 'OPEN';
    store('lang', l);
    document.dispatchEvent(new CustomEvent('ayfar:lang', {detail:l}));
  }
  var saved = store('lang');
  var nav = (navigator.language || 'az').slice(0,2);
  setLang(['az','en','ru'].indexOf(saved) >= 0 ? saved : (nav === 'ru' ? 'ru' : nav === 'en' ? 'en' : 'az'));
  document.querySelectorAll('[data-set-lang]').forEach(function(b){ b.addEventListener('click', function(){ setLang(b.dataset.setLang); }); });

  /* ---------- preloader (home) ---------- */
  var loader = document.getElementById('loader');
  function ready(){ body.classList.remove('loading'); setTimeout(function(){ body.classList.add('ready'); }, 250); }
  if(loader){
    var finished = false;
    var finishLoad = function(){
      if(finished) return; finished = true;
      loader.classList.add('done'); ready();
      setTimeout(function(){ loader.classList.add('gone'); }, 1200);
    };
    var seen = false; try{ seen = sessionStorage.getItem('seen') === '1'; sessionStorage.setItem('seen','1'); }catch(e){}
    if(reduce || seen){ loader.classList.add('done','gone'); body.classList.add('ready'); }
    else{
      body.classList.add('loading');
      var lnum = document.getElementById('lnum'), lbar = document.getElementById('lbar'), t0 = performance.now();
      var iv = setInterval(function(){
        var n = Math.min(100, Math.round(Math.pow(Math.max(0, performance.now() - t0) / 1100, .8) * 100));
        lnum.textContent = String(n).padStart(3,'0'); lbar.style.width = n + '%';
        if(n >= 100){ clearInterval(iv); setTimeout(finishLoad, 200); }
      }, 30);
      setTimeout(finishLoad, 1700);
      loader.addEventListener('click', finishLoad);
    }
  } else body.classList.add('ready');

  /* ---------- page transition curtain ---------- */
  var curtain = document.getElementById('curtain');
  if(curtain && !reduce){
    var arrived = false; try{ arrived = sessionStorage.getItem('curtain') === '1'; sessionStorage.removeItem('curtain'); }catch(e){}
    if(arrived){
      curtain.classList.add('enter');
      requestAnimationFrame(function(){ requestAnimationFrame(function(){ curtain.classList.add('leave'); }); });
      setTimeout(function(){ curtain.className = ''; }, 900);
    }
    document.addEventListener('click', function(e){
      var a = e.target.closest('a[data-nav]');
      if(!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
      // same page + #section: just scroll there, no curtain (the page never reloads, so the curtain would stay shut)
      if(a.hash && a.pathname === location.pathname) return;
      e.preventDefault();
      try{ sessionStorage.setItem('curtain','1'); }catch(err){}
      curtain.className = 'cover';
      setTimeout(function(){ location.href = a.href; }, 560);
    });
    addEventListener('pageshow', function(e){ if(e.persisted) curtain.className = ''; });
  }

  /* ---------- mobile menu ---------- */
  var mbtn = document.querySelector('.menu-btn'), hdrEl = document.getElementById('hdr');
  if(mbtn && hdrEl){
    var setMenu = function(open){
      hdrEl.classList.toggle('open', open); mbtn.setAttribute('aria-expanded', String(open));
    };
    mbtn.addEventListener('click', function(){ setMenu(mbtn.getAttribute('aria-expanded') !== 'true'); });
    document.querySelectorAll('.mnav a').forEach(function(a){ a.addEventListener('click', function(){ setMenu(false); }); });
    addEventListener('keydown', function(e){ if(e.key === 'Escape' && mbtn.getAttribute('aria-expanded') === 'true'){ setMenu(false); mbtn.focus(); } });
    document.addEventListener('click', function(e){ if(!hdrEl.contains(e.target)) setMenu(false); });
    addEventListener('resize', function(){ if(innerWidth > 760) setMenu(false); });
  }

  /* ---------- message dialog (Formspree) + photo zoom ---------- */
  function L3(az, en, ru){ var l = root.getAttribute('data-lang'); return l === 'en' ? en : l === 'ru' ? ru : az; }
  var dlg = document.getElementById('msgDlg'), form = document.getElementById('msgForm');
  if(dlg && form && dlg.showModal){
    var status = form.querySelector('.msg-status'), sendBtn = form.querySelector('button[type=submit]');
    var openDlg = function(){ status.textContent = ''; status.className = 'msg-status'; dlg.showModal(); var n = document.getElementById('msgName'); if(n) n.focus(); };
    document.querySelectorAll('[data-msg-open]').forEach(function(b){ b.addEventListener('click', function(){
      var h = document.getElementById('hdr'); if(h) h.classList.remove('open');
      var mb = document.querySelector('.menu-btn'); if(mb) mb.setAttribute('aria-expanded', 'false');
      openDlg();
    }); });
    dlg.querySelector('[data-msg-close]').addEventListener('click', function(){ dlg.close(); });
    dlg.addEventListener('click', function(e){ if(e.target === dlg) dlg.close(); });
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(!form.checkValidity()){ form.reportValidity(); return; }
      form.classList.add('busy'); sendBtn.disabled = true; status.textContent = '';
      fetch(form.action, {method:'POST', body:new FormData(form), headers:{'Accept':'application/json'}})
        .then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); })
        .then(function(){
          form.reset(); status.className = 'msg-status ok';
          status.textContent = L3('Göndərildi ✓ Tezliklə cavab yazacam.', 'Sent ✓ I will get back to you soon.', 'Отправлено ✓ Скоро отвечу.');
        })
        .catch(function(){
          status.className = 'msg-status err';
          status.textContent = L3('Göndərmək alınmadı. WhatsApp-a yazın: +994 77 217 23 58', 'Could not send. Message me on WhatsApp: +994 77 217 23 58', 'Не удалось отправить. Напишите в WhatsApp: +994 77 217 23 58');
        })
        .then(function(){ form.classList.remove('busy'); sendBtn.disabled = false; });
    });
  } else {
    /* very old browsers without <dialog>: send people to WhatsApp instead */
    document.querySelectorAll('[data-msg-open]').forEach(function(b){ b.addEventListener('click', function(){ location.href = 'https://wa.me/994772172358'; }); });
  }
  var pdlg = document.getElementById('photoDlg');
  document.querySelectorAll('img[data-zoom]').forEach(function(im){
    var open = function(){
      if(!pdlg || !pdlg.showModal) return;
      var big = pdlg.querySelector('img'); big.src = im.dataset.zoom; big.alt = im.alt; pdlg.showModal();
    };
    im.addEventListener('click', open);
    im.addEventListener('keydown', function(e){ if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); open(); } });
  });
  if(pdlg){
    pdlg.addEventListener('click', function(){ pdlg.close(); });
  }

  /* ---------- rotating words ---------- */
  document.querySelectorAll('.rot').forEach(function(el){
    var words = el.dataset.words.split('|'), wi = 0;
    if(reduce || words.length < 2) return;
    setInterval(function(){
      if(document.hidden) return;
      el.classList.add('out');
      setTimeout(function(){
        wi = (wi + 1) % words.length;
        el.textContent = words[wi];
        el.classList.remove('out'); el.classList.add('pre');
        void el.offsetWidth;
        el.classList.remove('pre');
      }, 380);
    }, 2400);
  });

  /* ---------- hero word: one gradient across all letters ---------- */
  var word = document.querySelector('.word');
  if(word){
    var measure = function(){
      var spans = word.querySelectorAll('span');
      word.style.setProperty('--ww', word.scrollWidth + 'px');
      spans.forEach(function(s){ s.style.setProperty('--ox', (s.offsetLeft - word.offsetLeft) + 'px'); });
    };
    measure();
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
    addEventListener('resize', measure);
  }

  /* ---------- reveal + counters ---------- */
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(!e.isIntersecting) return;
      var t = e.target; t.classList.add('in');
      setTimeout(function(){ t.style.transitionDelay = ''; }, 1400);
      t.querySelectorAll('.stat').forEach(function(s, i){ setTimeout(function(){ s.classList.add('in'); }, i * 120); });
      t.querySelectorAll('[data-count]').forEach(function(c){
        var to = +c.dataset.count, s0 = performance.now();
        (function f(now){ var p = Math.min(1, (now - s0) / 1400); c.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))); if(p < 1) requestAnimationFrame(f); })(s0);
      });
      io.unobserve(t);
    });
  }, {threshold:.12, rootMargin:'0px 0px -6% 0px'});
  document.querySelectorAll('.reveal').forEach(function(el){ io.observe(el); });

  /* ---------- header + progress ---------- */
  var hdr = document.getElementById('hdr'), prog = document.getElementById('progress'), lastY = 0;
  addEventListener('scroll', function(){
    var y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
    if(prog) prog.style.transform = 'scaleX(' + (h > 0 ? y / h : 0) + ')';
    if(hdr) hdr.classList.toggle('hide', y > lastY && y > 300);
    lastY = y;
  }, {passive:true});

  /* ---------- cursor, tilt, magnet ---------- */
  if(fine && !reduce){
    body.classList.add('has-cursor');
    var dot = document.querySelector('.cur-dot'), ring = document.querySelector('.cur-ring');
    var mx = -100, my = -100, rx = -100, ry = -100;
    addEventListener('pointermove', function(e){ mx = e.clientX; my = e.clientY; dot.style.transform = 'translate3d(' + mx + 'px,' + my + 'px,0)'; }, {passive:true});
    (function loop(){ rx += (mx - rx) * .18; ry += (my - ry) * .18; ring.style.transform = 'translate3d(' + rx + 'px,' + ry + 'px,0)'; requestAnimationFrame(loop); })();
    document.addEventListener('pointerover', function(e){ ring.classList.toggle('hot', !!e.target.closest('a[href], [data-hot]')); });

    document.querySelectorAll('.tiltable').forEach(function(c){
      c.addEventListener('pointermove', function(e){
        var r = c.getBoundingClientRect(), px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        var amt = +(c.dataset.tilt || 7);
        c.style.transform = 'perspective(1100px) rotateX(' + ((.5 - py) * amt) + 'deg) rotateY(' + ((px - .5) * amt) + 'deg)';
        c.style.setProperty('--mx', px * 100 + '%'); c.style.setProperty('--my', py * 100 + '%');
      });
      c.addEventListener('pointerleave', function(){ c.style.transform = ''; });
    });

    document.querySelectorAll('.magnet').forEach(function(m){
      m.addEventListener('pointermove', function(e){
        var r = m.getBoundingClientRect();
        m.style.transform = 'translate(' + (e.clientX - r.left - r.width / 2) * .3 + 'px,' + (e.clientY - r.top - r.height / 2) * .4 + 'px)';
      });
      m.addEventListener('pointerleave', function(){ m.style.transform = ''; });
    });
  }

  /* ---------- metro scene HUD ---------- */
  document.querySelectorAll('.metro').forEach(function(scene){
    var cash = scene.querySelector('.cash span'), spd = scene.querySelector('.spd span'), money = 0, on = false;
    new IntersectionObserver(function(es){ on = es[0].isIntersecting; }).observe(scene);
    setInterval(function(){
      if(!on || document.hidden) return;
      var gain = 50 + Math.floor(Math.random() * 450);
      money += gain; cash.textContent = money.toLocaleString('az');
      spd.textContent = 40 + Math.floor(Math.random() * 45);
      if(!reduce){
        var p = document.createElement('div'); p.className = 'pop-cash'; p.textContent = '+' + gain + ' ₼';
        p.style.left = (20 + Math.random() * 60) + '%'; p.style.top = (35 + Math.random() * 30) + '%';
        scene.appendChild(p); setTimeout(function(){ p.remove(); }, 1300);
      }
    }, 900);
  });

  /* ---------- background network ---------- */
  var cv = document.getElementById('net');
  if(!cv) return;
  var ctx = cv.getContext('2d');
  var W, H, DPR, nodes = [], edges = [], adj = [], trains = [], pm = {x:-9999, y:-9999};
  var COLORS = ['52,245,176', '255,79,216', '91,140,255', '255,201,77'];
  function newTrain(){ var a = Math.floor(Math.random() * nodes.length); return {a:a, b:adj[a][0], p:Math.random(), s:.004 + Math.random() * .008, c:COLORS[Math.floor(Math.random() * COLORS.length)], trail:[]}; }
  function build(){
    DPR = Math.min(devicePixelRatio || 1, 2); W = innerWidth; H = innerHeight;
    cv.width = W * DPR; cv.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    var count = Math.round(Math.min(56, Math.max(20, W * H / 32000)));
    nodes = []; edges = []; adj = [];
    for(var i = 0; i < count; i++){ nodes.push({x:Math.random() * W, y:Math.random() * H, vx:(Math.random() - .5) * .12, vy:(Math.random() - .5) * .12}); adj.push([]); }
    nodes.forEach(function(a, i){
      var d = nodes.map(function(b, j){ return {j:j, d:Math.hypot(a.x - b.x, a.y - b.y)}; }).sort(function(p, q){ return p.d - q.d; });
      for(var k = 1; k <= 2; k++){ var j = d[k].j; if(adj[i].indexOf(j) < 0){ adj[i].push(j); adj[j].push(i); edges.push([i, j]); } }
    });
    trains = [];
    for(var t = 0; t < Math.round(count / 5); t++) trains.push(newTrain());
  }
  addEventListener('pointermove', function(e){ pm.x = e.clientX; pm.y = e.clientY; }, {passive:true});
  var rt, lastW = innerWidth; addEventListener('resize', function(){ if(innerWidth === lastW && Math.abs(innerHeight - H) < 120) return; lastW = innerWidth; clearTimeout(rt); rt = setTimeout(build, 200); });
  build();
  function draw(){
    ctx.clearRect(0, 0, W, H);
    var off = (scrollY * .08) % H;
    nodes.forEach(function(n){
      n.x += n.vx; n.y += n.vy;
      if(n.x < -20) n.x = W + 20; if(n.x > W + 20) n.x = -20; if(n.y < -20) n.y = H + 20; if(n.y > H + 20) n.y = -20;
    });
    function Y(n){ var y = n.y - off; return y < -40 ? y + H : y; }
    ctx.lineWidth = 1;
    edges.forEach(function(e){
      var a = nodes[e[0]], b = nodes[e[1]], ay = Y(a), by = Y(b);
      if(Math.abs(ay - by) > H / 2 || Math.abs(a.x - b.x) > W / 2) return;
      var near = Math.max(0, 1 - Math.hypot((a.x + b.x) / 2 - pm.x, (ay + by) / 2 - pm.y) / 220);
      ctx.strokeStyle = 'rgba(140,170,200,' + (.07 + near * .35) + ')';
      ctx.beginPath(); ctx.moveTo(a.x, ay); ctx.lineTo(b.x, by); ctx.stroke();
    });
    nodes.forEach(function(n){
      var y = Y(n), near = Math.max(0, 1 - Math.hypot(n.x - pm.x, y - pm.y) / 180);
      ctx.fillStyle = 'rgba(200,220,240,' + (.25 + near * .75) + ')';
      ctx.beginPath(); ctx.arc(n.x, y, 1.6 + near * 2.5, 0, 6.283); ctx.fill();
      if(near > .3){ ctx.strokeStyle = 'rgba(52,245,176,' + (near * .5) + ')'; ctx.beginPath(); ctx.moveTo(n.x, y); ctx.lineTo(pm.x, pm.y); ctx.stroke(); }
    });
    trains.forEach(function(t, i){
      var a = nodes[t.a], b = nodes[t.b];
      if(!b){ trains[i] = newTrain(); return; }
      t.p += t.s;
      if(t.p >= 1){ var nx = adj[t.b].filter(function(k){ return k !== t.a; }); t.a = t.b; t.b = nx.length ? nx[Math.floor(Math.random() * nx.length)] : adj[t.b][0]; t.p = 0; return; }
      var ay = Y(a), by = Y(b);
      if(Math.abs(ay - by) > H / 2 || Math.abs(a.x - b.x) > W / 2){ t.trail = []; return; }
      var x = a.x + (b.x - a.x) * t.p, y = ay + (by - ay) * t.p;
      t.trail.push([x, y]); if(t.trail.length > 18) t.trail.shift();
      ctx.lineWidth = 2;
      for(var k = 1; k < t.trail.length; k++){
        ctx.strokeStyle = 'rgba(' + t.c + ',' + (k / t.trail.length * .8) + ')';
        ctx.beginPath(); ctx.moveTo(t.trail[k - 1][0], t.trail[k - 1][1]); ctx.lineTo(t.trail[k][0], t.trail[k][1]); ctx.stroke();
      }
      ctx.lineWidth = 1;
      ctx.fillStyle = 'rgba(' + t.c + ',.18)'; ctx.beginPath(); ctx.arc(x, y, 8, 0, 6.283); ctx.fill();
      ctx.fillStyle = 'rgba(' + t.c + ',1)'; ctx.beginPath(); ctx.arc(x, y, 2.6, 0, 6.283); ctx.fill();
    });
  }
  if(reduce) draw();
  else {
    /* the background is decoration: draw it at ~30 fps and pause it while the page is being scrolled,
       so scrolling (and the project gallery) gets the whole frame budget */
    var scrolling = 0, lastDraw = 0;
    addEventListener('scroll', function(){ scrolling = performance.now(); }, {passive:true});
    (function frame(now){
      requestAnimationFrame(frame);
      if(document.hidden || now - scrolling < 180 || now - lastDraw < 32) return;
      lastDraw = now; draw();
    })(0);
  }
})();
