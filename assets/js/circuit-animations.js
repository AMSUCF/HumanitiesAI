// ============================================
// HUMANITIES IN THE AGE OF AI - CIRCUIT BOARD ANIMATIONS
// ============================================

// Circuit Board Animation Functions
function initializeCircuitBoard() {
  const svg = document.querySelector('.circuit-svg');
  if (!svg) return;
  
  // Clear existing content
  svg.innerHTML = '';
  
  // Create circuit paths
  createCircuitPaths(svg);
  
  // Create circuit nodes
  createCircuitNodes(svg);
}

function createCircuitPaths(svg) {
  const paths = [
    // Horizontal lines
    { x1: 50, y1: 100, x2: 300, y2: 100 },
    { x1: 400, y1: 150, x2: 700, y2: 150 },
    { x1: 800, y1: 200, x2: 1100, y2: 200 },
    { x1: 100, y1: 250, x2: 500, y2: 250 },
    { x1: 600, y1: 300, x2: 1000, y2: 300 },
    
    // Vertical lines
    { x1: 200, y1: 50, x2: 200, y2: 350 },
    { x1: 500, y1: 100, x2: 500, y2: 300 },
    { x1: 800, y1: 75, x2: 800, y2: 325 },
    { x1: 1000, y1: 125, x2: 1000, y2: 275 },
    
    // Diagonal connections
    { x1: 300, y1: 100, x2: 400, y2: 150 },
    { x1: 700, y1: 150, x2: 800, y2: 200 },
    { x1: 500, y1: 250, x2: 600, y2: 300 },
    { x1: 200, y1: 100, x2: 300, y2: 200 },
  ];
  
  paths.forEach((path, index) => {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', path.x1);
    line.setAttribute('y1', path.y1);
    line.setAttribute('x2', path.x2);
    line.setAttribute('y2', path.y2);
    line.setAttribute('class', 'circuit-path');
    line.style.animationDelay = `${index * 0.2}s`;
    svg.appendChild(line);
  });
}

function createCircuitNodes(svg) {
  const nodes = [
    { x: 200, y: 100, r: 4 },
    { x: 500, y: 150, r: 6 },
    { x: 800, y: 200, r: 5 },
    { x: 300, y: 250, r: 4 },
    { x: 700, y: 300, r: 5 },
    { x: 400, y: 100, r: 3 },
    { x: 600, y: 200, r: 4 },
    { x: 900, y: 250, r: 6 },
    { x: 150, y: 175, r: 3 },
    { x: 750, y: 125, r: 4 },
  ];
  
  nodes.forEach((node, index) => {
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', node.x);
    circle.setAttribute('cy', node.y);
    circle.setAttribute('r', node.r);
    circle.setAttribute('class', 'circuit-node');
    circle.style.animationDelay = `${index * 0.3}s`;
    svg.appendChild(circle);
  });
}

