from django.urls import path, include
from django_starter.contrib.guide import views as guide_views
from . import views

urlpatterns = [
    path('', guide_views.index),
    path('admin/', include('django_starter.contrib.admin.urls')),
    path('health/', views.health_check, name='health_check'),
    path('metrics/', views.metrics, name='metrics'),
]
