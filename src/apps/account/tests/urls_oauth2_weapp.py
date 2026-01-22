from django.urls import include, path
from ninja import NinjaAPI

from apps.account.apis.oauth2.weapp import router as weapp_router

api = NinjaAPI(urls_namespace="oauth2-weapp", version="0.0.0-test")
api.add_router("account/oauth2/weapp", weapp_router)

urlpatterns = [
    path("", include("apps.home.urls")),
    path("about/", include("django_starter.contrib.about.urls")),
    path("accounts/", include("apps.account.urls")),
    path("demo/", include("apps.demo.urls")),
    path("api/", api.urls),
]

