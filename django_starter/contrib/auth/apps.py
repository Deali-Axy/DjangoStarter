from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_starter.contrib.auth'
    verbose_name = '用户资料管理'
