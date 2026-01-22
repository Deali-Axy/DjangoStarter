import json
import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthApiTestCase(TestCase):
    """
    账号体系的 Ninja Auth API 测试：
    - /api/account/auth/login
    - /api/account/auth/register
    - /api/account/auth/current-user

    说明：
    - 这里使用 Django 自带的 TestCase + test client，不依赖额外测试库。
    - 请求体使用 JSON 字符串，避免因 content_type=application/json 但 body 非 JSON 造成的 422。
    """

    def setUp(self):
        self.user: User = User.objects.create_user(username="test", email="test@example.com", password="test")
        self.user.profile.phone = "13812341234"
        self.user.profile.save()

    def _post_json(self, url_name: str, payload: dict):
        return self.client.post(
            reverse(url_name),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def _get_json(self, url_name: str, headers: dict | None = None):
        extra: dict = {}
        for key, value in (headers or {}).items():
            if key.lower() == "authorization":
                extra["HTTP_AUTHORIZATION"] = value
            else:
                extra[key] = value
        return self.client.get(reverse(url_name), **extra)

    def test_auth_login_success(self):
        resp = self._post_json("api:account/auth/login", {"username": "test", "password": "test"})
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("data", body)
        self.assertIn("token", body["data"])
        self.assertIn("exp", body["data"])

    def test_auth_login_failed(self):
        resp = self._post_json(
            "api:account/auth/login",
            {"username": uuid.uuid4().hex, "password": uuid.uuid4().hex},
        )
        self.assertEqual(resp.status_code, 401)

    def test_auth_register_success(self):
        username = uuid.uuid4().hex
        password = uuid.uuid4().hex
        email = f"{uuid.uuid4().hex}@example.com"

        resp = self._post_json(
            "api:account/auth/register",
            {
                "email": email,
                "username": username,
                "password": password,
                "confirm_password": password,
            },
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("data", body)
        self.assertIn("token", body["data"])

        self.assertTrue(User.objects.filter(username=username, email=email).exists())

    def test_auth_register_failed_cases(self):
        # 1) 注册已存在用户名
        resp = self._post_json(
            "api:account/auth/register",
            {
                "email": "another@example.com",
                "username": "test",
                "password": "test",
                "confirm_password": "test",
            },
        )
        self.assertEqual(resp.status_code, 400)

        # 2) 注册已存在邮箱
        resp = self._post_json(
            "api:account/auth/register",
            {
                "email": "test@example.com",
                "username": uuid.uuid4().hex,
                "password": "test",
                "confirm_password": "test",
            },
        )
        self.assertEqual(resp.status_code, 400)

        # 3) 密码不一致
        username = uuid.uuid4().hex
        resp = self._post_json(
            "api:account/auth/register",
            {
                "email": f"{uuid.uuid4().hex}@example.com",
                "username": username,
                "password": "abcd1234",
                "confirm_password": "another-password",
            },
        )
        self.assertEqual(resp.status_code, 400)

        # 4) 手机号格式错误
        resp = self._post_json(
            "api:account/auth/register",
            {
                "email": f"{uuid.uuid4().hex}@example.com",
                "username": uuid.uuid4().hex,
                "password": "abcd1234",
                "confirm_password": "abcd1234",
                "phone": "1234",
            },
        )
        self.assertEqual(resp.status_code, 400)

        # 5) 注册已存在手机号的用户
        resp = self._post_json(
            "api:account/auth/register",
            {
                "email": f"{uuid.uuid4().hex}@example.com",
                "username": uuid.uuid4().hex,
                "password": "abcd1234",
                "confirm_password": "abcd1234",
                "phone": "13812341234",
            },
        )
        self.assertEqual(resp.status_code, 400)

    def test_auth_get_current_user_success(self):
        login_resp = self._post_json("api:account/auth/login", {"username": "test", "password": "test"})
        token = login_resp.json()["data"]["token"]

        resp = self.client.get(
            "/api/account/auth/current-user",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.json().get("data", {}).get("username"), "test", resp.json())

    def test_auth_get_current_user_unauthorized(self):
        # 1) 缺少 Authorization 头
        resp = self.client.get("/api/account/auth/current-user")
        self.assertIn(resp.status_code, (401, 403))

        # 2) 无效 token
        resp = self.client.get(
            "/api/account/auth/current-user",
            HTTP_AUTHORIZATION="Bearer not-a-jwt",
        )
        self.assertIn(resp.status_code, (401, 403))

