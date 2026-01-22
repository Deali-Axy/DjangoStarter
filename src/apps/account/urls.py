from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('2fa/setup/', views.two_factor_setup, name='2fa-setup'),
    path('2fa/verify/', views.two_factor_verify, name='2fa-verify'),
    path('2fa/disable/', views.two_factor_disable, name='2fa-disable'),
    path(
        'password/forgot/',
        auth_views.PasswordResetView.as_view(
            template_name='account/password/forgot.html',
            email_template_name='account/password/reset_email.txt',
            subject_template_name='account/password/reset_subject.txt',
            success_url=reverse_lazy('account:password-reset-done'),
        ),
        name='password-forgot',
    ),
    path(
        'password/forgot/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/password/reset_sent.html',
        ),
        name='password-reset-done',
    ),
    path(
        'password/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/password/reset_confirm.html',
            success_url=reverse_lazy('account:password-reset-complete'),
        ),
        name='password-reset-confirm',
    ),
    path(
        'password/reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='account/password/reset_complete.html',
        ),
        name='password-reset-complete',
    ),
    path('charge/', views.charge, name='charge'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('settings/developer/', views.settings_developer, name='settings-developer'),
    path('settings/developer/token/', views.settings_developer_token, name='settings-developer-token'),
    path('profile/', views.profile, name='profile'),
    path('login/sso/', views.login_sso, name='login-sso'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
