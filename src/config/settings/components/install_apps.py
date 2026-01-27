import os
from typing import Tuple

# 应用定义
INSTALLED_APPS: Tuple[str, ...] = (
    # 后台扩展
    "jazzmin",
    # 'multi_captcha_admin',

    # Django核心
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # DjangoStarter组件
    'django_starter.contrib.about',
    'django_starter.contrib.admin',
    'django_starter.contrib.auth',
    'django_starter.contrib.code_generator',
    'django_starter.contrib.config',
    'django_starter.contrib.docs',
    'django_starter.contrib.guide',
    'django_starter.contrib.navbar',
    'django_starter.contrib.notifications',
    'django_starter.contrib.seed',

    # 第三方组件
    'captcha',
    'corsheaders',
    'django_watchfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'simple_history',

    # 我们自己的应用
    'apps.account.apps.AccountConfig',
    'apps.billing.apps.BillingConfig',
    'apps.demo',
    'apps.home',
)

if os.environ.get('ALLAUTH_ENABLED', 'false') == 'true':
    providers = [
        p.strip()
        for p in (os.environ.get('ALLAUTH_PROVIDERS', '').split(','))
        if p.strip()
    ]
    provider_apps = tuple(f'allauth.socialaccount.providers.{p}' for p in providers)
    INSTALLED_APPS = INSTALLED_APPS + (
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        *provider_apps,
    )
