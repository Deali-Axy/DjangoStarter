from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from django.http import HttpRequest


@dataclass(frozen=True)
class ProviderCreatePaymentResult:
    """
    创建支付会话/意图的返回值（抽象层）。

    说明：
    - provider_reference：第三方侧的支付对象 ID（如 Stripe PaymentIntent/CheckoutSession）
    - client_secret：前端拉起支付可能需要的 secret（Stripe 常见）
    - pay_url：跳转式支付可用的 URL（如 Checkout）
    """

    provider_reference: str
    client_secret: str | None = None
    pay_url: str | None = None


class PaymentProvider(Protocol):
    """
    支付网关抽象接口。

    目标：
    - 让“充值单 TopUp 的创建/入账逻辑”与具体支付渠道解耦
    - 后续接入 Stripe/支付宝时，只需要补齐 Provider 实现与 webhook/notify 处理
    """

    code: str

    def create_topup_payment(self, *, request: HttpRequest, topup_id: int) -> ProviderCreatePaymentResult:
        """
        为指定充值单创建支付对象（PaymentIntent/TradeOrder 等）。
        """

        raise NotImplementedError

    def verify_webhook(self, *, request: HttpRequest) -> bool:
        """
        验证 webhook/notify 的签名与合法性。
        """

        raise NotImplementedError

    def handle_webhook(self, *, request: HttpRequest) -> dict:
        """
        处理 webhook/notify 事件，返回结构化结果（用于日志/排障）。

        典型职责：
        - 幂等落库（TopUp 状态、外部单号）
        - 支付成功后入账（TopUp.mark_succeeded）
        - 支付失败后记录失败原因
        """

        raise NotImplementedError

