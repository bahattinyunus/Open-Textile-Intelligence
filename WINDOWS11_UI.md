# Windows 11 Modern UI - Design Specification

## Overview

The Open Textile Intelligence application features a modern Windows 11-inspired dark theme with clean typography, proper spacing, and professional visual hierarchy.

---

## Design System

### Color Palette

**Background Colors:**
- Primary Background: `#202020` (Dark neutral)
- Surface/Cards: `#2b2b2b` (Elevated surface)
- Borders: `#3a3a3a` (Subtle dividers)
- Hover States: `#303030` (Interactive feedback)

**Text Colors:**
- Primary Text: `#ffffff` (High emphasis)
- Secondary Text: `#a0a0a0` (Medium emphasis)
- Tertiary Text: `#909090` (Low emphasis)

**Accent Colors:**
- Primary Accent: `#0067c0` (Windows 11 Blue)
- Success: `#0f7b0f` (Green)
- Warning: `#f7630c` (Orange)
- Critical: `#d13438` (Red)
- Caution: `#ffc83d` (Yellow)

---

## Typography

**Font Family:**
- Primary: Segoe UI (Windows 11 default)
- Fallback: Segoe UI Variable, Arial, sans-serif

**Font Sizes:**
- Section Titles: 14pt, Weight 600
- Metric Values: 32pt, Weight 600
- Metric Titles: 9pt, Weight 600
- Metric Units: 11pt, Weight 400
- Body Text: 10pt
- Status Text: 9pt

---

## Component Specifications

### Metric Cards

**Dimensions:**
- Min Height: 120px
- Min Width: 180px
- Border Radius: 12px

**Spacing:**
- Padding: 20px (all sides)
- Internal Spacing: 8px between elements
- Card Gap: 8px between cards

**Visual:**
- Background: `#2b2b2b`
- Border: 1px solid `#3a3a3a`
- Hover: Background `#303030`, Border `#404040`

**Layout:**
```
┌─────────────────────────┐
│  TITLE (9pt, #a0a0a0)  │  ← 20px padding top
│                         │
│  32                     │  ← Value (32pt, #ffffff)
│  unit                   │  ← Unit (11pt, #909090)
│                         │
│                         │  ← Stretch to fill
└─────────────────────────┘
   20px padding sides
```

### Buttons

**Primary (Accent):**
- Background: `#0067c0`
- Hover: `#005ba1`
- Pressed: `#004a7f`
- Height: 36px minimum
- Padding: 10px 24px
- Border Radius: 6px

**Start Button:**
- Background: `#0f7b0f`
- Hover: `#0d6b0d`

**Stop Button:**
- Background: `#d13438`
- Hover: `#b52e31`

### Progress Bars

**Style:**
- Height: 28px
- Border Radius: 6px
- Background: `#2b2b2b`
- Border: 1px solid `#3a3a3a`
- Chunk (Fill): `#0067c0`, Border Radius 5px

### Table

**Style:**
- Background: `#2b2b2b`
- Alternate Row: `#282828`
- Border Radius: 8px
- Border: 1px solid `#3a3a3a`
- Cell Padding: 12px 16px

**Header:**
- Background: `#252525`
- Border Bottom: 1px solid `#3a3a3a`
- Font Weight: 600
- Padding: 12px 16px

**Selection:**
- Background: `#0067c0`
- Color: `#ffffff`

### ComboBox (Dropdown)

**Style:**
- Background: `#2b2b2b`
- Border: 1px solid `#3a3a3a`
- Border Radius: 6px
- Padding: 8px 12px
- Min Height: 32px
- Hover Border: `#505050`

### Slider

**Style:**
- Groove: `#2b2b2b`, 6px height, Border Radius 3px
- Handle: `#0067c0`, 18px diameter, Border Radius 9px
- Hover Handle: `#005ba1`

### Scrollbar

**Style:**
- Width: 12px
- Handle: `#505050`, Border Radius 6px
- Hover Handle: `#606060`
- Min Handle Height: 30px

---

## Spacing System

**Standard Spacing Units:**
- Extra Small: 4px
- Small: 8px
- Medium: 12px
- Large: 16px
- Extra Large: 20px
- XXL: 24px

**Card Padding:** 20px (Windows 11 standard)
**Button Padding:** 10px vertical, 24px horizontal
**Section Spacing:** 8px between sections

---

## Interactive States

### Hover States
- Buttons: Darken by ~10%
- Cards: Lighten background slightly
- Borders: Increase contrast

### Pressed States
- Buttons: Darken by ~20%
- Scale: No scale effects (follows Windows 11 guidelines)

### Disabled States
- Background: `#3a3a3a`
- Text: `#707070`
- Opacity: Not reduced (Windows 11 style)

---

## Defect Severity Colors

**Color Mapping:**
- Critical (Delik, İplik Kopması, Yırtık): `#d13438` (Red)
- Warning (Leke, Dokuma Hatası): `#f7630c` (Orange)
- Caution (Renk Uyuşmazlığı): `#ffc83d` (Yellow)
- Success (Temiz): `#0f7b0f` (Green)
- Default: `#a0a0a0` (Gray)

---

## Layout Guidelines

### Window
- Default Size: 95% of screen, max 1800x950
- Centered on screen
- Min Size: 1200x800

### Grid System
- Use QVBoxLayout and QHBoxLayout
- No absolute positioning
- Responsive resizing with stretch factors

### Content Hierarchy
1. **Top**: Mode selector, controls, camera test
2. **Middle**: Metric cards (horizontal row)
3. **Middle**: Progress bars
4. **Bottom**: Split view (Camera feed | Detection table)
5. **Footer**: Status bar

---

## Accessibility

### Contrast Ratios
- Text on Dark Background: 12:1 (AAA)
- Interactive Elements: Minimum 3:1 border contrast
- Status Colors: High contrast (4.5:1 minimum)

### Font Sizing
- No text smaller than 9pt
- Interactive elements minimum 32px tall
- Touch targets minimum 36px

---

## Implementation Notes

### QSS (Qt Style Sheets)
- All styles defined in `desktop_app/ui/styles.py`
- DARK_THEME variable contains complete stylesheet
- No inline styles in widgets (except specific overrides)

### Widgets
- MetricCard: Custom QFrame with VBoxLayout
- All other components use standard Qt widgets
- Object names used for targeted styling

### Responsive Behavior
- Splitters allow user-adjustable layout
- Metric cards maintain minimum width
- Tables stretch to fill available space
- Camera view maintains aspect ratio

---

## Future Enhancements

### Light Mode (Planned)
- Background: `#f5f5f5`
- Surface: `#ffffff`
- Text: `#1a1a1a`
- Accent: Same blue `#0067c0`

### Animations (Planned)
- Fade transitions on value updates
- Smooth progress bar fills
- Subtle hover effects

### Customization (Planned)
- User-selectable accent colors
- Adjustable font sizes
- Layout presets

---

## References

- Windows 11 Design Guidelines: https://learn.microsoft.com/en-us/windows/apps/design/
- Fluent Design System: https://fluent2.microsoft.design/
- Qt Style Sheets: https://doc.qt.io/qt-6/stylesheet-reference.html
