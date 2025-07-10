# 环境变量配置指南

本指南说明如何使用新的环境变量配置系统来管理 DjangoStarter 项目的所有配置。

## 概述

我们已经将所有硬编码的配置项提取到环境变量中，实现了：
- 统一的配置管理（通过 `.env` 文件）
- Nginx 配置的动态模板化（支持 URL_PREFIX）
- 所有服务的完全环境变量化
- 无需修改 `docker-compose.yml` 文件

## 快速开始

### 1. 复制环境变量模板

```bash
cp .env.example .env
```

### 2. 编辑 `.env` 文件

根据你的需求修改 `.env` 文件中的配置项。重要配置项说明：

#### 核心应用配置
```bash
# 应用基础配置
APP_NAME=django-starter
URL_PREFIX=/api/django-starter  # 设置 URL 前缀，留空则无前缀
ENVIRONMENT=docker
DEBUG=false
TZ=Asia/Shanghai

# 端口配置
APP_PORT=8001                   # 外部访问端口
APP_INTERNAL_PORT=8000          # 应用内部端口
NGINX_INTERNAL_PORT=8001        # Nginx 内部端口
```

#### 服务端口配置
```bash
# 监控服务端口
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
REDIS_PORT=6379
```

#### 资源限制配置
```bash
# CPU 和内存限制
APP_CPU_LIMIT=1.0
APP_MEMORY_LIMIT=512M
NGINX_CPU_LIMIT=0.3
NGINX_MEMORY_LIMIT=128M
```

### 3. 启动服务

```bash
docker-compose up -d
```

## URL_PREFIX 配置详解

### 什么是 URL_PREFIX？

`URL_PREFIX` 允许你为应用添加统一的 URL 前缀，例如：
- 无前缀：`http://localhost:8001/api/health/`
- 有前缀：`http://localhost:8001/api/django-starter/api/health/`

### 配置示例

#### 场景 1：无 URL 前缀
```bash
URL_PREFIX=
```
访问地址：`http://localhost:8001/api/health/`

#### 场景 2：有 URL 前缀
```bash
URL_PREFIX=/api/django-starter
```
访问地址：`http://localhost:8001/api/django-starter/api/health/`

#### 场景 3：多级前缀
```bash
URL_PREFIX=/v1/api/django-starter
```
访问地址：`http://localhost:8001/v1/api/django-starter/api/health/`

### 注意事项

1. **前缀格式**：URL_PREFIX 应该以 `/` 开头，不以 `/` 结尾
   - ✅ 正确：`/api/django-starter`
   - ❌ 错误：`api/django-starter/`

2. **空前缀**：如果不需要前缀，将 URL_PREFIX 设置为空字符串
   ```bash
   URL_PREFIX=
   ```

3. **健康检查**：系统会自动更新所有健康检查 URL 以包含正确的前缀

## 服务配置详解

### Redis 配置
```bash
REDIS_IMAGE=redis:7-alpine
REDIS_PORT=6379
REDIS_CPU_LIMIT=0.2
REDIS_MEMORY_LIMIT=128M
```

### Nginx 配置
```bash
NGINX_IMAGE=nginx:stable-alpine
NGINX_CPU_LIMIT=0.3
NGINX_MEMORY_LIMIT=128M
```

### 应用配置
```bash
APP_IMAGE_NAME=django-starter
APP_IMAGE_TAG=latest
PYTHON_VERSION=3.11
NODE_VERSION=18
APP_CPU_LIMIT=1.0
APP_MEMORY_LIMIT=512M
```

### 监控服务配置
```bash
# Prometheus
PROMETHEUS_IMAGE=prom/prometheus:latest
PROMETHEUS_PORT=9090
PROMETHEUS_RETENTION=200h
PROMETHEUS_CPU_LIMIT=0.5
PROMETHEUS_MEMORY_LIMIT=256M

# Grafana
GRAFANA_IMAGE=grafana/grafana:latest
GRAFANA_PORT=3000
GRAFANA_ADMIN_PASSWORD=admin
GRAFANA_ALLOW_SIGN_UP=false
GRAFANA_CPU_LIMIT=0.3
GRAFANA_MEMORY_LIMIT=128M
```

