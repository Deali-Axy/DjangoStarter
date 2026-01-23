from django.urls import path

from . import views

app_name = "djs_notifications"

urlpatterns = [
    path("", views.notifications_index, name="index"),
    path("mark-all-read", views.notifications_mark_all_read, name="mark-all-read"),
    path("<int:notification_id>/read", views.notifications_mark_read, name="mark-read"),
    path("tasks/", views.tasks_index, name="tasks"),
    path("tasks/enqueue-test-notification", views.tasks_enqueue_test_notification, name="enqueue-test-notification"),
]

