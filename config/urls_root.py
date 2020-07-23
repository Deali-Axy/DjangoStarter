from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path(f'{settings.URL_PREFIX}', include('config.urls')),
]

# 调试模式下的静态文件服务
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
