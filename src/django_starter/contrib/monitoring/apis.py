import asyncio

from ninja import Router
from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
from redis import Redis
from redis.exceptions import RedisError
from redis import asyncio as aioredis
import os
import time
import platform
import subprocess
import anyio

router = Router(tags=['djs-monitoring'])


# 获取系统启动时间（跨平台支持）
def get_uptime():
    system = platform.system()
    if system == 'Linux':
        try:
            # Linux系统使用/proc/1的创建时间
            return time.time() - os.stat('/proc/1').st_ctime
        except (FileNotFoundError, PermissionError):
            try:
                # 备选方法：使用uptime命令
                cmd = ['uptime', '-s']
                boot_time_str = subprocess.check_output(cmd).decode().strip()
                boot_time = time.mktime(time.strptime(boot_time_str, "%Y-%m-%d %H:%M:%S"))
                return time.time() - boot_time
            except (subprocess.SubprocessError, ValueError):
                return 0
    elif system == 'Darwin':  # macOS
        try:
            # 使用系统命令获取启动时间
            cmd = ['sysctl', '-n', 'kern.boottime']
            boot_time = subprocess.check_output(cmd).decode().strip()
            # 解析输出格式 { sec = 1234567890, usec = 123456 } Mon Jan 1 00:00:00 2023
            boot_timestamp = float(boot_time.split()[3].rstrip(','))
            return time.time() - boot_timestamp
        except (subprocess.SubprocessError, ValueError, IndexError):
            try:
                # 备选方法：使用uptime命令
                cmd = ['uptime']
                output = subprocess.check_output(cmd).decode().strip()
                # 解析uptime输出，格式类似于 "10:30  up 2 days, 14:22, 5 users"
                up_parts = output.split('up ')[1].split(',')
                uptime_str = up_parts[0].strip()

                # 解析天数和小时
                uptime_seconds = 0
                if 'day' in uptime_str:
                    days = int(uptime_str.split('day')[0].strip())
                    uptime_seconds += days * 86400  # 一天86400秒

                # 解析小时和分钟
                if ':' in uptime_str:
                    time_part = uptime_str.split(':')[-2:]
                    hours = int(time_part[0].split()[-1])
                    minutes = int(time_part[1])
                    uptime_seconds += hours * 3600 + minutes * 60
                elif 'min' in uptime_str:
                    minutes = int(uptime_str.split('min')[0].strip())
                    uptime_seconds += minutes * 60

                return uptime_seconds
            except (subprocess.SubprocessError, ValueError, IndexError):
                return 0
    elif system == 'Windows':
        try:
            # 使用系统命令获取启动时间（单位：秒）
            cmd = ['net', 'statistics', 'workstation']
            output = subprocess.check_output(cmd).decode(errors='ignore')
            for line in output.splitlines():
                if 'Statistics since' in line or '统计开始于' in line:
                    # 解析日期时间并转换为时间戳
                    # 英文: Statistics since 1/23/2025 12:00:00 AM
                    # 中文: 统计开始于 2025/1/23 12:00:00
                    parts = line.split('Statistics since')
                    if len(parts) < 2:
                        parts = line.split('统计开始于')
                    
                    if len(parts) < 2:
                        continue
                        
                    date_str = parts[1].strip()
                    try:
                        # 尝试解析英文格式日期 (例如: "1/2/2023 12:34:56 AM")
                        boot_time = time.mktime(time.strptime(date_str, "%m/%d/%Y %I:%M:%S %p"))
                    except ValueError:
                        try:
                            # 尝试解析中文格式日期 (例如: "2023/1/2 12:34:56")
                            boot_time = time.mktime(time.strptime(date_str, "%Y/%m/%d %H:%M:%S"))
                        except ValueError:
                            # 如果以上格式都不匹配，尝试使用locale设置的默认格式
                            try:
                                boot_time = time.mktime(time.strptime(date_str))
                            except ValueError:
                                return 0
                    return time.time() - boot_time
            return 0
        except (subprocess.SubprocessError, ValueError, IndexError, FileNotFoundError, OSError):
            try:
                # 备选方法：使用wmic命令获取系统启动时间
                cmd = ['wmic', 'os', 'get', 'lastbootuptime']
                output = subprocess.check_output(cmd).decode(errors='ignore')
                boot_time_str = output.strip().split('\n')[1].strip()
                # 格式通常为：20230101123456.789012+000
                year = int(boot_time_str[0:4])
                month = int(boot_time_str[4:6])
                day = int(boot_time_str[6:8])
                hour = int(boot_time_str[8:10])
                minute = int(boot_time_str[10:12])
                second = int(boot_time_str[12:14])
                boot_time = time.mktime((year, month, day, hour, minute, second, 0, 0, 0))
                return time.time() - boot_time
            except (subprocess.SubprocessError, ValueError, IndexError, FileNotFoundError, OSError):
                return 0
    else:
        return 0  # 不支持的系统返回0


