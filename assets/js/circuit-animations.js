// ============================================
// HUMANITIES IN THE AGE OF AI - HEADER ART + PAGE INTERACTIONS
// ============================================
// The old circuit-board header animation has been repurposed into a
// falling-data / thermoptic-shimmer motif (see THEME_README.md at the repo
// root for the full writeup). Everything below `initializeDataStream` /
// `initializeGhostReveal` is unrelated general-site behavior kept as-is.

// ---- Falling-data column drift --------------------------------------------
// Places a sparse set of vertical glyph columns inside a `.data-stream-svg`.
// Placement (position/content/timing offsets) happens here in JS, but all
// *movement* is driven purely by the `dataDrift` CSS keyframe, which only
// exists inside `@media (prefers-reduced-motion: no-preference)` in
// style.scss. That means under reduced motion the columns simply render at
// the position placed here -- the required static "first frame" -- with no
// extra branching needed in this file.
const DATA_GLYPHS = ['0', '1', 'ø', 'λ', 'Ω', '§', '∆', '¶'];

function randomGlyphString(length) {
  let out = '';
  for (let i = 0; i < length; i++) {
    out += DATA_GLYPHS[Math.floor(Math.random() * DATA_GLYPHS.length)];
  }
  return out;
}

function buildDataStream(svg, { columns, rows, viewWidth, viewHeight }) {
  if (!svg) return;

  svg.innerHTML = '';

  const spacing = viewWidth / columns;

  for (let c = 0; c < columns; c++) {
    // Sparse: skip roughly a third of the grid at random so the header
    // stays subtle instead of filling with glyphs edge-to-edge.
    if (Math.random() < 0.35) continue;

    // Two nested groups because CSS transforms OVERRIDE the SVG transform
    // attribute: the drift animation sets a CSS transform on the inner
    // group, so horizontal placement must live on a separate outer group
    // or every column collapses to x=0 at the left edge.
    const pos = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    const x = Math.round(c * spacing + spacing / 2);
    pos.setAttribute('transform', `translate(${x}, 0)`);

    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'data-glyph-col');

    // Slow, staggered drift (8-18s) with a negative delay so columns start
    // mid-cycle instead of all animating in lockstep.
    const duration = 8 + Math.random() * 10;
    const delay = Math.random() * duration;
    g.style.animationDuration = `${duration}s`;
    g.style.animationDelay = `-${delay}s`;

    const glyphs = randomGlyphString(rows);
    for (let r = 0; r < rows; r++) {
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', 0);
      text.setAttribute('y', Math.round((r / rows) * viewHeight * 2));
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('font-size', 16);
      text.textContent = glyphs[r];
      g.appendChild(text);
    }
    pos.appendChild(g);
    svg.appendChild(pos);
  }
}

function initializeDataStream() {
  const mainSvg = document.querySelector('#header-container .data-stream-svg');
  buildDataStream(mainSvg, { columns: 16, rows: 10, viewWidth: 1200, viewHeight: 400 });

  const compactSvg = document.querySelector('#compact-header .data-stream-svg');
  buildDataStream(compactSvg, { columns: 12, rows: 4, viewWidth: 1200, viewHeight: 120 });
}

// ---- Ghost-silhouette scroll reveal ----------------------------------------
// The silhouette (pure CSS shapes colored with var(--text) in style.scss,
// so it always contrasts correctly against the header background in both
// themes) grows slightly more visible once the reader scrolls past the
// header. Under reduced motion we skip the scroll listener entirely and
// leave the silhouette at its CSS resting opacity -- that resting state IS
// the static first frame required by the brief.
function initializeGhostReveal() {
  const silhouette = document.querySelector('.ghost-silhouette');
  if (!silhouette) return;

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const reveal = () => {
    silhouette.classList.toggle('is-revealed', window.pageYOffset > 60);
  };

  window.addEventListener('scroll', reveal, { passive: true });
  reveal();
}

// Text Effects
function initializeTextEffects() {
  const titleParts = document.querySelectorAll('.title-part');
  
  titleParts.forEach(part => {
    const text = part.getAttribute('data-text');
    part.innerHTML = '';
    
    // Create spans for each letter
    for (let i = 0; i < text.length; i++) {
      const span = document.createElement('span');
      span.textContent = text[i];
      span.style.animationDelay = `${i * 0.1}s`;
      span.style.display = 'inline-block';
      span.classList.add('letter-animation');
      part.appendChild(span);
    }
  });
  
  // Add letter animation styles
  const style = document.createElement('style');
  style.textContent = `
    .letter-animation {
      animation: letterGlow 4s ease-in-out infinite;
    }
    
    @keyframes letterGlow {
      0%, 100% { 
        transform: translateY(0px) scale(1);
        text-shadow: 0 0 3px currentColor;
        opacity: 0.9;
      }
      50% { 
        transform: translateY(-2px) scale(1.02);
        text-shadow: 0 0 6px currentColor;
        opacity: 1;
      }
    }
  `;
  document.head.appendChild(style);
}

