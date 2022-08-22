from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets
from . import views

router = DefaultRouter()
router.register('auth', viewsets.AuthViewSet, basename='auth')
router.register('profile', viewsets.UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('current/', views.get_current_user_info, name='current'),
]
