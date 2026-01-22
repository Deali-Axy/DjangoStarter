import pytest
from django.conf import settings
from django.urls import reverse

from .models import About, Contact
from .views import get_about

@pytest.mark.django_db
class TestAboutApp:
    def test_about_singleton(self):
        """验证 About 模型的创建与读取"""
        about = About.objects.create(
            title="Test About",
            story="Story",
            mission="Mission",
            email="test@example.com",
            phone="123",
            address="Address"
        )
        assert About.objects.count() == 1
        assert About.objects.first().title == "Test About"

    def test_index_renders(self, client):
        """关于我们主页面可正常渲染"""
        url = reverse('djs_about:index')
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode()
        assert 'id="mission"' in content
        assert 'id="milestones"' in content
        assert 'id="team"' in content
        assert 'id="faq"' in content

    def test_contact_submission(self, client):
        """模拟 POST 请求提交联系表单"""
        url = reverse('djs_about:contact')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'message': 'Hello World'
        }
        response = client.post(url, data)
        # 提交成功后通常重定向
        assert response.status_code == 302
        
        # 验证数据是否存入数据库
        assert Contact.objects.count() == 1
        contact = Contact.objects.first()
        assert contact.name == 'Test User'
        assert contact.message == 'Hello World'

    def test_get_about_fallback_when_empty(self):
        about = get_about()
        assert about is not None
        assert getattr(about, 'title', None)
        assert getattr(about, 'mission', None)
        assert getattr(about, 'email', None)
        assert isinstance(getattr(about, 'milestones', []), list)

    def test_contact_form_disabled(self, client):
        url = reverse('djs_about:contact')
        original = settings.DJANGO_STARTER['site']['enable_contact_form']
        settings.DJANGO_STARTER['site']['enable_contact_form'] = False
        try:
            response = client.post(url, {
                'name': 'Test User',
                'email': 'test@example.com',
                'phone': '1234567890',
                'message': 'Hello World',
            })
        finally:
            settings.DJANGO_STARTER['site']['enable_contact_form'] = original

        assert response.status_code == 302
        assert Contact.objects.count() == 0

    @pytest.mark.parametrize("url_name, load_more_id", [
        ('djs_about:partials_milestones', 'milestoneLoadMore'),
        ('djs_about:partials_team', 'teamLoadMore'),
        ('djs_about:partials_faq', 'faqLoadMore'),
    ])
    def test_htmx_partials_pagination(self, client, url_name, load_more_id):
        """HTMX 端点返回追加内容与按钮 OOB 更新"""
        url = reverse(url_name)
        response = client.get(url, {'offset': 0}, HTTP_HX_REQUEST='true')
        assert response.status_code == 200
        content = response.content.decode()
        assert 'hx-swap-oob="outerHTML"' in content
        assert f'id="{load_more_id}"' in content
