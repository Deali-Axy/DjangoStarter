# Django Cache Configuration System

这是一个为 Django 项目设计的集中化缓存配置系统，提供了灵活、可维护且类型安全的缓存管理方案。

## 特性

- 🎯 **集中化配置**: 所有缓存配置都在一个地方管理
- 🔧 **灵活配置**: 支持 Redis 和本地内存缓存的无缝切换
- 📝 **类型安全**: 使用 NamedTuple 和类型注解确保配置正确性
- 🌍 **环境感知**: 自动根据环境变量调整配置
- 📚 **易于扩展**: 简单添加新的缓存后端
- 🧪 **测试友好**: 支持测试环境的特殊配置

## 快速开始

### 1. 基本使用

在你的 Django 设置文件中：

```python
from django_starter.cache import CacheBackendSpec, get_django_cache_settings
from config.settings.components.common import DOCKER, DEBUG

# 定义缓存后端规范
CACHE_BACKEND_SPECS = [
    CacheBackendSpec(
        alias='default',
        db_index=0,
        key_prefix='myapp',
        description='默认缓存'
    ),
    CacheBackendSpec(
        alias='select2',
        db_index=2,
        key_prefix='select2',
        description='Select2 组件缓存'
    ),
]

# 生成缓存配置
CACHES = get_django_cache_settings(
    docker_mode=DOCKER,
    debug_mode=DEBUG,
    custom_specs=CACHE_BACKEND_SPECS
)
```

### 2. 高级使用

```python
from django_starter.cache import CacheConfigManager

# 创建缓存管理器
cache_manager = CacheConfigManager(
    docker_mode=False,
    debug_mode=True
)

# 获取缓存设置
cache_settings = cache_manager.get_cache_settings(custom_specs=CACHE_BACKEND_SPECS)

# 打印缓存信息（用于调试）
cache_manager.print_cache_info(custom_specs=CACHE_BACKEND_SPECS)
```

## 配置说明

### CacheBackendSpec 参数

- `alias`: 缓存别名（如 'default', 'select2'）
- `db_index`: Redis 数据库索引
- `key_prefix`: 缓存键前缀
- `description`: 可选的描述信息

### 环境变量支持

系统支持以下环境变量：

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `REDIS_HOST` | localhost (非Docker) / redis (Docker) | Redis 主机地址 |
| `REDIS_PORT` | 6379 | Redis 端口 |
| `REDIS_PASSWORD` | (空) | Redis 密码 |
| `REDIS_MAX_CONNECTIONS` | 512 | Redis 最大连接数 |
| `CACHE_TIMEOUT` | 30 | 缓存超时时间（秒） |
| `USE_REDIS_IN_DEBUG` | false | 调试模式下是否使用 Redis |
| `REDIS_DB_DEFAULT` | 0 | 默认缓存的 Redis 数据库索引 |
| `REDIS_DB_SELECT2` | 2 | Select2 缓存的 Redis 数据库索引 |

## 使用场景

### 1. 开发环境

```python
# 开发环境通常使用本地内存缓存
CACHES = get_django_cache_settings(
    docker_mode=False,
    debug_mode=True,  # 自动使用本地内存缓存
    custom_specs=CACHE_BACKEND_SPECS
)
```

### 2. 生产环境

```python
# 生产环境使用 Redis
CACHES = get_django_cache_settings(
    docker_mode=True,
    debug_mode=False,  # 自动使用 Redis
    custom_specs=CACHE_BACKEND_SPECS
)
```

### 3. 测试环境

```python
# 测试环境强制使用本地内存缓存
cache_manager = CacheConfigManager(docker_mode=False, debug_mode=True)
CACHES = cache_manager.build_cache_backends(
    specs=CACHE_BACKEND_SPECS,
    use_redis=False  # 强制使用本地缓存
)
```

## 添加新的缓存后端

只需在 `CACHE_BACKEND_SPECS` 列表中添加新的规范：

```python
CACHE_BACKEND_SPECS = [
    # 现有配置...
    CacheBackendSpec(
        alias='sessions',
        db_index=1,
        key_prefix='sessions',
        description='用户会话缓存'
    ),
    CacheBackendSpec(
        alias='api_cache',
        db_index=3,
        key_prefix='api',
        description='API 响应缓存'
    ),
]
```

## 迁移指南

### 从旧的配置系统迁移

1. **安装新模块**: 确保 `django_starter.cache` 模块可用

2. **更新导入**:
   ```python
   # 旧的方式
   from config.settings.components.caches import get_cache_settings
   
   # 新的方式
   from django_starter.cache import get_django_cache_settings
   ```

3. **更新配置定义**:
   ```python
   # 旧的方式 - 分散在函数中
   def get_cache_backend_specs():
       return [...]
   
   # 新的方式 - 集中在顶部
   CACHE_BACKEND_SPECS = [...]
   ```

4. **更新生成逻辑**:
   ```python
   # 旧的方式
   CACHES = get_cache_settings()
   
   # 新的方式
   CACHES = get_django_cache_settings(
       docker_mode=DOCKER,
       debug_mode=DEBUG,
       custom_specs=CACHE_BACKEND_SPECS
   )
   ```

## 最佳实践

1. **配置集中化**: 将所有缓存规范定义在文件顶部的 `CACHE_BACKEND_SPECS` 中

2. **环境变量**: 使用环境变量覆盖默认的数据库索引和其他设置

3. **描述信息**: 为每个缓存后端添加清晰的描述信息

4. **测试配置**: 在测试中使用本地内存缓存以提高性能

5. **监控**: 在生产环境中监控 Redis 连接和性能

## 故障排除

### 常见问题

1. **Redis 连接失败**
   - 检查 `REDIS_HOST` 和 `REDIS_PORT` 环境变量
   - 确认 Redis 服务正在运行
   - 检查网络连接和防火墙设置

2. **缓存键冲突**
   - 确保不同的缓存后端使用不同的 `key_prefix`
   - 使用不同的 `db_index` 来隔离数据

3. **性能问题**
   - 调整 `REDIS_MAX_CONNECTIONS` 设置
   - 监控 Redis 内存使用情况
   - 考虑使用缓存分片

### 调试工具

```python
# 打印缓存配置信息
cache_manager = CacheConfigManager(docker_mode=DOCKER, debug_mode=DEBUG)
cache_manager.print_cache_info(custom_specs=CACHE_BACKEND_SPECS)

# 获取所有缓存别名
aliases = cache_manager.get_cache_aliases(custom_specs=CACHE_BACKEND_SPECS)
print(f"可用的缓存别名: {aliases}")
```

## 更多示例

查看 `cache_usage_examples.py` 文件获取更多详细的使用示例和高级配置模式。