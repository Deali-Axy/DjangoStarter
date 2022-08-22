from django.contrib import admin
from django.shortcuts import render
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ratelimit.decorators import ratelimit


# 覆盖默认的admin登录方法实现登录限流
@ratelimit(key='ip', rate='5/m', block=True)
def extend_admin_login(request, extra_context=None):
    return admin.site.login(request, extra_context)


# 扩展admin主页，美化后台
def extend_admin_home(request):
    return render(request, 'admin/extend_home.html')
