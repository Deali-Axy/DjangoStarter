from __future__ import annotations

from decimal import Decimal

from django.db import transaction

from .models import Wallet, Subscription, TopUp, TopUpChannel, TopUpStatus


def get_or_create_wallet(*, user_id: int, currency: str = 'CNY') -> Wallet:
    """
    获取或创建用户钱包（按币种）。

    说明：MVP 阶段默认只用 CNY；后续多币种时仍可复用此函数。
    """

    wallet, _created = Wallet.objects.get_or_create(user_id=user_id, currency=currency)
    return wallet


def get_current_subscription(*, user_id: int) -> Subscription | None:
    """
    获取用户当前订阅（VIP）。
    """

    return (
        Subscription.objects.filter(user_id=user_id, is_current=True)
        .select_related('plan')
        .first()
    )


@transaction.atomic
def create_topup(
    *,
    user_id: int,
    amount: Decimal,
    currency: str = 'CNY',
    channel: str = TopUpChannel.ADMIN,
    created_by_id: int | None = None,
    status: str = TopUpStatus.CREATED,
    idempotency_key: str = '',
    provider_trade_no: str = '',
    provider_intent_id: str = '',
) -> TopUp:
    """
    创建充值单。

    常见用法：
    - 后台充值：channel=ADMIN, status=SUCCEEDED，然后调用 topup.mark_succeeded() 入账
    - 在线支付：channel=STRIPE/ALIPAY, status=PENDING，等待 webhook/notify 再入账
    """

    wallet = get_or_create_wallet(user_id=user_id, currency=currency)
    topup = TopUp.objects.create(
        user_id=user_id,
        wallet=wallet,
        amount=amount,
        currency=currency,
        status=status,
        channel=channel,
        created_by_id=created_by_id,
        idempotency_key=idempotency_key,
        provider_trade_no=provider_trade_no,
        provider_intent_id=provider_intent_id,
    )
    return topup

