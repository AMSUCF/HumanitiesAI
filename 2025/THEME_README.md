# Humanities in the Age of AI - Circuit Board Theme

## Overview

This Jekyll site features a custom **Circuit Board Theme** designed specifically for the "Humanities in the Age of AI" course. The theme combines futuristic aesthetics with educational functionality, creating an immersive digital learning environment.

## Features

### 🎨 Visual Design
- **Animated Circuit Board Header**: Dynamic SVG circuits with pulsing nodes and flowing data paths
- **Neural Network Aesthetics**: Floating particles, glowing effects, and cyberpunk color scheme
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Interactive Animations**: Mouse-responsive elements and click effects

### 🚀 Technical Features
- **Custom Jekyll Layouts**: 
  - `default.html` - Full header with circuit board animation
  - `page.html` - Compact header for individual pages
- **Advanced CSS**: Custom properties, animations, and interactive effects
- **JavaScript Enhancements**: Circuit generation, particle systems, and user interactions
- **GitHub Pages Compatible**: Uses only supported Jekyll features

### 📱 Interactive Elements
- **Animated Typography**: Letter-by-letter text animations
- **Hover Effects**: Dynamic response to mouse movement
- **Scroll Animations**: Content fades in as user scrolls
- **Keyboard Shortcuts**: 
  - `Ctrl/Cmd + Enter` - Navigate to homepage
  - `Space` - Smooth scroll down
  - `Escape` - Scroll to top

## File Structure

```
├── _layouts/
│   ├── default.html      # Main layout with full header
│   └── page.html         # Compact layout for individual pages
├── assets/
│   ├── css/
│   │   └── style.scss    # Main stylesheet with circuit board theme
│   └── js/
│       └── circuit-animations.js  # JavaScript for animations
├── index.md             # Main course page
├── weekone.md           # Example week page
└── _config.yml          # Jekyll configuration
```

## Color Scheme

The theme uses a cyberpunk-inspired color palette:

- **Primary Background**: `#0a0a0f` (Deep space black)
- **Secondary Background**: `#1a1a2e` (Dark navy)
- **Accent Blue**: `#00ffff` (Cyan glow)
- **Accent Purple**: `#a855f7` (Electric purple)
- **Accent Pink**: `#ec4899` (Neon pink)
- **Circuit Green**: `#10b981` (Matrix green)
- **Text Light**: `#f8fafc` (Clean white)

## Typography

- **Headers**: 'Orbitron' - Futuristic sans-serif
- **Body Text**: 'Roboto Mono' - Readable monospace
- **Code**: System monospace fonts

## Animation Details

### Circuit Board Header
- **Dynamic SVG Generation**: Creates random circuit paths on page load
- **Pulsing Nodes**: Animated connection points with glow effects
- **Floating Particles**: Background elements that respond to mouse movement
- **Neural Pulse**: Expanding rings that trigger on user interaction

### Text Effects
- **Letter Animation**: Individual character scaling and glow
- **Heading Markers**: Animated arrow indicators
- **Link Transitions**: Smooth color changes and underline effects

### Interactive Elements
- **Table Enhancements**: Row highlighting and hover effects
- **Button Animations**: Sliding shine effects and elevation changes
- **Form Styling**: Glowing focus states and cyberpunk aesthetics

## Usage

### For Main Pages
Use the default layout for primary pages that should display the full animated header:

```yaml
---
layout: default
title: Your Page Title
---
```

### For Individual Lessons/Weeks
Use the page layout for a more compact header:

```yaml
---
layout: page
title: "Week One: Your Topic"
---
```

## Customization

### Adding New Animations
Add custom animations in `assets/js/circuit-animations.js`:

```javascript
function yourCustomAnimation() {
  // Your animation code here
}

// Add to initialization
document.addEventListener('DOMContentLoaded', function() {
  // ... existing initializations
  yourCustomAnimation();
});
```

### Modifying Colors
Update CSS custom properties in `assets/css/style.scss`:

```scss
:root {
  --your-custom-color: #your-hex-value;
}
```

### Adding New Circuit Patterns
Modify the `createCircuitPaths()` function in the JavaScript file to add new circuit patterns.

## Browser Compatibility

- **Modern Browsers**: Full support for all animations and effects
- **Safari**: Requires `-webkit-` prefixes (included)
- **Mobile**: Touch-optimized interactions
- **Fallbacks**: Graceful degradation for older browsers

## Performance Considerations

- **Optimized Animations**: Uses CSS transforms and opacity for smooth performance
- **Lazy Loading**: Particles and complex animations load after initial content
- **Responsive Images**: Properly sized for different screen densities
- **Minimal JavaScript**: Lightweight code with efficient event handling

## Accessibility

- **High Contrast**: Meets WCAG guidelines for text readability
- **Keyboard Navigation**: Full keyboard accessibility support
- **Screen Readers**: Semantic HTML structure
- **Reduced Motion**: Respects user's motion preferences (can be enhanced)

## Future Enhancements

Potential additions for future versions:
- **Dark/Light Mode Toggle**: User preference switching
- **Theme Customization**: Student-selectable color schemes
- **Advanced Interactions**: AI-powered content recommendations
- **Performance Monitoring**: Real-time optimization
- **Progressive Web App**: Offline functionality

## Contributing

When making changes to the theme:
1. Test across multiple browsers and devices
2. Ensure animations don't interfere with content readability
3. Maintain the cyberpunk aesthetic while prioritizing usability
4. Document any new features or customizations

---

**Created for ENG 6806: Humanities in the Age of AI - Fall 2025**
