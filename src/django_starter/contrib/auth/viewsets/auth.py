import re

from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_starter.http.response import responses

from django_starter.contrib.auth.models import UserProfile
from django_starter.contrib.auth.services import login_by_password
from django_starter.contrib.auth.view_models import LoginResult


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

        result: LoginResult = login_by_password(request, username, password)

        if not result.is_successful:
            return responses.unauthorized('登录失败，用户名或密码错误')

        return responses.ok('登录成功', result.to_dict())

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
        UserProfile.objects.create(
            user=user_obj,
            name=name,
            alias=alias,
            gender=gender,
            phone=username
        )

        result: LoginResult = login_by_password(request, username, password)

        return responses.ok('注册成功！', result.to_dict())
