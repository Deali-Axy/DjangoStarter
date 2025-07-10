from typing import Dict, Any, List
from config.settings.components.common import DOCKER, DEBUG
from django_starter.contrib.cache import CacheBackendSpec, get_django_cache_settings


# =============================================================================
# CACHE BACKEND CONFIGURATIONS
# =============================================================================
# This is the main configuration section - modify here to add/remove cache backends

CACHE_BACKEND_SPECS = [
    CacheBackendSpec(
        alias='default',
        db_index=0,  # Can be overridden by REDIS_DB_DEFAULT env var
        key_prefix='django_starter',
        description='Default cache for general application use'
    ),
    # Add more cache backends here as needed:
    # CacheBackendSpec(
    #     alias='sessions',
    #     db_index=1,
    #     key_prefix='sessions',
    #     description='Session storage cache'
    # ),
]


# =============================================================================
# CACHE SETTINGS GENERATION
# =============================================================================

def get_cache_settings() -> Dict[str, Any]:
    """Generate complete cache settings using the centralized cache manager.
    
    This function uses the django_starter.cache module to generate cache
    configurations based on the CACHE_BACKEND_SPECS defined above.
    
    Returns:
        Complete Django CACHES configuration dictionary
    """
    return get_django_cache_settings(
        docker_mode=DOCKER,
        debug_mode=DEBUG,
        custom_specs=CACHE_BACKEND_SPECS
    )


# Generate cache configuration
CACHES = get_cache_settings()
