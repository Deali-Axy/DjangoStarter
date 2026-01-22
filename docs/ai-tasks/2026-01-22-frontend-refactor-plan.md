# 前端 UI 重构方案：从 Flowbite 迁移至 DaisyUI

时间: 2026-01-22 10:42:32

## TODO

### 1. 设计调研与规范制定 (Design Research & Specs)
- [x] **调研顶级产品设计风格**:
    - [x] 分析 **Linear / Vercel** (SaaS 标杆): 学习其高对比度、微交互、以及“黑白灰”的高级运用。
    - [x] 分析 **Apple** (Human Interface Guidelines): 学习其模糊效果 (Backdrop Blur)、圆角处理和图标一致性。
    - [x] 分析 **Google** (Material Design 3): 借鉴其色彩系统 (Dynamic Color) 和海拔 (Elevation) 阴影处理。
    - [x] 产出调研总结：已创建 [Frontend Design System](../design_system.md)。
- [x] **制定前端设计规范**:
    - [x] 定义 **Color System**: 确定 Primary/Secondary/Accent 色板，以及 Dark Mode 适配规则。
    - [x] 定义 **Typography**: 设定 H1-H6 字体大小、行高、字重 (Inter 字体)。
    - [x] 定义 **Spacing & Radius**: 统一间距 (4px grid) 和圆角 (0.5rem / 1rem)。
    - [x] 定义 **Shadows & Depth**: 设定不同层级的阴影效果。

### 2. 组件重构清单 (Component Refactoring)
- [ ] **基础原子组件**:
    - [ ] Button: 迁移至 DaisyUI `btn`，定义 primary, ghost, link 变体。
    - [ ] Inputs: 迁移至 `input`, `textarea`, `checkbox`, `toggle`，统一 Focus Ring 样式。
    - [ ] Badge/Tag: 迁移至 `badge`，用于状态标识。
    - [ ] Avatar: 迁移至 `avatar` 组件。
- [ ] **复合交互组件**:
    - [ ] Navbar: 实现响应式顶部导航，集成移动端 Drawer 开关。
    - [ ] Sidebar: 实现可折叠/固定侧边栏，菜单项高亮逻辑。
    - [ ] Modal: 使用原生 `<dialog>` + DaisyUI 样式，支持 ESC 关闭。
    - [ ] Dropdown: 结合 Alpine.js 实现点击外部关闭。
    - [ ] Toast/Alert: 实现全局通知组件。
- [ ] **数据展示组件**:
    - [ ] Table: 迁移至 `table table-zebra`，优化移动端滚动体验。
    - [ ] Card: 统一卡片容器 padding 和 border 样式。
    - [ ] Pagination: 分页器样式统一。

### 3. 实施与验收 (Implementation & QA)
- [x] **Phase 1: 基础环境与规范 (Week 1)**
    - [x] 移除 Flowbite，安装配置 DaisyUI & Alpine.js。
    - [x] 建立全局 CSS 变量 (Design Tokens) (已通过 DaisyUI Themes 配置)。
- [ ] **Phase 2: 组件库迁移 (Components)**
    - [x] **Navbar 重构**: 已使用 DaisyUI `navbar` + Alpine.js 实现响应式导航。
    - [x] **Page Header 重构**: 已更新 `page_header.html` 适配新设计风格。
    - [x] **Alert 重构**: 已更新 `alert.html` 使用 DaisyUI `alert` 组件。
    - [x] **Sidebar 重构**: 已在 `_base.html` 中实现 Drawer 侧边栏结构。
    - [ ] **单元测试**: 为核心交互组件 (如 Dropdown, Modal) 编写简单的 JS 逻辑测试 (可选)。
    - [ ] **UI测试**: 确保每个组件在 Light/Dark 模式下表现一致。
- [ ] **Phase 3: 页面重构 (Pages)**
    - [ ] 重构 `_base.html` 布局。
    - [ ] 重构 Landing Page (Home)。
    - [ ] 重构 Auth 页面。
    - [ ] 重构 Dashboard 核心页。

### 4. 文档维护 (Documentation)
- [ ] **实时更新**: 每完成一个 Checkbox，同步更新本文档状态。
- [ ] **决策记录**: 在 `docs/architecture/decisions` (如有) 或本文档末尾记录关键 UI 变更决策。
- [ ] **截图对比**: 记录重构前后的对比截图和性能指标变化。

