from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.extend_admin_login),
    path('extend_home/', views.extend_admin_home),
]
