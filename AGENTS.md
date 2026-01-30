# DjangoStarter项目开发规范

## 项目背景

DjangoStarter 是下一代 Django 项目快速开发模板，专为提升开发效率和性能而设计。通过这个全新的框架版本，开发者能够迅速搭建起符合现代 web 应用标准的项目基础架构。

## 技术栈

### 后端

- Python版本: 3.14
- 包管理器: uv
- Web框架: Django 6.0+ (with argon2)
- API框架: Django-Ninja 1.5+
- 缓存: 
  - 本地开发时使用内存缓存  `django.core.cache.backends.locmem.LocMemCache`
  - 部署生产环境时使用 Redis `django_redis.cache.RedisCache`


### 前端(基于Django后端渲染)

- 包管理: pnpm
- 构建工具: Gulp
- 模板引擎: Django Templates
- 交互框架: HTMX
- JavaScript框架: Alpine.js
- CSS框架: TailwindCSS v4
- 组件库: DaisyUI v5 (Pure CSS)
- 图标: Font Awesome Free 6
- 动画: AOS (Animate On Scroll)

### 开发工具

- 容器化: Docker + Docker Compose
- 测试框架: Pytest

## Essential Commands

### Setup

```bash
# Install Python dependencies
uv sync

# Run database migrations
uv run ./src/manage.py migrate

# Install frontend dependencies
pnpm install

# Copy frontend assets
pnpm gulp:move
```

### Development

```bash
# Django dev server (WSGI)
uv run ./src/manage.py runserver

# Watch TailwindCSS changes
pnpm run tw:watch
```

### Code Generation

```bash
# Generate CRUD + tests + admin for an app
uv run ./src/manage.py autocode app_name "Display Name"

# Generate specific models only
uv run ./src/manage.py autocode blog "Blog" --models post category

# skip some modules
uv run ./src/manage.py autocode blog "Blog" --no-admin --no-apps --no-tests --no-apis

# Generate seed data for an app
uv run ./src/manage.py  seed app_label 10
```

### Database

```bash
# Create migrations
uv run ./src/manage.py makemigrations

# Apply migrations
uv run ./src/manage.py migrate
```

### Testing

```bash
# Django tests
uv run ./src/manage.py test
```

## Architecture

### Directory Structure

```
src/
├── apps/                  # Business applications
│   ├── account/           # Authentication system
│   └── demo/              # Demo app (reference implementation)
├── config/                # Django configuration
│   ├── settings/          # Split settings (django-split-settings)
│   │   ├── components/    # Config components (cache, auth, security, etc.)
│   │   └── environments/  # Environment-specific configs
│   ├── urls.py            # Main URL config
│   ├── apis.py            # NinjaAPI initialization - register routers here
│   └── wsgi.py/asgi.py    # Entry points
├── django_starter/        # Core framework code
│   ├── contrib/           # Built-in components (code_generator, admin, monitoring)
│   ├── db/models.py       # ModelExt base class
│   ├── http/              # Response handling
│   └── middleware/        # Security middleware
├── static/                # Static files
├── templates/             # common Django templates, don't edit!
└── locale/                # i18n
```

### Core Framework Components

**ModelExt Base Class** (`src/django_starter/db/models.py`):
All models inherit from `ModelExt`, which provides:

- Soft delete via `is_deleted` field
- Automatic timestamps (`created_time`, `updated_time`)
- Custom manager that filters out deleted objects

**Django-Ninja API Organization**:

- APIs organized per app in `apps/[app]/apis/`
- Automatic CRUD generation via `autocode` command
- Type-safe Pydantic schemas
- Auto-generated OpenAPI docs at `/api/docs`

**Split Settings** (`src/config/settings/`):

- Base settings in `components/`
- Environment-specific overrides in `environments/`
- Docker-aware configuration detection

### Application Development Pattern

When creating a new app:

1. Create app: `cd apps && uv run django-admin startapp app_name`
2. Add to `INSTALLED_APPS` in `src/config/settings/components/install_apps.py`
3. Define models in `apps/app_name/models.py` (inherit from `django_starter.db.models.ModelExt`)
4. Run `python manage.py autocode app_name "Display Name"` to generate CRUD apis, tests, admin
5. Register router in `src/config/apis.py`: `api.add_router('app_name', router)`
6. Run migrations

## 开发规范

### 代码风格

#### Python代码规范

- 遵循 PEP 8 代码风格
- 使用类型注解（Type Hints）
- 函数和类必须添加 docstring 注释 (reStructuredText风格)
- 变量和函数命名使用snake_case
- 类名使用PascalCase
- 常量使用UPPER_CASE


### Django应用开发规范

#### 模型定义规范

