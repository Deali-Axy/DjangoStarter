from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_starter.contrib.monitoring'
    verbose_name = '监控和健康检查'
