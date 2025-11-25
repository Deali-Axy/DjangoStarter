ARG PYTHON_BASE=3.12
ARG NODE_BASE=22

# python 构建
FROM python:$PYTHON_BASE AS python_builder

# 设置 python 环境变量
ENV PYTHONUNBUFFERED=1
# 禁用更新检查
ENV PDM_CHECK_UPDATE=false

# 设置国内源
RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/ && \
    # 安装 pdm
    pip install -U pdm && \
    # 配置镜像
    pdm config pypi.url "https://mirrors.cloud.tencent.com/pypi/simple/"

# 复制文件
COPY pyproject.toml pdm.lock /project/

# 安装依赖项和项目到本地包目录
WORKDIR /project
RUN pdm install --check --prod --no-editable

# node 构建
FROM node:$NODE_BASE AS node_builder

# 配置镜像 && 安装 pnpm
RUN npm config set registry https://registry.npmmirror.com && \
    npm install -g pnpm

# 复制依赖文件
COPY package.json pnpm-lock.yaml /project/

# 安装依赖
WORKDIR /project
RUN pnpm i


 


# gulp 构建
FROM node:$NODE_BASE AS gulp_builder

# 配置镜像 && 安装 pnpm
RUN npm --registry https://registry.npmmirror.com install -g gulp-cli

# 复制依赖文件
COPY gulpfile.js /project/

# 从构建阶段获取包
COPY --from=node_builder /project/node_modules/ /project/node_modules

# 复制依赖文件
WORKDIR /project
RUN gulp move


# tailwindcss 构建（置于 gulp 之后，使用已复制的前端依赖）
FROM node:$NODE_BASE AS tailwind_builder

# 复制依赖文件
COPY tailwind.config.js /project/
COPY src/static/css/tailwind.src.css /project/src/static/css/

# 复制用于扫描的模板与脚本（满足 tailwind.config.js 的 content 路径）
COPY src/templates/ /project/src/templates/
COPY src/apps/ /project/src/apps/
COPY src/django_starter/ /project/src/django_starter/

# 从构建阶段获取包
COPY --from=node_builder /project/node_modules/ /project/node_modules

# 引入 gulp 阶段生成的静态资源（包含 flowbite 等依赖）
COPY --from=gulp_builder /project/src/static/ /project/src/static/

# 构建 tailwindcss
WORKDIR /project
RUN npx tailwindcss -c ./tailwind.config.js -i ./src/static/css/tailwind.src.css -o ./src/static/css/tailwind.prod.css --minify

# django 构建
FROM python:$PYTHON_BASE AS django_builder

COPY . /project/

# 从构建阶段获取包
COPY --from=python_builder /project/.venv/ /project/.venv
COPY --from=gulp_builder /project/src/static/ /project/src/static/
COPY --from=tailwind_builder /project/src/static/css/tailwind.prod.css /project/src/static/css/tailwind.prod.css

WORKDIR /project
ENV PATH="/project/.venv/bin:$PATH"
# 处理静态资源资源
RUN python ./src/manage.py collectstatic --noinput


# 运行阶段
FROM python:$PYTHON_BASE-slim AS final

# 添加元数据标签
LABEL maintainer="DealiAxy <dealiaxy@gmail.com>"
LABEL description="基于Django定制的快速Web开发模板"
LABEL version="1.0"

# 换 Debian apt 源为清华源（适用于 Debian 12, slim 基础镜像）
RUN sed -i 's|http://deb.debian.org/debian|https://mirrors.tuna.tsinghua.edu.cn/debian|g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's|http://security.debian.org/debian-security|https://mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list.d/debian.sources

# 安装运行时必要的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    uwsgi \
    uwsgi-plugin-python3 \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段获取包
COPY --from=python_builder /project/.venv/ /project/.venv
COPY --from=django_builder /project/static-dist/ /project/static-dist
ENV PATH="/project/.venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONPATH=/project/src
ENV PYTHONUNBUFFERED=1

# 复制应用代码
COPY src /project/src
WORKDIR /project

# 创建非root用户并设置适当的权限
RUN groupadd -r django && \
    useradd -r -g django -d /project -s /bin/bash django && \
    chown -R django:django /project

# 切换到非root用户
USER django

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import requests; r = requests.get('http://localhost:8000/health/'); exit(0 if r.status_code == 200 else 1)"

# 暴露端口
EXPOSE 8000

# 设置默认命令
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "-v", "3", "--proxy-headers", "config.asgi:application"]
