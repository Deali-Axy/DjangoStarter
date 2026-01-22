import json
from copy import deepcopy
from unittest import mock

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from django_starter.contrib.auth.models import UserClaim


def _oauth2_settings(**overrides):
    """
    生成带 oauth2 配置的 DJANGO_STARTER settings 副本，便于 override_settings 使用。
    overrides 采用 dict 结构，按层级 merge 到 DJANGO_STARTER['oauth2']。
    """

    cfg = deepcopy(settings.DJANGO_STARTER)
    oauth2 = cfg.get("oauth2", {})
    for provider, values in overrides.items():
        oauth2.setdefault(provider, {}).update(values)
    cfg["oauth2"] = oauth2
    return cfg


class OAuth2ApiTestCase(TestCase):
    """
    OAuth2 Ninja API 测试：
    - weapp: /api/account/oauth2/weapp/login
    - wecom: /api/account/oauth2/wecom/authorize-url, /login
    - wechat: /api/account/oauth2/wechat/authorize-url, /qrconnect-url

    说明：
    - 由于 oauth2 路由在 import 时按 settings 开关决定是否挂载，这里通过 override_settings(ROOT_URLCONF=...)
      指向测试专用 URLConf，并在其中 reload 相关模块来确保开关生效。
    - 所有外部 HTTP/SDK 调用均通过 mock/stub 方式隔离。
    """

    @override_settings(
        ROOT_URLCONF="apps.account.tests.urls_oauth2_disabled",
        DJANGO_STARTER=_oauth2_settings(
            weapp={"enabled": False},
            wecom={"enabled": False},
            wechat={"enabled": False},
        ),
    )
    def test_oauth2_routes_disabled_returns_404(self):
        resp = self.client.post(
            "/api/account/oauth2/weapp/login",
            data=json.dumps({"code": "x"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 404)

    @override_settings(
        ROOT_URLCONF="apps.account.tests.urls_oauth2_weapp",
        DJANGO_STARTER=_oauth2_settings(
            weapp={"enabled": True, "appid": "app", "secret": "sec"},
            wecom={"enabled": False},
            wechat={"enabled": False},
        ),
    )
    def test_weapp_login_creates_user_claim_and_logs_in(self):
        class _Resp:
            def __init__(self, payload):
                self._payload = payload

            def json(self):
                return self._payload

        payload = {"openid": "openid-1", "unionid": "union-1", "session_key": "sk-1"}

        with mock.patch("apps.account.apis.oauth2.weapp.requests.get", return_value=_Resp(payload)):
            resp = self.client.post(
                "/api/account/oauth2/weapp/login",
                data=json.dumps({"code": "code-1"}),
                content_type="application/json",
            )

        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("token", body)
        self.assertIn("exp", body)

        self.assertTrue("_auth_user_id" in self.client.session)
        self.assertTrue(UserClaim.objects.filter(name="oauth2:weapp:openid", value="openid-1").exists())

        user_count = User.objects.count()

        with mock.patch("apps.account.apis.oauth2.weapp.requests.get", return_value=_Resp(payload)):
            resp = self.client.post(
                "/api/account/oauth2/weapp/login",
                data=json.dumps({"code": "code-1"}),
                content_type="application/json",
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.count(), user_count)

    @override_settings(
        ROOT_URLCONF="apps.account.tests.urls_oauth2_wecom",
        DJANGO_STARTER=_oauth2_settings(
            weapp={"enabled": False},
            wecom={"enabled": True, "corp_id": "cid", "secret": "sec", "redirect_uri": "https://example.com/cb"},
            wechat={"enabled": False},
        ),
    )
    def test_wecom_authorize_and_login(self):
        resp = self.client.get("/api/account/oauth2/wecom/authorize-url")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertIn("url", resp.json())

        resp = self.client.post(
            "/api/account/oauth2/wecom/login",
            data=json.dumps({"code": "u001"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertTrue("_auth_user_id" in self.client.session)
        self.assertTrue(UserClaim.objects.filter(name="oauth2:wecom:userid", value="u001").exists())

    @override_settings(
        ROOT_URLCONF="apps.account.tests.urls_oauth2_wechat",
        DJANGO_STARTER=_oauth2_settings(
            weapp={"enabled": False},
            wecom={"enabled": False},
            wechat={"enabled": True, "app_id": "aid", "secret": "sec", "redirect_uri": "https://example.com/cb"},
        ),
    )
    def test_wechat_authorize_urls(self):
        resp = self.client.get("/api/account/oauth2/wechat/authorize-url")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("url", resp.json())

        resp = self.client.get("/api/account/oauth2/wechat/qrconnect-url")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("url", resp.json())