### 5. 质量保证 (Quality Assurance)
- [ ] **设计评审**: 检查视觉还原度。
- [ ] **代码审查**: 检查 HTML 语义化和 Tailwind 类名使用。
- [ ] **用户体验测试**: 重点测试移动端和深色模式。

## 1. 概述

本项目计划对前端 UI 进行全面重构，移除 `flowbite` 及其相关 JS 依赖，全面拥抱 **Tailwind CSS + DaisyUI** 生态。

使用 daisyui MCP 查询相关组件，确保新的组件库符合项目需求。

### 1.1 重构目标

*   **提升代码质量**：利用 DaisyUI 的语义化组件类（如 `btn btn-primary`）替代冗长的 Utility Classes，大幅精简 HTML 代码。
*   **统一设计语言**：通过 DaisyUI 的组件系统强制统一 UI 风格，避免“样式碎片化”。
*   **升级交互体验**：利用 Drawer 布局优化响应式体验，引入更现代的 Skeleton 加载屏；**引入 Alpine.js 处理复杂交互**。
*   **增强主题能力**：实现基于 CSS 变量的纯 CSS 主题切换（Light/Dark 及更多预设主题），去除复杂的主题切换 JS 逻辑。

### 1.2 技术栈变更

| 模块 | 当前状态 (Old) | 目标状态 (New) | 优势 |
| :--- | :--- | :--- | :--- |
| **CSS 框架** | Tailwind CSS v3 + Flowbite Plugin | Tailwind CSS **v4** + **DaisyUI v5 Plugin** | 代码量减少 ~70%，语义更清晰，构建更快 |
| **组件库** | Flowbite (HTML + JS) | **DaisyUI v5** (Pure CSS) | 移除 JS 依赖，性能更好，定制更易 |
| **交互逻辑** | Flowbite JS / Vanilla JS | **Alpine.js** | 声明式语法，轻量级，易维护 |
| **布局系统** | 自定义 Flex/Grid 布局 | **DaisyUI Drawer** 组件 | 原生支持移动端侧滑菜单，结构更稳固 |
| **主题切换** | 手动 JS 控制 DOM Class | **Theme Controller** (CSS only) | 无闪烁，配置简单，支持多主题 |
| **图标库** | FontAwesome 6 | FontAwesome 6 (保持不变) | - |

---

## 2. 详细设计方案

### 2.1 视觉风格 (Visual Identity)

采用 **SaaS 企业级** 设计风格，对标 Linear / Vercel。

*   **默认主题 (Light)**: 使用 `corporate` 主题。
    *   *特征*：冷灰色系，高对比度，边框细腻，专业感强。
*   **暗色主题 (Dark)**: 使用 `business` 主题。
    *   *特征*：深灰背景（非纯黑），层级分明，适合长时间工作。
*   **圆角系统**: 全局使用 `rounded-box` 变量，设定为 `0.5rem` (8px)，兼顾现代感与稳重。
*   **排版**: 标题使用 `font-bold tracking-tight`，正文保持 `Inter` 字体。

### 2.2 布局架构重构 (`_base.html`)

废弃原有的流式布局，改用 DaisyUI 的 **Drawer (抽屉)** 布局作为根容器。

```html
<!-- 根布局示意 -->
<body class="bg-base-100 text-base-content">
  <div class="drawer lg:drawer-open">
    <input id="app-drawer" type="checkbox" class="drawer-toggle" />
    
    <!-- 1. 页面主内容 -->
    <div class="drawer-content flex flex-col">
      <!-- 顶部导航栏 (Navbar) -->
      <div class="navbar bg-base-100 border-b border-base-300 sticky top-0 z-30 backdrop-blur">
         <!-- 移动端菜单开关 -->
         <div class="flex-none lg:hidden">
            <label for="app-drawer" class="btn btn-square btn-ghost">
                <i class="fa-solid fa-bars"></i>
            </label>
         </div>
         <div class="flex-1">...</div>
         <div class="flex-none">...</div>
      </div>

      <!-- 内容区 -->
      <main class="p-6">
        {% block content %}{% endblock %}
      </main>
      
      <!-- Footer -->
      <footer class="footer ...">...</footer>
    </div>

    <!-- 2. 侧边栏 (Sidebar) -->
    <div class="drawer-side z-40">
      <label for="app-drawer" class="drawer-overlay"></label>
      <aside class="menu p-4 w-80 min-h-full bg-base-200 text-base-content border-r border-base-300">
        <!-- 侧边菜单内容 -->
      </aside>
    </div>
  </div>
</body>
```

