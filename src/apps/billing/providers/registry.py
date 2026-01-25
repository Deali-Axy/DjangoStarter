from __future__ import annotations

from .base import PaymentProvider
from .stripe import StripeProvider
from .alipay import AlipayProvider


_PROVIDERS: dict[str, PaymentProvider] = {
    StripeProvider.code: StripeProvider(),
    AlipayProvider.code: AlipayProvider(),
}


def get_provider(code: str) -> PaymentProvider:
    """
    获取支付网关实现。

    说明：当前为占位实现；接入真实支付时，可在此扩展更多 provider。
    """

    if code not in _PROVIDERS:
        raise ValueError(f'Unsupported provider: {code}')
    return _PROVIDERS[code]

