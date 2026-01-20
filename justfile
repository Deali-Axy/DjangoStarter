# 使用 PowerShell 替代 sh:
set shell := ["powershell.exe", "-c"]

# 默认列出所有可用命令
default:
    @just --list

# --- 数据库操作 ---

# 生成迁移文件 (uv run manage.py makemigrations)
mm:
    uv run src/manage.py makemigrations

# 执行迁移 (uv run manage.py migrate)
migrate:
    uv run src/manage.py migrate

# 快速二合一：生成并执行迁移
db-sync:
    just mm
    just migrate

# --- 开发与运行 ---

# 使用 Granian 启动 ASGI (开发模式)
serve:
    uv run granian --interface asgi config.asgi:application \
        --static-path-route /static \
        --static-path-mount ./static-dist \
        --reload

# 传统的 Django 开发服务器
dev:
    uv run src/manage.py runserver

# 进入 Django Shell
shell:
    uv run src/manage.py shell

# --- 清理与维护 ---

# 清理 Python 缓存文件
clean:
    Get-ChildItem -Path . -Include "__pycache__" -Recurse -Directory -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Include "*.pyc" -Recurse -File -Force -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
