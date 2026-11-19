# Visual Style Guide

## Overview
This document defines the visual identity for the drift website - a live view of run history. The design philosophy prioritizes readability, clarity, and a cohesive dark theme that reduces eye strain during extended reading sessions.

## Design Principles

1. **Readability First**: All visual elements must enhance, not compromise, readability
2. **Dark Theme**: Reduces eye strain for extended reading sessions
3. **Minimalist**: Clean, uncluttered design that lets content shine
4. **Accessible**: High contrast ratios, readable font sizes, clear navigation
5. **Consistent**: Unified design language throughout all pages

## Color Palette

### Primary Colors

| Color Name | Hex | RGB | Usage |
|------------|-----|-----|-------|
| Background | `#0f172a` | 15, 23, 42 | Main page background |
| Surface | `#1e293b` | 30, 41, 59 | Cards, sections, containers |
| Surface Lighter | `#334155` | 51, 65, 85 | Borders, separators |
| Foreground | `#e2e8f0` | 226, 232, 240 | Main text, headings |
| Foreground Dim | `#94a3b8` | 148, 163, 184 | Secondary text, metadata |
| Foreground Muted | `#64748b` | 100, 116, 139 | Tertiary text, labels |

### Accent Colors

| Color Name | Hex | RGB | Usage |
|------------|-----|-----|-------|
| Primary Accent | `#38bdf8` | 56, 189, 248 | Links, highlights, active states |
| Success | `#22c55e` | 34, 197, 94 | Success messages, valid states |
| Warning | `#f59e0b` | 245, 158, 11 | Warnings, alerts |
| Error | `#ef4444` | 239, 68, 68 | Errors, failures |
| Info | `#3b82f6` | 59, 130, 246 | Informational messages |

### Semantic Colors

These colors are used for conveying meaning beyond decoration:

- **Success** (green): Successful operations, valid states
- **Warning** (amber): Attention needed, caution
- **Error** (red): Failures, errors, important warnings
- **Info** (blue): Informational content, helpful notes

## Typography

### Font Family
- **Primary**: System UI, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- **Fallback**: Monospace for code snippets and technical content

### Font Sizes

| Element | Size | Line Height |
|---------|------|-------------|
| H1 | 2.5rem (40px) | 1.2 |
| H2 | 2rem (32px) | 1.3 |
| H3 | 1.5rem (24px) | 1.4 |
| Body | 1rem (16px) | 1.6 |
| Small | 0.875rem (14px) | 1.5 |
| X-small | 0.75rem (12px) | 1.4 |

### Font Weights

| Element | Weight |
|---------|--------|
| Body Text | 400 (normal) |
| Headings | 600 (semibold) |
| Emphasis | 700 (bold) |

## Spacing System

All spacing uses 4px base units:

| Size | Value | Usage |
|------|-------|-------|
| XS | 4px | Tight spacing, icons inside text |
| SM | 8px | Small gaps, button padding |
| MD | 16px | Standard spacing between elements |
| LG | 24px | Section padding, major gaps |
| XL | 32px | Large section spacing |
| 2XL | 48px | Major section spacing |
| 3XL | 64px | Extra large spacing |

## Border Radius

- **Small**: 4px (buttons, inputs, small elements)
- **Medium**: 8px (cards, sections, containers)
- **Large**: 12px (major containers, modals)

## Shadows

The site uses subtle shadows for depth:

- **Subtle**: `0 1px 3px rgba(0, 0, 0, 0.1)`
- **Medium**: `0 4px 6px rgba(0, 0, 0, 0.1)`
- **Large**: `0 10px 15px rgba(0, 0, 0, 0.1)`

## Components

### Buttons

**Primary Button**
- Background: Primary Accent (`#38bdf8`)
- Text: Surface (`#0f172a`)
- Padding: 0.75rem 1.5rem
- Border Radius: 4px
- Hover: Darker accent (`#0ea5e9`)

**Secondary Button**
- Background: Surface (`#1e293b`)
- Text: Foreground (`#e2e8f0`)
- Border: 1px solid Surface Lighter (`#334155`)
- Padding: 0.75rem 1.5rem
- Border Radius: 4px
- Hover: Surface Lighter (`#334155`)

### Cards

- Background: Surface (`#1e293b`)
- Border: 1px solid Surface Lighter (`#334155`)
- Border Radius: 8px
- Padding: 1.5rem
- Shadow: Subtle
- Margin: 1.5rem

### Links

- Color: Primary Accent (`#38bdf8`)
- Underline: None
- Hover: Darker accent (`#0ea5e9`)
- Active: Accent with darker underline

### Badges

Small inline indicators for categories, tags, or status:

- Background: Surface Lighter (`#334155`)
- Text: Foreground Dim (`#94a3b8`)
- Padding: 0.25rem 0.5rem
- Border Radius: 12px
- Font Size: 0.75rem (12px)

### Icons

- Size: 16px × 16px (inline)
- Color: Foreground Dim (`#64748b`)
- Fill: None (outline style preferred)
- Stroke: 2px

## Layout

### Container
- Max Width: 1200px
- Padding: 0 1.5rem
- Margin: 0 auto

### Section Spacing
- Top: 2rem (32px)
- Bottom: 2rem (32px)

### Navigation
- Background: Surface (`#1e293b`)
- Border Bottom: 1px solid Surface Lighter (`#334155`)
- Padding: 1rem 0
- Links: Foreground (`#e2e8f0`)
- Active Link: Accent (`#38bdf8`)

## Responsive Design

### Breakpoints

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

### Mobile Adjustments

- Reduce font sizes by 10% for smaller screens
- Stack flex containers vertically
- Increase touch target sizes (minimum 44px)
- Reduce padding to improve space utilization

### Tablet Adjustments

- Medium font sizes
- 2-column grid layouts
- Standard padding and spacing

## Accessibility

### Color Contrast

- Minimum contrast ratio: 4.5:1 for normal text
- Enhanced contrast: 3:1 for large text (18px+)
- Interactive elements must have at least 3:1 contrast

### Focus States

- All interactive elements have visible focus states
- Focus ring: 2px solid Primary Accent
- Focus ring offset: 2px

### Text Resizing

- Support text resizing to 200% without breaking layout
- Avoid fixed width elements
- Use relative units (rem, em, %) instead of px

## Animation

### Transitions

- Smooth transitions for hover states
- Duration: 0.2s
- Easing: ease-in-out

### Loading States

- Subtle spinner or skeleton loading
- Color: Foreground Dim
- Size: 24px

### Micro-interactions

- Button hover: Slight lift (translateY -2px)
- Link hover: Underline appears
- Focus: Clear border outline

## Implementation Notes

### CSS Variables

Use CSS custom properties for easy theming:

```css
:root {
  --bg: #0f172a;
  --surface: #1e293b;
  --surface-lighter: #334155;
  --fg: #e2e8f0;
  --fg-dim: #94a3b8;
  --fg-muted: #64748b;
  --accent: #38bdf8;
  /* ... other variables */
}
```

### Prefers Reduced Motion

Respect user's motion preferences:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Dark Mode Support

Currently using dark theme as default. Future enhancement could support system preference.

## Maintenance

- All colors must be defined in CSS variables
- Components must follow the defined specifications
- Regular accessibility audits recommended
- Update this guide when design changes are made
