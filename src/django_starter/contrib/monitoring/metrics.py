from prometheus_client import Counter, Histogram
import threading

# 定义Prometheus指标
REQUEST_COUNT = Counter('django_http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('django_http_request_latency_seconds', 'Request latency', ['method', 'endpoint'])

# 创建一个线程锁，防止并发写入问题
prometheus_lock = threading.Lock() 