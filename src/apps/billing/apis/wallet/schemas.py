from __future__ import annotations

from decimal import Decimal
from typing import Any, Optional

from ninja import Schema


class WalletOut(Schema):
    """
    钱包输出。
    """

    id: int
    currency: str
    balance: Decimal


class CurrentSubscriptionOut(Schema):
    """
    当前订阅（VIP）输出。
    """

    id: int
    plan_code: str
    plan_name: str
    status: str
    current_period_end: Optional[str] = None


class BalanceOut(Schema):
    """
    余额 + 当前订阅概览。
    """

    wallet: WalletOut
    subscription: Optional[CurrentSubscriptionOut] = None

