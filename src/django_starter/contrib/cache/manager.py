"""Django cache configuration utilities.

This module provides a centralized cache configuration system that supports
both Redis and local memory backends with flexible environment-based configuration.
"""

import os
from typing import Dict, Any, List, NamedTuple, Optional


class CacheBackendSpec(NamedTuple):
    """Cache backend specification.
    
    Attributes:
        alias: Cache alias name (e.g., 'default', 'select2')
        db_index: Redis database index
        key_prefix: Cache key prefix
        description: Optional description for documentation
    """
    alias: str
    db_index: int
    key_prefix: str
    description: Optional[str] = None


class CacheConfigManager:
    """Centralized cache configuration manager.
    
    This class provides a clean interface for managing Django cache configurations
    with support for both Redis and local memory backends.
    """
    
    # Default cache backend specifications
    # This is the main configuration point - easy to modify and extend
    DEFAULT_CACHE_SPECS = [
        CacheBackendSpec(
            alias='default',
            db_index=0,
            key_prefix='django_starter',
            description='Default cache for general application use'
        ),
        CacheBackendSpec(
            alias='select2',
            db_index=2,
            key_prefix='select2',
            description='Cache for Select2 widget data'
        ),
        # Add more cache backends here as needed:
        # CacheBackendSpec(
        #     alias='sessions',
        #     db_index=1,
        #     key_prefix='sessions',
        #     description='Session storage cache'
        # ),
    ]
    
    def __init__(self, docker_mode: bool = False, debug_mode: bool = True):
        """Initialize cache configuration manager.
        
        Args:
            docker_mode: Whether running in Docker environment
            debug_mode: Whether running in debug mode
        """
        self.docker_mode = docker_mode
        self.debug_mode = debug_mode
    
    def get_env_value(self, key: str, default: str = '') -> str:
        """Get environment variable value with default fallback."""
        return os.environ.get(key, default)
    
    def get_redis_location(self, db_index: int = 0) -> str:
        """Generate Redis connection URL based on environment."""
        host = self.get_env_value('REDIS_HOST', 'redis' if self.docker_mode else 'localhost')
        port = self.get_env_value('REDIS_PORT', '6379')
        password = self.get_env_value('REDIS_PASSWORD', '')
        
        if password:
            return f'redis://:{password}@{host}:{port}/{db_index}'
        return f'redis://{host}:{port}/{db_index}'
    
    def get_local_cache_config(self) -> Dict[str, Any]:
        """Generate local memory cache configuration."""
        return {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'local-dev-cache',
        }
    
    def get_redis_cache_config(self, db_index: int = 0, key_prefix: str = 'django_starter') -> Dict[str, Any]:
        """Generate Redis cache configuration."""
        max_connections = int(self.get_env_value('REDIS_MAX_CONNECTIONS', '512'))
        timeout = int(self.get_env_value('CACHE_TIMEOUT', '30'))
        password = self.get_env_value('REDIS_PASSWORD', '')
        
        config = {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': [self.get_redis_location(db_index)],
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
    
    def get_cache_backend_specs(self, custom_specs: Optional[List[CacheBackendSpec]] = None) -> List[CacheBackendSpec]:
        """Get cache backend specifications.
        
        Args:
            custom_specs: Optional custom specifications to override defaults
            
        Returns:
            List of cache backend specifications
        """
        if custom_specs is not None:
            return custom_specs
        
        # Allow environment variable overrides for database indices
        specs = []
        for spec in self.DEFAULT_CACHE_SPECS:
            env_key = f'REDIS_DB_{spec.alias.upper()}'
            db_index = int(self.get_env_value(env_key, str(spec.db_index)))
            
            specs.append(CacheBackendSpec(
                alias=spec.alias,
                db_index=db_index,
                key_prefix=spec.key_prefix,
                description=spec.description
            ))
        
        return specs
    
    def build_cache_backends(self, specs: List[CacheBackendSpec], use_redis: bool) -> Dict[str, Any]:
        """Build cache backends from specifications.
        
        Args:
            specs: List of cache backend specifications
            use_redis: Whether to use Redis or local memory cache
            
        Returns:
            Dictionary of cache configurations
        """
        if use_redis:
            return {
                spec.alias: self.get_redis_cache_config(
                    db_index=spec.db_index,
                    key_prefix=spec.key_prefix
                )
                for spec in specs
            }
        else:
            # In development, all backends can share the same local cache instance
            local_cache = self.get_local_cache_config()
            return {spec.alias: local_cache for spec in specs}
    
    def should_use_redis(self) -> bool:
        """Determine whether to use Redis based on environment.
        
        Returns:
            True if Redis should be used, False for local memory cache
        """
        use_redis_in_debug = self.get_env_value('USE_REDIS_IN_DEBUG', 'false').lower() == 'true'
        return not self.debug_mode or use_redis_in_debug
    
    def get_cache_settings(self, custom_specs: Optional[List[CacheBackendSpec]] = None) -> Dict[str, Any]:
        """Generate complete cache settings based on environment.
        
        Args:
            custom_specs: Optional custom cache specifications
            
        Returns:
            Complete Django CACHES configuration dictionary
        """
        use_redis = self.should_use_redis()
        specs = self.get_cache_backend_specs(custom_specs)
        return self.build_cache_backends(specs, use_redis)
    
    def get_cache_aliases(self, custom_specs: Optional[List[CacheBackendSpec]] = None) -> List[str]:
        """Get list of all cache aliases.
        
        Args:
            custom_specs: Optional custom cache specifications
            
        Returns:
            List of cache alias names
        """
        specs = self.get_cache_backend_specs(custom_specs)
        return [spec.alias for spec in specs]
    
    def print_cache_info(self, custom_specs: Optional[List[CacheBackendSpec]] = None) -> None:
        """Print cache configuration information for debugging.
        
        Args:
            custom_specs: Optional custom cache specifications
        """
        specs = self.get_cache_backend_specs(custom_specs)
        use_redis = self.should_use_redis()
        
        print(f"Cache Configuration (Redis: {use_redis})")
        print("=" * 50)
        
        for spec in specs:
            print(f"Alias: {spec.alias}")
            print(f"  DB Index: {spec.db_index}")
            print(f"  Key Prefix: {spec.key_prefix}")
            if spec.description:
                print(f"  Description: {spec.description}")
            if use_redis:
                print(f"  Location: {self.get_redis_location(spec.db_index)}")
            print()


# Convenience functions for backward compatibility and easy usage
def create_cache_manager(docker_mode: bool = False, debug_mode: bool = True) -> CacheConfigManager:
    """Create a cache configuration manager instance.
    
    Args:
        docker_mode: Whether running in Docker environment
        debug_mode: Whether running in debug mode
        
    Returns:
        CacheConfigManager instance
    """
    return CacheConfigManager(docker_mode=docker_mode, debug_mode=debug_mode)


def get_django_cache_settings(docker_mode: bool = False, debug_mode: bool = True, 
                             custom_specs: Optional[List[CacheBackendSpec]] = None) -> Dict[str, Any]:
    """Get Django cache settings using the default configuration.
    
    Args:
        docker_mode: Whether running in Docker environment
        debug_mode: Whether running in debug mode
        custom_specs: Optional custom cache specifications
        
    Returns:
        Complete Django CACHES configuration dictionary
    """
    manager = create_cache_manager(docker_mode=docker_mode, debug_mode=debug_mode)
    return manager.get_cache_settings(custom_specs=custom_specs)