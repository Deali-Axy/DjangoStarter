from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register('user_profile', viewsets.UserProfileViewSet, basename='user_profile')

urlpatterns = [
    path('', include(router.urls))
]
