import os
from typing import Dict, Any
from config.settings.components.common import DOCKER, DEBUG


def get_env_value(key: str, default: str = '') -> str:
    """Get environment variable value with default fallback."""
    return os.environ.get(key, default)


def get_redis_location(db_index: int = 0) -> str:
    """Generate Redis connection URL based on environment."""
    host = get_env_value('REDIS_HOST', 'redis' if DOCKER else 'localhost')
    port = get_env_value('REDIS_PORT', '6379')
    password = get_env_value('REDIS_PASSWORD', '')
    
    if password:
        return f'redis://:{password}@{host}:{port}/{db_index}'
    return f'redis://{host}:{port}/{db_index}'


def get_local_cache_config() -> Dict[str, Any]:
    """Generate local memory cache configuration."""
    return {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'local-dev-cache',
    }


def get_redis_cache_config(db_index: int = 0, key_prefix: str = 'django_starter') -> Dict[str, Any]:
    """Generate Redis cache configuration."""
    max_connections = int(get_env_value('REDIS_MAX_CONNECTIONS', '512'))
    timeout = int(get_env_value('CACHE_TIMEOUT', '30'))
    password = get_env_value('REDIS_PASSWORD', '')
    
    config = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [get_redis_location(db_index)],
        'KEY_PREFIX': key_prefix,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': max_connections,
            },
        },
        'TIMEOUT': timeout
    }
    
    # Add password to OPTIONS if provided
    if password:
        config['OPTIONS']['PASSWORD'] = password
    
    return config


def get_cache_settings() -> Dict[str, Any]:
    """Generate complete cache settings based on environment."""
    default_db = int(get_env_value('REDIS_DB_DEFAULT', '0'))
    
    # Check if Redis should be used in DEBUG mode
    use_redis_in_debug = get_env_value('USE_REDIS_IN_DEBUG', 'false').lower() == 'true'
    
    if DEBUG and not use_redis_in_debug:
        # Use local memory cache for development (default behavior)
        local_cache = get_local_cache_config()
        return {
            'default': local_cache,
        }
    else:
        # Use Redis cache for production or when explicitly enabled in DEBUG
        return {
            'default': get_redis_cache_config(db_index=default_db),
        }


# Generate cache configuration
CACHES = get_cache_settings()
