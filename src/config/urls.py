import os

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from config.apis import api

monitoring_root_enabled = os.environ.get("MONITORING_ROOT_ENDPOINTS_ENABLED", "true") == "true"

urlpatterns = [
    # path('', include('django_starter.contrib.guide.urls')),
    path('', include('apps.home.urls')),
    path('api/', api.urls),
    path('about/', include('django_starter.contrib.about.urls')),
    path('accounts/', include('apps.account.urls')),
    path('auth/', include('allauth.urls')) if os.environ.get('ALLAUTH_ENABLED', 'false') == 'true' else None,
    path('monitoring/', include('django_starter.contrib.monitoring.urls')),
    path('demo/', include('apps.demo.urls')),

    # DjangoStarter
    path('django-starter/', include('django_starter.urls')),

    # 管理后台
    path('admin/', include('django_starter.contrib.admin.urls')),  # 实现 admin 登录验证码
    path('admin/', admin.site.urls),

    # 验证码
    path('captcha/', include('captcha.urls')),
    
    # 国际化语言切换
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns = [p for p in urlpatterns if p is not None]
