from typing import Tuple, Optional

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer
from .view_models import LoginResult


def login_by_password(request, username, password) -> LoginResult:
    """
    使用用户名、密码登录

    :param request:
    :param username:
    :param password:
    :return: 是否成功, user_data, profile_data, token
    """
    user_obj: User = authenticate(request, username=username, password=password)
    if user_obj is None:
        return LoginResult(False)
    user_data = UserSerializer(user_obj).data

    # 生成token
    token, created = Token.objects.get_or_create(user=user_obj)
    # 记录登录状态
    login(request, user_obj)

    profile_data = None
    profile_set = UserProfile.objects.filter(user=user_obj)
    if profile_set.exists():
        profile_data = UserProfileSerializer(profile_set.first()).data

    return LoginResult(True, user_data, profile_data, token.key)
