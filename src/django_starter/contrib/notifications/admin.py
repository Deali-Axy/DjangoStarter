from django.contrib import admin

from .models import Notification, TaskRun


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "level", "read_time", "created_time")
    list_filter = ("level", "read_time", "created_time")
    search_fields = ("title", "content", "user__username", "user__email")
    ordering = ("-created_time",)


@admin.register(TaskRun)
class TaskRunAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "status", "created_time", "started_time", "finished_time")
    list_filter = ("status", "created_time")
    search_fields = ("name", "user__username", "user__email")
    ordering = ("-created_time",)

