ARG PYTHON_BASE=3.11
ARG NODE_BASE=18

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
COPY pyproject.toml pdm.lock README.md /project/

# 安装依赖项和项目到本地包目录
WORKDIR /project
RUN pdm install --check --prod --no-editable

# node 构建
FROM node:$NODE_BASE as node_builder

# 配置镜像 && 安装 pnpm
RUN npm config set registry https://registry.npmmirror.com && \
    npm install -g pnpm

# 复制依赖文件
COPY package.json pnpm-lock.yaml /project/

# 安装依赖
WORKDIR /project
RUN pnpm i


# gulp 构建
FROM node:$NODE_BASE as gulp_builder

# 配置镜像 && 安装 pnpm
RUN npm --registry https://registry.npmmirror.com install -g gulp-cli

# 复制依赖文件
COPY gulpfile.js /project/

# 从构建阶段获取包
COPY --from=node_builder /project/node_modules/ /project/node_modules

# 复制依赖文件
WORKDIR /project
RUN gulp move


# django 构建
FROM python:$PYTHON_BASE as django_builder

COPY . /project/

# 从构建阶段获取包
COPY --from=python_builder /project/.venv/ /project/.venv
COPY --from=gulp_builder /project/static/ /project/static

WORKDIR /project
ENV PATH="/project/.venv/bin:$PATH"
# 处理静态资源资源
RUN python ./src/manage.py collectstatic


# 运行阶段
FROM python:$PYTHON_BASE as final

# 从构建阶段获取包
COPY --from=python_builder /project/.venv/ /project/.venv
COPY --from=django_builder /project/static-dist/ /project/static-dist
ENV PATH="/project/.venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONPATH=/project/src
ENV PYTHONUNBUFFERED=1
COPY src /project/src
WORKDIR /project