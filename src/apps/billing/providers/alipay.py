from __future__ import annotations

from django.http import HttpRequest

from .base import PaymentProvider, ProviderCreatePaymentResult


class AlipayProvider(PaymentProvider):
    code = 'alipay'

    def create_topup_payment(self, *, request: HttpRequest, topup_id: int) -> ProviderCreatePaymentResult:
        raise NotImplementedError('AlipayProvider 尚未接入，请先实现创建交易单逻辑')

    def verify_webhook(self, *, request: HttpRequest) -> bool:
        raise NotImplementedError('AlipayProvider 尚未接入，请先实现 notify 验签')

    def handle_webhook(self, *, request: HttpRequest) -> dict:
        raise NotImplementedError('AlipayProvider 尚未接入，请先实现 notify 处理与入账')

