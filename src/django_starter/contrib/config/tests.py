from django.test import TestCase
from .models import ConfigItem
from . import services


# Create your tests here.
class ConfigItemTestCase(TestCase):
    def setUp(self):
        for i in range(1, 5):
            ConfigItem.objects.create(display_name=f'Test{i}', key=f'test{i}', value=f'value{i}')

        for i in range(1, 5):
            services.set_str(f'str{i}', f'str-value-{i}')

        for i in range(1, 5):
            services.set_int(f'int{i}', i)

        for i in range(1, 5):
            services.set_json(f'json{i}', {'value': f'value{i}'})

    def test_config_item(self):
        for i in range(1, 5):
            config = ConfigItem.objects.get(key=f'test{i}')
            self.assertEqual(config.display_name, f'Test{i}')

    def test_config_str(self):
        for i in range(1, 5):
            value = services.get_str(f'str{i}')
            self.assertEqual(value, f'str-value-{i}')

    def test_config_int(self):
        for i in range(1, 5):
            value = services.get_int(f'int{i}')
            self.assertEqual(value, i)

    def test_config_json(self):
        for i in range(1, 5):
            value = services.get_json(f'json{i}')
            self.assertEqual(value, {'value': f'value{i}'})

    def test_api_get_config_list(self):
        resp = self.client.get('/api/django-starter/config/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']), 16)

    def test_api_get_config_dict(self):
        resp = self.client.get('/api/django-starter/config/dict')
        self.assertEqual(len(resp.json()['data']), 16)
