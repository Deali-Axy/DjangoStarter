import pytest
import time
import jwt
from django.contrib.auth.models import User
from django.http import HttpRequest
from . import services
from .services import generate_token, decode, get_user
from .models import UserClaim
from .bearers import JwtBearer

@pytest.mark.django_db
class TestAuthServices:
    def test_jwt_generation_and_decode(self):
        """验证 JWT 生成与解析"""
        payload = {'username': 'testuser', 'user_id': 1}
        token_obj = generate_token(payload)
        assert token_obj.token is not None
        assert token_obj.exp > time.time()

        decoded = decode(token_obj.token)
        assert decoded is not None
        assert decoded['username'] == 'testuser'
        assert decoded['user_id'] == 1

    def test_jwt_decode_invalid(self):
        """验证无效 Token 解析"""
        assert decode("invalid.token.string") is None

    def test_user_claim_model(self):
        """验证 UserClaim 模型"""
        user = User.objects.create_user(username='testuser', password='password')
        claim = UserClaim.objects.create(user=user, name='role', value='admin')
        assert claim.value == 'admin'
        assert claim.user == user

    def test_get_user_from_authorization_header(self, django_user_model):
        user = django_user_model.objects.create_user(username='header-user', password='password')
        token_obj = generate_token({'username': user.username})

        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {token_obj.token}'
        assert get_user(request) == user

    def test_get_user_missing_or_malformed_header(self):
        request = HttpRequest()
        assert get_user(request) is None

        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Bearer'
        assert get_user(request) is None

    def test_decode_expired_token(self):
        expired_token = jwt.encode(
            payload={'exp': int(time.time()) - 1, 'username': 'expired-user'},
            key=services.salt,
            algorithm=services.algo,
            headers=services.headers,
        )
        assert decode(expired_token) is None

@pytest.mark.django_db
class TestJwtBearer:
    def test_authenticate_success(self):
        """验证 Bearer 认证成功"""
        payload = {'username': 'testuser'}
        token_obj = generate_token(payload)
        
        bearer = JwtBearer()
        # authenticate 方法接收 token 字符串
        assert bearer.authenticate(HttpRequest(), token_obj.token) is True

    def test_authenticate_fail(self):
        """验证 Bearer 认证失败"""
        bearer = JwtBearer()
        assert bearer.authenticate(HttpRequest(), "invalid.token") is False
