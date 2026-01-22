import sys
import types

from django.urls import include, path
from ninja import NinjaAPI


def _ensure_wechatpy_enterprise_stub():
    wechatpy_module = sys.modules.get("wechatpy")
    if wechatpy_module is None:
        wechatpy_module = types.ModuleType("wechatpy")
        sys.modules["wechatpy"] = wechatpy_module

    enterprise_module = types.ModuleType("wechatpy.enterprise")

    class _StubOAuth:
        def authorize_url(self, redirect_uri: str):
            return f"https://example.com/authorize?redirect_uri={redirect_uri}"

        def get_user_info(self, code: str):
            return {"UserId": code}

    class WeChatClient:
        def __init__(self, corp_id: str, secret: str):
            self.corp_id = corp_id
            self.secret = secret
            self.oauth = _StubOAuth()

    enterprise_module.WeChatClient = WeChatClient
    sys.modules["wechatpy.enterprise"] = enterprise_module


_ensure_wechatpy_enterprise_stub()

import importlib  # noqa: E402

import apps.account.apis.oauth2.wecom as wecom_mod  # noqa: E402

importlib.reload(wecom_mod)
wecom_router = wecom_mod.router

api = NinjaAPI(urls_namespace="oauth2-wecom", version="0.0.0-test")
api.add_router("account/oauth2/wecom", wecom_router)

urlpatterns = [
    path("", include("apps.home.urls")),
    path("about/", include("django_starter.contrib.about.urls")),
    path("accounts/", include("apps.account.urls")),
    path("demo/", include("apps.demo.urls")),
    path("api/", api.urls),
]

