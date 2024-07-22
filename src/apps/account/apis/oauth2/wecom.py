from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from ninja import Router, Schema
from ninja.errors import HttpError
from wechatpy.enterprise import WeChatClient

from django_starter.contrib.auth.models import UserClaim
from django_starter.contrib.auth.services import generate_token
from django_starter.http.response import responses

router = Router(tags=['wecom'])
client = WeChatClient(
    corp_id=settings.DJANGO_STARTER['oauth2']['wecom']['corp_id'],
    secret=settings.DJANGO_STARTER['oauth2']['wecom']['secret'],
)

redirect_uri = settings.DJANGO_STARTER['oauth2']['wecom']['redirect_uri']


class WecomLoginSchema(Schema):
    code: str


@router.get('authorize-url', summary='生成登录链接')
def get_authorize_url(request):
    return responses.ok('生成登录链接', {
        'url': client.oauth.authorize_url(redirect_uri=redirect_uri)
    })


@router.post('login', summary='通过code登录')
def login(request, payload: WecomLoginSchema):
    try:
        user_info = client.oauth.get_user_info(payload.code)
    except Exception as e:
        raise HttpError(400, f'请求企微登录接口出错：{e}')

    # user_id 实际上是手机号
    user_id = user_info['UserId']
    is_created_user = False

    claim_qs = UserClaim.objects.filter(name='oauth2:wecom:userid', value=user_id)

    if claim_qs.exists():
        claim = claim_qs.first()
        user: User = claim.user
    else:
        is_created_user = True
        user = User.objects.create_user(username=f'wecom-{user_id}')
        UserClaim.objects.create(user=user, name='oauth2:wecom:userid', value=user_id)

    # 记录Django登录状态
    login(request, user)

    token = generate_token({'username': user.username})

    return responses.ok('登录成功', token)
