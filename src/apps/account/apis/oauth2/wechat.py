from django.conf import settings
from ninja import Router
from wechatpy.oauth import WeChatOAuth

from django_starter.http.response import responses

router = Router(tags=['wechat'])

client = WeChatOAuth(
    app_id=settings.DJANGO_STARTER['oauth2']['wechat']['app_id'],
    secret=settings.DJANGO_STARTER['oauth2']['wechat']['secret'],
    redirect_uri=settings.DJANGO_STARTER['oauth2']['wechat']['redirect_uri'],
)


@router.get('authorize-url', summary='生成登录链接')
def get_authorize_url(request):
    return responses.ok('生成登录链接', {'url': client.authorize_url})


@router.get('qrconnect-url', summary='生成扫码登录地址')
def get_qr_connect_url(request):
    return responses.ok('生成扫码登录地址', {'url': client.qrconnect_url})
