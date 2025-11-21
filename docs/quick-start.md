# DjangoStarter v3 零基础快速入门

面向没有 Django 基础的 Python 开发者，带你在 60–90 分钟内完成环境搭建、项目运行、页面与 API 编写、以及代码生成器的使用。教程完全基于本仓库结构与约定（Django 5 + Django-Ninja + HTMX/Alpine/Tailwind）。

---

## 你将收获
- 了解 Django 与 DjangoStarter 的关系与优势
- 在 Windows + PowerShell 下完成依赖安装与项目启动
- 掌握项目目录结构与关键配置位置（settings、urls、api）
- 编写一个页面视图（模板）与一个 Ninja API（类型安全）
- 使用自动代码生成器按模型生成 CRUD 接口与测试
- 了解 URL 前缀、缓存、后台、安全等常用配置入口

## Django 与 DjangoStarter 的关系与优势

- 关系
  - DjangoStarter 基于 Django 5，保留标准目录结构与配置习惯；不替代、不绕开 Django，只是将最佳实践工程化并约定化。
  - 集成 Django-Ninja 作为 API 层，类型安全、自动生成文档、性能更好；接口开发更快更简洁。
  - 模板视图、URL、Admin、ORM、迁移等全部沿用 Django；你现有的 Django 技能零迁移。

- 优势
  - 工程化开箱即用：拆分 settings、统一 URL 前缀、缓存、认证与密码策略（Argon2）、CORS。
  - 安全增强：Admin 登录验证码、IP 白名单限制、中间件与错误查看权限。
  - 生产级能力：Docker 多阶段构建、Nginx 模板、健康检查、ASGI（Daphne/Granian）、日志与观测。
  - 开发效率：自动代码生成器（按模型生成 schema/CRUD/tests/admin）、随机种子数据。
  - 前端集成：HTMX/Alpine/Tailwind + pnpm/gulp 构建管线。
  - AI 原生：预留 LLM 接入、向量检索/嵌入、函数调用、异步任务与流式响应扩展点。
  - 典型场景：个人/独立产品 MVP、企业内部工具、数据看板、以及各类 AI Agent/助手的后端。

- 总结
  - 用 Django 的可靠性 + Ninja 的速度，减少样板与部署细节，让你把时间全部留给业务。

---

## 前置知识与准备

- 会使用 Python 与基础命令行即可（不需要 Django 经验）
- 操作系统：Windows（PowerShell）、macOS（zsh/bash）、Linux（bash）
- Python：推荐 3.12（3.11 也可运行）
- 包管理器：PDM（后端）、pnpm（前端）
- Node.js：任意 LTS 版本（建议 v18+）
- 可选：Redis（用于限流、缓存等）

> 如果你尚未克隆本仓库，请参考 README 的克隆与版本说明。示例命令分别给出 Windows 与 macOS/Linux 版本。项目根路径示例：`d:\Code\DjangoStarter`（Windows）或 `~/Code/DjangoStarter`（macOS/Linux）。

---

## 第 1 部分：启动项目（10–20 分钟）

以下分别给出 Windows（PowerShell）与 macOS（zsh/bash）命令。推荐在项目根目录下创建与启用虚拟环境。

1) 创建并启用虚拟环境（任选其一）

```powershell
# 方式 A：Python venv（推荐初学者）
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 方式 B：Conda（如已安装）
conda create -n django-starter python=3.12
conda activate django-starter
```

2) 安装 PDM 并安装后端依赖

```powershell
pip install pdm
pdm install
```

3) 安装前端依赖并构建静态资源

```powershell
# 如未安装 pnpm，可先安装：
# npm install -g pnpm
pnpm install

# 将前端资源复制到静态目录（一次性）
gulp move
# 如需使用 TailwindCSS，可执行：
# npm run tailwind:watch
```

4) 初始化数据库并启动开发服务器

```powershell
# 进入 src 目录（manage.py 在此）
cd src
python manage.py migrate
python manage.py runserver
```

### macOS 终端（zsh/bash）

1) 创建并启用虚拟环境（任选其一）

