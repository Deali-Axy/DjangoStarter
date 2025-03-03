import os
from typing import Dict, List, Tuple, Union

from config.settings import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@4gkf7*k+_1@u8z$2*ila%%)ck&i=o$g1lnr40=%mlt-4rh+xd'

# SECURITY WARNING: don't run with debug turned on in production!
# 读取环境变量判断是否开启Debug模式，无须手动设置
DEBUG = os.environ.get('DEBUG', 'true') == 'true'

# 读取环境变量判断是否docker环境，无须手动设置
DOCKER = os.environ.get('ENVIRONMENT', 'default') == 'docker'

# 读取环境变量，设置URL前缀
URL_PREFIX = os.environ.get('URL_PREFIX', '')
# 不为空则后面加个斜杠
if len(URL_PREFIX) > 0:
    URL_PREFIX += '/'

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'config.urls_root'

WSGI_APPLICATION = 'config.wsgi.application'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static-dist')
STATIC_URL = f'/{URL_PREFIX}static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = f'/{URL_PREFIX}media/'

# Security
# https://docs.djangoproject.com/en/4.2/topics/security/

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

# https://github.com/DmytroLitvinov/django-http-referrer-policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
REFERRER_POLICY = 'same-origin'

# https://github.com/adamchainz/django-permissions-policy#setting
PERMISSIONS_POLICY: Dict[str, Union[str, List[str]]] = {}  # noqa: WPS234
