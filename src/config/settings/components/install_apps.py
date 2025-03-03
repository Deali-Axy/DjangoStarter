from typing import Tuple

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