```bash
# 方式 A：Python venv（推荐初学者）
python3 -m venv .venv
source .venv/bin/activate

# 方式 B：Conda（如已安装）
conda create -n django-starter python=3.12
conda activate django-starter
```

2) 安装 PDM 并安装后端依赖

```bash
python3 -m pip install pdm
pdm install
```

3) 安装前端依赖并构建静态资源

```bash
# 如未安装 pnpm，可先安装：
# npm install -g pnpm
pnpm install

# 将前端资源复制到静态目录（一次性）
gulp move
# 如需使用 TailwindCSS，可执行：
# npm run tailwind:watch
```

4) 初始化数据库并启动开发服务器

```bash
cd src
python3 manage.py migrate
python3 manage.py runserver
```

5) 验证运行
- 首页（欢迎页）：`http://localhost:8000/`
- 管理后台：`http://localhost:8000/admin/`
- API 文档（Swagger）：`http://localhost:8000/api/docs`

> 如果你配置了 URL 前缀（见后文），地址会变为 `http://localhost:8000/<前缀>/...`。

---

## 第 2 部分：项目结构一览（5 分钟）

本仓库核心目录结构（精简版）：

```
src/
├── apps/                    # 你的业务应用（建议新增应用都放这里）
├── config/                  # 项目配置（settings/urls/apis）
│   ├── settings/            # 拆分配置（components + environments）
│   ├── urls.py              # 核心 URL 路由
│   ├── urls_root.py         # 前缀路由入口（支持 URL_PREFIX）
│   └── apis.py              # NinjaAPI 初始化与路由注册
├── django_starter/          # 框架内置模块（中间件、生成器、http包装等）
├── templates/               # 全局模板（含 _base.html）
├── static/                  # 静态文件（前端构建产物）
└── manage.py                # Django 管理脚本
```

你会频繁修改的位置：
- `src/config/settings/components/install_apps.py`：将新应用加入 `INSTALLED_APPS`
- `src/config/urls.py`：为新应用添加网页路由（传统 Django 视图）
- `src/config/apis.py`：为新应用添加 API 路由（Django-Ninja）
- `src/apps/<your_app>/`：你的模型、视图、URL、模板、API 文件都在这里

---

## 第 3 部分：第一个页面（Django 模板视图）

目标：创建一个名为 `blog` 的应用，编写一个最简单的“欢迎页面”。

1) 创建应用

```powershell
cd d:\Code\DjangoStarter\src\apps
django-admin startapp blog
```

2) 注册应用到 `INSTALLED_APPS`

编辑 `src/config/settings/components/install_apps.py`，将 `apps.blog` 添加到“我们的应用”区域：

```python
# 我们自己的应用
'apps.account',
'apps.demo',
'apps.blog',  # 新增的应用
```

3) 编写视图（`src/apps/blog/views.py`）

```python
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def hello(request: HttpRequest) -> HttpResponse:
    """
    视图：渲染欢迎页面

    Args:
        request: 当前请求对象
    Returns:
        HttpResponse: 渲染后的 HTML 响应
    """
    context = {"page_title": "Blog 欢迎页", "message": "Hello, DjangoStarter!"}
    return render(request, "blog/hello.html", context)
```

4) 定义应用路由（`src/apps/blog/urls.py`）

```python
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.hello, name="hello"),
]
```

5) 注册到项目路由（`src/config/urls.py`）

在 `urlpatterns` 中添加一行：

```python
path('blog/', include('apps.blog.urls')),
```

6) 创建模板文件（推荐放到应用内：`src/apps/blog/templates/blog/hello.html`）

```html
{% extends '_base.html' %}
{% load static %}

{% block title %}{{ page_title }}{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8" x-data="{open:true}">
  <h1 class="text-3xl font-bold text-gray-900 mb-6">{{ page_title }}</h1>
  <p class="text-gray-700">{{ message }}</p>
</div>
{% endblock %}
```

7) 运行并访问：`http://localhost:8000/blog/`

> 注意：如果设置了 URL 前缀，比如 `djangostarter`，则地址为 `http://localhost:8000/djangostarter/blog/`。
 
8) 如果页面缺少样式，请启动 TailwindCSS 构建
 
