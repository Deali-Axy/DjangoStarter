# DjangoStarter v3 项目开发规范

## 项目背景

DjangoStarter v3 是下一代 Django 项目快速开发模板，专为提升开发效率和性能而设计。

结合了 Django 的丰富功能和 Django-Ninja 的性能、灵活、简洁特性，v3 版本旨在为开发者提供一个更加强大、简洁和高速的开发体验。

通过这个全新的框架版本，开发者能够迅速搭建起符合现代 web 应用标准的项目基础架构。

## 技术栈

### 后端技术

- **Python版本**: 3.12
- **包管理器**: UV
- **Web框架**: Django 6.0+ (with argon2)
- **API框架**: Django-Ninja 1.5+
- **数据库**: 支持多种数据库（PostgreSQL推荐）
- **缓存**: Redis 7.0+
- **异步支持**: ASGI服务器

### 前端技术

- **模板引擎**: Django Templates + Jinja2
- **交互框架**: HTMX
- **JavaScript框架**: Alpine.js
- **CSS框架**: TailwindCSS
- **组件库**: Flowbite
- **图标**: Font Awesome Free 6
- **动画**: AOS (Animate On Scroll)

### 开发工具

- **构建工具**: Gulp
- **容器化**: Docker + Docker Compose
- **测试框架**: Pytest

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
├── templates/             # 模板文件
└── locale/                # 国际化文件
```

## 开发规范

### 代码风格

#### Python代码规范

- 遵循 PEP 8 代码风格
- 使用类型注解（Type Hints）
- 函数和类必须添加 docstring 注释
- 变量和函数命名使用snake_case
- 类名使用PascalCase
- 常量使用UPPER_CASE


### Django应用开发规范

#### 模型定义规范

- 使用明确的字段名称
- 添加适当的Meta类配置
- 实现__str__方法
- 使用django-simple-history进行历史记录

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

- 使用Pydantic模型进行数据验证
- 实现适当的错误处理
- 添加API文档注释
- 使用JWT进行身份验证

```python
from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from typing import List

api = NinjaAPI(title="DjangoStarter API", version="3.0.0")

class UserSchema(Schema):
    """用户信息模式"""
    id: int
    username: str
    email: str
    nickname: str = None

class AuthBearer(HttpBearer):
    """JWT认证"""
    def authenticate(self, request, token):
        # JWT验证逻辑
        pass

@api.get("/users", response=List[UserSchema], auth=AuthBearer())
def list_users(request):
    """
    获取用户列表
    
    Returns:
        用户信息列表
    """
    # 实现逻辑
    pass
```

### 前端开发规范

#### HTML模板

- 使用语义化HTML标签
- 遵循无障碍访问标准
- 使用TailwindCSS类进行样式设计
- 集成Alpine.js进行交互

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

- 优先使用TailwindCSS工具类
- 自定义样式放在独立的CSS文件中
- 使用响应式设计原则
- 遵循移动优先的设计理念

### 测试规范

#### 测试覆盖要求

- 模型测试：测试所有自定义方法和属性
- 视图测试：测试所有HTTP方法和权限
- 表单测试：测试验证逻辑和错误处理
- API测试：测试所有端点和数据格式

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.account.models import UserProfile

class UserProfileModelTest(TestCase):
    """
    用户档案模型测试
    """
    
    def setUp(self):
        """测试数据准备"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_user_profile_creation(self):
        """测试用户档案创建"""
        profile = UserProfile.objects.create(
            user=self.user,
            nickname='测试用户'
        )
        self.assertEqual(str(profile), 'testuser - 测试用户')
        self.assertTrue(profile.created_at)
```

### 安全规范

#### 数据安全

- 使用Django的内置安全功能
- 实施CSRF保护
- 使用参数化查询防止SQL注入
- 对用户输入进行验证和清理
- 使用HTTPS进行数据传输

#### 身份验证和授权

- 使用强密码策略
- 实施登录尝试限制
- 使用JWT进行API认证
- 实现基于角色的访问控制

### 性能优化

#### 数据库优化

- 使用select_related和prefetch_related优化查询
- 添加适当的数据库索引
- 使用Redis进行缓存
- 实施数据库连接池

#### 前端优化

- 使用TailwindCSS的purge功能减少CSS体积
- 实施静态文件压缩和合并
- 使用CDN加速静态资源
- 实现懒加载和代码分割

### 部署规范

#### Docker部署

- 使用多阶段构建优化镜像大小
- 配置健康检查
- 使用环境变量管理配置
- 实施日志收集和监控

#### 环境配置

- 开发环境：使用SQLite和Django开发服务器
- 测试环境：使用PostgreSQL和完整的测试套件
- 生产环境：使用PostgreSQL、Redis、Nginx和Gunicorn

### 文档规范

#### 代码文档

- 所有函数和类必须有文档字符串
- 使用Google风格的文档字符串格式
- 在复杂逻辑处添加行内注释
- 维护API文档的实时更新

#### 项目文档

- 维护详细的README文件
- 记录部署和配置步骤
- 提供开发环境搭建指南
- 维护变更日志和版本说明

## 开发工作流

### Git工作流

- 使用feature分支进行功能开发
- 提交信息使用约定式提交格式
- 代码审查后才能合并到主分支
- 使用语义化版本进行发布

### 开发环境搭建

1. 安装Python 3.12和PDM
2. 克隆项目并安装依赖：`pdm install`
3. 安装Node.js依赖：`pnpm install`
4. 配置环境变量
5. 运行数据库迁移：`python manage.py migrate`
6. 启动开发服务器：`python manage.py runserver`

### 常用命令

```bash
# 安装依赖
pdm install
pnpm install

# 数据库操作
python manage.py makemigrations
python manage.py migrate

# 静态文件处理
npm run tailwind:build
npm run build:assets

# 测试
python manage.py test
pytest

# 代码质量检查
flake8 src/
mypy src/

# Docker部署
docker-compose up -d
```

## 故障排除

### 常见问题

1. **静态文件404**：检查STATIC_URL和STATIC_ROOT配置
2. **数据库连接错误**：验证数据库配置和连接参数
3. **Redis连接失败**：确认Redis服务状态和配置
4. **前端资源加载失败**：检查TailwindCSS和Gulp构建过程

### 调试工具

- Django Debug Toolbar（开发环境）
- Django日志系统
- Redis监控工具
- 浏览器开发者工具