// Enhanced scroll animations
function initializeScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, observerOptions);
  
  // Observe all elements that should animate on scroll
  document.querySelectorAll('h2, h3, p, table, ul, ol').forEach(el => {
    el.classList.add('fade-in-on-scroll');
    observer.observe(el);
  });
}

// Enhanced page loading effect
function initializePageLoader() {
  // Create loader element
  const loader = document.createElement('div');
  loader.className = 'page-loader';
  loader.innerHTML = '<div class="loader-circuit"></div>';
  document.body.appendChild(loader);
  
  // Show loader on page navigation (exclude anchor links, new-tab/modified
  // clicks, and downloads — none of those navigate this page, so the loader
  // would never get a chance to hide)
  document.addEventListener('click', function(e) {
    if (e.defaultPrevented || e.button !== 0 ||
        e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) {
      return;
    }
    const link = e.target.closest('a');
    if (link && link.href &&
        !link.href.includes('#') &&
        link.hostname === window.location.hostname &&
        link.target !== '_blank' &&
        !link.hasAttribute('download') &&
        !link.classList.contains('anchor-link')) {
      loader.classList.add('active');
    }
  });

  // Hide loader on pageshow, not load: when the browser restores a page from
  // the back/forward cache (bfcache), 'load' does not re-fire — the page comes
  // back exactly as it was, loader still active, which made the back button
  // appear broken. 'pageshow' fires on both normal loads and bfcache restores.
  window.addEventListener('pageshow', () => {
    loader.classList.remove('active');
  });
}

// Enhanced keyboard shortcuts
function initializeKeyboardShortcuts() {
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to go to homepage
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      window.location.href = '/HumanitiesAI/';
      e.preventDefault();
    }
    
    // Space to scroll down smoothly
    if (e.key === ' ' && !e.target.matches('input, textarea')) {
      e.preventDefault();
      window.scrollBy({
        top: window.innerHeight * 0.8,
        behavior: 'smooth'
      });
    }
    
    // Escape to scroll to top
    if (e.key === 'Escape') {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  });
}

// Enhanced table interactions
function initializeTableEnhancements() {
  document.querySelectorAll('table').forEach(table => {
    // Add hover effects to rows
    const rows = table.querySelectorAll('tr');
    rows.forEach(row => {
      row.addEventListener('mouseenter', function() {
        this.style.background = 'color-mix(in srgb, var(--accent) 10%, transparent)';
        this.style.transform = 'scale(1.01)';
      });
      
      row.addEventListener('mouseleave', function() {
        this.style.background = '';
        this.style.transform = '';
      });
    });
    
    // Add sort functionality to table headers
    const headers = table.querySelectorAll('th');
    headers.forEach(header => {
      header.style.cursor = 'pointer';
      header.addEventListener('click', function() {
        // Simple visual feedback for clicking headers
        this.style.background = 'color-mix(in srgb, var(--accent-2) 30%, transparent)';
        setTimeout(() => {
          this.style.background = '';
        }, 200);
      });
    });
  });
}

// Initialize all animations when page loads
document.addEventListener('DOMContentLoaded', function() {
  initializeDataStream();
  initializeGhostReveal();
  initializeTextEffects();
  initializeScrollAnimations();
  initializePageLoader();
  initializeKeyboardShortcuts();
  initializeTableEnhancements();
});

// Note: no window "resize" rebuild here -- the data-stream SVGs use
// viewBox + preserveAspectRatio, so they already scale responsively without
// needing regeneration (keeps the header art subtle and cheap, per brief).

// ============================================
// THEME TOGGLE FUNCTIONALITY
// ============================================
// Theme init/toggle now lives in assets/js/theme-toggle.js (loaded in <head>,
// sets data-theme + window.toggleTheme before body renders). The old
// duplicate implementation that lived here read a different localStorage
// key ('theme-preference'), defaulted to dark, and targeted button/span
// ids ('theme-toggle', 'theme-icon', 'theme-text') that no longer exist in
// the layouts -- keeping it would silently overwrite the light-first theme
// on every page load. Removed.
