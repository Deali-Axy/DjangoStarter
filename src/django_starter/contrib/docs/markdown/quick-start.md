# 快速开始

本指南整理自项目 README 与开发规范，帮助你快速启动 DjangoStarter。

## 1. Python 环境

推荐使用 uv 来管理 Python 环境。

```bash
uv venv --python 3.14
```

激活虚拟环境：

- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

## 2. 安装依赖

```bash
uv sync
```

## 3. 前端依赖

```bash
pnpm install
gulp move
```

如果你需要 Tailwind 的实时编译：

```bash
pnpm run tw:watch
```

## 4. 数据库迁移

```bash
uv run ./src/manage.py migrate
```

## 5. 本地启动

```bash
uv run ./src/manage.py runserver
```
