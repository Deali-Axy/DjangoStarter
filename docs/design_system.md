# DjangoStarter Frontend Design System (v2.0)

## 1. Design Philosophy: "Native Composition"
This design system leverages **DaisyUI** as the single source of truth to achieve a "Linear/Vercel-grade" aesthetic. We prioritize **consistency** and **maintainability** by strictly adhering to utility classes and standard components.

### Core Principles
- **DaisyUI First**: Use standard components (`btn`, `card`, `input`) for 100% of UI elements.
- **Composition over Customization**: Achieve high-end visuals through layout (Grid/Flex), spacing (Whitespace), and typography, not custom CSS.
- **Micro-Interactions**: Use standard `hover:` and `active:` states combined with AOS animations.

## 2. Design Tokens

### 2.1 Themes (DaisyUI)
We utilize two specific themes to ensure SaaS-grade contrast and professionalism.
- **Light Mode**: `corporate`
  - *Characteristics*: Cool grays, clear borders, high legibility.
  - *Usage*: Default for day-to-day operations.
- **Dark Mode**: `business`
  - *Characteristics*: Deep slate backgrounds (no pure black), high contrast text.
  - *Usage*: Automatic switching via `theme-controller`.

### 2.2 Typography
- **Font**: `Inter` (via Google Fonts or Local).
- **Scale**:
  - H1: `text-4xl font-bold tracking-tight` (Hero/Landing)
  - H2: `text-2xl font-bold tracking-tight` (Page Titles)
  - H3: `text-lg font-semibold` (Card Titles)
  - Body: `text-sm text-base-content/80` (Standard readability)

### 2.3 Motion & Animation (AOS)
We use **AOS (Animate On Scroll)** to add polish.
- **Standard Entry**: `data-aos="fade-up"`
- **Duration**: `300` - `500` ms (Snappy, not sluggish).
- **Easing**: `ease-out-cubic`.

### 2.4 Accessibility (WCAG 2.1 AA)
- **Contrast**: Ensure text is at least 4.5:1 ratio (DaisyUI themes handle this by default).
- **Focus**: All interactive elements must have visible focus rings (`outline-offset-2`).
- **Semantic HTML**: Use `<main>`, `<nav>`, `<aside>`, `<footer>`.
- **ARIA**: Labels for icon-only buttons (`aria-label="Toggle Sidebar"`).

## 3. Component Guidelines

### 3.1 App Shell
- **Drawer**: The core layout container. Sidebar (`drawer-side`) + Content (`drawer-content`).
- **Navbar**: Sticky top (`sticky top-0 z-30`), glass effect (`backdrop-blur`).
- **Sidebar**: `menu` component with `w-80` width.

### 3.2 Data Display
- **Cards**: `card bg-base-100 shadow-sm border border-base-200`.
- **Tables**: `table table-zebra table-pin-rows`.
- **Stats**: `stats shadow` for dashboards.

### 3.3 Forms
- **Input**: `input input-bordered w-full`.
- **Select**: `select select-bordered w-full`.
- **Toggle**: `toggle toggle-primary`.

## 4. Development Workflow
1.  **Identify Need**: "I need a modal."
2.  **Query MCP**: Use `mcp_daisyui_get_component('modal')` to see the latest syntax.
3.  **Implement**: Copy the HTML structure, adjust content.
4.  **Verify**: Check Dark Mode and Mobile responsiveness.
