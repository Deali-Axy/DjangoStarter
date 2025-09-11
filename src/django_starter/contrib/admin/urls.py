from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.extend_admin_login),
]
