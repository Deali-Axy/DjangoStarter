import pytest
from django.urls import reverse

class TestGuideViews:
    def test_guide_index(self, client):
        """验证向导页面渲染"""
        url = reverse('djs_guide:index')
        response = client.get(url)
        assert response.status_code == 200

    def test_enqueue_task(self, client):
        """验证任务入队接口"""
        url = reverse('djs_guide:enqueue_task')
        response = client.get(url)
        assert response.status_code == 200
        assert response.json()['queued'] is True
