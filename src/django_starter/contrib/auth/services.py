import logging
import uuid
from typing import Optional
import jwt
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from apps.account.apis.auth.schemas import LoginToken

logger = logging.getLogger('common')

# 算法
algo = settings.DJANGO_STARTER['auth']['jwt']['algo']
# 随机的salt密钥，只有token生成者（同时也是校验者）自己能有，用于校验生成的token是否合法
salt = settings.DJANGO_STARTER['auth']['jwt']['salt']
# token 有效时间 （单位：秒）
TOKEN_LIFETIME = settings.DJANGO_STARTER['auth']['jwt']['lifetime']

# 设置headers，即加密算法的配置
headers = {
    "alg": algo,
    "typ": "JWT"
}


def generate_token(payload: dict) -> LoginToken:
    """
    生成 jwt token

    参考： https://www.jianshu.com/p/03ad32c1586c

    :param payload:
    :return:
    """
    exp = int(timezone.now().timestamp() + TOKEN_LIFETIME)
    # 配置主体信息，一般是登录成功的用户之类的，因为jwt的主体信息很容易被解码，所以不要放敏感信息
    # 当然也可以将敏感信息加密后再放进payload
    token = jwt.encode(payload={
        'exp': exp,
        'iss': 'DjangoStarter-Sales',
        'sub': 'antd-admin',
        # jwt的签发时间
        'iat': timezone.now().timestamp(),
        # jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。
        'jti': uuid.uuid4().hex,
        **payload
    }, key=salt, algorithm=algo, headers=headers)

    return LoginToken(token=token, exp=exp)


def decode(token: str) -> Optional[dict]:
    """
    从 JWT 中获取 payload

    :param token:
    :return: 返回payload信息，如果验证失败返回 None
    """

    try:
        # 第三个参数代表是否校验，如果设置为False，那么只要有token，就能够对其进行解码
        info = jwt.decode(token, salt, verify=True, algorithms=algo)
        return info
    except jwt.ExpiredSignatureError as e:
        logger.error(e)
        return None


def get_user(request: HttpRequest) -> Optional[User]:
    """
    从 `HttpRequest` 的 `Authorization` header 中获取 `JWT`, 查询数据库获取用户

    :param request:
    :return: 如果没有 `Authorization` header 或者 JWT 失效，返回 None
    """

    auth_header: str = request.headers.get('Authorization', '')
    if len(auth_header.split(' ')) <= 1:
        return None

    token = auth_header.split(' ')[1]
    payload = decode(token)

    if not payload:
        return None

    user_qs = User.objects.filter(username=payload.get('username', ''))

    return user_qs.first()
