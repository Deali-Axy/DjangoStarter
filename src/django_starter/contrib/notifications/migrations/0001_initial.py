from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="软删除标志")),
                ("created_time", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_time", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("title", models.CharField(max_length=200, verbose_name="标题")),
                ("content", models.TextField(blank=True, default="", verbose_name="内容")),
                ("link", models.URLField(blank=True, default="", verbose_name="链接")),
                ("level", models.CharField(choices=[("info", "info"), ("success", "success"), ("warning", "warning"), ("error", "error")], default="info", max_length=20, verbose_name="级别")),
                ("read_time", models.DateTimeField(blank=True, null=True, verbose_name="已读时间")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to=settings.AUTH_USER_MODEL, verbose_name="用户")),
            ],
            options={
                "verbose_name": "通知",
                "verbose_name_plural": "通知",
                "db_table": "djs_notification",
                "ordering": ("-created_time",),
            },
        ),
        migrations.CreateModel(
            name="TaskRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="软删除标志")),
                ("created_time", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_time", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("name", models.CharField(max_length=200, verbose_name="任务名称")),
                ("status", models.CharField(choices=[("queued", "queued"), ("running", "running"), ("success", "success"), ("failed", "failed")], default="queued", max_length=20, verbose_name="状态")),
                ("payload", models.JSONField(blank=True, default=dict, verbose_name="参数")),
                ("result", models.JSONField(blank=True, null=True, verbose_name="结果")),
                ("error", models.TextField(blank=True, default="", verbose_name="错误信息")),
                ("started_time", models.DateTimeField(blank=True, null=True, verbose_name="开始时间")),
                ("finished_time", models.DateTimeField(blank=True, null=True, verbose_name="结束时间")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="task_runs", to=settings.AUTH_USER_MODEL, verbose_name="用户")),
            ],
            options={
                "verbose_name": "任务",
                "verbose_name_plural": "任务",
                "db_table": "djs_task_run",
                "ordering": ("-created_time",),
            },
        ),
    ]