@router.get('health')
def simple_health_check(request):
    """健康检查端点，用于容器健康检查和监控"""
    response_data = {
        'status': 'healthy',
        'status_code': 200,
    }

    return response_data


async def check_db_async():
    """数据库检查（同步 ORM → 放线程池）"""
    try:
        def _check():
            for conn in connections.all():
                conn.cursor()
            return True

        return await anyio.to_thread.run_sync(_check)
    except OperationalError:
        return False


async def check_redis_async():
    """Redis 异步检查（注意：确保关闭客户端以释放连接池）"""
    try:
        redis_client = aioredis.Redis(
            host="redis",
            port=6379,
            socket_connect_timeout=1,
            decode_responses=True,
        )
        try:
            ok = await redis_client.ping()
            return bool(ok)
        finally:
            # 关闭客户端和连接池，避免连接泄露（在短生命周期的容器/请求里很重要）
            try:
                await redis_client.close()
            except Exception:
                pass
            try:
                await redis_client.connection_pool.disconnect()
            except Exception:
                pass
    except Exception:
        return False


def check_db_sync():
    """同步检查数据库连接"""
    try:
        for conn in connections.all():
            conn.cursor()
        return True
    except OperationalError:
        return False


def check_redis_sync():
    """同步检查 Redis"""
    if os.environ.get('ENVIRONMENT') != 'docker':
        return True  # 本地环境默认通过

    try:
        client = Redis(host='redis', port=6379, socket_connect_timeout=1)
        return client.ping()
    except RedisError:
        return False


def get_system_info():
    return {
        'timestamp': time.time(),
        'hostname': os.environ.get('HOSTNAME', ''),
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'os': platform.system(),
    }


@router.get('health/async')
async def health_check_async(request):
    """Async 模式健康检查（ASGI 优化版）"""
    # 使用 asyncio.gather 并发运行 DB 和 Redis 检查
    db_ok, redis_ok = await asyncio.gather(
        check_db_async(),
        check_redis_async(),
    )

    status = "healthy" if db_ok and redis_ok else "unhealthy"
    status_code = 200 if status == "healthy" else 503

    return {
        "status": status,
        "status_code": status_code,
        "checks": {
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
        },
        "system": get_system_info(),
    }


@router.get('health/sync')
def health_check_sync(request):
    """同步版本的健康检查接口"""

    # --- 检查数据库 & Redis ---
    db_ok = check_db_sync()
    redis_ok = check_redis_sync()

    # --- 系统信息 ---
    system_info = {
        "timestamp": time.time(),
        "uptime": get_uptime(),
        "hostname": os.environ.get("HOSTNAME", ""),
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "os": platform.system(),
    }

    # --- 状态码 ---
    status = "healthy" if db_ok and redis_ok else "unhealthy"
    status_code = 200 if status == "healthy" else 503

    # --- 返回数据 ---
    return {
        "status": status,
        "status_code": status_code,
        "checks": {
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
        },
        "system": system_info,
    }