// Floating Nodes Animation
function initializeFloatingNodes() {
  const container = document.querySelector('.floating-nodes');
  if (!container) return;
  
  // Create floating nodes with varied properties
  for (let i = 0; i < 20; i++) {
    const node = document.createElement('div');
    node.className = 'floating-node';
    
    // Random positioning
    node.style.left = Math.random() * 100 + '%';
    node.style.top = Math.random() * 100 + '%';
    
    // Random animation delay and duration
    node.style.animationDelay = Math.random() * 6 + 's';
    node.style.animationDuration = (Math.random() * 4 + 4) + 's';
    
    // Random sizes for variety
    const size = Math.random() * 6 + 4; // 4-10px
    node.style.width = size + 'px';
    node.style.height = size + 'px';
    
    // Random colors with different intensities
    const colors = ['#00ffff', '#a855f7', '#ec4899', '#10b981', '#3b82f6'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    node.style.background = randomColor;
    
    // Enhanced glow with motion blur effect
    const glowIntensity = Math.random() * 20 + 10;
    node.style.boxShadow = `0 0 ${glowIntensity}px ${randomColor}, 0 0 ${glowIntensity * 2}px ${randomColor}`;
    
    // Add different animation classes for variety
    const animationTypes = ['', 'nth-child(2n)', 'nth-child(3n)'];
    if (i % 3 === 1) {
      node.style.animationName = 'floatReverse';
    } else if (i % 3 === 2) {
      node.style.animationName = 'floatDiagonal';
    }
    
    container.appendChild(node);
  }
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

// Neural Pulse Animation
function initializeNeuralPulse() {
  const pulse = document.querySelector('.neural-pulse');
  if (!pulse) return;
  
  // Add click interaction
  document.addEventListener('click', function(e) {
    // Create temporary pulse at click location
    const tempPulse = document.createElement('div');
    tempPulse.style.position = 'fixed';
    tempPulse.style.left = e.clientX + 'px';
    tempPulse.style.top = e.clientY + 'px';
    tempPulse.style.width = '10px';
    tempPulse.style.height = '10px';
    tempPulse.style.border = '2px solid #00ffff';
    tempPulse.style.borderRadius = '50%';
    tempPulse.style.pointerEvents = 'none';
    tempPulse.style.zIndex = '9999';
    tempPulse.style.transform = 'translate(-50%, -50%)';
    tempPulse.style.animation = 'clickPulse 0.6s ease-out forwards';
    
    document.body.appendChild(tempPulse);
    
    setTimeout(() => {
      tempPulse.remove();
    }, 600);
  });
  
  // Add click pulse animation
  const clickStyle = document.createElement('style');
  clickStyle.textContent = `
    @keyframes clickPulse {
      0% { 
        opacity: 1; 
        transform: translate(-50%, -50%) scale(1);
        box-shadow: 0 0 0 0 rgba(0, 255, 255, 0.4);
      }
      100% { 
        opacity: 0; 
        transform: translate(-50%, -50%) scale(4);
        box-shadow: 0 0 0 20px rgba(0, 255, 255, 0);
      }
    }
  `;
  document.head.appendChild(clickStyle);
}

// Parallax scrolling effect for circuit board
function initializeParallax() {
  window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.circuit-background');
    
    parallaxElements.forEach(element => {
      const speed = 0.5;
      element.style.transform = `translateY(${scrolled * speed}px)`;
    });
  });
}

// Interactive hover effects
function initializeInteractiveEffects() {
  // Add hover effects to circuit elements
  document.addEventListener('mousemove', function(e) {
    const nodes = document.querySelectorAll('.circuit-node');
    const mouseX = e.clientX;
    const mouseY = e.clientY;
    
    nodes.forEach(node => {
      const rect = node.getBoundingClientRect();
      const nodeX = rect.left + rect.width / 2;
      const nodeY = rect.top + rect.height / 2;
      
      const distance = Math.sqrt(
        Math.pow(mouseX - nodeX, 2) + Math.pow(mouseY - nodeY, 2)
      );
      
      if (distance < 100) {
        const intensity = (100 - distance) / 100;
        node.style.opacity = 0.5 + (intensity * 0.5);
        node.style.transform = `scale(${1 + intensity * 0.5})`;
      } else {
        node.style.opacity = '';
        node.style.transform = '';
      }
    });
  });
}

// Matrix rain effect (optional enhancement)
function createMatrixRain() {
  const canvas = document.createElement('canvas');
  canvas.style.position = 'fixed';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  canvas.style.pointerEvents = 'none';
  canvas.style.zIndex = '1';
  canvas.style.opacity = '0.1';
  
  document.body.appendChild(canvas);
  
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  const chars = '01';
  const charArray = chars.split('');
  const fontSize = 14;
  const columns = canvas.width / fontSize;
  const drops = [];
  
  for (let x = 0; x < columns; x++) {
    drops[x] = 1;
  }
  
  function draw() {
    ctx.fillStyle = 'rgba(10, 10, 15, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#00ffff';
    ctx.font = fontSize + 'px monospace';
    
    for (let i = 0; i < drops.length; i++) {
      const text = charArray[Math.floor(Math.random() * charArray.length)];
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);
      
      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }
      drops[i]++;
    }
  }
  
  setInterval(draw, 100);
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
  
  // Show loader on page navigation (exclude anchor links)
  document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (link && link.href && 
        !link.href.includes('#') && 
        link.hostname === window.location.hostname &&
        !link.classList.contains('anchor-link')) {
      loader.classList.add('active');
    }
  });
  
  // Hide loader when page loads
  window.addEventListener('load', () => {
    loader.classList.remove('active');
  });
}

