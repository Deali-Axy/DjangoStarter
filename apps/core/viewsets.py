from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from . import serializers


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有用户资料', operation_id='获取所有用户资料', operation_description='获取所有用户资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定用户资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加用户资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定用户资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定用户资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定用户资料'))
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名(或手机号)'),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }),
        responses={
            '201': openapi.Schema(type=openapi.TYPE_OBJECT)
        },
        operation_summary='登录或注册')
    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def sign_up(self, request):
        """登录或注册功能, 如果用户名和密码存在则登录, 反之则创建新用户, 两种操作都会返回一个token"""
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            user_obj: User = User.objects.get(username=username)
        else:
            user_obj: User = User.objects.create_user(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user_obj)
        return Response({'token': token.key})
