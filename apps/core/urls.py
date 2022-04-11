from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets
from . import views

router = DefaultRouter()
router.register('user_profile', viewsets.UserProfileViewSet, basename='user_profile')

urlpatterns = [
    path('', include(router.urls)),
    path('refresh_captcha', views.refresh_captcha),
]
