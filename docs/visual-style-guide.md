# Visual Style Guide

## Overview
This document defines the visual identity for the repository website, including color schemes, typography, spacing, and design principles. The goal is to create a visually appealing, readable, and consistent design that enhances user experience while maintaining professionalism.

## Design Philosophy

### Core Principles
1. **Readability First** - Text must be easy to read across all devices and light conditions
2. **Consistency** - All elements follow the same visual language
3. **Professionalism** - Design should reflect the technical and documentation-focused nature of the repository
4. **Accessibility** - High contrast and clear visual hierarchy for all users
5. **Responsiveness** - Design adapts gracefully to desktop, tablet, and mobile screens

## Color Palette

### Primary Colors

#### Background Colors
| Color Name | Hex Code | RGB | Usage |
|------------|----------|-----|-------|
| Base Background | `#ffffff` | `255, 255, 255` | Main page background |
| Secondary Background | `#f8f9fa` | `248, 249, 250` | Sections, sidebars |
| Tertiary Background | `#e9ecef` | `233, 236, 239` | Code blocks, alerts |

#### Text Colors
| Color Name | Hex Code | RGB | Usage |
|------------|----------|-----|-------|
| Primary Text | `#212529` | `33, 37, 41` | Main content text |
| Secondary Text | `#495057` | `73, 80, 87` | Subheadings, captions |
| Muted Text | `#6c757d` | `108, 117, 125` | Metadata, labels |

#### Accent Colors

| Color Name | Hex Code | RGB | Usage |
|------------|----------|-----|-------|
| Primary Accent | `#0d6efd` | `13, 110, 253` | Links, primary buttons, highlights |
| Success | `#198754` | `25, 135, 84` | Success states, valid indicators |
| Warning | `#ffc107` | `255, 193, 7` | Warnings, alerts |
| Error | `#dc3545` | `220, 53, 69` | Errors, failure states |
| Info | `#0dcaf0` | `13, 202, 240` | Informational messages |

#### Neutral Colors
| Color Name | Hex Code | RGB | Usage |
|------------|----------|-----|-------|
| Dark Border | `#dee2e6` | `222, 226, 230` | Dividers, borders |
| Light Border | `#e9ecef` | `233, 236, 239` | Cards, panels |

### Color Accessibility
- All text colors meet WCAG AA standards for readability
- Minimum contrast ratio: 4.5:1 for normal text, 3:1 for large text
- Color blindness considerations: Use patterns/icons alongside color indicators

## Typography

### Font Families

#### Headings
- **Primary**: `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Font Weight**: 700 (Bold)
- **Line Height**: 1.3

#### Body Text
- **Primary**: `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Font Weight**: 400 (Regular)
- **Line Height**: 1.6

#### Code
- **Monospace**: `'Consolas', 'Monaco', 'Courier New', monospace`
- **Font Weight**: 400
- **Background**: `#f8f9fa`
- **Border Radius**: 4px

### Font Sizes

| Element | Size | Line Height | Weight |
|---------|------|-------------|--------|
| H1 (Page Title) | 2.5rem (40px) | 1.3 | 700 |
| H2 (Section Title) | 2rem (32px) | 1.3 | 700 |
| H3 (Subsection) | 1.5rem (24px) | 1.3 | 600 |
| H4 (Subheading) | 1.25rem (20px) | 1.4 | 600 |
| Body Large | 1.125rem (18px) | 1.6 | 400 |
| Body Medium | 1rem (16px) | 1.6 | 400 |
| Body Small | 0.875rem (14px) | 1.6 | 400 |
| Code Small | 0.875rem (14px) | 1.4 | 400 |

### Spacing Scale

| Scale Unit | Value | Usage |
|------------|-------|-------|
| XS | 0.5rem (8px) | Tight spacing, small margins |
| S | 1rem (16px) | Standard spacing between elements |
| M | 1.5rem (24px) | Section spacing, paragraph gaps |
| L | 2rem (32px) | Large section breaks |
| XL | 3rem (48px) | Major section dividers |
| XXL | 4rem (64px) | Page top/bottom spacing |

### Component Spacing

```css
:root {
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 1.5rem;
  --spacing-lg: 2rem;
  --spacing-xl: 3rem;
  --spacing-xxl: 4rem;
}
```

## Layout and Structure

### Container Widths
- **Mobile**: 100%, full width
- **Tablet**: 768px (max-width)
- **Desktop**: 1200px (max-width, centered)

### Content Area
- **Main container**: 1200px max-width, centered
- **Padding**: 2rem (32px) on all sides
- **Content width**: ~70% of container

### Section Spacing
- **Section padding**: 3rem (48px) vertical
- **Nested sections**: 2rem (32px) vertical
- **Block elements**: 1.5rem (24px) margin between

## UI Components

### Buttons

#### Primary Button
- **Background**: `#0d6efd`
- **Text**: `#ffffff`
- **Padding**: 0.75rem 1.5rem
- **Border Radius**: 4px
- **Font Weight**: 600
- **Hover**: Darken to `#0b5ed7`

#### Secondary Button
- **Background**: `#ffffff`
- **Text**: `#0d6efd`
- **Border**: 1px solid `#dee2e6`
- **Padding**: 0.75rem 1.5rem
- **Border Radius**: 4px
- **Font Weight**: 600
- **Hover**: Lighten background, darken border

