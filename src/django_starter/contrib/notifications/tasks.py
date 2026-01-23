import traceback

from django.contrib.auth.models import User
from django.db import transaction
from django.tasks import task
from django.utils import timezone

from .models import Notification, TaskRun


@task
def create_notification(
    *,
    task_run_id: int,
    user_id: int,
    title: str,
    content: str = "",
    link: str = "",
    level: str = Notification.LEVEL_INFO,
) -> int:
    """
    创建通知并更新 TaskRun 状态。
    """
    task_run = TaskRun.objects.filter(id=task_run_id).first()
    if task_run:
        task_run.status = TaskRun.STATUS_RUNNING
        task_run.started_time = timezone.now()
        task_run.save(update_fields=["status", "started_time"])

    try:
        user = User.objects.get(id=user_id)
        with transaction.atomic():
            n = Notification.objects.create(
                user=user,
                title=title,
                content=content,
                link=link,
                level=level,
            )
            if task_run:
                task_run.status = TaskRun.STATUS_SUCCESS
                task_run.finished_time = timezone.now()
                task_run.result = {"notification_id": n.id}
                task_run.save(update_fields=["status", "finished_time", "result"])
        return n.id
    except Exception:
        err = traceback.format_exc()
        if task_run:
            task_run.status = TaskRun.STATUS_FAILED
            task_run.finished_time = timezone.now()
            task_run.error = err
            task_run.save(update_fields=["status", "finished_time", "error"])
        raise

