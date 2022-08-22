from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import WechatViewSet, WechatWorkViewSet

router = DefaultRouter()

router.register('wechat', WechatViewSet, basename='wechat')
router.register('wechat_work', WechatWorkViewSet, basename='wechat_work')

urlpatterns = [
    path('', include(router.urls))
]
