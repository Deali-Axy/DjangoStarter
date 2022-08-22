def config_rest_framework():
    return {
        # 全局配置异常模块（使用DjangoStarter封装的全局异常处理）
        'EXCEPTION_HANDLER': 'django_starter.http.response.exception.custom_handler',
        # 修改默认返回JSON的renderer的类（使用DjangoStarter封装的全局异常处理）
        'DEFAULT_RENDERER_CLASSES': (
            'django_starter.http.response.renderer.CustomRenderer',
        ),
        # 设置分页（使用DjangoStarter封装的分页器）
        'DEFAULT_PAGINATION_CLASS': 'django_starter.core.paginator.NumberPaginator',
        # 默认解析器配置
        # 'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
        'PAGE_SIZE': 10,
        # 认证与权限
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ],
        # 文档
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
        # 默认的限流类(使用速率来限流)
        'DEFAULT_THROTTLE_CLASSES': (
            'rest_framework.throttling.AnonRateThrottle',  # 匿名用户节流
            'rest_framework.throttling.UserRateThrottle'  # 登录用户节流
        ),
        # 限流的速率
        'DEFAULT_THROTTLE_RATES': {
            'anon': '30/min',  # 匿名用户对应的节流次数，每分钟30次
            'user': '60/min'  # 登录用户对应节流  每分钟60次
        },
    }
