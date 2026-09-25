/* ============================================
   Engine: scaling, scene changes, panels,
   dialogue typewriter, navigation (keys,
   clicker, click, #hash), and the render loop
   ============================================ */

const Engine = (() => {
  const $ = (id) => document.getElementById(id);
  const stage = $('stage'), viewport = $('viewport'), content = $('content'), fx = $('fx');
  const canvas = $('world'), ctx = canvas.getContext('2d');
  const dialogue = $('dialogue-text');
  ctx.imageSmoothingEnabled = false;

  const SECTIONS = [
    { id: 'intro', label: 'INTRO', name: '01 // COURSE INTRODUCTION' },
    { id: 'objectives', label: 'GOALS', name: '02 // OBJECTIVES + COMPETENCIES' },
    { id: 'philosophy', label: 'DESIGN', name: '03 // DESIGN PHILOSOPHY' },
    { id: 'topics', label: 'TOPICS', name: '04 // TOPICS + ASSESSMENT' },
    { id: 'assignments', label: 'MAKING', name: '05 // EXEMPLARY ASSIGNMENTS' },
    { id: 'feedback', label: 'VOICES', name: '06 // STUDENT RESPONSE' },
  ];

  let index = -1, busy = false, typer = null, debug = false, skipWalk = false;

  // ---------- scaling ----------
  function fit() {
    const s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    stage.style.transform = `scale(${s})`;
    stage.style.left = ((window.innerWidth - 1280 * s) / 2) + 'px';
    stage.style.top = ((window.innerHeight - 720 * s) / 2) + 'px';
  }

  // ---------- panels ----------
  const esc = (s) => String(s);

  function box(p, def) {
    const b = Object.assign({ x: 300, y: 18, w: 950, h: 490 }, def || {}, p.box || {});
    return `left:${b.x}px;top:${b.y}px;width:${b.w}px;${b.auto ? '' : `height:${b.h}px;`}`;
  }

  function tag(p) {
    if (!p.tag && !p.tagRight) return '';
    return `<div class="tag"><span>${esc(p.tag || '')}</span><span class="right">${esc(p.tagRight || '')}</span></div>`;
  }

  const RENDER = {
    title: (p) => `<section class="panel title" style="${box(p, { x: 360, y: 60, w: 860, auto: true })}">
        <div class="kicker">${p.kicker}</div><h1>${p.title}</h1><div class="sub">${p.sub}</div>
        <div class="byline">${p.byline}</div><div class="start">PRESS &#9654; OR CLICK TO JACK IN</div></section>`,

    quote: (p) => `<section class="panel quote" style="${box(p, { auto: true })}">${tag(p)}
        ${p.heading ? `<h2>${p.heading}</h2>` : ''}<blockquote>${p.text}</blockquote>
        ${p.cite ? `<cite>${p.cite}</cite>` : ''}${p.note ? `<p class="note small">${p.note}</p>` : ''}</section>`,

    text: (p) => `<section class="panel" style="${box(p, { auto: true })}">${tag(p)}
        ${p.heading ? `<h2>${p.heading}</h2>` : ''}${p.body}</section>`,

    list: (p) => `<section class="panel" style="${box(p, { auto: true })}">${tag(p)}
        ${p.heading ? `<h2>${p.heading}</h2>` : ''}
        <${p.ordered ? 'ol' : 'ul'}>${p.items.map(i => `<li>${i}</li>`).join('')}</${p.ordered ? 'ol' : 'ul'}>
        ${p.after || ''}</section>`,

    stats: (p) => `<section class="panel" style="${box(p, { auto: true })}">${tag(p)}
        ${p.heading ? `<h2>${p.heading}</h2>` : ''}
        <div class="stats">${p.items.map(s => `<div class="stat${s.flag ? ' flag' : ''}"><div class="k">${s.k}</div><div class="v">${s.v}</div></div>`).join('')}</div>
        ${p.after || ''}</section>`,

    cards: (p) => `<section class="panel" style="${box(p, { auto: true })}">${tag(p)}
        ${p.heading ? `<h2>${p.heading}</h2>` : ''}
        <div class="cards" style="grid-template-columns:repeat(${p.cols || 2},1fr)">${p.items.map(c =>
          `<div class="card ${c.cls}"><div class="name">${c.name}</div><div class="weeks">${c.weeks}</div><p>${c.text}</p></div>`).join('')}</div>
        ${p.after || ''}</section>`,

    weeks: (p) => `<section class="panel" style="${box(p)}">${tag(p)}
        <table class="weeks"><thead><tr><th></th><th>WK</th><th>TITLE</th><th>EXERCISE</th><th>TOOLS</th></tr></thead><tbody>
        ${p.rows.map(r => `<tr class="${r[0]}"><td class="unit"></td><td class="wk">${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td class="tool">${r[4]}</td></tr>`).join('')}
        </tbody></table></section>`,

    compare: (p) => `<section class="panel" style="${box(p, { auto: true })}">${tag(p)}
        ${p.heading ? `<h2>${p.heading}</h2>` : ''}
        <div class="compare"><div class="h"></div><div class="h">${p.left || '2025'}</div><div class="h">${p.right || '2026'}</div>
        ${p.rows.map(r => `<div class="k">${r[0]}</div><div class="old">${r[1]}</div><div class="new">${r[2]}</div>`).join('')}</div>
        ${p.after || ''}</section>`,

    lineage: (p) => `<section class="panel" style="${box(p, { auto: true })}">${tag(p)}
        ${p.heading ? `<h2>${p.heading}</h2>` : ''}
        <div class="lineage">${p.rows.map(r => `<div class="who">${r.who}</div><div class="chain">${r.chain.map((c, i) =>
          (i ? '<i>&rarr;</i>' : '') + `<span class="${c.s || ''}">${c.t}</span>`).join('')}</div>`).join('')}</div>
        ${p.after || ''}</section>`,

    grades: (p) => `<section class="panel" style="${box(p, { auto: true })}">${tag(p)}
        ${p.heading ? `<h2>${p.heading}</h2>` : ''}${p.body || ''}</section>`,

    image: (p) => `<section class="panel media" style="${box(p)}">
        <div class="bar"><span>${p.label}</span>${p.href ? `<a href="${p.href}" target="_blank" rel="noopener">OPEN &#8599;</a>` : ''}</div>
        <div class="screen"><img src="${p.src}" alt="${p.alt || ''}"></div>
        ${p.caption ? `<div class="caption">${p.caption}</div>` : ''}</section>`,

    embed: (p) => `<section class="panel media embed" style="${box(p)}" data-zoom="${p.zoom || 0.7}">
        <div class="bar"><span><span class="live">&#9679; LIVE</span> &nbsp;${p.label}</span><a href="${p.src}" target="_blank" rel="noopener">OPEN &#8599;</a></div>
        <div class="screen"><iframe src="${p.src}" title="${p.label}" referrerpolicy="${p.referrer || 'no-referrer'}" allow="${p.allow || ''}" allowfullscreen></iframe></div>
        ${p.caption ? `<div class="caption">${p.caption}</div>` : ''}</section>`,

    video: (p) => `<section class="panel media" style="${box(p)}">
        <div class="bar"><span>${p.label}</span></div>
        <div class="screen"><video src="${p.src}"${p.poster ? ` poster="${p.poster}"` : ''} controls preload="metadata"></video></div>
        ${p.caption ? `<div class="caption">${p.caption}</div>` : ''}</section>`,

    voices: (p) => `<section class="panel" style="${box(p, { auto: true })}">${tag(p)}
        <div class="voices">${p.items.map(v => `<figure class="voice"><blockquote>${v.q}</blockquote>
          <figcaption>— ENG 6806 STUDENT, ${v.a.toUpperCase()}</figcaption></figure>`).join('')}</div></section>`,

    placeholder: (p) => `<section class="panel placeholder" style="${box(p, { auto: true })}">${tag(p)}
        <div class="glyph">${p.glyph || '[ ? ]'}</div><h2>${p.heading}</h2>${p.body || ''}</section>`,
  };

  function renderPanels(scene) {
    engaged = false;
    $('focus-hint').classList.add('hidden');
    const panels = scene.panels || (scene.panel ? [scene.panel] : []);
    content.innerHTML = panels.map(p => RENDER[p.type](p)).join('');
    content.querySelectorAll('.embed').forEach(sizeEmbed);
  }

  /** Render embeds at desktop width and scale them down to fit their screen. */
  function sizeEmbed(panel) {
    const screen = panel.querySelector('.screen');
    const frame = panel.querySelector('iframe');
    const z = parseFloat(panel.dataset.zoom);
    const w = screen.clientWidth, h = screen.clientHeight;
    frame.style.width = (w / z) + 'px';
    frame.style.height = (h / z) + 'px';
    frame.style.transform = `scale(${z})`;
    frame.addEventListener('mouseleave', () => { engaged = false; releaseFocus(); });
    frame.addEventListener('mouseenter', () => { engaged = true; $('focus-hint').classList.remove('hidden'); });
  }

  // Embedded demos often focus their own input when they load, which would swallow the
  // arrow keys and clicker. Until the pointer is actually over a demo, take focus back.
  let engaged = false;
  window.addEventListener('blur', () => {
    setTimeout(() => {
      const el = document.activeElement;
      if (el && el.tagName === 'IFRAME' && !engaged) { el.blur(); window.focus(); }
    }, 0);
  });

  function releaseFocus() {
    $('focus-hint').classList.add('hidden');
    if (document.activeElement && document.activeElement.tagName === 'IFRAME') document.activeElement.blur();
    window.focus();
  }

  // ---------- dialogue ----------
  // html (optional) replaces the typed text once it finishes, so links can live in the dialogue
  function type(text, html) {
    clearInterval(typer);
    dialogue.textContent = '';
    dialogue.classList.add('typing');
    let i = 0;
    typer = setInterval(() => {
      i += 2;
      dialogue.textContent = text.slice(0, i);
      if (i >= text.length) {
        clearInterval(typer);
        dialogue.classList.remove('typing');
        if (html) dialogue.innerHTML = html;
      }
    }, 16);
  }

  // ---------- HUD ----------
  function buildNav() {
    const nav = $('hud-sections');
    nav.innerHTML = SECTIONS.map(s => `<button data-s="${s.id}">${s.label}</button>`).join('');
    nav.addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b) return;
      e.stopPropagation();
      const target = SCENES.findIndex(sc => sc.section === b.dataset.s);
      if (target >= 0) go(target);
    });
  }

  function updateHud(scene) {
    const sec = SECTIONS.find(s => s.id === scene.section);
    $('hud-section').textContent = sec ? sec.name : 'TEACHING AI // ENG 6806';
    document.querySelectorAll('#hud-sections button').forEach(b => b.classList.toggle('active', !!sec && b.dataset.s === sec.id));
    $('hud-construction').classList.toggle('hidden', !scene.construction);
    const n = String(SCENES.length - 1).padStart(2, '0');
    $('hud-counter').textContent = `${String(index).padStart(2, '0')}/${n}`;
    $('speaker').textContent = scene.speaker || 'A. SALTER';
    $('next-btn').style.visibility = index === SCENES.length - 1 ? 'hidden' : '';
  }

  // ---------- scene changes ----------
  const wait = (ms) => new Promise(r => setTimeout(r, ms));

  async function go(i, instant) {
    if (busy) { skipWalk = true; return; }     // a press mid-walk just finishes the walk
    if (i < 0 || i >= SCENES.length || i === index) return;
    busy = true;
    skipWalk = false;
    const scene = SCENES[i];
    const prev = SCENES[index];
    index = i;
    history.replaceState(null, '', '#' + i);

    const old = content.querySelectorAll('.panel');
    old.forEach(p => p.classList.add('out'));

    const roomChanges = !prev || prev.room !== scene.room;
    if (roomChanges && !instant && prev) {
      clearInterval(typer);
      dialogue.textContent = '';
      Avatar.cloak(true);
      await wait(380);
      const kind = scene.transition || (scene.room === 'net' || prev.room === 'net' ? 'dive' : 'fade');
      fx.className = '';
      void fx.offsetWidth;
      fx.className = kind;
      await wait(kind === 'dive' ? 450 : 330);
      World.load(scene.room);
      Avatar.setTarget(-14, true);               // enter from the left edge…
      Avatar.setTarget(scene.x ?? 40);           // …and walk in while decloaking
      await wait(kind === 'dive' ? 450 : 330);
      Avatar.cloak(false);
      // let the room breathe: content arrives once the Major has stopped walking
      const t0 = performance.now();
      while (Avatar.isWalking() && !skipWalk && performance.now() - t0 < 5000) await wait(50);
      if (Avatar.isWalking()) Avatar.setTarget(scene.x ?? 40, true);
      await wait(skipWalk ? 0 : 250);
    } else {
      if (roomChanges) World.load(scene.room);
      // same room: pace a little between scenes so the Major keeps moving
      const base = scene.x ?? 40;
      const x = instant || roomChanges ? base : base + (i % 2 ? 14 : 0);
      Avatar.setTarget(x, instant || roomChanges);
      await wait(instant ? 0 : 180);
    }
    Avatar.setVisible(scene.avatar !== false);

    renderPanels(scene);
    updateHud(scene);
    const html = scene.dialogueHtml;
    type(html ? html.replace(/<[^>]+>/g, '') : (scene.dialogue || ''), html);
    if (debug) $('debug').textContent = `scene ${i} · room ${scene.room} · x ${scene.x ?? 40}`;
    busy = false;
  }

  function next() { go(index + 1); }
  function prev() { go(index - 1); }

  // ---------- input ----------
  function bind() {
    document.addEventListener('keydown', (e) => {
      if (e.target.closest && e.target.closest('input, textarea')) return;
      switch (e.key) {
        case 'ArrowRight': case 'ArrowDown': case 'PageDown': case ' ': case 'Enter':
          e.preventDefault(); next(); break;
        case 'ArrowLeft': case 'ArrowUp': case 'PageUp': case 'Backspace':
          e.preventDefault(); prev(); break;
        case 'Home': e.preventDefault(); go(0); break;
        case 'End': e.preventDefault(); go(SCENES.length - 1); break;
        case 'f': case 'F':
          if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen();
          break;
        case 'd': case 'D':
          debug = !debug; $('debug').classList.toggle('hidden', !debug);
          $('debug').textContent = `scene ${index} · room ${World.key}`;
          break;
      }
    });
    viewport.addEventListener('click', (e) => {
      if (e.target.closest('a, button, iframe, input, .panel.media, #hud')) return;
      next();
    });
    $('next-btn').addEventListener('click', next);
    $('prev-btn').addEventListener('click', prev);
    window.addEventListener('hashchange', () => {
      const h = parseInt(location.hash.slice(1), 10);
      if (!isNaN(h) && h !== index) go(h, true);
    });
    window.addEventListener('resize', () => { fit(); content.querySelectorAll('.embed').forEach(sizeEmbed); });
  }

  // ---------- render loop ----------
  let last = performance.now(), clock = 0;
  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    clock += dt;
    World.render(ctx, clock, dt);
    Avatar.update(dt);
    Avatar.draw(ctx, World.floor(), World.mode(), clock);
    requestAnimationFrame(frame);
  }

  function start() {
    fit();
    buildNav();
    bind();
    const h = parseInt(location.hash.slice(1), 10);
    const first = !isNaN(h) && h >= 0 && h < SCENES.length ? h : 0;
    go(first, true);
    requestAnimationFrame(frame);
  }

  return { start, go, next, prev };
})();

document.fonts.ready.then(() => Engine.start());
