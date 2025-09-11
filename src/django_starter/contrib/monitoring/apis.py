from ninja import Router
from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError
from redis import Redis
from redis.exceptions import RedisError
import os
import time
import platform
import subprocess

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
            output = subprocess.check_output(cmd).decode()
            for line in output.splitlines():
                if 'Statistics since' in line:
                    # 解析日期时间并转换为时间戳
                    date_str = line.split('Statistics since')[1].strip()
                    try:
                        # 尝试解析英文格式日期 (例如: "1/2/2023 12:34:56 AM")
                        boot_time = time.mktime(time.strptime(date_str, "%m/%d/%Y %I:%M:%S %p"))
                    except ValueError:
                        try:
                            # 尝试解析中文格式日期 (例如: "2023/1/2 12:34:56")
                            boot_time = time.mktime(time.strptime(date_str, "%Y/%m/%d %H:%M:%S"))
                        except ValueError:
                            # 如果以上格式都不匹配，尝试使用locale设置的默认格式
                            boot_time = time.mktime(time.strptime(date_str))
                    return time.time() - boot_time
            return 0
        except (subprocess.SubprocessError, ValueError, IndexError):
            try:
                # 备选方法：使用wmic命令获取系统启动时间
                cmd = ['wmic', 'os', 'get', 'lastbootuptime']
                output = subprocess.check_output(cmd).decode()
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
            except (subprocess.SubprocessError, ValueError, IndexError):
                return 0
    else:
        return 0  # 不支持的系统返回0


@router.get('health')
def health_check(request):
    """健康检查端点，用于容器健康检查和监控"""
    # 检查数据库连接
    db_conn_ok = True
    try:
        for conn in connections.all():
            conn.cursor()
    except OperationalError:
        db_conn_ok = False

    # 检查Redis连接
    redis_ok = True
    if os.environ.get('ENVIRONMENT') == 'docker':
        try:
            redis_client = Redis(host='redis', port=6379, socket_connect_timeout=1)
            response = redis_client.ping()
            redis_ok = response
        except RedisError:
            redis_ok = False

    # 基本系统信息
    system_info = {
        'timestamp': time.time(),
        'uptime': get_uptime(),
        'hostname': os.environ.get('HOSTNAME', ''),
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'os': platform.system(),
    }

    # 整体状态
    status = 'healthy' if db_conn_ok and redis_ok else 'unhealthy'

    status_code = 200 if status == 'healthy' else 503

    response_data = {
        'status': status,
        'status_code': status_code,
        'checks': {
            'database': 'ok' if db_conn_ok else 'error',
            'redis': 'ok' if redis_ok else 'error',
        },
        'system': system_info,
    }


    return response_data
