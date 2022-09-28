from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import WechatViewSet, WechatWorkViewSet

router = DefaultRouter()

# todo 等微信公众号登录实现再加上
# router.register('wechat', WechatViewSet, basename='wechat')
router.register('wechat_work', WechatWorkViewSet, basename='wechat_work')

urlpatterns = [
    path('', include(router.urls))
]
