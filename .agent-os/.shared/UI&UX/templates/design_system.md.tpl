# $project Design System

> **Generated:** $timestamp
> **Core Objective:** Establish a cohesive, accessible, and high-performance UI foundation.

---

## Brand Foundation

### Colors
**Mood:** $color_mood

| Role | Hex | Preview |
|------|-----|---------|
| Primary | `$colors_primary` | 🟦 |
| Secondary | `$colors_secondary` | 🟪 |
| CTA / Accent | `$colors_cta` | 🟧 |
| Background | `$colors_background` | ⬜ |
| Text | `$colors_text` | ⬛ |
| Border | `$colors_border` | 🔲 |

### Typography
**Mood:** $typography_mood

- **Heading Font:** `$typography_heading`
- **Body Font:** `$typography_body`

**Google Fonts Import:**
```css
$typography_import
```

---

## Component Specs

### Buttons
```css
/* Primary Button */
.btn-primary {
  background: $colors_cta;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 200ms ease;
  cursor: pointer;
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: $colors_primary;
  border: 2px solid $colors_primary;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 200ms ease;
  cursor: pointer;
}
```

### Cards
```css
.card {
  background: $colors_background;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 200ms ease;
  cursor: pointer;
}

.card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}
```

### Inputs
```css
.input {
  padding: 12px 16px;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 200ms ease;
}

.input:focus {
  border-color: $colors_primary;
  outline: none;
  box-shadow: 0 0 0 3px ${colors_primary}20;
}
```

---

## Style Guidelines

**Style:** $style_name
**Keywords:** $style_keywords
**Best For:** $style_best_for
**Key Effects:** $key_effects

### Page Pattern
**Pattern Name:** $pattern_name
- **Conversion Strategy:** $pattern_conversion
- **CTA Placement:** $pattern_cta_placement
- **Section Order:** $pattern_sections

---

## Anti-Patterns (Do NOT Use)

$anti_patterns

### Additional Forbidden Patterns
- ❌ **Emojis as icons** — Use SVG icons (Heroicons, Lucide, Simple Icons)
- ❌ **Missing cursor:pointer** — All clickable elements must have cursor:pointer
- ❌ **Layout-shifting hovers** — Avoid scale transforms that shift layout
- ❌ **Low contrast text** — Maintain 4.5:1 minimum contrast ratio
- ❌ **Instant state changes** — Always use transitions (150-300ms)
- ❌ **Invisible focus states** — Focus states must be visible for a11y

---

## 2026 Capabilities

| Dimension | Value |
|-----------|-------|
| Dark Mode Strategy | $dark_mode_strategy |
| AI Integration | $ai_integration |
| Privacy Tier | $privacy_tier |
| Agent Readiness | $agent_readiness |
| Performance Budget | $performance_budget |

---

## Pre-Delivery Checklist

Before delivering any UI code, verify:
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px
- [ ] No content hidden behind fixed navbars
- [ ] No horizontal scroll on mobile
- [ ] Dark mode: `prefers-color-scheme` detection + manual toggle
- [ ] AI responses: progressive streaming + confidence indicators
- [ ] Privacy: consent-before-track + GDPR/CCPA delete flow
- [ ] Core Web Vitals: LCP<2.5s, CLS<0.1, INP<200ms
