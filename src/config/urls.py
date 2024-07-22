from django.contrib import admin
from django.urls import path, include

# DjangoStarter 主页
from django_starter.contrib.guide import views

from config.apis import api

urlpatterns = [
    path('', views.index),
    path('api/', api.urls),
    path('demo', include('apps.demo.urls')),

    # DjangoStarter
    path('django-starter/', include('django_starter.urls')),

    # 管理后台
    path('admin/', include('django_starter.contrib.admin.urls')),  # 实现 admin 登录验证码
    path('admin/', admin.site.urls),

    # 验证码
    path('captcha/', include('captcha.urls')),
]
