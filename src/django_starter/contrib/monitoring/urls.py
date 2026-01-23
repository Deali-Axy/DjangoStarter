from django.urls import path

from . import views

app_name = "djs_monitoring"

urlpatterns = [
    path("health", views.health, name="health"),
    path("ready", views.ready, name="ready"),
    path("metrics", views.metrics, name="metrics"),
]

