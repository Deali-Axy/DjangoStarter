import os

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

# DjangoStarter 主页
from django_starter.contrib.guide import views
from django_starter.contrib.monitoring import views as monitoring_views

from config.apis import api

urlpatterns = [
    # path('', include('django_starter.contrib.guide.urls')),
    path('', include('apps.home.urls')),
    path('about/', include('django_starter.contrib.about.urls')),
    path('health', monitoring_views.health),
    path('ready', monitoring_views.ready),
    path('metrics', monitoring_views.metrics),
    path('api/', api.urls),
    path('accounts/', include('apps.account.urls')),
    path('auth/', include('allauth.urls')) if os.environ.get('ALLAUTH_ENABLED', 'false') == 'true' else None,
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
