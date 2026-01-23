from django.urls import path, include

urlpatterns = [
    path('', include('django_starter.contrib.guide.urls')),
    path('docs/', include('django_starter.contrib.docs.urls')),
    path('notifications/', include('django_starter.contrib.notifications.urls')),
    path('admin/', include('django_starter.contrib.admin.urls')),
]
