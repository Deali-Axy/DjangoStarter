from __future__ import annotations

from decimal import Decimal
from typing import Optional

from ninja import Schema


class TopUpOut(Schema):
    """
    充值记录输出。
    """

    id: int
    amount: Decimal
    currency: str
    status: str
    channel: str
    created_time: str
    succeeded_time: Optional[str] = None


class CreateTopUpIn(Schema):
    """
    创建充值单（在线支付入口预留）。

    说明：当前版本只创建充值单，不会自动入账；入账需要支付回调或管理员操作。
    """

    amount: Decimal
    currency: str = 'CNY'
    channel: str
    idempotency_key: str = ''


class AdminCreditIn(Schema):
    """
    后台给用户充值（API 方式）。
    """

    user_id: int
    amount: Decimal
    currency: str = 'CNY'
    idempotency_key: str = ''

