from django.urls import path, include
from django_starter.contrib.guide import views

urlpatterns = [
    path('', views.index),
    path('admin/', include('django_starter.contrib.admin.urls')),
]