### 备份服务配置
```bash
BACKUP_IMAGE=alpine:latest
BACKUP_CPU_LIMIT=0.2
BACKUP_MEMORY_LIMIT=64M
```

### 健康检查配置
```bash
HEALTHCHECK_INTERVAL=30s
HEALTHCHECK_TIMEOUT=5s
HEALTHCHECK_RETRIES=3
HEALTHCHECK_START_PERIOD=10s
```

## 技术实现说明

### Nginx 模板化

我们使用 `nginx.conf.template` 文件和 `envsubst` 实现动态配置：

1. **模板文件**：`nginx.conf.template` 包含环境变量占位符
2. **自动替换**：Nginx 容器启动时自动将环境变量替换到配置中
3. **动态路由**：根据 `URL_PREFIX` 自动配置路由规则

#### 技术实现原理

Nginx 官方镜像内置了模板处理机制：
- **自动扫描**：容器启动时自动扫描 `/etc/nginx/templates/` 目录
- **模板处理**：使用 `envsubst` 工具处理 `.template` 文件中的环境变量
- **配置生成**：将处理后的配置文件输出到 `/etc/nginx/conf.d/` 目录
- **无需干预**：整个过程完全自动化，无需手动执行任何命令

这种机制使得我们可以通过简单的文件挂载和环境变量传递来实现动态配置，而不需要复杂的初始化脚本。

### 环境变量传递

所有环境变量通过以下方式传递：
1. `.env` 文件定义变量
2. `docker-compose.yml` 引用变量
3. 容器内使用变量

## 故障排除

### 常见问题

#### 1. 服务无法启动
- 检查 `.env` 文件是否存在
- 验证环境变量格式是否正确
- 查看 Docker 日志：`docker-compose logs [service_name]`

#### 2. URL_PREFIX 不生效
- 确认 `nginx.conf.template` 文件存在
- 检查 Nginx 容器日志
- 验证环境变量是否正确传递

#### 3. 端口冲突
- 修改 `.env` 文件中的端口配置
- 确保端口未被其他服务占用

### 调试命令

```bash
# 查看环境变量
docker-compose config

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs nginx
docker-compose logs app

# 进入容器调试
docker-compose exec nginx sh
docker-compose exec app bash
```

## 最佳实践

### 1. 环境分离
- 开发环境：使用 `.env.development`
- 生产环境：使用 `.env.production`
- 测试环境：使用 `.env.testing`

### 2. 安全配置
- 不要将 `.env` 文件提交到版本控制
- 生产环境使用强密码
- 定期更新镜像版本

### 3. 性能优化
- 根据实际负载调整资源限制
- 监控服务性能指标
- 定期清理日志文件

### 4. 备份策略
- 定期备份数据库和媒体文件
- 测试备份恢复流程
- 保留多个备份版本

## 升级指南

### 从旧版本升级

1. **备份现有配置**
   ```bash
   cp docker-compose.yml docker-compose.yml.backup
   cp nginx.conf nginx.conf.backup
   ```

2. **更新文件**
   - 使用新的 `docker-compose.yml`
   - 创建 `nginx.conf.template`
   - 更新 `.env.example`

3. **迁移配置**
   - 将旧的硬编码值迁移到 `.env` 文件
   - 测试新配置

4. **验证功能**
   - 检查所有服务是否正常启动
   - 验证 URL_PREFIX 是否生效
   - 测试健康检查

## 支持

如果遇到问题，请：
1. 查看本文档的故障排除部分
2. 检查项目的 GitHub Issues
3. 提交新的 Issue 并包含详细的错误信息

---

**注意**：本配置系统向后兼容，但建议使用新的环境变量方式进行配置管理。