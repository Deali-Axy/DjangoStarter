# 环境初始化

import os

from django.conf import settings


def init_logging_from_settings():
    if not os.path.exists(settings.LOGGING_DIR_CONFIG['base']):
        os.mkdir(settings.LOGGING_DIR_CONFIG['base'])

    if not os.path.exists(settings.LOGGING_DIR_CONFIG['error']):
        os.mkdir(settings.LOGGING_DIR_CONFIG['error'])

    if not os.path.exists(settings.LOGGING_DIR_CONFIG['request']):
        os.mkdir(settings.LOGGING_DIR_CONFIG['request'])

    if not os.path.exists(settings.LOGGING_DIR_CONFIG['script']):
        os.mkdir(settings.LOGGING_DIR_CONFIG['script'])


def init_logging(dir_list: list):
    for path in dir_list:
        if not os.path.exists(path):
            os.mkdir(path)
