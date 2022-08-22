from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.extend_admin_home),
]
