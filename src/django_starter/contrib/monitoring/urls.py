from django.urls import path

from apps.account.urls import app_name
from . import views

app_name = 'djs_monitoring'

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('metrics/', views.metrics, name='metrics'),
]
