from django.contrib import admin
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ratelimit.decorators import ratelimit


# 覆盖默认的admin登录方法实现登录限流
@ratelimit(key='ip', rate='5/m', block=True)
def extend_admin_login(request, extra_context=None):
    return admin.site.login(request, extra_context)


@swagger_auto_schema(method='get', operation_summary='刷新验证码')
@permission_classes([permissions.AllowAny])
@api_view()
def refresh_captcha(request):
    from contrib import captcha
    captcha_item = captcha.refresh()
    return Response({
        "key": captcha_item.key,
        "image_url": captcha_item.image_url,
        "audio_url": captcha_item.audio_url,
    })
