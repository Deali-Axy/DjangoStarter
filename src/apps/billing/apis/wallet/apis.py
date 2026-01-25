from ninja.router import Router
from ninja.errors import HttpError

from django_starter.contrib.auth.bearers import JwtBearer
from django_starter.contrib.auth.services import get_user

from apps.billing.services import get_or_create_wallet, get_current_subscription
from .schemas import BalanceOut, WalletOut, CurrentSubscriptionOut


router = Router(tags=['wallet'])


@router.get('/balance', auth=JwtBearer(), response=BalanceOut, url_name='billing/wallet/balance')
def balance(request):
    user = get_user(request)
    if not user:
        raise HttpError(401, '未登录或用户不存在！')

    wallet = get_or_create_wallet(user_id=user.id, currency='CNY')
    subscription = get_current_subscription(user_id=user.id)

    subscription_out = None
    if subscription:
        subscription_out = CurrentSubscriptionOut(
            id=subscription.id,
            plan_code=subscription.plan.code,
            plan_name=subscription.plan.name,
            status=subscription.status,
            current_period_end=subscription.current_period_end.isoformat() if subscription.current_period_end else None,
        )

    return BalanceOut(
        wallet=WalletOut(id=wallet.id, currency=wallet.currency, balance=wallet.balance),
        subscription=subscription_out,
    )

