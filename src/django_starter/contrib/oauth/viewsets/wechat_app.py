import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django_starter.contrib.auth.models import UserProfile
from django_starter.contrib.oauth.models import OAuthClaim
from django_starter.http.response import responses


class WechatAppViewSet(viewsets.ViewSet):
    """
    微信小程序认证服务

    https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
    """

    appid = settings.DJANGO_STARTER['oauth']['wechat_app_config']['appid']
    secret = settings.DJANGO_STARTER['oauth']['wechat_work_config']['secret']

    @swagger_auto_schema(
        operation_summary='微信小程序 - 通过code登录',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='从微信企业号服务器获取到的code'
                ),
            }
        )
    )
    @action(methods=['post'], detail=False)
    def login_by_code(self, request: Request):
        code = request.data.get('code', None)

        if not code:
            return responses.bad_request('没有code')

        try:
            login_info: dict = requests.get('https://api.weixin.qq.com/sns/jscode2session', params={
                'appid': self.appid,
                'secret': self.secret,
                'js_code': code,
                'grant_type': 'authorization_code'
            }).json()
        except Exception as e:
            raise APIException(detail=e)

        openid = login_info.get('openid')

        if 'errcode' in login_info or not openid:
            return responses.bad_request('小程序登录失败', {
                'login_info': login_info
            })

        is_created_user = False

        if OAuthClaim.objects.filter(name='wechat_openid', value=openid).exists():
            claim = OAuthClaim.objects.get(name='wechat_openid', value=openid)
            user_obj = claim.user
        else:
            is_created_user = True
            user_obj: User = User.objects.create_user(username=openid)
            OAuthClaim.objects.create(user=user_obj, name='wechat_openid', value=openid)

        if UserProfile.objects.filter(user=user_obj).exists():
            profile: UserProfile = UserProfile.objects.get(user=user_obj)
        else:
            profile: UserProfile = UserProfile.objects.create(user=user_obj)

        # 记录Django登录状态
        login(request, user_obj)
        # 生成drf token
        token, created = Token.objects.get_or_create(user=user_obj)

        return Response({
            'successful': True,
            'is_created_user': is_created_user,
            'token': token.key,
            'detail': '登录成功',
            'login_info': login_info
        })
