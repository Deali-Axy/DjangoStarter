from django.urls import include, path
from ninja import NinjaAPI

api = NinjaAPI(urls_namespace="oauth2-disabled", version="0.0.0-test")

urlpatterns = [
    path("", include("apps.home.urls")),
    path("about/", include("django_starter.contrib.about.urls")),
    path("accounts/", include("apps.account.urls")),
    path("demo/", include("apps.demo.urls")),
    path("api/", api.urls),
]

