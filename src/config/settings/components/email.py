from os import environ

EMAIL_BACKEND = environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

DEFAULT_FROM_EMAIL = environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'no-reply@example.com')

EMAIL_HOST = environ.get('DJANGO_EMAIL_HOST', '')
EMAIL_PORT = int(environ.get('DJANGO_EMAIL_PORT', '25'))
EMAIL_HOST_USER = environ.get('DJANGO_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = environ.get('DJANGO_EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = environ.get('DJANGO_EMAIL_USE_TLS', 'false').lower() == 'true'
EMAIL_USE_SSL = environ.get('DJANGO_EMAIL_USE_SSL', 'false').lower() == 'true'

