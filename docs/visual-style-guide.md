# Visual Style Guide

## Vision Statement

To maintain a high-quality, well-documented repository that serves as a living example of best practices in software engineering, documentation, and community-driven development, presented with a clean, modern, and professional visual identity.

## Design Philosophy

The visual identity should:
- Enhance readability and user experience
- Reflect the repository's technical nature
- Maintain consistency across all pages
- Support both desktop and mobile viewing
- Use minimal, purposeful design elements

## Color Scheme

### Primary Colors

**Background Colors:**
- Main background: `#f8f9fa` (Light gray, easy on eyes)
- Card/Content background: `#ffffff` (White, high contrast)
- Secondary background: `#e9ecef` (Subtle borders, hover states)

**Text Colors:**
- Primary text: `#212529` (Dark gray, readable)
- Secondary text: `#6c757d` (Medium gray, for metadata)
- Code text: `#343a40` (Darker gray for code blocks)

**Accent Colors:**
- Primary accent: `#3b82f6` (Blue, for links and highlights)
- Success: `#10b981` (Green, for positive states)
- Warning: `#f59e0b` (Amber, for warnings)
- Error: `#ef4444` (Red, for errors)

### Usage Guidelines

- Use blue for primary actions and links
- Use green for success states and positive information
- Use amber for warnings and important but not critical information
- Use red for errors and critical information
- Ensure sufficient contrast ratios (WCAG AA minimum: 4.5:1)

## Typography

### Font Families

**Primary font:** System sans-serif fonts (Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto)
- Font stack ensures fast loading and native feel

### Font Sizes

- Heading 1 (H1): `2.25rem` (36px)
- Heading 2 (H2): `1.75rem` (28px)
- Heading 3 (H3): `1.5rem` (24px)
- Body text: `1rem` (16px)
- Small text: `0.875rem` (14px)

### Line Heights

- Headings: `1.2`
- Body: `1.6`
- Code: `1.5`

## Spacing System

### Standard Spacing Scale (Base unit: 8px)

- `0.5rem` (8px): Tight spacing
- `1rem` (16px): Normal spacing
- `1.5rem` (24px): Comfortable spacing
- `2rem` (32px): Large spacing
- `3rem` (48px): Section spacing

### Usage

- Vertical rhythm: Use consistent spacing between elements
- Margins: Use for separating distinct sections
- Padding: Use for inside containers and elements
- Responsive: Scale spacing on smaller screens

## Components

### Buttons

**Primary Button:**
- Background: `#3b82f6` (Blue)
- Text: `#ffffff` (White)
- Padding: `0.75rem 1.5rem`
- Border radius: `0.25rem` (4px)
- Hover: `#2563eb` (Darker blue)
- Transition: `0.2s ease`

**Secondary Button:**
- Background: `transparent`
- Border: `1px solid #ced4da`
- Text: `#495057`
- Padding: `0.75rem 1.5rem`
- Border radius: `0.25rem`
- Hover: `#e9ecef` (Light gray)

### Cards

- Background: `#ffffff`
- Border: `1px solid #dee2e6`
- Border radius: `0.25rem` (4px)
- Padding: `1.5rem`
- Shadow: `0 1px 3px rgba(0,0,0,0.1)`

### Tables

- Border: `1px solid #dee2e6`
- Header background: `#f8f9fa`
- Row hover: `#f1f3f5`
- Cell padding: `0.75rem`
- Text align: left

### Code Blocks

- Background: `#f8f9fa`
- Border: `1px solid #dee2e6`
- Border radius: `0.25rem`
- Padding: `1rem`
- Font: Monospace, `0.875rem`
- Line height: `1.5`

## Layout

### Container

- Max width: `1200px`
- Padding: `0 1.5rem`
- Centered horizontally

### Grid System

- 12-column grid for complex layouts
- Responsive breakpoints at 768px (tablet) and 1024px (desktop)

## Responsive Design

### Breakpoints

- Mobile: `< 768px`
- Tablet: `768px - 1023px`
- Desktop: `>= 1024px`

### Mobile Considerations

- Stack vertical layouts
- Reduce font sizes for very small screens
- Increase touch target sizes (minimum 44px)
- Simplify navigation (hamburger menu if needed)

## Accessibility

### Contrast

- All text must meet WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Color should not be the only means of conveying information
- Use high contrast for important information

### Focus States

- Visible focus indicators (outline: `2px solid #3b82f6`)
- Focus offset: `2px`
- Focus ring: `4px`

### Semantic HTML

- Use proper heading hierarchy (H1, H2, H3)
- Use semantic elements (header, nav, main, footer)
- Include ARIA labels where needed

## Animation and Transitions

### Guidelines

- Use transitions for interactive elements (hover, focus, active)
- Animation duration: `0.2s` to `0.3s`
- Easing: `ease` or `ease-in-out`
- No animations that could cause seizures or motion sickness

### Examples

- Button hover: `background-color 0.2s ease`
- Card hover: `transform translateY(-2px), box-shadow 0.2s ease`
- Fade-in: `opacity 0.3s ease`

## Best Practices

1. **Consistency:** Use the same styles and patterns throughout the site
2. **Simplicity:** Avoid unnecessary visual complexity
3. **Readability:** Prioritize content readability over decoration
4. **Performance:** Optimize images and CSS for fast loading
5. **Accessibility:** Design for all users, including those with disabilities
6. **Responsiveness:** Ensure all designs work on all screen sizes

## Implementation Notes

- This guide should be used by all developers working on the repository
- All new design decisions should align with this guide
- Regular reviews should ensure consistency across the site
- Consider user feedback when making design changes