### 2.3 核心组件映射表

| 组件 | Flowbite (原) | DaisyUI (新) | 备注 |
| :--- | :--- | :--- | :--- |
| **Primary Button** | `text-white bg-blue-700 hover:bg-blue-800 ...` | `btn btn-primary` | 自动适配主题色 |
| **Card** | `bg-white border border-gray-200 shadow ...` | `card bg-base-100 shadow-xl border border-base-200` | 结构分为 `card-body` |
| **Input** | `bg-gray-50 border-gray-300 text-gray-900 ...` | `input input-bordered w-full` | Focus 状态更统一 |
| **Modal** | `div` + `data-modal-target` + JS | `dialog.modal` + `form[method="dialog"]` | 原生 HTML Dialog |
| **Dropdown** | `div` + `data-dropdown-toggle` + JS | `details.dropdown` | 纯 CSS 实现 |
| **Alert** | `p-4 mb-4 text-blue-800 bg-blue-50 ...` | `alert alert-info` | 支持 icon 插槽 |
| **Badge** | `bg-blue-100 text-blue-800 ...` | `badge badge-primary` | - |
| **Table** | `w-full text-sm text-left ...` | `table table-zebra` | 自动斑马纹 |

### 2.4 交互增强方案 (Alpine.js Integration)

虽然 DaisyUI 提供了纯 CSS 的组件状态，但在复杂场景下仍需 JS 介入。我们将使用 **Alpine.js** 来处理以下场景：

*   **复杂表单逻辑**：如多步表单验证、动态字段增删 (Repeater Fields)。
*   **异步状态管理**：配合 HTMX 处理加载状态、局部刷新后的 UI 响应。
*   **UI 状态联动**：如 Sidebar 的展开/收起状态持久化 (localStorage)。
*   **Dropdown/Modal 增强**：在需要点击外部关闭、ESC 关闭等高级交互时，使用 Alpine.js 包装 DaisyUI 组件。

示例 - 结合 Alpine 的 Dropdown：
```html
<div x-data="{ open: false }" class="dropdown">
  <div tabindex="0" role="button" class="btn m-1" @click="open = !open">Click</div>
  <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52" x-show="open" @click.outside="open = false">
    <li><a>Item 1</a></li>
    <li><a>Item 2</a></li>
  </ul>
</div>
```

### 2.5 项目开发规范遵循 (Compliance)

本重构方案严格遵循 `AGENTS.md` 中定义的开发规范：

*   **工作流集成**：
    *   使用 `pnpm` 管理前端依赖。
    *   使用 `Gulp` 处理静态资源移动 (`pnpm gulp:move`)。
    *   开发时使用 `pnpm run tw:watch` 实时编译 Tailwind CSS。
*   **目录结构**：
    *   保持 `src/templates` 存放通用模板（如 `_base.html`）。
    *   保持 `src/apps/[app]/templates` 存放应用特定模板。
*   **模板规范**：
    *   继续使用 `{% load page_tags %}` 和 `{% page_header ... %}` 组件，需同步更新其实现以适配 DaisyUI。
    *   遵循 Django Template 语义化标签和无障碍标准。

### 2.6 架构优化：引入 Home 应用

当前主页位于 `django_starter/contrib/guide` 应用中，这不符合常规认知且耦合了文档与核心着陆页逻辑。我们将引入全新的 `home` 应用。

*   **应用定位**: `src/apps/home`
*   **职责范围**:
    *   **Landing Page (首页)**: 产品展示、功能介绍、定价方案 (Marketing Site)。
    *   **Dashboard (控制台首页)**: 登录后的首屏，展示核心指标、快捷入口 (App Shell)。
*   **设计灵感 (World-Class Design)**:
    *   **风格对标**: Linear (精致暗黑/高对比度), Vercel (极简几何), Stripe (细节微交互)。
    *   **Landing Page 核心元素**:
        *   **Hero Section**: 醒目的 H1 标题 (Tracking-tight)，副标题高亮关键价值，双 CTA 按钮 (Primary/Ghost)。
        *   **Bento Grid**: 使用“便当盒”网格布局展示特性，替代传统的左右图文排版，提升视觉密度和现代感。
        *   **Social Proof**: 动态滚动的客户/合作伙伴 Logo 墙。
    *   **Dashboard 核心元素**:
        *   **Overview Cards**: 关键指标卡片，包含迷你趋势图 (Sparklines)。
        *   **Quick Actions**: 常用操作的快捷入口，使用大图标+文字描述。
        *   **Activity Feed**: 最近活动的时间轴展示。

