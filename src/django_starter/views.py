from django.http import JsonResponse, HttpResponse
from django.db import connections
from django.db.utils import OperationalError
from redis import Redis
from redis.exceptions import RedisError
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY, CONTENT_TYPE_LATEST
import threading

# 定义Prometheus指标
REQUEST_COUNT = Counter('django_http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('django_http_request_latency_seconds', 'Request latency', ['method', 'endpoint'])

# 创建一个线程锁，防止并发写入问题
prometheus_lock = threading.Lock()

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
        'uptime': time.time() - os.stat('/proc/1').st_ctime,
        'hostname': os.environ.get('HOSTNAME', ''),
        'environment': os.environ.get('ENVIRONMENT', 'development'),
    }

    # 整体状态
    status = 'healthy' if db_conn_ok and redis_ok else 'unhealthy'

    response_data = {
        'status': status,
        'checks': {
            'database': 'ok' if db_conn_ok else 'error',
            'redis': 'ok' if redis_ok else 'error',
        },
        'system': system_info,
    }

    status_code = 200 if status == 'healthy' else 503

    # 记录请求指标
    endpoint = 'health'
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=status_code).inc()

    return JsonResponse(response_data, status=status_code)

def metrics(request):
    """Prometheus指标端点，提供监控数据"""
    with prometheus_lock:
        data = generate_latest(REGISTRY)
    return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