- 说明：本项目的样式由 TailwindCSS 生成。未启动构建或未复制初始资源时，页面可能看起来无样式。
 
- 初始化静态资源（首次或变更后执行）：
 
```powershell
# Windows（PowerShell）
pnpm run gulp:move
```
 
```bash
# macOS/Linux（zsh/bash）
pnpm run gulp:move
```
 
- 开发模式（持续监听并生成样式，建议在单独终端运行）：
 
```powershell
# Windows（PowerShell）
pnpm run tailwind:watch
```
 
```bash
# macOS/Linux（zsh/bash）
pnpm run tailwind:watch
```
 
- 生产/一次性构建（不监听，仅生成压缩后的样式）：
 
```powershell
# Windows（PowerShell）
pnpm run tailwind:build
```
 
```bash
# macOS/Linux（zsh/bash）
pnpm run tailwind:build
```
 
> 提示：若你更习惯 npm，也可将以上命令中的 `pnpm run` 替换为 `npm run`。

---

## 第 4 部分：第一个 API（Django-Ninja）

目标：在 `blog` 应用中创建一个简单的 API，并注册到全局 `NinjaAPI`。

1) 创建 API 路由文件（`src/apps/blog/apis.py`）

```python
from typing import Optional
from ninja import Router, Schema

router = Router(tags=["blog"])  # 在 Swagger 中使用该标签分组


class HelloOut(Schema):
    """
    输出：Hello 接口的响应模型

    Attributes:
        message: 文本消息
        name: 可选的名称
    """
    message: str
    name: Optional[str] = None


@router.get("/hello", response=HelloOut)
def hello(request, name: Optional[str] = None) -> HelloOut:
    """
    接口：返回问候消息

    Args:
        request: 当前请求对象（由 Django 提供）
        name: 可选的来访者名称
    Returns:
        HelloOut: 问候消息与名称
    """
    who = name or "world"
    return HelloOut(message="Hello from Ninja!", name=who)
```

> 也可以将 apis 按模型拆分到 `apps/blog/apis/<model>/apis.py`，后续在代码生成器章节会自动生成这类结构。

2) 注册 API 路由（`src/config/apis.py`）

将 `blog` 路由加入全局 API：

```python
from apps.blog.apis import router as blog_router

api.add_router('blog', blog_router)
```

3) 访问接口与文档
- Hello 接口：`http://localhost:8000/api/blog/hello`
- Swagger 文档：`http://localhost:8000/api/docs`（可交互测试）

---

## 第 5 部分：自动代码生成器（CRUD + 测试）

自动生成器让你“只写模型”，其余（admin、apps、schemas、apis、tests 等）自动产出，极大减少重复劳动。

1) 设计模型（`src/apps/blog/models.py`）

```python
from django.db import models


class Author(models.Model):
    """
    作者模型

    字段：
        name: 作者名称
    """
    name = models.CharField("作者名称", max_length=20)

    def __str__(self) -> str:
        """返回该模型的友好字符串表示。"""
        return self.name

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    文章模型

    字段：
        name: 文章名称
        content: 正文内容
        author: 作者外键
    """
    name = models.CharField("文章名称", max_length=50)
    content = models.TextField("文章内容")
    author = models.ForeignKey("Author", verbose_name="文章作者", on_delete=models.CASCADE)

    def __str__(self) -> str:
        """返回该模型的友好字符串表示。"""
        return self.name

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
```

> 规范要点：为字段加上中文 `verbose_name`、实现 `__str__`、定义 `Meta` 的友好名称。

2) 迁移并创建表

```powershell
cd d:\Code\DjangoStarter\src
python manage.py makemigrations blog
python manage.py migrate
```

3) 运行代码生成器

```powershell
python manage.py autocode blog 博客
```

生成器将：
- 在 `apps/blog/apis/` 下为每个模型生成 `schemas.py` 与 `apis.py`，并聚合到 `apps/blog/apis/__init__.py`
- 生成 `admin.py` 与 `apps.py` 等
- 在 `apps/blog/tests/` 下为每个模型生成基础测试用例

4) 注册路由并测试

在 `src/config/apis.py` 添加：

```python
from apps.blog.apis import router as blog_router
api.add_router('blog', blog_router)
```

