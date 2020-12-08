import os

from config.logging import config_logging
from config.caches import config_caches
from config.rest_framework import config_rest_framework

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
INSTALLED_APPS = [
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

    # 第三方组件
    'captcha',
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rq',

    # 我们自己的应用
    'apps.core',
    'apps.demo'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls_root'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 密码验证配置
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# 日志配置
# 不是调试模式才开启日志记录
# if not DEBUG:
LOGGING = config_logging(BASE_DIR)

# 静态文件配置 (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATIC_URL = f'/{URL_PREFIX}static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
MEDIA_URL = f'/{URL_PREFIX}media/'

# 配置redis缓存
CACHES = config_caches(DOCKER)

# Drf 配置
REST_FRAMEWORK = config_rest_framework()

# 验证码配置
MULTI_CAPTCHA_ADMIN = {
    'engine': 'simple-captcha',
}

# Cors Header 配置
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# SimpleUI 配置
SIMPLEUI_LOGO = f'/{URL_PREFIX}static/admin/images/1200px-China_Unicom.png'
SIMPLEUI_HOME_ICON = 'fa fa-home'
SIMPLEUI_HOME_INFO = False  # 显示服务器信息
SIMPLEUI_HOME_QUICK = True  # 快速操作
SIMPLEUI_HOME_ACTION = True  # 最近动作
SIMPLEUI_ANALYSIS = False  # 关闭使用分析
SIMPLEUI_STATIC_OFFLINE = True  # 离线模式
SIMPLEUI_ICON = {
    'Core': 'fa fa-cat',
    '商家': 'fa fa-store',
    '奖品': 'fas fa-user-tie',
    '令牌': 'fa fa-lock',
    '认证令牌': 'fa fa-lock',
    '用户分享记录': 'fa fa-share',
}

# Swagger 配置
SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'config.swagger.CustomSwaggerAutoSchema',
    'DEFAULT_GENERATOR_CLASS': 'config.swagger.CustomOpenAPISchemaGenerator',
    # Controls the default expansion setting for the operations and tags.
    # ‘none’: everything is collapsed
    'DOC_EXPANSION': 'none',
}

# Django-RQ 消息队列配置
RQ_QUEUES = {
    'default': {
        # 使用项目配置的 Redis Cache
        'USE_REDIS_CACHE': 'default',
    },
}
