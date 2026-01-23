# Django authentication system
# https://docs.djangoproject.com/en/4.2/topics/auth/

import os

from config.settings.components.common import URL_PREFIX


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


LOGIN_URL = f"/{URL_PREFIX}accounts/login"

if os.environ.get('ALLAUTH_ENABLED', 'false') == 'true':
    AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + (
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    SITE_ID = int(os.environ.get('SITE_ID', '1'))

    ACCOUNT_AUTHENTICATION_METHOD = os.environ.get('ACCOUNT_AUTHENTICATION_METHOD', 'username_email')
    ACCOUNT_EMAIL_REQUIRED = os.environ.get('ACCOUNT_EMAIL_REQUIRED', 'true') == 'true'
    ACCOUNT_USERNAME_REQUIRED = os.environ.get('ACCOUNT_USERNAME_REQUIRED', 'true') == 'true'
    ACCOUNT_EMAIL_VERIFICATION = os.environ.get('ACCOUNT_EMAIL_VERIFICATION', 'optional')

    SOCIALACCOUNT_AUTO_SIGNUP = os.environ.get('SOCIALACCOUNT_AUTO_SIGNUP', 'true') == 'true'
    SOCIALACCOUNT_QUERY_EMAIL = os.environ.get('SOCIALACCOUNT_QUERY_EMAIL', 'true') == 'true'

    ACCOUNT_FORMS = {
        'login': 'apps.account.allauth_forms.LoginForm',
        'signup': 'apps.account.allauth_forms.SignupForm',
    }
