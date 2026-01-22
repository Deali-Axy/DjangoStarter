# DjangoStarter Frontend Design System (2026)

## 1. Design Philosophy
This design system adopts the **"Linear-style"** aesthetic—characterized by high density, high contrast, and refined typography. It prioritizes content legibility and workflow efficiency over decorative elements.

### Key Principles
- **Content-First**: UI chrome (borders, backgrounds) recedes; content stands out.
- **Micro-Interactions**: Subtle feedback (hover, focus, active) confirms user actions.
- **Monochrome Foundation**: Use a neutral grayscale (Slate/Zinc) for 90% of the UI, reserving color for actions and status.
- **High Density**: Efficient use of screen real estate, suitable for complex SaaS dashboards.

## 2. Design Tokens

### 2.1 Color System (Tailwind + DaisyUI)
We utilize semantic color names mapped to specific hex values via CSS variables.

**Theme: Light (Corporate-based)**
- **Base**: White (`#ffffff`) & Slate-50 (`#f8fafc`)
- **Surface**: White with thin borders (`border-base-200`)
- **Primary**: Indigo-600 (`#4f46e5`) - Used for primary actions.
- **Text**: Slate-900 (Primary), Slate-600 (Secondary), Slate-400 (Tertiary)

**Theme: Dark (Business-based)**
- **Base**: Slate-950 (`#020617`)
- **Surface**: Slate-900 (`#0f172a`)
- **Primary**: Indigo-500 (`#6366f1`)
- **Text**: Slate-50 (Primary), Slate-400 (Secondary)

### 2.2 Typography
**Font Family**: `Inter`, system-ui, sans-serif.

| Role | Class | Size | Weight | Tracking |
| :--- | :--- | :--- | :--- | :--- |
| **H1 (Page Title)** | `text-3xl font-bold tracking-tight` | 30px | 700 | -0.025em |
| **H2 (Section)** | `text-xl font-semibold tracking-tight` | 20px | 600 | -0.025em |
| **H3 (Card Title)** | `text-base font-medium` | 16px | 500 | Normal |
| **Body** | `text-sm` | 14px | 400 | Normal |
| **Caption** | `text-xs text-base-content/60` | 12px | 400 | Normal |

### 2.3 Spacing & Radius
- **Grid Unit**: 4px (Tailwind `1` = 0.25rem = 4px).
- **Container Padding**: `p-6` (24px) for main content areas.
- **Component Gap**: `gap-4` (16px) standard.
- **Border Radius**:
    - `rounded-btn`: `0.5rem` (8px) - Buttons, Inputs.
    - `rounded-box`: `0.75rem` (12px) - Cards, Modals.

## 3. Component Guidelines

### 3.1 Buttons
- **Primary**: `btn btn-primary btn-sm` (Solid color, white text).
- **Secondary**: `btn btn-outline btn-sm` (Border only).
- **Ghost**: `btn btn-ghost btn-sm` (Transparent, hover effect) - Used for low-priority actions like "Cancel".
- **Icon**: `btn btn-square btn-ghost btn-sm` - Used for toolbar actions.

### 3.2 Cards
- **Style**: Minimalist, single pixel border, very subtle shadow (`shadow-sm`).
- **Structure**:
  ```html
  <div class="card bg-base-100 border border-base-200 shadow-sm">
    <div class="card-body p-5">
      <h3 class="card-title text-base">Card Title</h3>
      ...
    </div>
  </div>
  ```

### 3.3 Data Tables
- **Layout**: Full width, `table-zebra` optional.
- **Header**: Uppercase, smaller font (`text-xs`), subtle color.
- **Rows**: Hover effect (`hover`), clear borders (`border-b`).
- **Actions**: Right-aligned, usually hidden until hover (optional) or Ghost buttons.

### 3.4 Navigation (Sidebar)
- **Active State**: Left border accent or subtle background tint (`bg-base-200`).
- **Grouping**: Clear section headers (`menu-title`).
- **Collapse**: Support specific "mini-sidebar" mode for desktop.

## 4. Interactive Patterns (Alpine.js)

### 4.1 Modals
Use `<dialog>` element.
- **Open**: `document.getElementById('my_modal').showModal()`
- **Close**: `form method="dialog"` or clicking backdrop.

### 4.2 Dropdowns
Alpine.js for click-outside handling:
```html
<div x-data="{ open: false }" @click.outside="open = false">
  <button @click="open = !open">Trigger</button>
  <div x-show="open" x-transition>Menu</div>
</div>
```

## 5. Accessibility (A11y)
- **Focus Rings**: Ensure `outline-offset-2` is visible on keyboard navigation.
- **Contrast**: Text color must pass WCAG AA standards against background.
- **Semantic HTML**: Use `<nav>`, `<main>`, `<aside>`, `<footer>`.
