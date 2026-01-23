from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from django_starter.db.models import ModelExt
from django_starter.utilities import table_name_wrapper


class Notification(ModelExt):
    """
    站内通知。
    """

    LEVEL_INFO = "info"
    LEVEL_SUCCESS = "success"
    LEVEL_WARNING = "warning"
    LEVEL_ERROR = "error"

    LEVEL_CHOICES = (
        (LEVEL_INFO, "info"),
        (LEVEL_SUCCESS, "success"),
        (LEVEL_WARNING, "warning"),
        (LEVEL_ERROR, "error"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", verbose_name="用户")
    title = models.CharField("标题", max_length=200)
    content = models.TextField("内容", blank=True, default="")
    link = models.URLField("链接", blank=True, default="")
    level = models.CharField("级别", max_length=20, choices=LEVEL_CHOICES, default=LEVEL_INFO)
    read_time = models.DateTimeField("已读时间", null=True, blank=True)

    class Meta:
        db_table = table_name_wrapper("notification")
        verbose_name = "通知"
        verbose_name_plural = verbose_name
        ordering = ("-created_time",)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.title}"

    def mark_read(self) -> None:
        self.read_time = timezone.now()
        self.save(update_fields=["read_time"])


class TaskRun(ModelExt):
    """
    Django Tasks 的最小执行记录。
    """

    STATUS_QUEUED = "queued"
    STATUS_RUNNING = "running"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = (
        (STATUS_QUEUED, "queued"),
        (STATUS_RUNNING, "running"),
        (STATUS_SUCCESS, "success"),
        (STATUS_FAILED, "failed"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="task_runs", verbose_name="用户")
    name = models.CharField("任务名称", max_length=200)
    status = models.CharField("状态", max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED)
    payload = models.JSONField("参数", default=dict, blank=True)
    result = models.JSONField("结果", null=True, blank=True)
    error = models.TextField("错误信息", blank=True, default="")
    started_time = models.DateTimeField("开始时间", null=True, blank=True)
    finished_time = models.DateTimeField("结束时间", null=True, blank=True)

    class Meta:
        db_table = table_name_wrapper("task_run")
        verbose_name = "任务"
        verbose_name_plural = verbose_name
        ordering = ("-created_time",)

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"

