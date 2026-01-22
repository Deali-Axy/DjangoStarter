import pytest
from unittest.mock import patch

@pytest.mark.django_db
class TestMonitoringAPIs:
    def test_health_sync_ok(self, client):
        """系统正常时返回 200 (Sync)"""
        with patch('django_starter.contrib.monitoring.apis.get_uptime', return_value=123), \
             patch('django_starter.contrib.monitoring.apis.check_db_sync', return_value=True), \
             patch('django_starter.contrib.monitoring.apis.check_redis_sync', return_value=True):
            response = client.get('/api/django-starter/monitoring/health/sync')
            assert response.status_code == 200
            data = response.json()['data']

            assert data['status'] == 'healthy'
            assert data['status_code'] == 200
            assert data['checks']['database'] == 'ok'
            assert data['checks']['redis'] == 'ok'
            assert data['system']['uptime'] == 123

    def test_health_db_down(self, client):
        """模拟数据库连接失败"""
        with patch('django_starter.contrib.monitoring.apis.get_uptime', return_value=123), \
             patch('django_starter.contrib.monitoring.apis.check_db_sync', return_value=False), \
             patch('django_starter.contrib.monitoring.apis.check_redis_sync', return_value=True):
            response = client.get('/api/django-starter/monitoring/health/sync')
            assert response.status_code == 200
            data = response.json()['data']
            assert data['status'] == 'unhealthy'
            assert data['status_code'] == 503
            assert data['checks']['database'] == 'error'

    @pytest.mark.asyncio
    async def test_health_async(self, async_client):
        """验证异步健康检查接口"""
        # 异步测试中，需要 mock check_db_async 和 check_redis_async 避免真实的 IO 失败 (如无 Redis)
        with patch('django_starter.contrib.monitoring.apis.check_db_async', return_value=True), \
             patch('django_starter.contrib.monitoring.apis.check_redis_async', return_value=True):
            
            response = await async_client.get('/api/django-starter/monitoring/health/async')
            assert response.status_code == 200
            data = response.json()['data']
            assert data['status'] == 'healthy'
            assert data['checks']['database'] == 'ok'
