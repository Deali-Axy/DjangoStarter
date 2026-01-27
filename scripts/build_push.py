#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker镜像构建、推送和远程部署脚本

功能：
1. 获取最新git tag作为版本号
2. 读取 .env 文件并将其变量作为 --build-arg 注入 Docker 构建
3. 构建Docker镜像并推送到配置的镜像仓库
4. SSH连接到远程服务器进行自动部署

配置项(环境变量或默认值)：
- PLATFORMS: 构建目标平台，默认: linux/amd64
- DOCKERFILE: Dockerfile路径，默认: ./Dockerfile
- IMAGE_NAME: 镜像名称
- REGISTRIES: 镜像仓库配置列表，每个元素包含:
  - TYPE: 仓库类型，dockerhub或private
  - NAMESPACE: 镜像仓库命名空间
  - IMAGE_NAME: 镜像名称
- REMOTE_HOST: 远程服务器配置，如: user@server-ip -p 2022
- REMOTE_PROJECT_PATH: 远程项目路径
- ENV_FILE: .env 文件路径，默认: ./.env
"""

import os
import sys
import subprocess
import threading
import time
from typing import Optional, Tuple

# 默认配置
DEFAULTS = {
    "PLATFORMS": "linux/amd64",
    "DOCKERFILE": "./Dockerfile",
    'IMAGE_NAME': 'django-starter',
    'REGISTRIES': [
        {
            'TYPE': 'dockerhub', # 可选项：dockerhub 或 private
            'URL': '',  # 仅在 TYPE 为 private 时需要
            'NAMESPACE': 'dealiaxy',
            'IMAGE_NAME': 'django-starter',
        },
    ],
    'REMOTE_HOST': '',  # 远程服务器地址或~/.ssh/config中的Host别名
    'REMOTE_PROJECT_PATH': '',
    "ENABLED_DEPLOY": False,
    'ENV_FILE': './.env',
}


class ProgressDisplay:
    """
    管理一个持久的状态行，同时允许其他输出滚动显示。
    类似于tqdm的效果，但使用纯标准库实现。
    """

    def __init__(self):
        self.status_line = ""
        self.lock = threading.Lock()

    def set_status(self, status: str):
        """设置或更新状态行文本"""
        with self.lock:
            sys.stdout.write('\r\033[K')  # 清空当前行
            self.status_line = status
            sys.stdout.write(self.status_line)
            sys.stdout.flush()

    def print_output(self, line: str):
        """在状态行下方打印一行输出"""
        with self.lock:
            # 使用\r和\033[K清空当前行（即状态行）
            sys.stdout.write('\r\033[K')
            # 打印实际的命令输出行 (line from readline() includes \n)
            sys.stdout.write(line)
            # 重新绘制状态行
            sys.stdout.write(self.status_line)
            sys.stdout.flush()

    def finish_step(self, final_status: str):
        """完成一个步骤，将最终状态打印为普通行"""
        with self.lock:
            # 清空状态行
            sys.stdout.write('\r\033[K')
            # 打印最终状态
            sys.stdout.write(final_status + '\n')
            sys.stdout.flush()
            self.status_line = ""


def get_config(key: str) -> str | object:
    """获取配置值，优先使用环境变量，否则使用默认值"""
    return os.environ.get(key, DEFAULTS.get(key, ''))


def load_env_file(env_path: str) -> dict[str, str]:
    """从 .env 文件加载键值对，忽略注释、空行与可选的 export 前缀"""
    if not env_path:
        return {}
    if not os.path.exists(env_path):
        print(f"ℹ️ 未找到 {env_path}，将不注入 build args。")
        return {}

    env_vars: dict[str, str] = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('export '):
                line = line[7:].strip()
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            # 去除包裹引号
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            env_vars[key] = value
    return env_vars


def build_args_from_env(env_vars: dict[str, str]) -> str:
    """将环境变量转换为 Docker build --build-arg 参数字符串"""
    if not env_vars:
        return ""
    parts = []
    for k, v in env_vars.items():
        safe_v = v.replace('"', '\\"')
        parts.append(f'--build-arg {k}="{safe_v}"')
    return ' '.join(parts)


def _reader_thread(pipe, lines_list, progress_display: Optional[ProgressDisplay]):
    """在独立线程中读取管道输出"""
    try:
        for line in iter(pipe.readline, ''):
            lines_list.append(line)
            if progress_display:
                progress_display.print_output(line)
    except UnicodeDecodeError as e:
        # 处理编码错误，使用错误替换策略继续读取
        error_msg = f"编码错误: {e}，尝试使用错误替换策略继续\n"
        lines_list.append(error_msg)
        if progress_display:
            progress_display.print_output(error_msg)
    finally:
        pipe.close()


def run_cmd(cmd: str, progress_display: Optional[ProgressDisplay] = None) -> Tuple[int, str, str]:
    """
    执行命令并实时显示输出，同时捕获输出内容。
    返回状态码、stdout和stderr。
    """
    return run_cmd_ex(cmd, progress_display, exit_on_error=True)


def run_cmd_ex(
    cmd: str,
    progress_display: Optional[ProgressDisplay] = None,
    *,
    exit_on_error: bool = True,
    extra_env: Optional[dict[str, str]] = None,
) -> Tuple[int, str, str]:
    """
    执行命令并实时显示输出，同时捕获输出内容。
    返回状态码、stdout和stderr。

    - exit_on_error=True 时，失败会 sys.exit(1)
    - extra_env 可用于临时注入环境变量（例如禁用 BuildKit）
    """
    print(f"执行命令: {cmd}")

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
        encoding='utf-8',
        errors='replace',  # 遇到无法解码的字符时用替换字符代替
        env=env,
    )

    stdout_lines = []
    stderr_lines = []

    stdout_thread = threading.Thread(
        target=_reader_thread,
        args=(process.stdout, stdout_lines, progress_display)
    )
    stderr_thread = threading.Thread(
        target=_reader_thread,
        args=(process.stderr, stderr_lines, progress_display)
    )

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    returncode = process.wait()

    stdout = ''.join(stdout_lines)
    stderr = ''.join(stderr_lines)

    if returncode != 0 and exit_on_error:
        if progress_display:
            progress_display.print_output(f"\n❌ 命令执行失败 (返回码: {returncode})\n")
        else:
            print(f"\n错误: 命令 '{cmd}' 执行失败 (返回码: {returncode})")
            print(stderr)
        sys.exit(1)

    return returncode, stdout, stderr


def get_latest_tag() -> str:
    """获取最新git tag"""
    _, tag, _ = run_cmd("git describe --tags --abbrev=0")
    tag = tag.strip()
    return tag


def deploy_to_remote(version: str, progress: ProgressDisplay) -> None:
    """部署到远程服务器"""
    host = get_config('REMOTE_HOST')
    remote_path = get_config('REMOTE_PROJECT_PATH')

    # 1. 更新远程 .env 文件
    update_cmd = f'ssh {host} "sed -i \'s/^APP_IMAGE_TAG=.*/APP_IMAGE_TAG={version}/\' {remote_path}/.env"'
    run_cmd(update_cmd, progress)

    # 2. 重启远程容器
    restart_cmd = f'ssh {host} "cd {remote_path} && docker compose up -d"'
    run_cmd(restart_cmd, progress)


def main():
    progress = ProgressDisplay()
    print("🚀 开始Docker镜像构建、推送和部署流程\n")

    # 1. 获取最新tag
    progress.set_status("🔍 获取最新tag...")
    version = get_latest_tag()
    if not version:
        progress.finish_step("❌ 错误: 没有找到git tag")
        sys.exit(1)
    progress.finish_step(f"✅ 最新tag: {version}")

    # 2. 构建镜像
    progress.set_status("📦 构建Docker镜像...")
    image_name = get_config('IMAGE_NAME')
    env_file = get_config('ENV_FILE')
    env_vars = load_env_file(str(env_file))
    build_args = build_args_from_env(env_vars)
    progress.set_status(f"📦 构建Docker镜像...（注入 {len(env_vars)} 个 build-args）")
    build_cmd = (
        f"docker build "
        f"--file {get_config('DOCKERFILE')} "
        f"{build_args} "
        # 传入当前时间戳作为 CACHEBUST 参数，强制使 Dockerfile 中该指令之后的步骤（CSS构建）缓存失效
        # 这样既能利用依赖包的缓存（加速构建），又能确保每次都生成最新的 CSS（解决样式不更新问题）
        f"--build-arg CACHEBUST={int(time.time())} "
        f"--tag {image_name}:latest "
        f"."
    )
    run_cmd_ex(build_cmd, progress, exit_on_error=True, extra_env={"DOCKER_BUILDKIT": "0"})
    progress.finish_step("✅ Docker镜像构建完成")

    # 3. 打tag & 推送
    for registry in get_config('REGISTRIES'):
        if not registry:
            continue
        registry_type = registry.get('TYPE', '')
        registry_url = registry.get('URL', '')
        registry_namespace = registry.get('NAMESPACE', '')
        registry_image_name = registry.get('IMAGE_NAME', '')
        if registry_type == 'dockerhub':
            registry_image = f"{registry_namespace}/{registry_image_name}:{version}"
        else:
            registry_image = f"{registry_url}/{registry_namespace}/{registry_image_name}:{version}"

        progress.set_status(f"🏷️  给镜像打tag: {image_name} -> {registry_image}...")
        run_cmd(f"docker tag {image_name} {registry_image}", progress)
        progress.finish_step(f"✅ 镜像tag完成: {registry_image}")

        # 4. 推送镜像
        progress.set_status(f"📤 推送镜像到 {registry_image}...")
        run_cmd(f"docker push {registry_image}", progress)
        progress.finish_step(f"✅ 镜像已推送: {registry_image}")

    # 5. 远程部署
    if DEFAULTS['ENABLED_DEPLOY']:
        progress.set_status("🛰️  开始远程部署...")
        deploy_to_remote(version, progress)
        progress.finish_step("✅ 远程部署完成")

    print("\n🎉 所有任务已完成！")


if __name__ == "__main__":
    main()
