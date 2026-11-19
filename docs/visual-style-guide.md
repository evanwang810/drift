# Visual Style Guide

## Overview

This guide establishes the visual identity for the repository website, ensuring consistency, accessibility, and aesthetic appeal while maintaining readability and functionality.

## Design Philosophy

The design philosophy prioritizes:
- **Readability**: Content must be the primary focus with clear hierarchy
- **Accessibility**: High contrast ratios and readable fonts for all users
- **Consistency**: Repeated visual elements across all pages
- **Minimalism**: Clean, uncluttered interface with purposeful design elements
- **Professionalism**: A polished, trustworthy appearance suitable for documentation and knowledge sharing

## Color Palette

### Primary Colors

#### Primary Brand Color
- **Hex**: #2563eb
- **Name**: Royal Blue
- **Usage**: Primary buttons, links, active states, accents
- **Rationale**: Trustworthy and professional, widely used in documentation sites

#### Secondary Accent Color
- **Hex**: #10b981
- **Name**: Emerald Green
- **Usage**: Success states, positive highlights, verification badges
- **Rationale**: Green provides positive feedback and indicates success

### Semantic Colors

#### Error/Warning
- **Error**: #ef4444 (Red)
- **Warning**: #f59e0b (Amber)
- **Neutral**: #6b7280 (Gray)

#### Text Colors
- **Primary text**: #1f2937 (Dark Gray)
- **Secondary text**: #6b7280 (Medium Gray)
- **Muted text**: #9ca3af (Light Gray)
- **Code blocks**: #1e293b (Very Dark Gray)

### Background Colors
- **Page background**: #ffffff (White)
- **Section backgrounds**:
  - Light: #f9fafb (Very Light Gray)
  - Medium: #f3f4f6 (Light Gray)
  - Dark: #1f2937 (Dark Gray - for code blocks)

## Typography

### Font Family

- **Primary font**: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
- **Monospace font**: "SF Mono", "Fira Code", "Consolas", "Monaco", monospace
- **Fallback**: System fonts ensure fast loading and native feel

### Font Sizes

- **Display**: 2.5rem (40px) - Page titles
- **H1**: 2rem (32px) - Main headings
- **H2**: 1.5rem (24px) - Section headings
- **H3**: 1.25rem (20px) - Subsection headings
- **Body**: 1rem (16px) - Main content
- **Small**: 0.875rem (14px) - Captions, metadata
- **Code**: 0.875rem (14px) - Inline code

### Font Weights

- **Regular**: 400 - Body text
- **Medium**: 500 - Emphasis, highlights
- **Bold**: 700 - Headings, important text

## Spacing System

### Base Unit
- 4px grid system for consistent spacing

### Scale
- 4px: xs (small spacing)
- 8px: sm (element spacing)
- 12px: md (section spacing)
- 16px: lg (major spacing)
- 24px: xl (page spacing)
- 32px: 2xl (section spacing)
- 48px: 3xl (page section spacing)

## UI Components

### Buttons

#### Primary Button
- **Background**: #2563eb (Royal Blue)
- **Text**: #ffffff (White)
- **Padding**: 0.5rem 1rem
- **Border radius**: 0.375rem
- **Hover**: #1d4ed8 (Darker Blue)
- **Active**: #1e40af (Darkest Blue)

#### Secondary Button
- **Background**: #ffffff (White)
- **Text**: #2563eb (Royal Blue)
- **Border**: 1px solid #2563eb
- **Padding**: 0.5rem 1rem
- **Border radius**: 0.375rem
- **Hover**: #eff6ff (Light Blue Background)

### Cards

- **Background**: #ffffff (White)
- **Border**: 1px solid #e5e7eb (Light Gray)
- **Border radius**: 0.5rem
- **Padding**: 1.5rem
- **Shadow**: 0 1px 3px rgba(0, 0, 0, 0.1)
- **Hover shadow**: 0 4px 6px rgba(0, 0, 0, 0.1)

### Inputs

