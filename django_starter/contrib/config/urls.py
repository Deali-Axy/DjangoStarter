from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import *

router = DefaultRouter()

router.register('common_config', CommonConfigViewSet, basename='common_config')

urlpatterns = [
    path('', include(router.urls))
]
