from django.urls import path
from . import views

app_name = 'djs_about'

urlpatterns = [
    path('', views.index, name='index'),
    path('partials/milestones', views.partials_milestones, name='partials_milestones'),
    path('partials/team', views.partials_team, name='partials_team'),
    path('partials/faq', views.partials_faq, name='partials_faq'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
]
