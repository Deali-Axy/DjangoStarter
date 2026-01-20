# DjangoStarter项目开发规范

## 项目背景

DjangoStarter 是下一代 Django 项目快速开发模板，专为提升开发效率和性能而设计。通过这个全新的框架版本，开发者能够迅速搭建起符合现代 web 应用标准的项目基础架构。

## 技术栈

### 后端

- Python版本: 3.12
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
- CSS框架: TailwindCSS
- 组件库: Flowbite
- 图标: Font Awesome Free 6
- 动画: AOS (Animate On Scroll)

### 开发工具

- 容器化: Docker + Docker Compose
- 测试框架: Pytest

## 项目架构

### 目录结构

```
src/
├── apps/                   # 业务应用模块
│   ├── account/            # 用户账户管理
│   └── demo/               # 演示应用
├── config/                 # 项目配置
│   ├── settings/           # 分层设置
│   │   ├── components/     # 配置组件
│   │   └── environments/   # 环境配置
│   ├── urls.py            # 主URL配置
│   └── wsgi.py/asgi.py    # WSGI/ASGI入口
├── django_starter/         # 核心框架模块
│   ├── contrib/           # 各种核心功能模块
│   ├── db/                # 数据库相关
│   ├── http/              # HTTP响应处理
│   ├── middleware/        # 中间件
│   └── utilities.py       # 工具函数
├── static/                # 静态文件
├── templates/             # Django页面模板
└── locale/                # 国际化文件
```

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

#### HTML模板

- 使用语义化HTML标签
- 遵循无障碍访问标准
- 使用 TailwindCSS 类进行样式设计
- 集成 HTMX / Alpine.js 进行交互，根据具体情况选择合适的交互方式

```html
<!-- 示例模板结构 -->
{% extends '_base.html' %}
{% load static %}

{% block title %}页面标题{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8" x-data="pageData()">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">{{ page_title }}</h1>
    
    <!-- 内容区域 -->
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

#### CSS/TailwindCSS规范

- 优先使用 flowbite 组件库已有组件，保持界面设计风格统一
- 使用 TailwindCSS 工具类
- 避免直接使用 CSS
- 使用响应式设计原则
- 遵循移动优先的设计理念

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

