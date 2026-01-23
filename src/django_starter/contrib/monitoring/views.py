import os

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .apis import check_db_sync, check_redis_sync, get_system_info, get_uptime


def metrics(request: HttpRequest) -> HttpResponse:
    """
    Prometheus metrics endpoint.

    默认仅在 DEBUG 或配置了 METRICS_AUTH_TOKEN 时开放：
    - 若设置 METRICS_AUTH_TOKEN，则要求请求头 X-Metrics-Token 匹配。
    - 否则仅允许在 DEBUG 模式访问。
    """
    token = os.environ.get("METRICS_AUTH_TOKEN", "").strip()
    if token:
        provided = request.headers.get("X-Metrics-Token", "")
        if provided != token:
            return HttpResponse(status=403)
    else:
        if not settings.DEBUG:
            return HttpResponse(status=404)

    payload = generate_latest()
    return HttpResponse(payload, content_type=CONTENT_TYPE_LATEST)


def health(request: HttpRequest) -> JsonResponse:
    """
    Liveness probe endpoint.
    """
    return JsonResponse(
        {
            "status": "healthy",
            "status_code": 200,
            "system": get_system_info(),
        }
    )


def ready(request: HttpRequest) -> JsonResponse:
    """
    Readiness probe endpoint.
    """
    db_ok = check_db_sync()
    redis_ok = check_redis_sync()

    status = "healthy" if db_ok and redis_ok else "unhealthy"
    status_code = 200 if status == "healthy" else 503

    return JsonResponse(
        {
            "status": status,
            "status_code": status_code,
            "checks": {
                "database": "ok" if db_ok else "error",
                "redis": "ok" if redis_ok else "error",
            },
            "system": {
                **get_system_info(),
                "uptime": get_uptime(),
            },
        },
        status=status_code,
    )

