import re
from typing import Optional
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja.router import Router
from ninja.errors import HttpError
from .services import get_token, get_user
from .schemas import LoginSchema, LoginToken, UserSchema, RegisterSchema
from ...http.response import responses

router = Router(tags=['auth'])


@router.post('/login', auth=None, response={200: LoginToken}, operation_id='login')
def login(request, data: LoginSchema):
    user: User = authenticate(username=data.username, password=data.password)
    if user is not None:
        return responses.ok('登录成功', get_token({'username': user.username}))
    else:
        raise HttpError(401, '用户名或密码错误')


@router.get('/current-user', response=UserSchema, operation_id='current_user')
def current_user(request):
    user = get_user(request)
    if not user:
        raise HttpError(401, '未登录或用户不存在！')

    return user


@router.post('/register')
def register(request, data: RegisterSchema):
    if User.objects.filter(username=data.username).exists():
        return responses.bad_request('用户名/手机号已存在！')

    if data.password != data.confirm_password:
        return responses.bad_request('密码不一致！')

    phone_pattern = '^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\\d{8}$'
    if not re.match(phone_pattern, data.phone):
        return responses.bad_request('手机号码格式不对！')

    user_obj = User.objects.create_user(data.username, None, data.password)

    return responses.ok('注册成功！', get_token({'username': user_obj.username}))
