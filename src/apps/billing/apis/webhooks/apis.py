from ninja.router import Router

from django_starter.http.response.responses import ResponseGenerator

from apps.billing.providers.registry import get_provider


router = Router(tags=['webhooks'])
_resp = ResponseGenerator(router=router)


@router.post('/stripe', auth=None, url_name='billing/webhooks/stripe')
def stripe_webhook(request):
    provider = get_provider('stripe')
    return _resp.error(request, 'Stripe Webhook 尚未接入', {'provider': provider.code})


@router.post('/alipay', auth=None, url_name='billing/webhooks/alipay')
def alipay_webhook(request):
    provider = get_provider('alipay')
    return _resp.error(request, '支付宝 Notify 尚未接入', {'provider': provider.code})

