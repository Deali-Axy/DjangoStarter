import os
from pathlib import Path

from config.settings import BASE_DIR
from config.settings.components.common import DEBUG


def ensure_log_directory(log_dir: Path) -> None:
    """
    确保日志目录存在
    
    :param log_dir: 日志目录路径
    """
    log_dir.mkdir(parents=True, exist_ok=True)


def get_logging_config(base_dir: str, app_name: str = 'djangostarter') -> dict:
    """
    获取生产环境日志配置
    
    :param base_dir: Django项目根目录
    :param app_name: 应用名称，用于日志文件命名
    :return: logging配置字典
    """
    # 日志目录配置
    log_dir = Path(base_dir) / 'logs'
    ensure_log_directory(log_dir)
    
    # 日志文件路径
    app_log_file = log_dir / f'{app_name}_app.log'
    error_log_file = log_dir / f'{app_name}_error.log'
    django_log_file = log_dir / f'{app_name}_django.log'
    
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {asctime} {name} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'file_app': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(app_log_file),
                'maxBytes': 1024 * 1024 * 10,  # 10MB
                'backupCount': 5,
                'formatter': 'verbose',
            },
            'file_error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(error_log_file),
                'maxBytes': 1024 * 1024 * 10,  # 10MB
                'backupCount': 5,
                'formatter': 'verbose',
            },
            'file_django': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(django_log_file),
                'maxBytes': 1024 * 1024 * 10,  # 10MB
                'backupCount': 3,
                'formatter': 'verbose',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file_app'],
        },
        'loggers': {
            'django': {
                'handlers': ['file_django', 'console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['file_error', 'mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['file_error', 'mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            # 保持与现有代码的兼容性
            'common': {
                'handlers': ['console', 'file_app', 'file_error'],
                'level': 'INFO',
                'propagate': False,
            },
            'scripts': {
                'handlers': ['console', 'file_app'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    }


def get_debug_logging_config() -> dict:
    """
    获取开发环境日志配置
    
    :return: logging配置字典
    """
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {name} {module} {funcName}:{lineno} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            # 保持与现有代码的兼容性
            'common': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'scripts': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }


# 根据环境选择日志配置
if DEBUG:
    LOGGING = get_debug_logging_config()
else:
    LOGGING = get_logging_config(BASE_DIR)
