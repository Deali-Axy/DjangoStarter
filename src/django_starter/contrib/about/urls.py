from django.urls import path
from . import views

app_name = 'djs_about'

urlpatterns = [
    path('', views.index, name='index'),
]