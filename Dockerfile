FROM python:3.8

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code
WORKDIR /code

# 更新 pip
RUN pip install -i https://mirrors.aliyun.com/pypi/simple pip -U
# 设置国内源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

# 将 requirements.txt 复制到容器的 code 目录
ADD requirements.txt /code/

# 安装库
RUN pip install -r requirements.txt

# 将当前目录复制到容器的 code 目录
ADD . /code

# 安装uwsgi
RUN pip install uwsgi