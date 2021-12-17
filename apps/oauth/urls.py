from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import WechatWork

router = DefaultRouter()

router.register('wechat_work', WechatWork, basename='wechat_work')

urlpatterns = [
    path('', include(router.urls))
]