// Dynamic background particles
function createBackgroundParticles() {
  const particleContainer = document.createElement('div');
  particleContainer.style.position = 'fixed';
  particleContainer.style.top = '0';
  particleContainer.style.left = '0';
  particleContainer.style.width = '100%';
  particleContainer.style.height = '100%';
  particleContainer.style.pointerEvents = 'none';
  particleContainer.style.zIndex = '-1';
  particleContainer.style.opacity = '0.1';
  
  document.body.appendChild(particleContainer);
  
  for (let i = 0; i < 20; i++) {
    const particle = document.createElement('div');
    particle.style.position = 'absolute';
    particle.style.width = '2px';
    particle.style.height = '2px';
    particle.style.background = '#00ffff';
    particle.style.borderRadius = '50%';
    
    // Random starting position
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    
    // Random animation
    particle.style.animation = `backgroundFloat ${Math.random() * 20 + 10}s linear infinite`;
    
    particleContainer.appendChild(particle);
  }
  
  // Add animation styles
  const style = document.createElement('style');
  style.textContent = `
    @keyframes backgroundFloat {
      0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
      10% { opacity: 1; }
      90% { opacity: 1; }
      100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
  `;
  document.head.appendChild(style);
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
        this.style.background = 'rgba(0, 255, 255, 0.1)';
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
        this.style.background = 'rgba(168, 85, 247, 0.3)';
        setTimeout(() => {
          this.style.background = '';
        }, 200);
      });
    });
  });
}

// Initialize all animations when page loads
document.addEventListener('DOMContentLoaded', function() {
  initializeCircuitBoard();
  initializeFloatingNodes();
  initializeTextEffects();
  initializeNeuralPulse();
  initializeParallax();
  initializeInteractiveEffects();
  initializeScrollAnimations();
  initializePageLoader();
  initializeKeyboardShortcuts();
  initializeTableEnhancements();
  
  // Initialize background particles after a delay
  setTimeout(createBackgroundParticles, 1000);
  
  // Optional: Uncomment to add matrix rain effect
  // createMatrixRain();
});

// Handle window resize
window.addEventListener('resize', function() {
  initializeCircuitBoard();
});

// ============================================
// THEME TOGGLE FUNCTIONALITY
// ============================================

function toggleTheme() {
  const body = document.documentElement;
  const themeIcon = document.getElementById('theme-icon');
  const themeText = document.getElementById('theme-text');
  
  const currentTheme = body.getAttribute('data-theme');
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';
  
  body.setAttribute('data-theme', newTheme);
  
  // Update button appearance
  if (newTheme === 'light') {
    themeIcon.textContent = '☀️';
    themeText.textContent = 'Dark Mode';
  } else {
    themeIcon.textContent = '🌙';
    themeText.textContent = 'Light Mode';
  }
  
  // Save preference to localStorage
  localStorage.setItem('theme-preference', newTheme);
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function() {
  console.log('Theme toggle script loaded'); // Debug log
  
  const savedTheme = localStorage.getItem('theme-preference') || 'dark';
  const body = document.documentElement;
  const themeIcon = document.getElementById('theme-icon');
  const themeText = document.getElementById('theme-text');
  const themeToggle = document.getElementById('theme-toggle');
  
  console.log('Theme elements found:', { themeIcon, themeText, themeToggle }); // Debug log
  
  body.setAttribute('data-theme', savedTheme);
  console.log('Applied theme:', savedTheme); // Debug log
  
  if (savedTheme === 'light') {
    themeIcon.textContent = '☀️';
    themeText.textContent = 'Dark Mode';
  } else {
    themeIcon.textContent = '🌙';
    themeText.textContent = 'Light Mode';
  }
  
  // Add event listener for theme toggle
  if (themeToggle) {
    console.log('Adding click listener to theme toggle'); // Debug log
    themeToggle.addEventListener('click', function() {
      console.log('Theme toggle clicked'); // Debug log
      
      const currentTheme = body.getAttribute('data-theme');
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      
      console.log('Switching from', currentTheme, 'to', newTheme); // Debug log
      
      body.setAttribute('data-theme', newTheme);
      
      if (newTheme === 'light') {
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Dark Mode';
      } else {
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Light Mode';
      }
      
      localStorage.setItem('theme-preference', newTheme);
      console.log('Theme saved to localStorage:', newTheme); // Debug log
    });
  } else {
    console.error('Theme toggle button not found!'); // Debug log
  }
});
