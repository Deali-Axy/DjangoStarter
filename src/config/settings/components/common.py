import os

from config.settings import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@4gkf7*k+_1@u8z$2*ila%%)ck&i=o$g1lnr40=%mlt-4rh+xd'

# SECURITY WARNING: don't run with debug turned on in production!
# 读取环境变量判断是否开启Debug模式，无须手动设置
DEBUG = os.environ.get('DEBUG', 'true') == 'true'

# 读取环境变量判断是否docker环境，无须手动设置
DOCKER = os.environ.get('ENVIRONMENT', 'default') == 'docker'

# 读取环境变量，设置URL前缀
URL_PREFIX = os.environ.get('URL_PREFIX', '').strip('/')
# 不为空则前后加斜杠，确保格式正确
if len(URL_PREFIX) > 0:
    URL_PREFIX = f'{URL_PREFIX}/'

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'config.urls_root'

WSGI_APPLICATION = 'config.wsgi.application'


