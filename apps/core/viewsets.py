from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework import permissions
from . import models
from . import serializers


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有用户资料', operation_id='获取所有用户资料',operation_description='获取所有用户资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定用户资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加用户资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定用户资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定用户资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定用户资料'))
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
