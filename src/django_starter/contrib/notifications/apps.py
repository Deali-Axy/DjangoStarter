from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """
    通知与任务中心（站内通知 + Django Tasks 执行记录）。
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_starter.contrib.notifications"
    verbose_name = "通知中心"

