from django.urls import path
from . import views

app_name = 'demo'

urlpatterns = [
    path('', views.index, name='index'),
    path('styleguide/', views.styleguide, name='styleguide'),
    path('movies/', views.movies, name='movies'),
    path('actors/', views.actors, name='actors'),
    path('music/', views.music, name='music'),
    path('htmx/', views.htmx_test, name='htmx_test'),
    path('sse/', views.sse_demo, name='sse_demo'),
    
    # Error pages tests
    path('test-403/', views.test_403, name='test_403'),
    path('test-404/', views.test_404, name='test_404'),
    path('test-500/', views.test_500, name='test_500'),
]
