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

# 应用定义
INSTALLED_APPS: Tuple[str, ...] = (
    # 后台扩展
    'simpleui',
    'multi_captcha_admin',

    # Django核心
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # DjangoStarter组件
    'django_starter.contrib.admin',
    'django_starter.contrib.auth',
    'django_starter.contrib.code_generator',
    'django_starter.contrib.config',
    'django_starter.contrib.guide',
    'django_starter.contrib.seed',

    # 第三方组件
    'captcha',
    'corsheaders',
    'compressor',

    # 我们自己的应用
    'apps.account',
    'apps.demo',
)

MIDDLEWARE: Tuple[str, ...] = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls_root'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 国际化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# 静态文件配置 (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static-dist')
STATIC_URL = f'/{URL_PREFIX}static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = f'/{URL_PREFIX}media/'

# Django authentication system
# https://docs.djangoproject.com/en/4.2/topics/auth/

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# 密码验证配置
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

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
