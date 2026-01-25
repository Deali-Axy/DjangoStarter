from decimal import Decimal

from ninja.router import Router
from ninja.errors import HttpError

from django_starter.contrib.auth.bearers import JwtBearer
from django_starter.contrib.auth.services import get_user
from django_starter.http.response.responses import ResponseGenerator

from apps.billing.models import TopUp, TopUpChannel, TopUpStatus
from apps.billing.services import create_topup
from .schemas import TopUpOut, CreateTopUpIn, AdminCreditIn


router = Router(tags=['topups'])
_resp = ResponseGenerator(router=router)


@router.get('', auth=JwtBearer(), response=list[TopUpOut], url_name='billing/topups/list')
def list_topups(request):
    user = get_user(request)
    if not user:
        raise HttpError(401, '未登录或用户不存在！')

    qs = TopUp.objects.filter(user_id=user.id).order_by('-id')[:50]
    return [
        TopUpOut(
            id=t.id,
            amount=t.amount,
            currency=t.currency,
            status=t.status,
            channel=t.channel,
            created_time=t.created_time.isoformat(),
            succeeded_time=t.succeeded_time.isoformat() if t.succeeded_time else None,
        )
        for t in qs
    ]


@router.post('', auth=JwtBearer(), response=TopUpOut, url_name='billing/topups/create')
def create_user_topup(request, payload: CreateTopUpIn):
    user = get_user(request)
    if not user:
        raise HttpError(401, '未登录或用户不存在！')

    if payload.amount <= Decimal('0'):
        raise HttpError(400, '充值金额必须大于 0')

    if payload.channel == TopUpChannel.ADMIN:
        raise HttpError(403, '不允许使用后台充值渠道创建充值单')

    if payload.channel not in {TopUpChannel.STRIPE, TopUpChannel.ALIPAY}:
        raise HttpError(400, '不支持的充值渠道')

    topup = create_topup(
        user_id=user.id,
        amount=payload.amount,
        currency=payload.currency,
        channel=payload.channel,
        status=TopUpStatus.PENDING,
        idempotency_key=payload.idempotency_key,
    )

    return TopUpOut(
        id=topup.id,
        amount=topup.amount,
        currency=topup.currency,
        status=topup.status,
        channel=topup.channel,
        created_time=topup.created_time.isoformat(),
        succeeded_time=None,
    )


@router.post('/admin-credit', auth=JwtBearer(), url_name='billing/topups/admin_credit')
def admin_credit(request, payload: AdminCreditIn):
    user = get_user(request)
    if not user:
        raise HttpError(401, '未登录或用户不存在！')
    if not user.is_staff:
        return _resp.forbidden(request, '无权限执行后台充值')

    if payload.amount <= Decimal('0'):
        return _resp.bad_request(request, '充值金额必须大于 0')

    topup = create_topup(
        user_id=payload.user_id,
        amount=payload.amount,
        currency=payload.currency,
        channel=TopUpChannel.ADMIN,
        status=TopUpStatus.SUCCEEDED,
        created_by_id=user.id,
        idempotency_key=payload.idempotency_key,
    )
    topup.mark_succeeded(
        created_by_id=user.id,
        idempotency_key=payload.idempotency_key or f'admin-api-topup:{topup.id}',
        reference='admin-api',
    )
    return _resp.ok(request, '充值成功', {'topup_id': topup.id})