---

## 3. 实施步骤 (Roadmap)

### Phase 1: 环境准备与原型验证
1.  **依赖安装**: 安装 `daisyui` npm 包；**确认 `alpinejs` 已安装**；执行 `pnpm gulp:move` 更新静态资源。
2.  **配置 Tailwind**: 修改 `tailwind.config.js`，引入 `daisyui` 插件，配置 `themes: ["corporate", "business"]`。
3.  **集成 Alpine.js**: 在 `_base.html` 中引入 Alpine.js (替换 Flowbite JS)。
4.  **原型开发**: 创建 `src/templates/_base_daisy_demo.html`，实现新的 Drawer 布局，验证响应式效果；*开发过程中保持 `pnpm run tw:watch` 运行*。

### Phase 2: 核心组件迁移
1.  **Navbar 重构**: 使用 DaisyUI `navbar` 组件重写顶部导航，**结合 Alpine.js 实现移动端菜单切换**。
2.  **Page Header 重构**: 更新 `src/django_starter/contrib/navbar/templatetags/page_tags.py` 中的 `page_header` 组件以适配 DaisyUI 样式，组件模板代码在 `src/django_starter/contrib/navbar/templates/django_starter/components/page_header.html`。
3.  **Alert 重构**: 修改 `src/templates/_components/alert.html`。
4.  **Sidebar 重构**: 在 `account` 应用中测试新的侧边栏结构。

### Phase 3: 页面重构 (Pages)
- [x] **创建 Home 应用**:
    - [x] 创建应用 `src/apps/home` 并注册。
    - [x] 路由接管: 根路径 `/` 指向 `apps.home.urls`。
- [x] **Landing Page 重构 (Home)**:
    - [x] 新建 `index.html`，实现 Hero + Bento Grid + Social Proof。
    - [x] 适配 `_base.html` 的 Drawer 布局 (Landing Page 默认隐藏侧边栏)。
- [x] **Dashboard 重构 (Home)**:
    - [x] 新建 `dashboard.html`，实现 Stats, Quick Actions, Activity Feed。
- [x] **业务应用重构 (Apps)**:
    - [x] **Account (`src/apps/account`)**:
        - [x] Auth: 重构登录、注册、找回密码页面 (使用 DaisyUI Card, Input)。
        - [x] Profile: 重构个人中心与设置页 (使用 DaisyUI Menu, Card, Toggle)。
    - [x] **Demo (`src/apps/demo`)**:
        - [x] Data Display: 重构电影/音乐列表页 (使用 DaisyUI Card, Table Zebra, Menu)。
        - [x] HTMX: 验证 HTMX 交互 (保留原有 attributes, 样式适配)。
- [x] **核心组件库重构 (Contrib)**:
    * 参考世界顶级的产品的相关UI设计
    *   [x] **About (`contrib.about`)**: 重构关于、联系我们页 (移除 Slate 色系，使用 base-content/primary)。
    *   [x] **Docs (`contrib.docs`)**: 适配文档阅读器页面 (继承 `_base.html`, 使用 Drawer/Card 布局)。
    *   [x] **Forms (`contrib.forms`)**: 
        - [x] 更新 `widget_classes.py` 使用 DaisyUI `input-bordered` 等类。
        - [x] 重构 Datepicker Widget 为原生样式。
    *   [ ] **Guide (`contrib.guide`)**: 确认首页内容已迁移至 `Home` 应用，清理旧代码。

### Phase 4: 清理与收尾
1.  **移除 Flowbite**: 删除 `node_modules` 中的 flowbite。
2.  **清理静态资源**: 删除 `src/static/lib/flowbite`；执行 `pnpm gulp:move` 确保最终产物干净。
3.  **全局测试**: 确保 Light/Dark 切换正常，移动端菜单正常，所有 HTMX 交互正常。

---

## 4. 预期收益

1.  **开发效率提升**: 编写 HTML 的时间减少，不再需要记忆复杂的 Tailwind 类名组合。
2.  **维护成本降低**: UI 风格统一由 DaisyUI 配置文件管理，修改全局圆角或配色只需改一行配置。
3.  **代码可读性增强**: `btn btn-primary` 远比 20 个 utility classes 易读。
4.  **现代化体验**: 获得类似原生 App 的流畅交互感（Drawer, Modal）。
