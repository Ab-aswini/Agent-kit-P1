# DASHBOARD Design System

> **Generated:** 2026-02-24 11:36:13
> **Core Objective:** Establish a cohesive, accessible, and high-performance UI foundation.

---

## Brand Foundation

### Colors

**Mood:**

| Role         | Hex              | Preview |
| ------------ | ---------------- | ------- |
| Primary      | `primary_hex`    | 🟦      |
| Secondary    | `secondary_hex`  | 🟪      |
| CTA / Accent | `cta_hex`        | 🟧      |
| Background   | `background_hex` | ⬜      |
| Text         | `text_hex`       | ⬛      |
| Border       | ``               | 🔲      |

### Typography

**Mood:** mood_style_keywords

- **Heading Font:** `heading_font`
- **Body Font:** `body_font`

**Google Fonts Import:**

```css
css_import
```

---

## Component Specs

### Buttons

```css
/* Primary Button */
.btn-primary {
  background: cta_hex;
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
  color: primary_hex;
  border: 2px solid primary_hex;
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
  background: background_hex;
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
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 200ms ease;
}

.input:focus {
  border-color: primary_hex;
  outline: none;
  box-shadow: 0 0 0 3px primary_hex20;
}
```

---

## Style Guidelines

**Style:** Dark Mode (OLED)
**Keywords:** Dark theme, low light, high contrast, deep black, midnight blue, eye-friendly, OLED, power efficient
**Best For:** Night-mode apps, coding platforms, entertainment, OLED devices, AI dashboards, monitoring
**Key Effects:** Minimal glow (text-shadow: 0 0 10px), dark-to-light transitions, high readability, visible focus states

### Page Pattern

**Pattern Name:** Data-Dense Dashboard

- **Conversion Strategy:**
- **CTA Placement:** Above fold
- **Section Order:** Hero > Features > CTA

---

## Anti-Patterns (Do NOT Use)

- ❌ Light mode default
- ❌ Slow rendering

### Additional Forbidden Patterns

- ❌ **Emojis as icons** — Use SVG icons (Heroicons, Lucide, Simple Icons)
- ❌ **Missing cursor:pointer** — All clickable elements must have cursor:pointer
- ❌ **Layout-shifting hovers** — Avoid scale transforms that shift layout
- ❌ **Low contrast text** — Maintain 4.5:1 minimum contrast ratio
- ❌ **Instant state changes** — Always use transitions (150-300ms)
- ❌ **Invisible focus states** — Focus states must be visible for a11y

---

## 2026 Capabilities

| Dimension          | Value                        |
| ------------------ | ---------------------------- |
| Dark Mode Strategy | OLED-dark-default            |
| AI Integration     | anomaly-detect+forecast-ai   |
| Privacy Tier       | PCI-DSS+SOC2+GDPR            |
| Agent Readiness    | 5/5 financial AI             |
| Performance Budget | LCP<1.5s; CLS<0.05; INP<50ms |

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
