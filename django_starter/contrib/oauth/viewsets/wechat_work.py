from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from wechatpy.enterprise import WeChatClient


class WechatWorkViewSet(viewsets.ViewSet):
    """微信企业号相关认证服务"""
    client = WeChatClient(
        settings.DJANGO_STARTER['oauth']['wechat_work_config']['corp_id'],
        settings.DJANGO_STARTER['oauth']['wechat_work_config']['secret'],
    )

    @swagger_auto_schema(operation_summary='企业微信 - 生成登录链接')
    @action(detail=False)
    def get_authorize_url(self, request):
        return Response({
            'url': self.client.oauth.authorize_url('/oauth/wechat_work/login_callback')
        })

    @swagger_auto_schema(operation_summary='企业微信 - 登录回调')
    @action(detail=False)
    def authorize_redirect_uri(self, request: HttpRequest):
        code = request.GET.get('code', None)
        print(f'wechat code={code}')
        return Response({'code': code})

    @swagger_auto_schema(operation_summary='企业微信 - 通过code登录',
                         manual_parameters=[
                             openapi.Parameter(name='code', in_=openapi.IN_QUERY,
                                               description='从微信企业号服务器获取到的code', type=openapi.TYPE_STRING)
                         ])
    @action(detail=False)
    def login_by_code(self, request: HttpRequest):
        code = request.GET.get('code', None)
        try:
            user_info = self.client.oauth.get_user_info(code)
        except Exception as e:
            raise APIException(detail=e)

        phone = user_info['UserId']
        is_created_user = False

        if User.objects.filter(username=phone).exists():
            user_obj: User = User.objects.get(username=phone)
        else:
            is_created_user = True
            user_obj: User = User.objects.create_user(username=phone, password=phone)

        # 记录Django登录状态
        login(request, user_obj)
        # 生成drf token
        token, created = Token.objects.get_or_create(user=user_obj)

        return Response({
            'user_info': user_info,
            'successful': True,
            'is_created_user': is_created_user,
            'token': token.key,
            'detail': '登录成功',
        })
