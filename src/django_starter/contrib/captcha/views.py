from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_starter.contrib import captcha


@swagger_auto_schema(method='get', operation_summary='刷新验证码')
@permission_classes([permissions.AllowAny])
@api_view()
def refresh_captcha(request):
    captcha_item = captcha.refresh()
    return Response({
        "key": captcha_item.key,
        "image_url": captcha_item.image_url,
        "audio_url": captcha_item.audio_url,
    })
