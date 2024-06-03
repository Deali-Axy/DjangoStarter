from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_starter.contrib.auth'
    label = 'django_starter_auth'
    verbose_name = 'Djs认证扩展'
