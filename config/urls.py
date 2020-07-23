from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views as authtoken_view

# drf_yasg文档工具
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.core import views


urlpatterns = [
    path(f'core/', include('apps.core.urls')),

    # 管理后台
    path(f'admin/login/', views.extend_admin_login),
    path(f'admin/', admin.site.urls),

    # 验证码
    path(f'captcha/', include('captcha.urls')),

    # API认证
    path(f'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(f'api-token-auth/', authtoken_view.obtain_auth_token),
]


# 接口文档 仅调试模式可用
if settings.DEBUG:
    openapi_obj = openapi.Info(
        title="项目名称",
        default_version='v1',
        description="说明",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="feedback@deali.cn"),
        license=openapi.License(name="BSD License"),
    )
    schema_view = get_schema_view(
        openapi_obj,
        public=True,
        permission_classes=(permissions.IsAdminUser,),
    )
    urlpatterns.extend([
        # AutoScheme接口文档
        path(f'api-docs/auto/', include_docs_urls(title=openapi_obj.title)),
        # Swagger文档
        path(f'api-docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
        path(f'api-docs/swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        # redoc文档
        path(f'api-docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0))
    ])
