import time
from django_starter.contrib.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY


class PrometheusMiddleware:
    """
    Django中间件，用于收集Prometheus监控指标
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取请求开始时间
        start_time = time.time()

        # 处理请求
        response = self.get_response(request)

        # 请求耗时
        duration = time.time() - start_time

        # 请求路径作为endpoint标识，但不包含查询参数
        endpoint = request.path.rstrip('/').lstrip('/') or 'root'

        # 记录请求计数和延迟
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)

        return response
