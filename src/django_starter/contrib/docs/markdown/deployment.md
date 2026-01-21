# 部署指南

本指南整理了 DjangoStarter 在生产环境的部署要点，适用于 Docker 与传统服务器部署。

## 1. 环境准备

- Python 3.14
- Node.js 22+
- 生产环境建议使用 Redis

## 2. 依赖安装

```bash
uv sync
pnpm install
gulp move
pnpm run tw:build
```

## 3. 迁移与静态资源

```bash
uv run ./src/manage.py migrate
uv run ./src/manage.py collectstatic --noinput
```

## 4. 进程启动

WSGI 示例（Gunicorn）：

```bash
gunicorn config.wsgi:application -b 0.0.0.0:8000
```

ASGI 示例（Uvicorn）：

```bash
uvicorn config.asgi:application --host 0.0.0.0 --port 8000
```

## 5. Docker 部署建议

- 使用项目内的 Dockerfile 进行构建
- 配合 docker-compose 或 Caddy/Nginx 提供反向代理
- 将静态文件挂载为只读卷
