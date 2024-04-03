from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有通用配置资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定通用配置资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加通用配置资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定通用配置资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定通用配置资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定通用配置资料'))
class CommonConfigViewSet(viewsets.ModelViewSet):
    """通用配置相关操作"""
    serializer_class = CommonConfigSerializer
    queryset = ConfigItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['key']

    @swagger_auto_schema(operation_summary='获取配置字典')
    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def to_dict(self, request):
        data = {}
        for item in ConfigItem.objects.all():
            data[item.key] = item.value

        return Response(data)
