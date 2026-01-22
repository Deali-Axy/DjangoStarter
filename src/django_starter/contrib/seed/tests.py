import pytest
import json
from django.core.management import call_command
from django_starter.contrib.about.models import About, Contact
from django.apps import apps
from django_starter.contrib.seed.seeder import Seeder

@pytest.mark.django_db
class TestSeedCommand:
    def test_seed_contact(self):
        """测试为 about 应用生成数据"""
        initial_count = Contact.objects.count()
        count_to_seed = 5
        
        # 确认 app label
        app_config = apps.get_app_config('about')
        assert app_config.name == 'django_starter.contrib.about'

        call_command('seed', 'about', count_to_seed)
        
        new_count = Contact.objects.count()
        assert new_count == initial_count + count_to_seed
        
        # 验证生成的数据
        latest = Contact.objects.last()
        assert latest.name
        assert latest.email
        assert latest.message

    def test_jsonfield_values_serializable(self):
        seeder = Seeder()
        payload = seeder.seed(About)
        assert isinstance(payload.get('values'), (list, dict))
        assert isinstance(payload.get('milestones'), (list, dict))
        assert isinstance(payload.get('metrics'), (list, dict))

        json.dumps(payload.get('values'))
        json.dumps(payload.get('milestones'))
        json.dumps(payload.get('metrics'))
