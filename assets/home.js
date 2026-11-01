(function(){
  var A = window.AYFAR || {}, reduce = A.reduce;
  function lang(){ return document.documentElement.getAttribute('data-lang') || 'az'; }

  /* =================== MINI METRO GAME =================== */
  var cv = document.getElementById('game');
  if(cv){
    var ctx = cv.getContext('2d'), wrap = cv.parentElement;
    var hud = {cash:document.getElementById('gCash'), spd:document.getElementById('gSpd'), next:document.getElementById('gNext'), best:document.getElementById('gBest')};
    var over = document.getElementById('gOver'), start = document.getElementById('gStart'), toast = document.getElementById('gToast');
    var STATIONS = ['İçərişəhər','Sahil','28 May','Gənclik','Nərimanov','Ulduz','Koroğlu','Qara Qarayev','Neftçilər','Xalqlar Dostluğu','Əhmədli','Həzi Aslanov'];
    var W = 0, H = 200, DPR = 1, TX = 0, TRAIN = 156, RAIL;
    var S, mode = 'demo', holding = false, visible = false, best = +(A.store && A.store('best') || 0) || 0;
    hud.best.textContent = best.toLocaleString('az');

    function size(){
      DPR = Math.min(devicePixelRatio || 1, 2); W = wrap.clientWidth; H = wrap.clientHeight;
      cv.width = W * DPR; cv.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      TX = Math.max(30, W * .16); RAIL = H - 34;
    }
    function reset(){
      S = {x:0, v:0, cash:0, stIdx:0, objs:[], genX:400, t:0, shake:0, dist:0};
      gen(W + 2400);
    }
    function gen(until){
      while(S.genX < until){
        var k = S.objs.filter(function(o){ return o.type === 'st'; }).length;
        var gap = 1500 + Math.random() * 700;
        var sx = S.genX + gap;
        var coinsFrom = S.genX + 160, coinsTo = sx - 220;
        for(var c = coinsFrom; c < coinsTo; c += 70 + Math.random() * 40){
          if(Math.random() < .55) S.objs.push({type:'coin', x:c, y:RAIL - 40 - (Math.random() < .3 ? 18 : 0), got:false});
        }
        var difficulty = Math.min(1, S.genX / 12000);
        var nSig = Math.random() < .55 + difficulty * .4 ? 1 : 0;
        if(gap > 1900 && difficulty > .4) nSig = 2;
        for(var s = 0; s < nSig; s++){
          var px = S.genX + gap * (nSig === 2 ? (.33 + s * .34) : (.45 + Math.random() * .2));
          S.objs.push({type:'sig', x:px, period:2.6 + Math.random() * 2.2, phase:Math.random() * 5, red:.42 + difficulty * .12});
        }
        S.objs.push({type:'st', x:sx, len:300, name:STATIONS[k % STATIONS.length], done:false});
        S.genX = sx + 300;
      }
    }
    function sigState(o){
      var c = ((S.t + o.phase) % o.period) / o.period;
      if(c < 1 - o.red - .12) return 'g';
      if(c < 1 - o.red) return 'y';
      return 'r';
    }
    function nextOf(type, from){
      var best = null;
      S.objs.forEach(function(o){ if(o.type === type && o.x > from && (!best || o.x < best.x)) best = o; });
      return best;
    }
    function say(txt, cls){
      toast.textContent = txt; toast.className = 'g-toast show ' + (cls || '');
      clearTimeout(say.t); say.t = setTimeout(function(){ toast.className = 'g-toast'; }, 1300);
    }
    function crash(){
      mode = 'over'; holding = false; S.shake = 14;
      if(S.cash > best){ best = S.cash; A.store && A.store('best', String(best)); hud.best.textContent = best.toLocaleString('az'); }
      over.querySelector('[data-score]').textContent = S.cash.toLocaleString('az') + ' ₼';
      over.querySelector('[data-best]').textContent = best.toLocaleString('az') + ' ₼';
      over.classList.add('show');
    }
    function play(){
      reset(); mode = 'play'; over.classList.remove('show'); start.classList.add('hide'); wrap.classList.add('playing');
      say({az:'Basılı saxla: qaz · burax: tormoz', ru:'Держите: газ · отпустите: тормоз'}[lang()] || 'Hold: go · release: brake');
    }

    function step(dt){
      S.t += dt / 60;
      var front = S.x + TRAIN;
      if(mode === 'demo'){
        var st = nextOf('st', S.x + TRAIN - 300), target = 4.2;
        if(st && !st.done){
          var stopAt = st.x + st.len - 20 - TRAIN, d = stopAt - S.x;
          if(d < 260) target = Math.max(0, d / 60);
          if(d < 4 && S.v < .2){ st.done = true; st.wait = 70; }
        }
        if(st && st.wait > 0){ st.wait -= dt; target = 0; }
        S.v += (target - S.v) * .05 * dt;
      } else if(mode === 'play'){
        if(holding) S.v = Math.min(10, S.v + .13 * dt);
        else S.v = Math.max(0, S.v - .2 * dt);
      } else S.v = Math.max(0, S.v - .4 * dt);
      var prevFront = front;
      S.x += S.v * dt; front = S.x + TRAIN; S.dist += S.v * dt;
      if(mode === 'play'){
        S.objs.forEach(function(o){
          if(o.type === 'coin' && !o.got && o.x <= front && o.x >= S.x){ o.got = true; S.cash += 10; o.fx = 1; }
          if(o.type === 'sig' && prevFront < o.x && front >= o.x && sigState(o) === 'r'){ crash(); say({az:'Qırmızı işıq! Qəza', ru:'Красный свет! Авария'}[lang()] || 'Red signal! Crash', 'bad'); }
          if(o.type === 'st' && !o.done && S.v < .25 && S.x >= o.x - 4 && front <= o.x + o.len + 4){
            o.done = true; var bonus = 120 + Math.floor(Math.random() * 180) + Math.floor(S.dist / 400);
            S.cash += bonus; say(o.name + ' · +' + bonus + ' ₼', 'good');
          }
        });
      }
      S.objs = S.objs.filter(function(o){ return o.x > S.x - 900; });
      gen(S.x + W + 2400);
      if(S.shake > 0) S.shake *= .9;

      hud.cash.textContent = S.cash.toLocaleString('az');
      hud.spd.textContent = Math.round(S.v * 9);
      var ns = nextOf('st', S.x - 10);
      if(ns) hud.next.textContent = ns.name;
    }

    function rr(x, y, w, h, r){ ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
    function draw(){
      var sh = S.shake > .5 ? (Math.random() - .5) * S.shake : 0;
      ctx.save(); ctx.translate(sh, sh * .5);
      var g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#0b0f1a'); g.addColorStop(.7, '#090c14'); g.addColorStop(1, '#05070b');
      ctx.fillStyle = g; ctx.fillRect(-20, -20, W + 40, H + 40);
      // wall ribs
      ctx.strokeStyle = 'rgba(255,255,255,.04)'; ctx.lineWidth = 2;
      for(var rx = -((S.x * .6) % 120); rx < W; rx += 120){ ctx.beginPath(); ctx.moveTo(rx, 14); ctx.lineTo(rx, RAIL - 6); ctx.stroke(); }
      // tunnel lamps
      for(var lx = -((S.x * .45) % 260); lx < W; lx += 260){
        var lg = ctx.createRadialGradient(lx, 22, 0, lx, 22, 60); lg.addColorStop(0, 'rgba(255,214,140,.35)'); lg.addColorStop(1, 'rgba(255,214,140,0)');
        ctx.fillStyle = lg; ctx.fillRect(lx - 60, 0, 120, 90);
        ctx.fillStyle = '#ffdca0'; ctx.fillRect(lx - 9, 18, 18, 4);
      }
      // stations
      S.objs.forEach(function(o){
        if(o.type !== 'st') return;
        var sx = o.x - S.x + TX; if(sx > W + 50 || sx + o.len < -50) return;
        ctx.fillStyle = o.done ? 'rgba(52,245,176,.10)' : 'rgba(255,255,255,.06)'; ctx.fillRect(sx, RAIL - 74, o.len, 74);
        ctx.fillStyle = o.done ? 'rgba(52,245,176,.5)' : 'rgba(255,201,77,.55)'; ctx.fillRect(sx, RAIL - 2, o.len, 3);
        rr(sx + o.len / 2 - 70, RAIL - 108, 140, 24, 6); ctx.fillStyle = '#0e1726'; ctx.fill(); ctx.strokeStyle = o.done ? '#34f5b0' : '#5b8cff'; ctx.lineWidth = 1.5; ctx.stroke();
        ctx.fillStyle = '#e5394a'; ctx.beginPath(); ctx.arc(sx + o.len / 2 - 56, RAIL - 96, 6, 0, 6.283); ctx.fill();
        ctx.fillStyle = '#fff'; ctx.font = 'bold 9px "JetBrains Mono",monospace'; ctx.textAlign = 'center'; ctx.fillText('M', sx + o.len / 2 - 56, RAIL - 93);
        ctx.font = '600 11px "Space Grotesk",sans-serif'; ctx.fillText(o.name, sx + o.len / 2 + 6, RAIL - 92);
        if(!o.done && mode === 'play'){ ctx.fillStyle = 'rgba(255,201,77,.8)'; ctx.font = '600 9px "JetBrains Mono",monospace'; ctx.fillText('STOP', sx + o.len - 24, RAIL - 10); }
      });
      // rails + sleepers
      ctx.fillStyle = '#1a2230';
      for(var tx = -(S.x % 26); tx < W; tx += 26) ctx.fillRect(tx, RAIL + 4, 14, 5);
      ctx.fillStyle = '#7d8aa0'; ctx.fillRect(0, RAIL, W, 3);
      // coins
      S.objs.forEach(function(o){
        if(o.type !== 'coin') return;
        var cx = o.x - S.x + TX; if(cx < -20 || cx > W + 20) return;
        if(o.got){ o.fx = (o.fx || 1) - .06; if(o.fx <= 0) return; ctx.globalAlpha = o.fx; }
        var bob = Math.sin(S.t * 4 + o.x) * 3, y = o.y + bob - (o.got ? (1 - o.fx) * 30 : 0);
        ctx.fillStyle = '#ffc94d'; ctx.shadowColor = '#ffc94d'; ctx.shadowBlur = 10;
        ctx.beginPath(); ctx.ellipse(cx, y, 6 * Math.abs(Math.cos(S.t * 3 + o.x)) + 1.5, 7, 0, 0, 6.283); ctx.fill();
        ctx.shadowBlur = 0; ctx.globalAlpha = 1;
      });
      // signals
      S.objs.forEach(function(o){
        if(o.type !== 'sig') return;
        var px = o.x - S.x + TX; if(px < -20 || px > W + 20) return;
        var st = mode === 'demo' ? 'g' : sigState(o), col = st === 'g' ? '#34f5b0' : st === 'y' ? '#ffc94d' : '#ff3b3b';
        ctx.fillStyle = '#2a3445'; ctx.fillRect(px - 2, RAIL - 96, 4, 96);
        rr(px - 10, RAIL - 126, 20, 34, 6); ctx.fillStyle = '#0d121b'; ctx.fill();
        ctx.fillStyle = col; ctx.shadowColor = col; ctx.shadowBlur = 18;
        ctx.beginPath(); ctx.arc(px, st === 'r' ? RAIL - 116 : RAIL - 102, 6, 0, 6.283); ctx.fill(); ctx.shadowBlur = 0;
        if(st === 'r'){ ctx.fillStyle = 'rgba(255,59,59,.08)'; ctx.fillRect(px - 40, RAIL - 6, 80, 8); }
      });
      // headlight beam
      var fx = TX + TRAIN;
      var hb = ctx.createLinearGradient(fx, 0, fx + 220, 0); hb.addColorStop(0, 'rgba(255,240,200,.28)'); hb.addColorStop(1, 'rgba(255,240,200,0)');
      ctx.fillStyle = hb; ctx.beginPath(); ctx.moveTo(fx, RAIL - 30); ctx.lineTo(fx + 240, RAIL - 70); ctx.lineTo(fx + 240, RAIL + 10); ctx.lineTo(fx, RAIL - 14); ctx.closePath(); ctx.fill();
      // speed lines
      if(S.v > 6){ ctx.strokeStyle = 'rgba(255,255,255,' + ((S.v - 6) / 12) + ')'; ctx.lineWidth = 1;
        for(var i = 0; i < 6; i++){ var ly = 30 + ((i * 37 + S.x * .7) % (RAIL - 50)), lx2 = (W - ((S.x * 2 + i * 173) % (W + 200))); ctx.beginPath(); ctx.moveTo(lx2, ly); ctx.lineTo(lx2 + 60, ly); ctx.stroke(); } }
      // train
      for(var c = 0; c < 3; c++){
        var cx0 = TX + c * 52, cy = RAIL - 40, w = 48, front2 = c === 2;
        rr(cx0, cy, w, 36, front2 ? 10 : 5); ctx.fillStyle = '#f2f4f7'; ctx.fill();
        ctx.fillStyle = '#e5394a'; ctx.fillRect(cx0, cy + 22, w, 6);
        ctx.fillStyle = '#16202e';
        for(var wi = 0; wi < 3; wi++) rr(cx0 + 5 + wi * 14, cy + 6, 10, 11, 2), ctx.fill();
        ctx.fillStyle = '#0b0f14'; ctx.beginPath(); ctx.arc(cx0 + 10, RAIL - 2, 4, 0, 6.283); ctx.arc(cx0 + w - 10, RAIL - 2, 4, 0, 6.283); ctx.fill();
        if(front2){ ctx.fillStyle = '#fff6c8'; ctx.shadowColor = '#fff6c8'; ctx.shadowBlur = 14; ctx.beginPath(); ctx.arc(cx0 + w - 2, cy + 30, 3, 0, 6.283); ctx.fill(); ctx.shadowBlur = 0; }
        if(c < 2){ ctx.fillStyle = '#3a4456'; ctx.fillRect(cx0 + w, cy + 16, 4, 6); }
      }
      if(mode === 'over'){ ctx.fillStyle = 'rgba(255,40,40,.12)'; ctx.fillRect(0, 0, W, H); }
      ctx.restore();
    }

    var last = performance.now();
    function frame(now){
      var dt = Math.min(3, (now - last) / 16.67); last = now;
      if(visible && !document.hidden){ step(dt); draw(); }
      requestAnimationFrame(frame);
    }
    size(); reset();
    if(reduce){ draw(); }
    else requestAnimationFrame(frame);
    new IntersectionObserver(function(es){ visible = es[0].intersectionRatio > 0; }, {threshold:[0, .5]}).observe(wrap);
    addEventListener('resize', function(){ var w = W; size(); if(w !== W && mode !== 'play') reset(); if(reduce) draw(); });

    function down(e){
      if(mode !== 'play'){ if(e && e.type === 'keydown' && e.repeat) return; play(); }
      holding = true;
    }
    function up(){ holding = false; }
    cv.addEventListener('pointerdown', function(e){ e.preventDefault(); cv.setPointerCapture && cv.setPointerCapture(e.pointerId); down(e); });
    cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up); cv.addEventListener('lostpointercapture', up);
    /* press-and-hold on the start overlay starts the run and keeps the throttle open */
    start.addEventListener('pointerdown', function(e){ e.preventDefault(); play(); holding = true; });
    start.addEventListener('keydown', function(e){ if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); play(); } });
    addEventListener('pointerup', up); addEventListener('pointercancel', up);
    wrap.addEventListener('contextmenu', function(e){ e.preventDefault(); });
    over.querySelector('[data-again]').addEventListener('click', function(){ play(); });
    function inView(){ var r = wrap.getBoundingClientRect(); return r.top < innerHeight * .8 && r.bottom > innerHeight * .2; }
    addEventListener('keydown', function(e){
      if(!/^(Space|ArrowUp|KeyW)$/.test(e.code) || !inView()) return;
      if(e.target.closest && e.target.closest('input,textarea,button,a')) return;
      e.preventDefault(); down(e);
    });
    addEventListener('keyup', function(e){ if(/^(Space|ArrowUp|KeyW)$/.test(e.code)) up(); });
  }

  /* =================== SITE CHECK (SaytYoxla API) =================== */
  var sf = document.getElementById('scanForm');
  if(sf){
    var out = document.getElementById('scanOut'), inp = document.getElementById('scanUrl'), btn = sf.querySelector('button');
    var API = sf.dataset.api, SITE = sf.dataset.site, WA = sf.dataset.wa;
    var T = function(az, en, ru){ var l = lang(); return l === 'en' ? en : l === 'ru' ? (ru || en) : az; };
    var el = function(tag, cls, text){ var e = document.createElement(tag); if(cls) e.className = cls; if(text != null) e.textContent = text; return e; };
    var gradeColor = function(g){ return {A:'#34f5b0', B:'#7ee081', C:'#ffc94d', D:'#ff9a4d', F:'#ff4f6d'}[g] || '#8d99a8'; };
    var host = function(u){ try{ return new URL(/^https?:\/\//i.test(u) ? u : 'https://' + u).hostname; }catch(e){ return u; } };
    var busy = function(on){ sf.classList.toggle('busy', on); btn.disabled = on; inp.readOnly = on; };
    var showError = function(msg){
      out.textContent = ''; var e = el('div', 'scan-err', msg); e.setAttribute('role', 'alert'); out.appendChild(e);
    };
    var render = function(r){
      out.textContent = '';
      var card = el('div', 'scan-card'), col = gradeColor(r.grade), h = host(r.final_url || r.url);
      card.style.setProperty('--gc', col);
      // score ring
      var ring = el('div', 'scan-ring');
      ring.innerHTML = '<svg viewBox="0 0 120 120" aria-hidden="true"><circle class="t" cx="60" cy="60" r="52"/><circle class="v" cx="60" cy="60" r="52"/></svg>';
      var mid = el('div', 'scan-mid'); mid.appendChild(el('b', null, r.grade)); mid.appendChild(el('small', null, r.score + ' / 100'));
      ring.appendChild(mid); card.appendChild(ring);
      var body = el('div', 'scan-body');
      body.appendChild(el('div', 'scan-host', h));
      body.appendChild(el('p', 'scan-sum', r.summary));
      var probs = (r.findings || []).filter(function(f){ return f.status === 'fail' || f.status === 'warn'; })
        .sort(function(a, b){ return (b.status === 'fail') - (a.status === 'fail') || (b.weight || 0) - (a.weight || 0); });
      if(probs.length){
        var ul = el('ul', 'scan-list');
        probs.slice(0, 3).forEach(function(f){
          var li = el('li', f.status);
          li.appendChild(el('b', null, f.title));
          if(f.fix) li.appendChild(el('span', null, f.fix));
          ul.appendChild(li);
        });
        body.appendChild(ul);
        if(probs.length > 3) body.appendChild(el('p', 'scan-more', T('və daha ' + (probs.length - 3) + ' tövsiyə tam hesabatda.', 'plus ' + (probs.length - 3) + ' more in the full report.', 'и ещё ' + (probs.length - 3) + ' рекомендаций в полном отчёте.')));
      }
      var go = el('div', 'scan-go-row');
      var msg = probs.length
        ? 'Salam Ziya! Saytım (' + h + ') SaytYoxla-da ' + r.score + '/100 (' + r.grade + ') aldı. Problemləri düzəltmək istəyirəm.'
        : 'Salam Ziya! Saytım (' + h + ') SaytYoxla-da ' + r.score + '/100 aldı. Sizinlə sayt barədə danışmaq istəyirəm.';
      var wa = el('a', 'btn primary small', probs.length ? T('Bunları düzəldək', 'Fix these with me', 'Исправим это') : T('Yazın, danışaq', 'Message me', 'Напишите мне'));
      wa.href = WA + '?text=' + encodeURIComponent(msg); wa.target = '_blank'; wa.rel = 'noopener';
      var full = el('a', 'btn small', T('Tam hesabat ↗', 'Full report ↗', 'Полный отчёт ↗'));
      full.href = SITE + (lang() === 'az' ? '/' : '/' + lang() + '/') + '?url=' + encodeURIComponent(h); full.target = '_blank'; full.rel = 'noopener';
      go.appendChild(wa); go.appendChild(full); body.appendChild(go);
      card.appendChild(body); out.appendChild(card);
      // animate the ring after it is in the DOM
      var v = ring.querySelector('.v'), C = 2 * Math.PI * 52;
      v.style.strokeDasharray = C; v.style.strokeDashoffset = C;
      requestAnimationFrame(function(){ requestAnimationFrame(function(){ v.style.strokeDashoffset = C * (1 - r.score / 100); }); });
    };
    sf.addEventListener('submit', function(e){
      e.preventDefault();
      var u = inp.value.trim();
      if(!u){ showError(T('Saytın ünvanını yazın, məsələn: example.az', 'Enter a website address, e.g. example.az', 'Введите адрес сайта, например: example.az')); inp.focus(); return; }
      busy(true); out.textContent = ''; out.appendChild(el('div', 'scan-load', T('Sayt yoxlanılır…', 'Checking the site…', 'Проверяем сайт…')));
      var ctl = 'AbortController' in window ? new AbortController() : null, to = setTimeout(function(){ ctl && ctl.abort(); }, 60000);
      fetch(API, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({url:u, lang:lang()}), signal:ctl ? ctl.signal : undefined})
        .then(function(res){ return res.json().catch(function(){ return {}; }).then(function(d){ return {ok:res.ok, d:d}; }); })
        .then(function(x){
          if(x.ok && typeof x.d.score === 'number') render(x.d);
          else showError(x.d && x.d.detail ? String(x.d.detail) : T('Yoxlamaq alınmadı. Bir az sonra yenidən cəhd edin.', 'The check failed. Please try again shortly.', 'Проверка не удалась. Попробуйте чуть позже.'));
        })
        .catch(function(){ showError(T('Bağlantı alınmadı. İnterneti yoxlayıb yenidən cəhd edin.', 'Could not connect. Check your connection and try again.', 'Не удалось подключиться. Проверьте интернет и попробуйте снова.')); })
        .then(function(){ clearTimeout(to); busy(false); });
    });
  }

  /* =================== HORIZONTAL GALLERY =================== */
  var hs = document.querySelector('section.hs');
  if(hs){
    var track = hs.querySelector('.hs-track'), slides = [].slice.call(hs.querySelectorAll('.slide'));
    var cur = hs.querySelector('[data-cur]'), bar = hs.querySelector('.hs-bar i'), chips = [].slice.call(hs.querySelectorAll('[data-jump]'));
    var on = false, dist = 0, lastIdx = -1, top = 0, span = 1, centers = [], ks = [], queued = false;
    function mq(){ return innerWidth >= 900 && innerHeight >= 560 && !reduce; }
    /* all measuring happens here, never during scroll */
    function layout(){
      on = mq(); hs.classList.toggle('hs-on', on);
      track.style.transform = '';
      slides.forEach(function(s){ s.style.opacity = ''; s.style.transform = ''; });
      ks = [];
      if(!on){ hs.style.height = ''; return; }
      centers = slides.map(function(s){ return s.offsetLeft + s.offsetWidth / 2; });
      dist = Math.max(0, centers[centers.length - 1] - centers[0]);
      hs.style.height = (dist + innerHeight) + 'px';
      top = hs.getBoundingClientRect().top + scrollY;
      span = Math.max(1, hs.offsetHeight - innerHeight);
      update();
    }
    function targetFor(i){
      var T = centers[i] - centers[0];
      return top + (dist ? Math.min(1, Math.max(0, T / dist)) : 0) * span;
    }
    function update(){
      queued = false;
      if(!on) return;
      var p = Math.min(1, Math.max(0, (scrollY - top) / span)), x = innerWidth / 2 - centers[0] - p * dist;
      track.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)';
      bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
      var mid = innerWidth / 2, idx = 0, bestD = 1e9;
      for(var i = 0; i < slides.length; i++){
        var d = Math.abs(centers[i] + x - mid), k = Math.max(0, 1 - d / innerWidth);
        k = Math.round(k * 50) / 50;
        if(ks[i] !== k){
          ks[i] = k;
          slides[i].style.opacity = (.25 + k * .75).toFixed(2);
          slides[i].style.transform = 'scale(' + (.9 + k * .1).toFixed(3) + ')';
        }
        if(d < bestD){ bestD = d; idx = i; }
      }
      if(idx !== lastIdx){
        lastIdx = idx; cur.textContent = String(idx + 1).padStart(2, '0');
        slides.forEach(function(s, j){ s.classList.toggle('active', j === idx); });
        var cat = slides[idx].dataset.cat;
        chips.forEach(function(c){ c.classList.toggle('on', c.dataset.jump === cat); });
      }
    }
    function onScroll(){ if(!queued){ queued = true; requestAnimationFrame(update); } }
    chips.forEach(function(c){
      c.addEventListener('click', function(){
        var i = slides.findIndex(function(s){ return s.dataset.cat === c.dataset.jump; });
        if(i < 0) return;
        if(on) scrollTo({top:targetFor(i), behavior:'smooth'});
        else slides[i].scrollIntoView({behavior:'smooth', block:'start'});
      });
    });
    hs.addEventListener('focusin', function(e){
      var s = e.target.closest('.slide'), st = hs.querySelector('.hs-sticky');
      st.scrollLeft = 0; st.scrollTop = 0;
      if(!on || !s) return;
      scrollTo({top:targetFor(slides.indexOf(s))});
    });
    /* phones/tablets: no pinned gallery, so reveal each project as it scrolls into view */
    if('IntersectionObserver' in window && !reduce){
      var sio = new IntersectionObserver(function(es){
        es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('seen'); sio.unobserve(e.target); } });
      }, {threshold:.18, rootMargin:'0px 0px -8% 0px'});
      slides.forEach(function(s){ sio.observe(s); });
    } else slides.forEach(function(s){ s.classList.add('seen'); });
    addEventListener('scroll', onScroll, {passive:true});
    var rz; addEventListener('resize', function(){ clearTimeout(rz); rz = setTimeout(layout, 150); });
    addEventListener('load', layout);
    layout();

    /* fetch and decode every preview up front, while the visitor is still in the hero */
    var imgs = [].slice.call(hs.querySelectorAll('img'));
    function warm(){
      if(!on) return;
      imgs.forEach(function(im, i){
        setTimeout(function(){
          im.loading = 'eager';
          if(im.decode) im.decode().catch(function(){});
        }, i * 60);
      });
    }
    if('requestIdleCallback' in window) requestIdleCallback(warm, {timeout:1500}); else setTimeout(warm, 800);
  }
})();
