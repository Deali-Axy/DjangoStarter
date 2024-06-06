from config.settings.components.common import DOCKER

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',  # 缓存后端 Redis
        # 连接Redis数据库(服务器地址)
        # 一主带多从(可以配置个Redis，写走第一台，读走其他的机器)
        'LOCATION': [
            'redis://redis:6379/0' if DOCKER else 'redis://localhost:6379/0',
        ],
        'KEY_PREFIX': 'django_starter',  # 项目名当做文件前缀
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',  # 连接选项(默认，不改)
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 512,  # 连接池的连接(最大连接)
            },
            # 'PASSWORD': 'password', # Redis密码
        },
        # 缓存过期时间（秒）
        'TIMEOUT': 30
    }
}
