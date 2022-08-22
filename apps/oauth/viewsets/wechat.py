from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi
from wechatpy.oauth import WeChatOAuth


# todo 等他公众号申请完再接入
class WechatViewSet(viewsets.ViewSet):
    """微信认证服务"""
    oauth = WeChatOAuth('app_id', 'secret', 'redirect_url')

    @swagger_auto_schema(operation_summary='微信 - 生成登录链接')
    @action(detail=False)
    def get_authorize_url(self, request):
        return Response({'url': self.oauth.authorize_url()})

    @swagger_auto_schema(operation_summary='微信 - 生成扫码登录地址')
    @action(detail=False)
    def get_qr_connect_url(self, request):
        return Response({'url': self.oauth.qrconnect_url})
