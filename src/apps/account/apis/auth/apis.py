import re
from typing import Optional
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja.router import Router
from ninja.errors import HttpError

from django_starter.http.response import responses
from django_starter.contrib.auth.services import generate_token, get_user

from apps.account.models import UserProfile
from .schemas import LoginSchema, LoginToken, UserSchema, RegisterSchema

router = Router(tags=['auth'])


@router.post('/login', auth=None, response={200: LoginToken}, url_name='account/auth/login')
def login(request, data: LoginSchema):
    user: User = authenticate(username=data.username, password=data.password)
    if user is not None:
        return responses.ok('登录成功', generate_token({'username': user.username}).dict())
    else:
        raise HttpError(401, '用户名或密码错误')


@router.get('/current-user', response=UserSchema, url_name='account/auth/current_user')
def current_user(request):
    user = get_user(request)
    if not user:
        raise HttpError(401, '未登录或用户不存在！')

    return user


@router.post('/register', url_name='account/auth/register')
def register(request, data: RegisterSchema):
    if User.objects.filter(username=data.username).exists():
        return responses.bad_request('用户名已存在！')

    if data.phone:
        phone_pattern = '^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\\d{8}$'
        if not re.match(phone_pattern, data.phone):
            return responses.bad_request('手机号码格式不对！')

        if UserProfile.objects.filter(phone=data.phone).exists():
            return responses.bad_request('手机号已存在！')

    if data.password != data.confirm_password:
        return responses.bad_request('密码不一致！')

    user_obj: User = User.objects.create_user(data.username, None, data.password)

    if data.phone:
        user_obj.profile.phone = data.phone
    if data.full_name:
        user_obj.profile.full_name = data.full_name
    if data.gender:
        user_obj.profile.gender = data.gender

    user_obj.profile.save()

    return responses.ok('注册成功！', generate_token({'username': user_obj.username}).dict())
