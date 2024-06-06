import os
from datetime import datetime

from config import env_init
from config.settings import BASE_DIR
from config.settings.components.common import DEBUG


def config_logging(base_dir: str) -> dict:
    """
    配置日志

    :param base_dir: Djanago BaseDir
    :return: logging
    """

    # 日志目录配置
    logging_dir_config = {
        'base': os.path.join(base_dir, 'log'),
        'django': 'django',
        'error': 'error',
        'request': 'request',
        'script': 'script'
    }

    # 初始化日志目录 不存在的话会自动创建
    env_init.init_logging([
        logging_dir_config['base'],
        os.path.join(logging_dir_config['base'], logging_dir_config['django']),
        os.path.join(logging_dir_config['base'], logging_dir_config['error']),
        os.path.join(logging_dir_config['base'], logging_dir_config['request']),
        os.path.join(logging_dir_config['base'], logging_dir_config['script']),
    ])

    logging = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s] %(message)s'
            }
        },
        'filters': {},
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
            'django': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(logging_dir_config['base'], logging_dir_config['django'],
                                         f'QWebFX_{datetime.now().date()}.log'),
                'maxBytes': 1024 * 1024 * 5,  # 文件大小
                'backupCount': 1,  # 备份份数
                'formatter': 'standard',  # 使用哪种formatters日志格式
            },
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(logging_dir_config['base'], f'QWebFX_{datetime.now().date()}.log'),
                'maxBytes': 1024 * 1024 * 5,  # 文件大小
                'backupCount': 3,  # 备份份数
                'formatter': 'standard',  # 使用哪种formatters日志格式
            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(logging_dir_config['base'], logging_dir_config['error'],
                                         f'QWebFX_Error_{datetime.now().date()}.log'),
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 3,
                'formatter': 'standard',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'request_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(logging_dir_config['base'], logging_dir_config['request'],
                                         f'QWebFX_Request_{datetime.now().date()}.log'),
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 3,
                'formatter': 'standard',
            },
            'scripts_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(logging_dir_config['base'], logging_dir_config['script'],
                                         f'QWebFX_Script_{datetime.now().date()}.log'),
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 3,
                'formatter': 'standard',
            }
        },
        'loggers': {
            'django': {
                'handlers': ['django'],
                'level': 'DEBUG',
                'propagate': False
            },
            'django.request': {
                'handlers': ['request_handler'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'scripts': {
                'handlers': ['scripts_handler'],
                'level': 'INFO',
                'propagate': False
            },
            'console': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
            'common': {
                'handlers': ['console', 'default', 'error'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    }

    return logging


def config_debug_logging() -> dict:
    """
    调试模式的日志配置

    :return: logging
    """

    console_handler = {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'standard'
    }
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(pathname)s:%(funcName)s:%(lineno)d] [%(levelname)s] %(message)s'
            }
        },
        'handlers': {
            'console': console_handler,
        },
        'loggers': {
            'common': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    }


# 日志配置
# 不是调试模式才开启日志记录
if DEBUG:
    LOGGING = config_debug_logging()
else:
    LOGGING = config_logging(BASE_DIR)
