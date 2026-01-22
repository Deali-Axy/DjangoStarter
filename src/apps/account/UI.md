# Account 前端 UI 规范（DaisyUI）

本文件用于固定 account 应用的 UI 组件选型与类名组合，避免模板与表单样式分散。

## 表单（Form）

- 输入框：`input input-bordered w-full`
- 输入框错误态：`input input-bordered input-error w-full`
- 下拉：`select select-bordered w-full`
- 上传：`file-input file-input-bordered w-full`
- 开关：`toggle toggle-primary`
- 校验：在控件上追加 `validator`，错误提示使用 `validator-hint`

## 按钮（Button）

- 主按钮：`btn btn-primary`
- 次按钮：`btn btn-secondary`
- 轻量按钮：`btn btn-ghost`
- 链接按钮：`btn btn-link`
- 禁用：`btn btn-disabled` 或 `aria-disabled="true"`

## 提示（Alert / Toast）

- Alert：`alert` + `alert-success|alert-info|alert-warning|alert-error`
- Toast 容器：`toast toast-top toast-end`

## 对话框（Modal）

- 统一使用 `dialog.modal` + `div.modal-box` + `form.modal-backdrop`

## 导航（Menu / Tabs / Breadcrumbs）

- 设置中心侧边栏：`ul.menu menu-md`
- Tabs：`div.tabs` + `button.tab`，当前项加 `tab-active`

## 布局（Card / Table / Steps）

- 内容卡片：`card bg-base-100 shadow-sm border border-base-200`
- 表格：`table table-zebra`，外层包 `div.overflow-x-auto`
- 步骤：`ul.steps steps-vertical lg:steps-horizontal`，激活项加 `step-primary`