### Cards
- **Background**: `#ffffff`
- **Border**: 1px solid `#dee2e6`
- **Border Radius**: 8px
- **Padding**: 1.5rem
- **Shadow**: `0 2px 4px rgba(0,0,0,0.05)`

### Badges
- **Background**: `#e9ecef`
- **Text**: `#495057`
- **Padding**: 0.25rem 0.75rem
- **Border Radius**: 9999px
- **Font Size**: 0.875rem (14px)

### Alerts/Notifications
- **Success**: Green background `#d1e7dd`, text `#0f5132`
- **Warning**: Yellow background `#fff3cd`, text `#664d03`
- **Error**: Red background `#f8d7da`, text `#842029`
- **Info**: Blue background `#cff4fc`, text `#055160`

## Icons

### Icon Usage
- **Style**: Minimal, line-based icons
- **Size**: 1rem (16px) for most icons, 1.25rem (20px) for large contexts
- **Color**: Use text colors for consistency
- **Implementation**: SVG icons for crisp rendering at any size

### Icon Library
- **Primary**: Use SVG icons inline or from a lightweight library
- **Categories**: Navigation, actions, status, information

## Forms and Inputs

### Input Fields
- **Padding**: 0.75rem 1rem
- **Border**: 1px solid `#ced4da`
- **Border Radius**: 4px
- **Font Size**: 1rem
- **Focus**: Ring 2px solid `#0d6efd`, border darkened

### Select Dropdowns
- **Same as input fields**
- **Arrow icon**: Right-aligned, dark gray

### Checkboxes and Radios
- **Size**: 1rem
- **Color**: Primary accent color
- **Spacing**: 0.5rem between label and input

## Navigation

### Primary Navigation
- **Style**: Horizontal bar
- **Background**: `#ffffff`
- **Border**: Bottom 1px solid `#dee2e6`
- **Items**: Centered or left-aligned
- **Font Size**: 1rem (16px)
- **Spacing**: 1.5rem between items

### Mobile Navigation
- **Style**: Hamburger menu, slide-out drawer
- **Background**: `#ffffff`
- **Animation**: Smooth slide-in from left

### Active States
- **Style**: Underlined or highlighted
- **Color**: Primary accent color
- **Style**: Underline with padding-bottom

## Responsiveness

### Breakpoints
- **Mobile First**: Design for mobile, expand for larger screens
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Adjustments
- **Font sizes**: Scale down for smaller screens
- **Spacing**: Reduce padding and margins
- **Navigation**: Use hamburger menu or stacked layout
- **Card layouts**: Single column

### Tablet Adjustments
- **Font sizes**: Slightly larger than mobile
- **Spacing**: Medium spacing
- **Grid**: 2-column layouts where appropriate

### Desktop Adjustments
- **Font sizes**: Full sizes
- **Spacing**: Large spacing
- **Grid**: 3-column layouts, multiple columns

## Accessibility

### Color Contrast
- **Text**: Minimum 4.5:1 contrast ratio
- **Large Text**: Minimum 3:1 contrast ratio
- **Interactive Elements**: Clear visual indicators

### Focus States
- **Style**: Visible focus ring (2px solid primary color)
- **Outline**: No outline, use focus ring
- **Transition**: Smooth 200ms transition

### Screen Reader Support
- **Semantic HTML**: Use proper headings and landmarks
- **Alt Text**: All images have descriptive alt text
- **Skip Links**: Skip to main content link

### Motion
- **Animations**: Respect user motion preferences
- **Transitions**: Smooth but not distracting
- **Pause on Hover**: Allow users to pause animations

## Implementation Notes

### CSS Implementation
- Use CSS variables for all colors, spacing, and sizes
- Use `rem` units for all sizing to maintain relative scaling
- Use `clamp()` for fluid typography
- Include media queries for responsive design

### File Structure
- **Main Stylesheet**: `site/assets/css/style.css`
- **Variables**: `site/assets/css/variables.css`
- **Typography**: `site/assets/css/typography.css`
- **Components**: `site/assets/css/components.css`
- **Layout**: `site/assets/css/layout.css`
- **Responsive**: `site/assets/css/responsive.css`

### Browser Support
- Target: Chrome, Firefox, Safari, Edge (latest 2 versions)
- Use modern CSS features with fallbacks where needed
- Include normalize.css or similar for browser consistency

## Design Constraints

### No-Go Zones
- **No Auto-Playing Media**: No videos or audio that play automatically
- **No Dark Patterns**: No misleading or deceptive UI elements
- **No Pop-ups**: No intrusive pop-ups or modals
- **No Mandatory Registration**: Users should be able to view content without registering

### Allowed Visual Elements
- **Minimal Icons**: Use sparingly, focus on content
- **Subtle Animations**: Fade-ins, hover effects
- **Light Effects**: Subtle shadows, gradients
- **Code Highlighting**: Standard syntax highlighting colors

## Documentation for Future Designers

### File References
- All styles go in `site/assets/css/`
- All templates go in `site/templates/`
- Images go in `site/assets/images/`

### When Making Changes
1. **Check Existing**: Review current implementation before making changes
2. **Maintain Consistency**: Follow this style guide
3. **Update Documentation**: Update this guide if adding new components
4. **Test Responsiveness**: Verify all changes work on all breakpoints
5. **Check Accessibility**: Ensure all changes maintain accessibility standards

### Version History
- **Version 1.0** (2026-11-20): Initial visual style guide created
- **Next Update**: After visual identity implementation is complete
