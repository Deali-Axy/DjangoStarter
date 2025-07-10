"""Django Cache Configuration Usage Examples.

This file demonstrates how to use the django_starter.cache module
for various cache configuration scenarios.
"""

from django_starter.cache import (
    CacheBackendSpec,
    CacheConfigManager,
    create_cache_manager,
    get_django_cache_settings
)


# =============================================================================
# EXAMPLE 1: Basic Usage (Recommended for most projects)
# =============================================================================

def example_basic_usage():
    """Example of basic cache configuration usage."""
    
    # Define your cache backends
    cache_specs = [
        CacheBackendSpec(
            alias='default',
            db_index=0,
            key_prefix='myapp',
            description='Default cache for general use'
        ),
        CacheBackendSpec(
            alias='select2',
            db_index=2,
            key_prefix='select2',
            description='Cache for Select2 widgets'
        ),
    ]
    
    # Get Django cache settings
    cache_settings = get_django_cache_settings(
        docker_mode=False,  # Set based on your environment
        debug_mode=True,    # Set based on your environment
        custom_specs=cache_specs
    )
    
    return cache_settings


# =============================================================================
# EXAMPLE 2: Advanced Usage with Custom Manager
# =============================================================================

def example_advanced_usage():
    """Example of advanced cache configuration with custom manager."""
    
    # Create a cache manager instance
    cache_manager = create_cache_manager(
        docker_mode=False,
        debug_mode=True
    )
    
    # Define custom cache specifications
    custom_specs = [
        CacheBackendSpec(
            alias='default',
            db_index=0,
            key_prefix='myapp_main',
            description='Main application cache'
        ),
        CacheBackendSpec(
            alias='sessions',
            db_index=1,
            key_prefix='sessions',
            description='User session cache'
        ),
        CacheBackendSpec(
            alias='api_cache',
            db_index=3,
            key_prefix='api',
            description='API response cache'
        ),
        CacheBackendSpec(
            alias='file_cache',
            db_index=4,
            key_prefix='files',
            description='File processing cache'
        ),
    ]
    
    # Get cache settings
    cache_settings = cache_manager.get_cache_settings(custom_specs)
    
    # Print cache information for debugging
    cache_manager.print_cache_info(custom_specs)
    
    # Get list of cache aliases
    aliases = cache_manager.get_cache_aliases(custom_specs)
    print(f"Available cache aliases: {aliases}")
    
    return cache_settings


# =============================================================================
# EXAMPLE 3: Environment-Specific Configurations
# =============================================================================

def example_environment_specific():
    """Example of environment-specific cache configurations."""
    
    # Production configuration
    production_specs = [
        CacheBackendSpec(
            alias='default',
            db_index=0,
            key_prefix='prod_main',
            description='Production main cache'
        ),
        CacheBackendSpec(
            alias='sessions',
            db_index=1,
            key_prefix='prod_sessions',
            description='Production session cache'
        ),
        CacheBackendSpec(
            alias='api_cache',
            db_index=2,
            key_prefix='prod_api',
            description='Production API cache'
        ),
    ]
    
    # Development configuration
    development_specs = [
        CacheBackendSpec(
            alias='default',
            db_index=0,
            key_prefix='dev_main',
            description='Development main cache'
        ),
        CacheBackendSpec(
            alias='debug_cache',
            db_index=1,
            key_prefix='debug',
            description='Debug-specific cache'
        ),
    ]
    
    # Choose configuration based on environment
    import os
    is_production = os.environ.get('DJANGO_ENV') == 'production'
    
    if is_production:
        cache_settings = get_django_cache_settings(
            docker_mode=True,
            debug_mode=False,
            custom_specs=production_specs
        )
    else:
        cache_settings = get_django_cache_settings(
            docker_mode=False,
            debug_mode=True,
            custom_specs=development_specs
        )
    
    return cache_settings


# =============================================================================
# EXAMPLE 4: Testing Configuration
# =============================================================================

def example_testing_configuration():
    """Example of cache configuration for testing."""
    
    # For testing, you might want simpler cache specs
    test_specs = [
        CacheBackendSpec(
            alias='default',
            db_index=0,
            key_prefix='test',
            description='Test cache'
        ),
    ]
    
    # Force local memory cache for testing
    cache_manager = CacheConfigManager(
        docker_mode=False,
        debug_mode=True  # This will use local memory cache
    )
    
    # Override to ensure local cache even if USE_REDIS_IN_DEBUG is set
    cache_settings = cache_manager.build_cache_backends(
        specs=test_specs,
        use_redis=False  # Force local cache for tests
    )
    
    return cache_settings


# =============================================================================
# EXAMPLE 5: Dynamic Cache Configuration
# =============================================================================

def example_dynamic_configuration():
    """Example of dynamic cache configuration based on runtime conditions."""
    
    import os
    
    # Base cache specifications
    base_specs = [
        CacheBackendSpec(
            alias='default',
            db_index=0,
            key_prefix='app',
            description='Main application cache'
        ),
    ]
    
    # Add additional caches based on features enabled
    if os.environ.get('ENABLE_API_CACHE', 'false').lower() == 'true':
        base_specs.append(
            CacheBackendSpec(
                alias='api_cache',
                db_index=2,
                key_prefix='api',
                description='API response cache'
            )
        )
    
    if os.environ.get('ENABLE_FILE_CACHE', 'false').lower() == 'true':
        base_specs.append(
            CacheBackendSpec(
                alias='file_cache',
                db_index=3,
                key_prefix='files',
                description='File processing cache'
            )
        )
    
    # Get cache settings with dynamic specifications
    cache_settings = get_django_cache_settings(
        docker_mode=os.environ.get('DOCKER', 'false').lower() == 'true',
        debug_mode=os.environ.get('DEBUG', 'true').lower() == 'true',
        custom_specs=base_specs
    )
    
    return cache_settings


if __name__ == '__main__':
    # Run examples
    print("=== Basic Usage ===")
    basic_config = example_basic_usage()
    print(f"Basic config keys: {list(basic_config.keys())}")
    
    print("\n=== Advanced Usage ===")
    advanced_config = example_advanced_usage()
    
    print("\n=== Environment Specific ===")
    env_config = example_environment_specific()
    print(f"Environment config keys: {list(env_config.keys())}")
    
    print("\n=== Testing Configuration ===")
    test_config = example_testing_configuration()
    print(f"Test config keys: {list(test_config.keys())}")
    
    print("\n=== Dynamic Configuration ===")
    dynamic_config = example_dynamic_configuration()
    print(f"Dynamic config keys: {list(dynamic_config.keys())}")