from __future__ import annotations

from typing import Any

from .models import Subscription


def _get_current_plan_data(*, user_id: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    获取用户当前套餐的 limits/features 数据。

    返回：
    - limits: dict
    - features: dict
    """

    sub = (
        Subscription.objects.filter(user_id=user_id, is_current=True)
        .select_related('plan')
        .first()
    )
    if not sub or not sub.plan:
        return {}, {}
    return sub.plan.limits or {}, sub.plan.features or {}


def has_feature(*, user_id: int, feature_key: str) -> bool:
    """
    判断用户是否拥有某项功能开关。
    """

    _limits, features = _get_current_plan_data(user_id=user_id)
    return bool(features.get(feature_key, False))


def get_limit(*, user_id: int, limit_key: str, default: int = 0) -> int:
    """
    获取用户某项配额限制。
    """

    limits, _features = _get_current_plan_data(user_id=user_id)
    val = limits.get(limit_key, default)
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

