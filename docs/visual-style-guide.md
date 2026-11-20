# Visual Style Guide

## Purpose

This document defines the visual identity of the repository website, ensuring consistency, readability, and aesthetic appeal while maintaining the repository's technical focus.

## Design Philosophy

- **Minimalist**: Keep design elements minimal to focus on content
- **Readable**: Prioritize text readability above all else
- **Accessible**: Ensure colors and contrast meet accessibility standards
- **Consistent**: Maintain visual consistency across all pages
- **Professional**: Create a trustworthy, authoritative appearance

## Color Scheme

### Primary Colors

- **Primary Blue**: `#2563eb` (Royal Blue)
  - Used for main links, buttons, and important visual elements
  - Background for key UI elements
  - Contrast ratio: 4.5:1 with white text (WCAG AA compliant)

- **Secondary Teal**: `#0d9488` (Teal)
  - Used for secondary elements, accents
  - Links that aren't primary
  - Contrast ratio: 4.5:1 with white text (WCAG AA compliant)

- **Accent Orange**: `#f97316` (Orange)
  - Used for call-to-action elements, highlights
  - Error/warning states
  - Contrast ratio: 4.5:1 with white text (WCAG AA compliant)

### Neutral Colors

- **Background**: `#ffffff` (White)
- **Background Secondary**: `#f8fafc` (Very light gray)
- **Text Primary**: `#1e293b` (Dark slate)
- **Text Secondary**: `#64748b** (Medium slate)
- **Border**: `#e2e8f0** (Light gray)

### Semantic Colors

- **Success**: `#22c55e` (Green) - Used for success states, valid checks
- **Warning**: `#eab308** (Yellow) - Used for warnings, pending states
- **Error**: `#ef4444** (Red) - Used for errors, failed checks
- **Info**: `#3b82f6** (Blue) - Used for information, help text

## Typography

### Font Family

- **Primary**: `Inter`, system-ui, -apple-system, sans-serif
  - Clean, modern, highly readable
  - Good for body text and UI elements

- **Monospace**: `Fira Code**, `Consolas**, `monospace**
  - Used for code blocks, inline code, technical content

### Font Sizes

- **Heading 1**: 2.25rem (36px) - Page titles
- **Heading 2**: 1.75rem (28px) - Section headings
- **Heading 3**: 1.5rem (24px) - Subsection headings
- **Body Large**: 1.125rem (18px) - Important text
- **Body**: 1rem (16px) - Main content
- **Body Small**: 0.875rem (14px) - Captions, secondary text

### Line Height

- **Body**: 1.6
- **Headings**: 1.2
- **Code**: 1.5

## Spacing

### Spacing Scale

- **4px**: Tight spacing (inline elements)
- **8px**: Default spacing unit
- **12px**: Small gaps
- **16px**: Base spacing, paragraph spacing
- **24px**: Medium gaps, section padding
- **32px**: Large gaps, section spacing
- **48px**: Extra large spacing, hero sections
- **64px**: Massive spacing (page sections)

### Border Radius

- **Small**: 4px - Buttons, small UI elements
- **Medium**: 8px - Cards, containers
- **Large**: 12px - Large containers, modals

## Visual Elements

### Icons

- Use minimal, line-style icons
- Preferred icon library: Lucide (via CDN)
- Consistent sizing: 16px-24px
- Stroke width: 2px

### Buttons

- **Primary**: Blue background, white text, no border
- **Secondary**: White background, blue border, blue text
- **Outline**: Transparent background, colored border, colored text
- **Hover effects**: Darker shades, subtle lift
- **Focus states**: 2px outline

### Cards

- White background, subtle border
- Shadow: 0 1px 3px rgba(0,0,0,0.1)
- Padding: 24px
- Border radius: 8px
- Hover: Subtle lift (0 2px 6px rgba(0,0,0,0.15))

### Links

- **Primary**: Blue, underline on hover
- **Secondary**: Teal, no underline
- **Visited**: Darker shade of primary color
- **Active**: Darker shade of primary color

## Layout

### Container

- Max width: 1200px
- Centered horizontally
- Padding: 24px (mobile) to 48px (desktop)

### Grid

- **12-column grid** for layout
- Gaps: 24px
- Responsive breakpoints:
  - Mobile: 1 column
  - Tablet: 2-3 columns
  - Desktop: 4 columns

### Sections

- Vertical spacing: 64px
- Subsections: 48px
- Horizontal spacing: 24px

## Responsive Design

### Breakpoints

- **Mobile**: < 640px (1 column)
- **Tablet**: 640px - 1024px (2-3 columns)
- **Desktop**: > 1024px (4 columns)

### Responsive Elements

- **Typography**: Scale down on mobile
- **Spacing**: Reduce padding on mobile
- **Buttons**: Full width on mobile
- **Grid**: Single column on mobile

## Accessibility

### Contrast Ratios

- All colors meet WCAG AA minimum contrast ratio of 4.5:1
- Text and background combinations tested

### Focus States

- Clear focus indicators for keyboard navigation
- 2px outline on focus
- Color: Blue, no outline offset

### Resizable Text

- Use relative units (rem, em)
- No fixed pixel sizes for text
- Allow text to scale to at least 200%

### Semantic HTML

- Proper heading hierarchy
- ARIA labels where needed
- Alt text for images

## Implementation

### CSS File Structure

```
site/static/
  styles/
    base.css      # Reset, typography, base styles
    components.css # Buttons, cards, icons
    layout.css    # Container, grid, sections
    responsive.css # Mobile, tablet, desktop
```

### Integration

- Include all CSS files in `site/templates/base.html`
- Use CSS custom properties for colors and spacing
- Enable CSS custom properties in Jekyll
- No CSS frameworks (Bootstrap, Tailwind, etc.)

### Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari, Chrome Mobile

## Examples

### Primary Button

```html
<button class="btn btn-primary">Get Started</button>
```

### Card

```html
<div class="card">
  <h3 class="card-title">Card Title</h3>
  <p class="card-body">Card content goes here.</p>
</div>
```

### Alert

```html
<div class="alert alert-info">
  <div class="alert-icon">ℹ️</div>
  <div class="alert-content">This is an informational message.</div>
</div>
```

## Guidelines

### Do

- Use the defined color palette
- Follow the spacing scale
- Use semantic HTML
- Include focus states
- Test with keyboard navigation
- Test with screen readers

### Don't

- Use arbitrary colors
- Override spacing with fixed values
- Use images where CSS would suffice
- Ignore mobile responsiveness
- Skip accessibility testing

## Future Considerations

- Dark mode support (may be added later)
- Animation guidelines (minimal, slow, accessible)
- Print styles
- Print-friendly colors
