from django.urls import path, include

from . import views

urlpatterns = [
    path('refresh_captcha', views.refresh_captcha),
    path('admin_home', views.extend_admin_home),
]
