/* ============================================
   World: low-resolution (320x140) pixel rooms
   in the key of Ghost in the Shell (1995):
   rain on New Port City rooftops, the canal
   market, a Section-style ops room, the net,
   a data archive, the shell lab, a site under
   construction, and a night street.
   Each room paints a static layer once and
   animates a few things on top each frame.
   ============================================ */

const World = (() => {
  const W = 320, H = 140;
  const { rng, rect, px, ditherV, text, textWidth, vtext, offscreen } = Pixel;

  // ---------- shared pieces ----------

  function skyline(ctx, seed, base, minH, maxH, body, windows, density) {
    const r = rng(seed);
    let x = -4;
    while (x < W) {
      const w = 10 + Math.floor(r() * 22);
      const h = minH + Math.floor(r() * (maxH - minH));
      rect(ctx, x, base - h, w, h, body);
      if (r() < 0.35) rect(ctx, x + Math.floor(w / 3), base - h - 4, 2, 4, body); // antenna
      for (let wy = base - h + 3; wy < base - 2; wy += 3) {
        for (let wx = x + 2; wx < x + w - 2; wx += 3) {
          if (r() < density) px(ctx, wx, wy, windows[Math.floor(r() * windows.length)]);
        }
      }
      x += w + (r() < 0.3 ? 1 : 0);
    }
  }

  function makeRain(n, seed, speed, slant) {
    const r = rng(seed);
    return Array.from({ length: n }, () => ({
      x: r() * W, y: r() * H, v: speed * (0.8 + r() * 0.4), l: 2 + Math.floor(r() * 3), s: slant,
    }));
  }

  function drawRain(ctx, drops, dt, color, floor) {
    ctx.fillStyle = color;
    for (const d of drops) {
      d.y += d.v * dt;
      d.x += d.v * d.s * dt;
      if (d.y > floor) {
        if (floor < H) { ctx.fillRect(Math.round(d.x) - 1, floor, 1, 1); ctx.fillRect(Math.round(d.x) + 1, floor, 1, 1); }
        d.y = -d.l;
        d.x = Math.random() * (W + 40) - 40;
      }
      for (let i = 0; i < d.l; i++) {
        ctx.fillRect(Math.round(d.x + d.s * i), Math.round(d.y + i), 1, 1);
      }
    }
  }

  function neonSign(ctx, label, x, y, color, glow) {
    const w = textWidth(label) + 4;
    rect(ctx, x - 1, y - 1, w + 2, 9, glow);
    rect(ctx, x, y, w, 7, '#0a0710');
    text(ctx, label, x + 2, y + 1, color);
  }

  // ---------- rooms ----------

  const ROOMS = {};

  // 1. Rooftop over New Port City, in the rain
  ROOMS.rooftop = {
    floor: 128,
    build(ctx) {
      ditherV(ctx, 0, 0, W, 104, ['#070814', '#12143a', '#2a2358', '#4b2f63', '#6b3a62']);
      const r = rng(7);
      for (let i = 0; i < 40; i++) px(ctx, Math.floor(r() * W), Math.floor(r() * 40), r() < 0.5 ? '#5a5e9a' : '#34366a');
      skyline(ctx, 11, 104, 20, 64, '#221c44', ['#3b3570', '#463d7c'], 0.18);
      skyline(ctx, 23, 112, 14, 52, '#150f2c', ['#e9b45c', '#6fd6ff', '#f0e3a0', '#ff5fa2'], 0.22);
      // the tall tower
      rect(ctx, 236, 22, 26, 92, '#0e0a1f');
      rect(ctx, 246, 8, 6, 14, '#0e0a1f');
      rect(ctx, 248, 0, 2, 8, '#0e0a1f');
      for (let y = 26; y < 110; y += 4) for (let x = 239; x < 260; x += 4) if ((x * y) % 7 < 3) px(ctx, x, y, '#3fb8d8');
      neonSign(ctx, '2029', 60, 64, '#ff4fa0', '#5a1638');
      neonSign(ctx, 'NEW PORT', 150, 56, '#6ff3ff', '#123f52');
      // near roof
      rect(ctx, 0, 118, W, 22, '#23242d');
      rect(ctx, 0, 118, W, 2, '#4a4b59');
      for (let x = 0; x < W; x += 16) rect(ctx, x, 120, 1, 20, '#1b1c23');
      rect(ctx, 272, 96, 34, 22, '#30323d');
      rect(ctx, 272, 96, 34, 2, '#50535f');
      for (let x = 276; x < 304; x += 4) rect(ctx, x, 100, 2, 14, '#1d1e26');
      rect(ctx, 20, 74, 1, 44, '#3a3b47');
      rect(ctx, 16, 78, 9, 1, '#3a3b47');
    },
    init() { this.rain = makeRain(140, 3, 150, 0.35); this.car = -40; },
    animate(ctx, t, dt) {
      if (Math.floor(t * 1.2) % 2 === 0) px(ctx, 249, 0, '#ff3344');
      if (Math.floor(t * 0.9) % 2 === 0) px(ctx, 20, 73, '#ff3344');
      // neon flicker
      if (Math.sin(t * 13) > 0.97) rect(ctx, 61, 65, 17, 5, '#0a0710');
      // a hover car crossing the sky
      this.car += dt * 22;
      if (this.car > W + 60) this.car = -80;
      rect(ctx, this.car, 30, 8, 2, '#0b0918');
      px(ctx, this.car + 8, 30, '#fff2b0');
      if (Math.floor(t * 4) % 2) px(ctx, this.car, 31, '#ff3344');
      drawRain(ctx, this.rain, dt, 'rgba(150,165,220,0.55)', 128);
    },
  };

  // 2. The canal city: water, signs, reflections
  ROOMS.canal = {
    floor: 132,
    build(ctx) {
      ditherV(ctx, 0, 0, W, 96, ['#1a2626', '#2b3e3b', '#4a615a', '#6c7f70']);
      skyline(ctx, 41, 96, 30, 84, '#243432', ['#8fb3a0', '#c9d6a4'], 0.1);
      skyline(ctx, 43, 96, 16, 56, '#17221f', ['#e9b45c', '#ff6a4a', '#9ce0c8'], 0.16);
      // hanging signs
      const signs = [[28, 40, 'BAR', '#ff5a4a'], [84, 34, 'NET', '#ffd86a'], [196, 30, 'HOTEL', '#7af0d8'], [262, 42, 'EAT', '#ff5a4a']];
      for (const [x, y, s, c] of signs) {
        rect(ctx, x - 1, y - 2, 7, s.length * 6 + 3, '#0c1211');
        vtext(ctx, s, x + 1, y, c);
      }
      rect(ctx, 0, 96, W, 30, '#12211f');
      // quay
      rect(ctx, 0, 126, W, 14, '#3a403c');
      rect(ctx, 0, 126, W, 2, '#626a63');
      for (let x = 6; x < W; x += 40) { rect(ctx, x, 121, 4, 6, '#2a2f2c'); rect(ctx, x, 121, 4, 1, '#565d57'); }
    },
    init(staticCanvas) { this.src = staticCanvas; this.rain = makeRain(60, 9, 110, 0.15); this.boat = -60; },
    animate(ctx, t, dt) {
      // mirrored, rippling reflections of the city in the canal
      for (let y = 0; y < 29; y++) {
        const sy = 95 - y;
        const off = Math.round(Math.sin(t * 2 + y * 0.9) * (1 + y / 14));
        ctx.globalAlpha = 0.42 - y * 0.008;
        ctx.drawImage(this.src, 0, sy, W, 1, off, 97 + y, W, 1);
      }
      ctx.globalAlpha = 1;
      for (let i = 0; i < 18; i++) {
        const x = (i * 37 + Math.floor(t * 8)) % W;
        px(ctx, x, 100 + (i * 7) % 24, 'rgba(180,220,200,0.35)');
      }
      this.boat += dt * 9;
      if (this.boat > W + 40) this.boat = -70;
      const bx = Math.round(this.boat);
      rect(ctx, bx, 112, 30, 4, '#0b1110');
      rect(ctx, bx + 3, 108, 12, 4, '#18211f');
      px(ctx, bx + 26, 110, Math.floor(t * 2) % 2 ? '#ffd86a' : '#b89040');
      drawRain(ctx, this.rain, dt, 'rgba(170,200,190,0.4)', 126);
    },
  };

  // 3. Operations room: wall of monitors, a main display for content
  ROOMS.ops = {
    floor: 132,
    build(ctx) {
      rect(ctx, 0, 0, W, H, '#0b161b');
      for (let x = 0; x < W; x += 20) rect(ctx, x, 0, 1, 118, '#12262d');
      rect(ctx, 0, 10, W, 1, '#15313a');
      // bank of small monitors (left, above the Major)
      for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        const x = 6 + c * 22, y = 18 + r * 18;
        rect(ctx, x, y, 20, 15, '#1e4550');
        rect(ctx, x + 1, y + 1, 18, 13, '#06121a');
      }
      // main display frame (content sits here)
      rect(ctx, 76, 8, 238, 110, '#173640');
      rect(ctx, 78, 10, 234, 106, '#050d12');
      // desks and floor
      rect(ctx, 0, 118, W, 22, '#081116');
      for (let x = 0; x < W; x += 12) rect(ctx, x, 118, 1, 22, '#0f2027');
      rect(ctx, 0, 124, W, 1, '#0f2027');
      rect(ctx, 4, 104, 70, 4, '#223c45');
      rect(ctx, 8, 108, 3, 12, '#162a31');
      rect(ctx, 66, 108, 3, 12, '#162a31');
      rect(ctx, 18, 101, 20, 3, '#0e1d23');
    },
    init() {},
    animate(ctx, t) {
      for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
        const x = 7 + c * 22, y = 19 + r * 18, k = r * 3 + c;
        const col = ['#3ff0c0', '#ffb347', '#6fb8ff'][k % 3];
        if (k % 3 === 0) {
          for (let i = 0; i < 18; i++) px(ctx, x + i, y + 6 + Math.round(Math.sin(t * 3 + i * 0.6 + k) * 4), col);
        } else if (k % 3 === 1) {
          for (let i = 0; i < 5; i++) rect(ctx, x + 2 + i * 3, y + 12 - ((Math.floor(t * 2) + i * k) % 9), 2, (Math.floor(t * 2) + i * k) % 9, col);
        } else {
          const a = t * 2 + k;
          ctx.fillStyle = col;
          for (let i = 0; i < 6; i++) ctx.fillRect(Math.round(x + 9 + Math.cos(a) * i), Math.round(y + 6 + Math.sin(a) * i), 1, 1);
          if (Math.floor(t * 3 + k) % 5 === 0) px(ctx, x + 12, y + 4, '#ffffff');
        }
      }
      if (Math.floor(t * 2) % 2) rect(ctx, 20, 102, 2, 1, '#3ff0c0');
    },
  };

  // 4. The net: grid floor, falling code, linked nodes. The Major appears as a ghost.
  ROOMS.net = {
    floor: 132,
    mode: 'ghost',
    build(ctx) {
      rect(ctx, 0, 0, W, H, '#010604');
      ditherV(ctx, 0, 60, W, 22, ['#010604', '#03170d']);
    },
    init() {
      const r = rng(5);
      this.cols = Array.from({ length: 40 }, (_, i) => ({ x: i * 8 + 2, y: r() * H, v: 20 + r() * 40, seed: Math.floor(r() * 999) }));
      this.nodes = Array.from({ length: 9 }, () => ({ x: 90 + r() * 220, y: 14 + r() * 50, p: r() * 6 }));
    },
    animate(ctx, t, dt) {
      const vx = 160, vy = 80;
      ctx.fillStyle = '#0b4a2c';
      for (let i = -12; i <= 12; i++) {
        for (let y = vy; y < H; y++) {
          const x = vx + (i * 26) * ((y - vy) / (H - vy));
          ctx.fillRect(Math.round(x), y, 1, 1);
        }
      }
      for (let k = 0; k < 8; k++) {
        const z = ((k + (t * 0.6) % 1) / 8);
        const y = Math.round(vy + (H - vy) * z * z);
        ctx.fillStyle = z > 0.5 ? '#1c8a52' : '#0b4a2c';
        ctx.fillRect(0, y, W, 1);
      }
      // falling glyph columns (upper half)
      for (const c of this.cols) {
        c.y += c.v * dt;
        if (c.y > 90) { c.y = -30; }
        for (let i = 0; i < 6; i++) {
          const gy = Math.round(c.y - i * 6);
          if (gy < 0 || gy > 84) continue;
          const g = '0123456789ABCDEFXZ'[(c.seed + i + Math.floor(t * 6)) % 18];
          text(ctx, g, c.x, gy, i === 0 ? '#c8ffe0' : `rgba(61,255,138,${0.5 - i * 0.08})`);
        }
      }
      // linked nodes with travelling pulses
      ctx.strokeStyle = '#1f7a4a';
      for (let i = 0; i < this.nodes.length; i++) {
        const a = this.nodes[i], b = this.nodes[(i + 3) % this.nodes.length];
        const steps = 40;
        for (let s = 0; s < steps; s++) {
          if (s % 2) continue;
          px(ctx, a.x + (b.x - a.x) * s / steps, a.y + (b.y - a.y) * s / steps, '#145c37');
        }
        const f = (t * 0.4 + a.p) % 1;
        px(ctx, a.x + (b.x - a.x) * f, a.y + (b.y - a.y) * f, '#d7ffe9');
      }
      for (const n of this.nodes) {
        const s = 2 + Math.round(Math.sin(t * 2 + n.p));
        px(ctx, n.x, n.y - s, '#5dffa8'); px(ctx, n.x, n.y + s, '#5dffa8');
        px(ctx, n.x - s, n.y, '#5dffa8'); px(ctx, n.x + s, n.y, '#5dffa8');
        px(ctx, n.x, n.y, '#d7ffe9');
      }
    },
  };

  // 5. The archive: shelved data, artifacts on plinths, a hologram
  ROOMS.archive = {
    floor: 130,
    build(ctx) {
      ditherV(ctx, 0, 0, W, 120, ['#0f0b09', '#1d1510', '#2a1d14']);
      for (let s = 0; s < 6; s++) {
        const x = 70 + s * 42;
        rect(ctx, x, 12, 34, 100, '#261b13');
        for (let y = 16; y < 108; y += 8) {
          rect(ctx, x + 2, y, 30, 6, '#140e0a');
          for (let k = 0; k < 7; k++) rect(ctx, x + 3 + k * 4, y + 1, 3, 5, ['#3a2a1c', '#4a3322', '#2e2218'][(s + k + y) % 3]);
        }
      }
      // floor
      rect(ctx, 0, 120, W, 20, '#1a120c');
      for (let x = 0; x < W; x += 24) rect(ctx, x, 120, 1, 20, '#24190f');
      rect(ctx, 0, 120, W, 1, '#3a2a1a');
      // plinths with artifacts: a vessel and an inscribed stele
      rect(ctx, 4, 100, 16, 20, '#3a2f26'); rect(ctx, 4, 100, 16, 2, '#5a4a3a');
      rect(ctx, 8, 90, 8, 10, '#8a5a34'); rect(ctx, 10, 86, 4, 4, '#8a5a34'); rect(ctx, 7, 94, 10, 3, '#9e6c40');
      rect(ctx, 288, 98, 18, 22, '#3a2f26'); rect(ctx, 288, 98, 18, 2, '#5a4a3a');
      rect(ctx, 291, 76, 12, 22, '#6f6656');
      for (let y = 79; y < 96; y += 3) rect(ctx, 293, y, 8, 1, '#4a4336');
    },
    init() {
      const r = rng(17);
      this.leds = Array.from({ length: 60 }, () => ({ x: 73 + Math.floor(r() * 6) * 42 + Math.floor(r() * 7) * 4 + 1, y: 18 + Math.floor(r() * 12) * 8 + 4, p: r() * 10 }));
      this.dust = Array.from({ length: 30 }, () => ({ x: r() * W, y: r() * 120, v: 2 + r() * 4 }));
    },
    animate(ctx, t, dt) {
      for (const l of this.leds) if (Math.sin(t * 2 + l.p) > 0.6) px(ctx, l.x, l.y, (l.p > 5) ? '#ffb347' : '#5fe0d0');
      for (const d of this.dust) {
        d.y -= d.v * dt; d.x += Math.sin(t + d.y) * 0.05;
        if (d.y < 0) d.y = 120;
        px(ctx, d.x, d.y, 'rgba(255,210,150,0.35)');
      }
      // hologram of the vessel, turning
      for (let i = 0; i < 24; i++) {
        const a = t * 1.2 + i * 0.26;
        const yy = 60 + i;
        const rr = 4 + Math.round(Math.sin(i / 23 * Math.PI) * 5);
        px(ctx, 12 + Math.cos(a) * rr, yy, 'rgba(95,224,208,0.8)');
        px(ctx, 12 - Math.cos(a) * rr, yy, 'rgba(95,224,208,0.35)');
      }
    },
  };

  // 6. The shell lab: a body afloat in a tank
  ROOMS.lab = {
    floor: 130,
    build(ctx) {
      ditherV(ctx, 0, 0, W, 120, ['#0c1418', '#13232a', '#1b3038']);
      for (let x = 0; x < W; x += 32) rect(ctx, x, 0, 2, 120, '#0e1a1f');
      for (let i = 0; i < 7; i++) rect(ctx, 250 + i * 4 - 10, 0, 1, 20 + (i % 3) * 6, '#0a1114');
      // tank
      rect(ctx, 236, 20, 60, 98, '#2b3e45');
      rect(ctx, 240, 24, 52, 90, '#0f4f5c');
      ditherV(ctx, 240, 24, 52, 90, ['#1a6d7a', '#0f4f5c', '#0a3a44']);
      rect(ctx, 232, 112, 68, 8, '#3a4e55'); rect(ctx, 232, 16, 68, 6, '#3a4e55');
      // console
      rect(ctx, 150, 96, 60, 24, '#1e2d33'); rect(ctx, 150, 96, 60, 2, '#3a5058');
      rect(ctx, 156, 86, 48, 10, '#0a1418');
      rect(ctx, 0, 120, W, 20, '#0d1519');
      rect(ctx, 0, 120, W, 1, '#2a3c43');
    },
    init() {
      const r = rng(21);
      this.bubbles = Array.from({ length: 22 }, () => ({ x: 243 + r() * 46, y: 24 + r() * 88, v: 6 + r() * 10 }));
    },
    animate(ctx, t, dt) {
      const bob = Math.round(Math.sin(t * 0.8) * 2);
      const c = 'rgba(8,32,38,0.9)';
      // floating shell silhouette, arms slightly out
      rect(ctx, 263, 40 + bob, 6, 6, c);
      rect(ctx, 262, 46 + bob, 8, 18, c);
      rect(ctx, 256, 48 + bob, 6, 2, c); rect(ctx, 270, 48 + bob, 6, 2, c);
      rect(ctx, 253, 50 + bob, 3, 8, c); rect(ctx, 276, 50 + bob, 3, 8, c);
      rect(ctx, 262, 64 + bob, 3, 22, c); rect(ctx, 267, 64 + bob, 3, 22, c);
      for (let i = 0; i < 5; i++) rect(ctx, 264 + (i % 2) * 2, 20, 1, 20 + bob, '#0a1114');
      for (const b of this.bubbles) {
        b.y -= b.v * dt; if (b.y < 26) b.y = 110;
        px(ctx, b.x + Math.sin(t * 3 + b.y) , b.y, 'rgba(190,250,255,0.6)');
      }
      for (let i = 0; i < 10; i++) {
        const on = Math.sin(t * 3 + i) > 0;
        px(ctx, 158 + i * 4, 90, on ? '#3ff0c0' : '#123');
      }
      for (let i = 0; i < 44; i++) px(ctx, 158 + i, 93 - Math.round(Math.abs(Math.sin(t * 4 + i * 0.5)) * 2 * (i % 11 === 0 ? 2 : 0.5)), '#ff6a8a');
    },
  };

  // 7. Under construction: girders, a crane, sparks at dusk
  ROOMS.construction = {
    floor: 130,
    build(ctx) {
      ditherV(ctx, 0, 0, W, 116, ['#1d1432', '#4a2a55', '#9a4a5a', '#e98a4a']);
      skyline(ctx, 61, 116, 10, 40, '#2a1a2e', ['#e9b45c'], 0.08);
      // the building skeleton
      for (let fl = 0; fl < 6; fl++) rect(ctx, 96, 110 - fl * 16, 130, 2, '#1a1220');
      for (let c = 0; c < 6; c++) rect(ctx, 96 + c * 26, 30, 2, 82, '#1a1220');
      for (let fl = 0; fl < 5; fl++) for (let c = 0; c < 5; c++) {
        for (let i = 0; i < 16; i++) px(ctx, 98 + c * 26 + i * 1.5, 110 - fl * 16 - i, '#231829');
      }
      // crane
      rect(ctx, 250, 10, 4, 106, '#1a1220');
      rect(ctx, 170, 10, 130, 3, '#1a1220');
      for (let x = 172; x < 298; x += 6) px(ctx, x, 13, '#1a1220');
      rect(ctx, 290, 13, 8, 8, '#1a1220');
      // ground and barrier
      rect(ctx, 0, 116, W, 24, '#221a1c');
      rect(ctx, 0, 116, W, 1, '#4a3a38');
      for (let x = 0; x < W; x += 8) rect(ctx, x, 120, 4, 5, '#f2c230');
      for (let x = 4; x < W; x += 8) rect(ctx, x, 120, 4, 5, '#141014');
      const label = 'UNDER CONSTRUCTION';
      const lw = textWidth(label) + 6;
      const sx = 262;
      rect(ctx, sx - lw / 2 - 1, 101, lw + 2, 13, '#141014');
      rect(ctx, sx - lw / 2, 102, lw, 11, '#f2c230');
      text(ctx, label, sx - lw / 2 + 3, 105, '#141014');
      rect(ctx, sx - 6, 114, 2, 6, '#3a2e2c'); rect(ctx, sx + 4, 114, 2, 6, '#3a2e2c');
    },
    init() { this.sparks = []; },
    animate(ctx, t, dt) {
      const sway = Math.sin(t * 0.7) * 3;
      const hx = Math.round(200 + sway);
      for (let y = 13; y < 60; y++) px(ctx, 200 + sway * (y - 13) / 47, y, '#120c16');
      rect(ctx, hx - 2, 60, 5, 3, '#120c16');
      rect(ctx, hx - 10, 63, 22, 4, '#2a1f30');
      if (Math.floor(t * 1.5) % 2) px(ctx, 299, 10, '#ff3344');
      if (Math.random() < dt * 3) {
        for (let i = 0; i < 8; i++) this.sparks.push({ x: 174, y: 62, vx: (Math.random() - 0.3) * 40, vy: -Math.random() * 30, life: 0.6 + Math.random() * 0.5 });
      }
      this.sparks = this.sparks.filter(s => (s.life -= dt) > 0);
      for (const s of this.sparks) {
        s.x += s.vx * dt; s.y += s.vy * dt; s.vy += 80 * dt;
        px(ctx, s.x, s.y, s.life > 0.4 ? '#fff2b0' : '#ff9a3a');
      }
      if (Math.floor(t * 12) % 3 === 0) px(ctx, 174, 62, '#ffffff');
    },
  };

  // 8. Night street: shopfronts, cables, passers-by
  ROOMS.street = {
    floor: 132,
    build(ctx) {
      ditherV(ctx, 0, 0, W, 40, ['#07060f', '#161230']);
      const fronts = [['#2a1422', 'RAMEN', '#ff6a4a'], ['#14222a', 'NET CAFE', '#6ff3ff'], ['#221c10', 'BOOKS', '#ffd86a'], ['#1a1030', 'REPAIR', '#c08aff']];
      fronts.forEach(([body, label, neon], i) => {
        const x = i * 80;
        rect(ctx, x, 20, 78, 100, body);
        for (let y = 26; y < 70; y += 8) for (let k = 0; k < 6; k++) rect(ctx, x + 6 + k * 12, y, 6, 4, (y + k + i) % 3 ? '#0c0a12' : '#3a3050');
        rect(ctx, x + 6, 82, 66, 38, '#0c0a12');
        neonSign(ctx, label, x + 39 - (textWidth(label) + 4) / 2, 74, neon, '#1a1420');
        ditherV(ctx, x + 8, 86, 62, 32, ['#1d1826', neon === '#ffd86a' ? '#4a3a18' : '#2a1f3a']);
      });
      for (let x = 0; x < W; x++) px(ctx, x, 16 + Math.round(Math.sin(x / 40) * 3), '#0c0b14');
      for (let i = 0; i < 6; i++) { rect(ctx, 30 + i * 52, 18, 3, 4, '#ff4a4a'); }
      rect(ctx, 0, 120, W, 20, '#15131c');
      rect(ctx, 0, 120, W, 1, '#2d2a38');
    },
    init() {
      const r = rng(31);
      this.people = Array.from({ length: 6 }, (_, i) => ({ x: r() * W, v: (i % 2 ? -1 : 1) * (8 + r() * 8), h: 18 + Math.floor(r() * 6), c: ['#0a0810', '#120e1a', '#0e0c16'][i % 3] }));
      this.rain = makeRain(50, 12, 120, 0.2);
    },
    animate(ctx, t, dt) {
      for (const p of this.people) {
        p.x += p.v * dt;
        if (p.x > W + 10) p.x = -10; if (p.x < -10) p.x = W + 10;
        const step = Math.floor(t * 6 + p.x) % 2;
        rect(ctx, p.x, 131 - p.h, 5, p.h - 6, p.c);
        rect(ctx, p.x + 1, 128 - p.h, 3, 3, p.c);
        rect(ctx, p.x + (step ? 0 : 1), 125, 2, 6, p.c);
        rect(ctx, p.x + (step ? 3 : 2), 125, 2, 6, p.c);
      }
      for (let i = 0; i < 4; i++) {
        const y = 110 - ((t * 10 + i * 7) % 28);
        px(ctx, 40 + Math.sin(t + i) * 3, y, 'rgba(220,220,230,0.25)');
      }
      drawRain(ctx, this.rain, dt, 'rgba(160,160,210,0.4)', 132);
    },
  };

  // ---------- runtime ----------

  const cache = {};
  let current = null, currentKey = null;

  function load(key) {
    if (!cache[key]) {
      const room = ROOMS[key];
      const { canvas, ctx } = offscreen(W, H);
      room.build(ctx);
      room.init && room.init(canvas);
      cache[key] = { room, canvas };
    }
    currentKey = key;
    current = cache[key];
  }

  function render(ctx, t, dt) {
    if (!current) return;
    ctx.drawImage(current.canvas, 0, 0);
    current.room.animate(ctx, t, dt);
  }

  function floor() { return current ? current.room.floor : 130; }
  function mode() { return current && current.room.mode === 'ghost' ? 'ghost' : 'shell'; }

  return { W, H, load, render, floor, mode, rooms: Object.keys(ROOMS), get key() { return currentKey; } };
})();
