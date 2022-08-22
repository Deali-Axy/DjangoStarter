from django.urls import path, include

urlpatterns = [
    path('admin/', include('django_starter.contrib.admin.urls')),
    path('auth/', include('django_starter.contrib.auth.urls')),
    path('captcha/', include('django_starter.contrib.captcha.urls')),
    path('config/', include('django_starter.contrib.config.urls')),
    path('oauth/', include('django_starter.contrib.oauth.urls')),
]
