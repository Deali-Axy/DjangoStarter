from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path(f'{settings.URL_PREFIX}', include('config.urls')),
]
