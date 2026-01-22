import sys
import types

from django.urls import include, path
from ninja import NinjaAPI


def _ensure_wechatpy_oauth_stub():
    if "wechatpy.oauth" in sys.modules:
        return

    wechatpy_module = sys.modules.get("wechatpy")
    if wechatpy_module is None:
        wechatpy_module = types.ModuleType("wechatpy")
        sys.modules["wechatpy"] = wechatpy_module

    oauth_module = types.ModuleType("wechatpy.oauth")

    class WeChatOAuth:
        def __init__(self, app_id: str, secret: str, redirect_uri: str):
            self.app_id = app_id
            self.secret = secret
            self.redirect_uri = redirect_uri
            self.authorize_url = f"https://example.com/wechat/authorize?redirect_uri={redirect_uri}"
            self.qrconnect_url = f"https://example.com/wechat/qrconnect?redirect_uri={redirect_uri}"

    oauth_module.WeChatOAuth = WeChatOAuth
    sys.modules["wechatpy.oauth"] = oauth_module


_ensure_wechatpy_oauth_stub()

import importlib  # noqa: E402

import apps.account.apis.oauth2.wechat as wechat_mod  # noqa: E402

importlib.reload(wechat_mod)
wechat_router = wechat_mod.router

api = NinjaAPI(urls_namespace="oauth2-wechat", version="0.0.0-test")
api.add_router("account/oauth2/wechat", wechat_router)

urlpatterns = [
    path("", include("apps.home.urls")),
    path("about/", include("django_starter.contrib.about.urls")),
    path("accounts/", include("apps.account.urls")),
    path("demo/", include("apps.demo.urls")),
    path("api/", api.urls),
]