重启开发服务器后，访问：
- 列表/创建/更新/删除等接口：在 `http://localhost:8000/api/docs` 中通过 `blog` 标签查看并测试

---

## 第 6 部分：常用配置入口（URL 前缀 / 缓存 / 后台 / 安全）

- URL 前缀（统一为所有路由、静态与媒体添加前缀）
  - 文件：`src/config/settings/components/common.py`
  - 环境变量：`.env` 中设置 `URL_PREFIX=djangostarter`（不要包含斜杠）
  - 路由入口：`src/config/urls_root.py`（透传前缀到 `config.urls`）

- 注册应用：`src/config/settings/components/install_apps.py`（将 `apps.<your_app>` 加到 `INSTALLED_APPS`）

- 项目 URL：`src/config/urls.py`（网页路由、管理后台、验证码、国际化、Ninja API 入口）

- NinjaAPI：`src/config/apis.py`（初始化、渲染器、路由注册）

- 模板目录：`src/templates/`（全局模板，配合 `APP_DIRS=True` 可用应用内模板）

- 缓存：`src/config/settings/components/caches.py`（集中管理，默认 Redis；需先安装并运行 Redis）
 - macOS Redis 安装（可选）：`brew install redis`；启动：`brew services start redis`

- 管理后台：`src/config/settings/components/django_starter.py` 与 `simpleui.py`（外观与入口）

- 认证与密码策略：`src/config/settings/components/authentication.py`（默认 Argon2 等安全哈希）

---

## 第 7 部分：前端集成（HTMX / Alpine / Tailwind）

全局基础模板位于 `src/templates/_base.html`。你可以在应用模板中继承它：

```html
{% extends '_base.html' %}
{% load static %}

{% block title %}页面标题{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8" x-data="pageData()">
  <h1 class="text-3xl font-bold text-gray-900 mb-6">{{ page_title }}</h1>
  <div class="bg-white rounded-lg shadow-md p-6">
    <!-- 页面内容 -->
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
  function pageData() {
    return {
      // Alpine.js 数据和方法
    }
  }
</script>
{% endblock %}
```

> 如需更新或使用 TailwindCSS，请运行：`npm run tailwind:watch`。

---

## 第 8 部分：调试与排错

- 静态文件 404：确认已运行 `gulp move`，并检查 `STATIC_URL/STATIC_ROOT`；调试模式下 `urls_root.py` 会提供静态服务。
- 数据库连接或迁移失败：清理并重新迁移（`manage.py makemigrations` / `migrate`），检查模型是否正确。
- Redis 连接失败：确认 Redis 服务已启动且地址与端口正确（见 `caches.py`）。
- 管理后台样式丢失：如设置了 `URL_PREFIX`，重启服务并清除浏览器缓存。

---

## 第 9 部分：常用命令速查（PowerShell）

```powershell
# 后端依赖
pdm install

# 前端依赖与构建
pnpm install
gulp move
npm run tailwind:build

# 数据库
python manage.py makemigrations
python manage.py migrate

# 运行开发服务器
python manage.py runserver

# 测试（示例）
python manage.py test
pytest
```

### macOS（zsh/bash）

```bash
# 后端依赖
pdm install

# 前端依赖与构建
pnpm install
gulp move
npm run tailwind:build

# 数据库
python3 manage.py makemigrations
python3 manage.py migrate

# 运行开发服务器
python3 manage.py runserver

# 测试（示例）
python3 manage.py test
pytest
```

---

## 第 10 部分：下一步与建议

- 使用自动代码生成器为更多模型生成 CRUD 与测试，提升开发速度
- 阅读并按需启用中间件（IP 限制、错误处理等）：`src/django_starter/middleware/`
- 优化日志与观测：按需调整 `logging.py`、启用 `django_starter.contrib.monitoring`
- 部署：使用 Docker（`docker compose up --build`），并结合 Nginx/HTTPS

如果你在任何一步遇到问题，建议优先查看 `README.md` 的相关章节与本教程对应的文件位置；也可以在 `http://localhost:8000/api/docs` 中直接测试接口并观察响应结构。

祝你在 DjangoStarter v3 上开发愉快！