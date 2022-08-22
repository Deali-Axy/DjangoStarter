from django.urls import path, include

from . import views

urlpatterns = [
    path('refresh', views.refresh_captcha),
]
