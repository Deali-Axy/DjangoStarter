from django.conf import settings
from ninja import Router
from .weapp import router as weapp_router
from .wechat import router as wechat_router
from .wecom import router as wecom_router

router = Router(tags=['oauth2'])

if settings.DJANGO_STARTER['oauth2']['weapp']['enabled']:
    router.add_router('weapp', weapp_router)

if settings.DJANGO_STARTER['oauth2']['wechat']['enabled']:
    router.add_router('wechat', wechat_router)

if settings.DJANGO_STARTER['oauth2']['wecom']['enabled']:
    router.add_router('wecom', wecom_router)
