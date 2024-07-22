# 环境初始化

import os

from django.conf import settings


def init_logging_from_settings():
    """
    根据配置初始化日志功能，创建日志目录

    :return:
    """

    if not os.path.exists(settings.LOGGING_DIR_CONFIG['base']):
        os.mkdir(settings.LOGGING_DIR_CONFIG['base'])

    if not os.path.exists(settings.LOGGING_DIR_CONFIG['error']):
        os.mkdir(settings.LOGGING_DIR_CONFIG['error'])

    if not os.path.exists(settings.LOGGING_DIR_CONFIG['request']):
        os.mkdir(settings.LOGGING_DIR_CONFIG['request'])

    if not os.path.exists(settings.LOGGING_DIR_CONFIG['script']):
        os.mkdir(settings.LOGGING_DIR_CONFIG['script'])


def init_logging(dir_list: list):
    """
    根据传入的目录列表，初始化日志功能，创建日志目录

    :param dir_list:
    :return:
    """

    for path in dir_list:
        if not os.path.exists(path):
            os.mkdir(path)
