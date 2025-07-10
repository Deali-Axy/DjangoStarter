from django.urls import path, include
from django_starter.contrib.guide import views as guide_views

urlpatterns = [
    path('', guide_views.index),
    path('admin/', include('django_starter.contrib.admin.urls')),
]
