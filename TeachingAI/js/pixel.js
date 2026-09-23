/* ============================================
   Pixel helpers: seeded random, dithering,
   and a tiny 3x5 font for signs painted into
   the low-resolution world canvas
   ============================================ */

const Pixel = (() => {
  function rng(seed) {
    let a = seed >>> 0;
    return () => {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function rect(ctx, x, y, w, h, c) {
    ctx.fillStyle = c;
    ctx.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h));
  }

  function px(ctx, x, y, c) {
    ctx.fillStyle = c;
    ctx.fillRect(Math.round(x), Math.round(y), 1, 1);
  }

  const BAYER = [
    [0, 8, 2, 10],
    [12, 4, 14, 6],
    [3, 11, 1, 9],
    [15, 7, 13, 5],
  ];

  /** Vertical gradient through a list of colors, blended with 4x4 ordered dithering. */
  function ditherV(ctx, x, y, w, h, colors) {
    const bands = colors.length - 1;
    for (let j = 0; j < h; j++) {
      const f = (j / Math.max(1, h - 1)) * bands;
      const i = Math.min(bands - 1, Math.floor(f));
      const frac = f - i;
      for (let k = 0; k < w; k++) {
        const threshold = (BAYER[(y + j) & 3][(x + k) & 3] + 0.5) / 16;
        ctx.fillStyle = frac > threshold ? colors[i + 1] : colors[i];
        ctx.fillRect(x + k, y + j, 1, 1);
      }
    }
  }

  // 3x5 glyphs, rows top to bottom, 3 bits each
  const FONT = {
    A: [2, 5, 7, 5, 5], B: [6, 5, 6, 5, 6], C: [3, 4, 4, 4, 3], D: [6, 5, 5, 5, 6],
    E: [7, 4, 6, 4, 7], F: [7, 4, 6, 4, 4], G: [3, 4, 5, 5, 3], H: [5, 5, 7, 5, 5],
    I: [7, 2, 2, 2, 7], J: [1, 1, 1, 5, 2], K: [5, 5, 6, 5, 5], L: [4, 4, 4, 4, 7],
    M: [5, 7, 7, 5, 5], N: [6, 5, 5, 5, 5], O: [2, 5, 5, 5, 2], P: [6, 5, 6, 4, 4],
    Q: [2, 5, 5, 6, 3], R: [6, 5, 6, 5, 5], S: [3, 4, 2, 1, 6], T: [7, 2, 2, 2, 2],
    U: [5, 5, 5, 5, 7], V: [5, 5, 5, 5, 2], W: [5, 5, 7, 7, 5], X: [5, 5, 2, 5, 5],
    Y: [5, 5, 2, 2, 2], Z: [7, 1, 2, 4, 7],
    0: [7, 5, 5, 5, 7], 1: [2, 6, 2, 2, 7], 2: [6, 1, 2, 4, 7], 3: [6, 1, 2, 1, 6],
    4: [5, 5, 7, 1, 1], 5: [7, 4, 6, 1, 6], 6: [3, 4, 7, 5, 7], 7: [7, 1, 2, 2, 2],
    8: [7, 5, 7, 5, 7], 9: [7, 5, 7, 1, 6],
    '/': [1, 1, 2, 4, 4], '-': [0, 0, 7, 0, 0], '.': [0, 0, 0, 0, 2], ':': [0, 2, 0, 2, 0],
    '>': [4, 2, 1, 2, 4], '!': [2, 2, 2, 0, 2], '#': [5, 7, 5, 7, 5], ' ': [0, 0, 0, 0, 0],
  };

  function text(ctx, str, x, y, c) {
    ctx.fillStyle = c;
    let cx = Math.round(x);
    for (const ch of String(str).toUpperCase()) {
      const g = FONT[ch] || FONT[' '];
      for (let r = 0; r < 5; r++) {
        for (let b = 0; b < 3; b++) {
          if (g[r] & (4 >> b)) ctx.fillRect(cx + b, Math.round(y) + r, 1, 1);
        }
      }
      cx += 4;
    }
  }

  function textWidth(str) {
    return String(str).length * 4 - 1;
  }

  /** Vertical sign: one glyph per row. */
  function vtext(ctx, str, x, y, c) {
    let cy = y;
    for (const ch of String(str)) {
      text(ctx, ch, x, cy, c);
      cy += 6;
    }
  }

  function offscreen(w, h) {
    const c = document.createElement('canvas');
    c.width = w;
    c.height = h;
    const ctx = c.getContext('2d');
    ctx.imageSmoothingEnabled = false;
    return { canvas: c, ctx };
  }

  return { rng, rect, px, ditherV, text, textWidth, vtext, offscreen };
})();
