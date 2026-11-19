# Visual Style Guide

## Overview

This document establishes the visual identity for the repository website, ensuring consistency, readability, and aesthetic appeal while maintaining a professional, technical documentation feel.

## Design Principles

### 1. Readability First
- Content is the primary focus
- High contrast between text and background
- Legible font sizes for all content
- Comfortable line lengths for reading

### 2. Professional Tone
- Clean, minimal aesthetic
- No excessive decoration or ornamentation
- Consistent use of whitespace
- Technical but approachable

### 3. Technical Documentation Style
- Similar to documentation sites like MDN, Stripe Docs, or Ruby on Rails Guides
- Code blocks with syntax highlighting
- Clear hierarchy and organization
- Professional color palette

## Color Scheme

### Primary Colors

#### Background Colors
- **Light Background (Main):** `#F8F9FA` - Off-white for main content areas
- **White:** `#FFFFFF` - For cards, sidebars, and containers
- **Dark Background (Footer):** `#1A1A2E` - Deep blue-black for footer

#### Text Colors
- **Primary Text:** `#2C3E50` - Dark slate blue for main headings and content
- **Secondary Text:** `#586F7C` - Muted gray for body text and meta information
- **Muted Text:** `#95A5A6` - Very light gray for captions and metadata
- **White Text:** `#FFFFFF` - For text on dark backgrounds

#### Accent Colors
- **Primary Accent:** `#3498DB` - Bright blue for links, buttons, and highlights
- **Secondary Accent:** `#E74C3C` - Soft red for errors and warnings
- **Success:** `#27AE60` - Green for success indicators
- **Info:** `#16A085` - Teal for informational elements

### Semantic Color Usage

| Purpose | Background | Text |
|---------|-----------|------|
| Links | Transparent | `#3498DB` |
| Buttons | `#3498DB` | White |
| Code Blocks | `#1E1E1E` | `#F8F8F2` |
| Code Inline | `#F8F9FA` | `#E74C3C` |
| Headings | Transparent | `#2C3E50` |
| Body Text | Transparent | `#586F7C` |
| Alerts/Notes | `#FFF3E0` | `#D84315` |

## Typography

### Font Family

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

This uses system fonts for best performance and native feel on all platforms.

### Font Sizes

| Element | Size | Line Height |
|---------|------|-------------|
| H1 | 2.5rem (40px) | 1.2 |
| H2 | 2rem (32px) | 1.3 |
| H3 | 1.5rem (24px) | 1.4 |
| H4 | 1.25rem (20px) | 1.5 |
| Body | 1rem (16px) | 1.6 |
| Code | 0.875rem (14px) | 1.5 |
| Small | 0.875rem (14px) | 1.5 |

### Font Weights

- **Regular:** 400 (body text)
- **Medium:** 500 (headings)
- **Bold:** 700 (strong emphasis, code)

## Spacing

### Base Unit
- 8px base unit for all spacing

### Spacing Scale

| Purpose | Size |
|---------|------|
| Tiny (0.25rem) | 4px |
| Small (0.5rem) | 8px |
| Medium (1rem) | 16px |
| Large (1.5rem) | 24px |
| XL (2rem) | 32px |
| XXL (3rem) | 48px |

### Layout Spacing

```css
/* Container padding */
--spacing-container: 2rem;

/* Element spacing */
--spacing-element: 1rem;

/* Section spacing */
--spacing-section: 2rem;

/* Large section spacing */
--spacing-section-large: 4rem;
```

## Borders and Shadows

### Border Radius

```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
```

### Border Widths

```css
--border-light: 1px solid #E0E0E0;
--border-medium: 2px solid #E0E0E0;
```

### Shadows

```css
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
```

## Components

### Buttons

```css
/* Primary Button */
.button {
  background: var(--primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-md);
  font-weight: 600;
  border: none;
  transition: all 0.2s ease;
}

.button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}
```

### Cards

```css
.card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-element);
  border: var(--border-light);
}
```

### Code Blocks

```css
.code-block {
  background: #1E1E1E;
  border-radius: var(--radius-md);
  padding: 1rem;
  overflow-x: auto;
  font-family: "Consolas", "Monaco", "Courier New", monospace;
}

.code-block code {
  color: #F8F8F2;
}
```

## Layout

### Container

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-container);
}
```

### Header

```css
.header {
  background: white;
  border-bottom: var(--border-light);
  padding: 1rem var(--spacing-container);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}
```

### Main Content

```css
.main-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem var(--spacing-container);
}
```

## Responsive Design

### Breakpoints

```css
/* Mobile */
@media (max-width: 768px) {
  /* Styles for mobile devices */
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
  /* Styles for tablets */
}

/* Desktop */
@media (min-width: 1025px) {
  /* Styles for desktop */
}
```

### Mobile Adjustments

- Smaller font sizes
- More vertical spacing
- Simplified navigation
- Touch-friendly buttons (minimum 44px height)
- Stacked layouts instead of side-by-side

## Accessibility

### Color Contrast

- Minimum 4.5:1 contrast ratio for normal text
- Minimum 3:1 contrast ratio for large text
- All text on colored backgrounds meets WCAG AA standards

### Focus States

```css
*:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

### Semantic HTML

- Use proper heading hierarchy (h1 -> h2 -> h3)
- Use `<button>` for interactive elements
- Use `<a>` for links
- Use `<main>`, `<nav>`, `<footer>` for structure

## Icons

### Icon Style

- Simple, line-based icons
- Consistent stroke width (1.5px)
- 24x24px base size
- Neutral colors (gray or blue)

### Icon Library

Recommended: Heroicons (SVG inline) or Lucide (clean, modern icons)

## Animation

### Smooth Transitions

```css
transition: all 0.2s ease-in-out;
```

### Fade In

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}
```

## Implementation Notes

### CSS Architecture

1. **Base styles** in `_base.css` (reset, typography, colors)
2. **Layout styles** in `_layout.css` (container, grid, flexbox)
3. **Component styles** in `_components.css` (buttons, cards, inputs)
4. **Utilities** in `_utilities.css` (spacing, text alignment, etc.)
5. **Responsive overrides** in `_responsive.css`

### CSS Loading Order

1. Reset/Base styles
2. Variables/Custom properties
3. Typography
4. Layout
5. Components
6. Responsive

## Design Decisions

### Why This Color Scheme?

1. **Professional Blue:** Trustworthy, professional, technical
2. **Gray Scale:** Clean, reduces visual noise
3. **High Contrast:** Ensures readability (WCAG AA compliant)
4. **Subtle Accents:** Highlights important elements without overwhelming

### Why System Fonts?

1. **Performance:** Native fonts load instantly
2. **Familiarity:** Users expect system fonts
3. **Consistency:** Matches the user's OS
4. **Maintainability:** No external dependencies

### Why 8px Spacing Grid?

1. **Consistency:** Easy to maintain alignment
2. **Flexibility:** Easy to scale up or down
3. **Common Practice:** Industry standard

## Future Enhancements

- Dark mode support
- Custom icon set integration
- Animated transitions for navigation
- Smooth scrolling behavior
- Print styles for documentation
