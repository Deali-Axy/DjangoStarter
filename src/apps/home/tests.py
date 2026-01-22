import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestHomeViews:
    def test_index_anonymous(self, client):
        """未登录用户访问首页应返回 200 (Landing Page)"""
        url = reverse('home:index')
        response = client.get(url)
        assert response.status_code == 200

    def test_index_authenticated(self, client, django_user_model):
        """已登录用户访问首页应直接显示 Dashboard (200)"""
        user = django_user_model.objects.create_user(username='testuser', password='password')
        client.force_login(user)
        url = reverse('home:index')
        response = client.get(url)
        assert response.status_code == 200
        assert 'home/dashboard.html' in [t.name for t in response.templates]

    def test_dashboard_anonymous(self, client):
        """未登录用户访问 /dashboard/ 应 302 重定向至登录页"""
        url = reverse('home:dashboard')
        response = client.get(url)
        assert response.status_code == 302
        # 检查重定向URL包含 login
        assert '/login' in response.url or 'login' in response.url

    def test_dashboard_authenticated(self, client, django_user_model):
        """已登录用户访问 /dashboard/ 应返回 200"""
        user = django_user_model.objects.create_user(username='testuser', password='password')
        client.force_login(user)
        url = reverse('home:dashboard')
        response = client.get(url)
        assert response.status_code == 200
