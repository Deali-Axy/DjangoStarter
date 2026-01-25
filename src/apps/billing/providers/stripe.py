from __future__ import annotations

from django.http import HttpRequest

from .base import PaymentProvider, ProviderCreatePaymentResult


class StripeProvider(PaymentProvider):
    code = 'stripe'

    def create_topup_payment(self, *, request: HttpRequest, topup_id: int) -> ProviderCreatePaymentResult:
        raise NotImplementedError('StripeProvider 尚未接入，请先实现 PaymentIntent/Checkout 逻辑')

    def verify_webhook(self, *, request: HttpRequest) -> bool:
        raise NotImplementedError('StripeProvider 尚未接入，请先实现 webhook 签名验证')

    def handle_webhook(self, *, request: HttpRequest) -> dict:
        raise NotImplementedError('StripeProvider 尚未接入，请先实现 webhook 事件处理与入账')

