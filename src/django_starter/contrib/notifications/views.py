from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import Notification, TaskRun
from .tasks import create_notification


@login_required
def notifications_index(request: HttpRequest) -> HttpResponse:
    notifications = (
        Notification.objects.filter(user=request.user)
        .order_by("-created_time")
        .all()[:50]
    )
    unread_count = Notification.objects.filter(user=request.user, read_time__isnull=True).count()

    ctx = {
        "title": "通知中心",
        "breadcrumbs": [
            {"text": "主页", "url": reverse("home:index"), "icon": "fa-solid fa-house"},
            {"text": "通知中心", "url": None, "icon": "fa-regular fa-bell"},
        ],
        "notifications": notifications,
        "unread_count": unread_count,
    }
    return render(request, "django_starter/notifications/index.html", ctx)


@login_required
def notifications_mark_all_read(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect(reverse("djs_notifications:index"))

    Notification.objects.filter(user=request.user, read_time__isnull=True).update(read_time=timezone.now())
    return redirect(reverse("djs_notifications:index"))


@login_required
def notifications_mark_read(request: HttpRequest, notification_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect(reverse("djs_notifications:index"))

    n = get_object_or_404(Notification, id=notification_id, user=request.user)
    n.mark_read()
    return redirect(reverse("djs_notifications:index"))


@login_required
def tasks_index(request: HttpRequest) -> HttpResponse:
    tasks = TaskRun.objects.filter(user=request.user).order_by("-created_time").all()[:50]
    ctx = {
        "title": "任务中心",
        "breadcrumbs": [
            {"text": "主页", "url": reverse("home:index"), "icon": "fa-solid fa-house"},
            {"text": "任务中心", "url": None, "icon": "fa-solid fa-list-check"},
        ],
        "tasks": tasks,
    }
    return render(request, "django_starter/notifications/tasks.html", ctx)


@login_required
def tasks_enqueue_test_notification(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect(reverse("djs_notifications:tasks"))

    task_run = TaskRun.objects.create(
        user=request.user,
        name="create_notification",
        payload={"kind": "test"},
        status=TaskRun.STATUS_QUEUED,
    )

    create_notification.enqueue(
        task_run_id=task_run.id,
        user_id=request.user.id,
        title="测试通知",
        content="这是一条由 Django Tasks 触发的站内通知。",
        level=Notification.LEVEL_INFO,
    )
    messages.success(request, "已创建测试任务。")
    return redirect(reverse("djs_notifications:tasks"))
