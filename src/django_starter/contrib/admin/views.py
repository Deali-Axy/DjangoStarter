from django.contrib import admin
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit


# 覆盖默认的admin登录方法实现登录限流
# 使用 django_ratelimit 组件实现请求限流，限制只能一分钟10次
# 详情参考文档: https://django-ratelimit.readthedocs.io/en/stable/usage.html
@ratelimit(key='user_or_ip', rate='10/m')
def extend_admin_login(request, extra_context=None):
    return admin.site.login(request, extra_context)


# 扩展admin主页，美化后台
def extend_admin_home(request):
    return render(request, 'django_starter/admin/extend_home.html')
