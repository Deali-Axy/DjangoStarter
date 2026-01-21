from django.urls import path, include
from . import views

app_name = 'djs_guide'

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/guide-visit/', views.enqueue_task, name='enqueue_task'),
]
