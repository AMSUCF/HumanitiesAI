/* ============================================
   The Major: a cyborg guide in profile.
   Frames are composed from pixel maps (head,
   torso, swinging arm, rasterized legs), then
   outlined automatically. Two render modes:
   'shell' (full color) and 'ghost' (the net:
   a green wireframe of the same body).
   ============================================ */

const Avatar = (() => {
  const PAL = {
    H: '#3b2c66', h: '#5f4aa6', S: '#ecc8ae', s: '#c99a84', E: '#1b2d4a',
    e: '#7df0ff', M: '#b0676d', J: '#262a35', j: '#3f4558', T: '#8a2440',
    B: '#6a5a44', b: '#a8925f', P: '#1a1e2b', p: '#11141d', O: '#0d0e13',
    o: '#34353f', K: '#07060c',
  };

  // Facing right. '.' is empty. Width 16; frames are padded by 1 for the outline.
  const HEAD = [
    '......HHHH......',
    '.....HHHHHH.....',
    '....HHHHHhhH....',
    '...HHHHHHHhhH...',
    '...HHHHHHHHHHH..',
    '...HHHHHHHHHHS..',
    '...HHHHHHHHSSS..',
    '...HHHHHHHSSESS.',
    '...HHHHHHHSSSSSS',
    '...HHHHHHHsSSSS.',
    '...HHHHHHHHsMS..',
    '....HHHHHH.sSS..',
    '..........sSs...',
  ];

  const TORSO = [
    '........JJJJ....',
    '.......JJJJTJ...',
    '......JJJJJTTJ..',
    '......JJJJJTTJ..',
    '......JJJJJTTJ..',
    '......JJJJJTTJ..',
    '......JJJJJTJJ..',
    '......BBBBBbBB..',
    '......JJJJJJJJ..',
  ];

  const W = 16, H = 34, HIP_Y = 22, HIP_X = 10;

  // [backFootX, frontFootX, backLift, frontLift, handDX]
  const POSES = {
    idle:  [9, 11, 0, 0, 0],
    walk1: [6, 13, 0, 0, 2],
    walk2: [9, 10, 1, 0, 0],
    walk3: [13, 7, 0, 0, -2],
    walk4: [10, 9, 0, 1, 0],
  };

  function blank() {
    return Array.from({ length: H }, () => Array(W).fill('.'));
  }

  function stamp(grid, rows, top) {
    rows.forEach((row, r) => {
      [...row].forEach((ch, c) => {
        if (ch !== '.') grid[top + r][c] = ch;
      });
    });
  }

  function leg(grid, footX, lift, fill, shade) {
    const bottom = 30 - lift;
    for (let y = HIP_Y; y <= bottom; y++) {
      const t = (y - HIP_Y) / (bottom - HIP_Y);
      const x = Math.round(HIP_X + (footX - HIP_X) * t);
      for (let dx = -1; dx <= 1; dx++) {
        const xx = x + dx;
        if (xx >= 0 && xx < W) grid[y][xx] = dx === 1 ? shade : fill;
      }
    }
    // boot, toe pointing right
    for (let y = bottom + 1; y <= bottom + 3 && y < H; y++) {
      for (let xx = footX - 1; xx <= footX + 2; xx++) {
        if (xx >= 0 && xx < W) grid[y][xx] = (y === bottom + 1 && xx === footX) ? 'o' : 'O';
      }
    }
  }

  function arm(grid, handDX) {
    // shoulder near (8,14); sleeve runs down to the hand
    for (let y = 14; y <= 20; y++) {
      const t = (y - 14) / 6;
      const x = Math.round(8 + handDX * t);
      grid[y][x] = 'j';
      grid[y][x + 1] = 'j';
      if (x - 1 >= 0 && grid[y][x - 1] !== '.') grid[y][x - 1] = 'K';
    }
    const hx = Math.round(8 + handDX);
    grid[21][hx] = 'S';
    grid[21][hx + 1] = 's';
    grid[22][hx] = 's';
  }

  function compose(pose, blink) {
    const [bx, fx, bl, fl, hand] = POSES[pose];
    const g = blank();
    leg(g, bx, bl, 'p', 'p');
    leg(g, fx, fl, 'P', 'p');
    stamp(g, TORSO, 13);
    stamp(g, HEAD, 0);
    arm(g, hand);
    if (blink) g[7][12] = 'S';
    return g;
  }

  /** Paint a grid into a padded canvas; ghost mode draws only the outline and a sparse fill. */
  function paint(grid, mode) {
    const { canvas, ctx } = Pixel.offscreen(W + 2, H + 2);
    const filled = (y, x) => y >= 0 && y < H && x >= 0 && x < W && grid[y][x] !== '.';
    for (let y = -1; y <= H; y++) {
      for (let x = -1; x <= W; x++) {
        if (filled(y, x)) {
          const ch = grid[y][x];
          if (mode === 'ghost') {
            if ((x + y) % 3 === 0) Pixel.px(ctx, x + 1, y + 1, 'rgba(90,255,170,0.35)');
            if (ch === 'E') Pixel.px(ctx, x + 1, y + 1, '#d7ffe9');
          } else {
            Pixel.px(ctx, x + 1, y + 1, PAL[ch]);
          }
        } else if (filled(y - 1, x) || filled(y + 1, x) || filled(y, x - 1) || filled(y, x + 1)) {
          Pixel.px(ctx, x + 1, y + 1, mode === 'ghost' ? '#5dffa8' : PAL.K);
        }
      }
    }
    return canvas;
  }

  const FRAMES = { shell: {}, ghost: {} };
  for (const mode of ['shell', 'ghost']) {
    for (const pose of Object.keys(POSES)) {
      FRAMES[mode][pose] = paint(compose(pose, false), mode);
    }
    FRAMES[mode].blink = paint(compose('idle', true), mode);
  }

  // --- state ---
  let x = 40, targetX = 40, facing = 1, walkT = 0, visible = true;
  let camo = 0; // 0 = solid, 1 = fully cloaked (thermoptic camouflage)
  let camoTarget = 0;
  const SPEED = 24; // world px per second: an unhurried walk-in

  function setTarget(tx, instant) {
    targetX = tx;
    if (instant) x = tx;
  }

  function cloak(on) { camoTarget = on ? 1 : 0; }
  function isWalking() { return Math.abs(targetX - x) > 0.5; }
  function isSettled() { return !isWalking() && Math.abs(camo - camoTarget) < 0.01; }
  function setVisible(v) { visible = v; }

  function update(dt) {
    const d = targetX - x;
    if (Math.abs(d) > 0.5) {
      facing = d > 0 ? 1 : -1;
      x += Math.sign(d) * Math.min(Math.abs(d), SPEED * dt);
      walkT += dt;
    } else {
      x = targetX;
      walkT = 0;
    }
    const c = camoTarget - camo;
    camo += Math.sign(c) * Math.min(Math.abs(c), dt * 1.6);
  }

  /**
   * Draw the avatar standing on floorY. The world canvas must already hold
   * the room so the cloak can bend the background through the silhouette.
   */
  function draw(ctx, floorY, mode, t) {
    if (!visible) return;
    let pose = 'idle';
    if (isWalking()) {
      pose = ['walk1', 'walk2', 'walk3', 'walk4'][Math.floor(walkT * 5) % 4];
    } else if (t % 4.2 < 0.14) {
      pose = 'blink';
    }
    const frame = FRAMES[mode === 'ghost' ? 'ghost' : 'shell'][pose];
    const bob = !isWalking() && (t % 2) < 1 ? 0 : 0;
    const dx = Math.round(x - frame.width / 2);
    const dy = Math.round(floorY - frame.height + 1 + bob);

    if (camo <= 0.01) {
      drawFrame(ctx, frame, dx, dy);
      return;
    }
    // Thermoptic camouflage: refract the scene behind the body, fade the body out.
    const w = frame.width, h = frame.height;
    const bg = ctx.getImageData(dx, dy, w, h);
    const fr = frame.getContext('2d').getImageData(0, 0, w, h);
    const out = ctx.createImageData(w, h);
    for (let yy = 0; yy < h; yy++) {
      const shift = Math.round(Math.sin(t * 9 + yy * 0.7) * 2 * camo);
      for (let xx = 0; xx < w; xx++) {
        const i = (yy * w + xx) * 4;
        const a = fr.data[i + 3];
        if (!a) { out.data[i + 3] = 0; continue; }
        const sx = Math.min(w - 1, Math.max(0, xx + shift));
        const j = (yy * w + sx) * 4;
        const keep = 1 - camo;
        out.data[i] = fr.data[i] * keep + bg.data[j] * camo;
        out.data[i + 1] = fr.data[i + 1] * keep + bg.data[j + 1] * camo;
        out.data[i + 2] = fr.data[i + 2] * keep + bg.data[j + 2] * camo + 18 * camo;
        out.data[i + 3] = camo > 0.97 ? 60 : 255;
      }
    }
    const { canvas, ctx: octx } = Pixel.offscreen(w, h);
    octx.putImageData(out, 0, 0);
    drawFrame(ctx, canvas, dx, dy);
  }

  function drawFrame(ctx, img, dx, dy) {
    if (facing < 0) {
      ctx.save();
      ctx.translate(dx + img.width, dy);
      ctx.scale(-1, 1);
      ctx.drawImage(img, 0, 0);
      ctx.restore();
    } else {
      ctx.drawImage(img, dx, dy);
    }
  }

  return { setTarget, cloak, update, draw, isWalking, isSettled, setVisible, get x() { return x; } };
})();