- 使用明确的字段名称
- 每个字段需要提供友好的 `verbose_name`
- 添加适当的 `Meta` 类配置
- 实现 `__str__` 方法
- 使用 `django-simple-history` 进行历史记录

```python
from django.db import models
from simple_history.models import HistoricalRecords

class UserProfile(models.Model):
    """
    用户档案模型
    """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='用户')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 历史记录
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = '用户档案'
        verbose_name_plural = '用户档案'
        db_table = 'user_profile'
        
    def __str__(self) -> str:
        return f"{self.user.username} - {self.nickname}"
```

### API开发规范

#### Django-Ninja API

- 代码路径：
  - 简单逻辑:  apis path `app/apis.py`, schema path `app/schemas.py`
  - 复杂逻辑: 先将接口进行分组，代码放在 `app/apis/[group]`  package，分 apis.py, schemas.py 文件存储

- 使用Pydantic模型进行数据验证
- 实现适当的错误处理
- 添加 API 文档说明 (summary, description 参数)
- 使用`JwtBearer` 进行身份验证

```python
from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from typing import List
from django_starter.contrib.auth.bearers import JwtBearer

api = NinjaAPI(title="DjangoStarter API", version="3.0.0")

class UserSchema(Schema):
    """用户信息"""
    id: int
    username: str
    email: str
    nickname: str = None

@api.get("/users", response=List[UserSchema], auth=JwtBearer(), summary="获取用户列表", description ="获取用户列表，需要登录才能访问")
def list_users(request):
    """
    获取用户列表
    """
    # 实现逻辑
    pass
```

### 前端开发规范

### Django View

- **页面元数据**: 每个返回独立页面的视图函数（View）必须在 context 中定义 `title` 和 `breadcrumbs`，以保证统一的页面标题显示和导航体验。

  示例代码：

  ```python
  context = {
      'title': '项目中台',
      'breadcrumbs': [
          {'text': '主页', 'url': reverse('index'), 'icon': 'fa-solid fa-house'},
          {'text': '项目中台', 'url': None, 'icon': 'fa-solid fa-briefcase'},
      ],
  }
  ```

  

#### Django Template

- 使用语义化HTML标签
- 遵循无障碍访问标准
- 使用 TailwindCSS 类进行样式设计
- 在各个 app 下创建 templates 目录编写前端页面代码，不要直接修改 src\templates 里的代码
- DjangoStarter 提供 page_header 组件用于渲染标准页面标题和面包屑导航，位于 `django_starter/contrib/navbar/templatetags/page_tags.py` 内，使用时在模板代码顶部引入: `{% load page_tags %}`
- 根据具体情况选择合适的交互方式，DjangoStarter 默认已集成 HTMX / Alpine.js 相关依赖和配置
- **页面布局**: 默认使用 DaisyUI Drawer 布局，主内容区在 `block content` 中。

示例页面代码：

```html
<!-- 示例模板结构 -->
{% extends '_base.html' %}
{% load static %}
{% load page_tags %}

{% block title %}页面标题{% endblock %}

<!-- 额外的CSS或者其他head内容 -->
{% block head %}{% endblock %}

{% block content %}
{% page_header title breadcrumbs %}
<!-- 页面主体内容，外部已有 container 容器，这里直接写页面内容元素 -->
<div class="card bg-base-100 shadow-xl">
    <div class="card-body">
        <h2 class="card-title">Card Title</h2>
        <p>Content goes here...</p>
        <div class="card-actions justify-end">
            <button class="btn btn-primary">Action</button>
        </div>
    </div>
</div>
{% endblock %}

<!-- Alpine.js 交互脚本 -->
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

#### CSS/TailwindCSS规范

- **优先使用 DaisyUI 组件类** (如 `btn btn-primary`, `card`, `input input-bordered`)，减少冗长的 Utility Classes。
- 使用daisyui MCP查询组件列表和组件的类名。
- 使用 TailwindCSS 工具类处理布局和微调。
- 避免直接使用 CSS，利用 DaisyUI 的 Design Tokens (如 `bg-base-100`, `text-primary`) 确保 Light/Dark 主题适配。
- 使用响应式设计原则。
- 遵循移动优先的设计理念。

### 测试规范

#### 测试覆盖要求

- 模型测试：测试所有自定义方法和属性
- 视图测试：测试所有HTTP方法和权限
- 表单测试：测试验证逻辑和错误处理
- API测试：测试所有端点和数据格式

### 安全规范

#### 数据安全

- 使用Django的内置安全功能
- 实施CSRF保护
- 使用参数化查询防止SQL注入
- 对用户输入进行验证和清理

### 性能优化

#### 数据库优化

- 使用select_related和prefetch_related优化查询
- 添加适当的数据库索引
- 适当使用缓存优化热点数据访问性能