- **Background**: #ffffff (White)
- **Border**: 1px solid #d1d5db (Medium Gray)
- **Padding**: 0.5rem 0.75rem
- **Border radius**: 0.375rem
- **Focus border**: 2px solid #2563eb (Royal Blue)
- **Focus ring**: 0 0 0 3px rgba(37, 99, 235, 0.1)

### Tables

- **Border**: 1px solid #e5e7eb (Light Gray)
- **Header background**: #f9fafb (Very Light Gray)
- **Cell padding**: 0.75rem
- **Row hover**: #f9fafb (Very Light Gray)
- **Text alignment**: Left

### Icons

- **Style**: Minimal, outline style
- **Size**: 1.25rem (20px) for main icons
- **Color**: #6b7280 (Medium Gray)
- **Stroke width**: 2px

## Layout

### Container
- **Max width**: 1200px
- **Padding**: 0 1.5rem
- **Centered**: Yes

### Grid System
- **Columns**: 12
- **Gap**: 1.5rem
- **Responsive breakpoints**:
  - Mobile: 1 column
  - Tablet: 2-3 columns
  - Desktop: 3-4 columns

### Responsive Design

#### Mobile (≤ 640px)
- Single column layout
- Larger touch targets (44px minimum)
- Simple navigation
- Optimized spacing

#### Tablet (641px - 1024px)
- 2-column grid
- Balanced spacing
- Medium touch targets

#### Desktop (1025px+)
- Full grid layout
- Maximum 1200px container
- Optimal spacing

## Accessibility

### Color Contrast
- Minimum WCAG AA: 4.5:1 for body text
- Minimum WCAG AAA: 7:1 for body text
- Use contrast checker for all color combinations

### Focus States
- Clear visible focus indicators
- Minimum 2px outline
- Color contrast: 3:1 minimum

### Font Accessibility
- Line height: 1.5 for body text
- Letter spacing: Normal (no adjustment)
- Orphan control: No orphaned lines (allow widows)

## Design Tokens

### Colors
```css
--color-primary: #2563eb;
--color-primary-hover: #1d4ed8;
--color-primary-active: #1e40af;
--color-secondary: #10b981;
--color-error: #ef4444;
--color-warning: #f59e0b;
--color-text-primary: #1f2937;
--color-text-secondary: #6b7280;
--color-text-muted: #9ca3af;
--color-bg-page: #ffffff;
--color-bg-light: #f9fafb;
--color-bg-medium: #f3f4f6;
--color-bg-dark: #1f2937;
```

### Spacing
```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 12px;
--spacing-lg: 16px;
--spacing-xl: 24px;
--spacing-2xl: 32px;
--spacing-3xl: 48px;
```

### Typography
```css
--font-size-display: 2.5rem;
--font-size-h1: 2rem;
--font-size-h2: 1.5rem;
--font-size-h3: 1.25rem;
--font-size-body: 1rem;
--font-size-small: 0.875rem;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-bold: 700;
```

## Constraints

### What Not to Do
- ❌ Use more than 3 colors (primary, secondary, semantic)
- ❌ Use harsh or jarring color combinations
- ❌ Reduce line spacing below 1.5 for body text
- ❌ Use inline styles for layout
- ❌ Rely on color alone for information
- ❌ Use low contrast color combinations
- ❌ Use decorative elements that serve no purpose

### Best Practices
- ✅ Use system fonts for performance
- ✅ Provide alternative text for all images
- ✅ Ensure all interactive elements have focus states
- ✅ Test colors on different devices
- ✅ Verify contrast ratios before implementation
- ✅ Keep design consistent across all pages
- ✅ Use whitespace to improve readability

## Implementation Notes

### CSS File Organization
1. Reset styles
2. Base typography
3. Layout components
4. UI components
5. Responsive utilities
6. Print styles

### Browser Support
- Modern browsers: Chrome, Firefox, Safari, Edge (last 2 versions)
- Progressive enhancement approach
- Graceful degradation for older browsers

## Version History

- **v1.0** (2026-11-19): Initial visual style guide created
