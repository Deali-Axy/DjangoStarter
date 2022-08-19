import re

from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from utils.response import responses
from apps.parents.models import Parent
from apps.parents.serializers import ParentSerializer
from apps.user.models import UserProfile
from apps.user.serializers import UserProfileSerializer, UserSerializer
from apps.user.services import login_by_password


class AuthViewSet(viewsets.ViewSet):
    """认证相关"""

    @swagger_auto_schema(
        method='post', operation_summary='登录',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名(手机号)'),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }),
        responses={
            '201': openapi.Schema(type=openapi.TYPE_OBJECT),
            '401': openapi.Schema(type=openapi.TYPE_OBJECT),
        })
    @action(detail=False, methods=['post'])
    def login(self, request):
        """登录，使用用户名密码，返回一个token"""
        username = request.data.get('username')
        password = request.data.get('password')

        is_login, user_data, profile_data, token = login_by_password(request, username, password)
        if not is_login:
            return responses.unauthorized('登录失败，用户名或密码错误')

        return responses.ok('登录成功', {
            'user': user_data,
            'profile': profile_data,
            'token': token,
        })

    @swagger_auto_schema(
        method='post', operation_summary='注册',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名(手机号)'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='确认密码'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='姓名'),
                'alias': openapi.Schema(type=openapi.TYPE_STRING, description='别名'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='性别（male、female、unknown）'),
                'family_role': openapi.Schema(type=openapi.TYPE_STRING, description='家庭角色'),
            }
        )
    )
    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        name = request.data.get('name')
        alias = request.data.get('alias')
        gender = request.data.get('gender')
        family_role = request.data.get('family_role')

        if User.objects.filter(username=username).exists():
            return responses.bad_request('用户名/手机号已存在！')

        if password != confirm_password:
            return responses.bad_request('密码不一致！')

        phone_pattern = '^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\\d{8}$'
        if not re.match(phone_pattern, username):
            return responses.bad_request('手机号码格式不对！')

        if gender not in UserProfile.GenderChoice.values:
            return responses.bad_request('性别输入错误！')

        user_obj = User.objects.create_user(username, None, password)
        profile = UserProfile.objects.create(
            user=user_obj,
            name=name,
            alias=alias,
            gender=gender,
            phone=username
        )
        parent = Parent.objects.create(
            user=user_obj,
            family_role=family_role
        )

        _, user_data, profile_data, token = login_by_password(request, username, password)

        return responses.ok('注册成功！', {
            'user': user_data,
            'profile': profile_data,
            'parent': ParentSerializer(parent).data,
            'token': token
        })