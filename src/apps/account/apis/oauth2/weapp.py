import requests
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings
from ninja import Router, Schema
from ninja.errors import HttpError

from django_starter.contrib.auth.models import UserClaim
from django_starter.contrib.auth.services import generate_token
from django_starter.http.response import responses

router = Router(tags=['weapp'])

appid = settings.DJANGO_STARTER['oauth2']['weapp']['appid']
secret = settings.DJANGO_STARTER['oauth2']['weapp']['secret']


class WeappLoginSchema(Schema):
    code: str


@router.post('/login', auth=None, summary='微信小程序认证')
def login(request, payload: WeappLoginSchema):
    """
    微信小程序认证

    https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
    """
    try:
        login_info: dict = requests.get('https://api.weixin.qq.com/sns/jscode2session', params={
            'appid': appid,
            'secret': secret,
            'js_code': payload.code,
            'grant_type': 'authorization_code'
        }).json()
    except Exception as e:
        raise HttpError(400, f'请求企微登录接口出错：{e}')

    if 'errcode' in login_info:
        return responses.bad_request('小程序登录失败', {
            'login_info': login_info
        })

    is_created_user = False

    openid = login_info.get('openid')
    unionid = login_info.get('unionid')
    session_key = login_info.get('session_key')

    claim_qs = UserClaim.objects.filter(name='oauth2:weapp:openid', value=openid)

    if claim_qs.exists():
        claim = claim_qs.first()
        user: User = claim.user
    else:
        is_created_user = True
        user = User.objects.create_user(username=f'weapp-{openid}')
        UserClaim.objects.create(user=user, name='oauth2:weapp:openid', value=openid)
        UserClaim.objects.create(user=user, name='oauth2:weapp:unionid', value=unionid)
        UserClaim.objects.create(user=user, name='oauth2:weapp:session_key', value=session_key)

    # 记录Django登录状态
    login(request, user)

    token = generate_token({'username': user.username})

    return responses.ok('登录成功', token)
