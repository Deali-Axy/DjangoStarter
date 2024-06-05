import uuid

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# Create your tests here.
class AuthTestCase(TestCase):
    def setUp(self):
        user: User = User.objects.create_user(username='test', password='test')
        user.profile.phone = '13812341234'
        user.profile.save()

    def test_auth_login(self):
        resp = self.client.post(
            reverse_lazy('api:account/auth/login'),
            data={'username': 'test', 'password': 'test'},
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)

    def test_auth_login_failed(self):
        resp = self.client.post(
            reverse_lazy('api:account/auth/login'),
            data={'username': uuid.uuid4().hex, 'password': uuid.uuid4().hex},
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 401)

    def test_auth_register(self):
        username = uuid.uuid4().hex
        password = uuid.uuid4().hex
        resp = self.client.post(
            reverse_lazy('api:account/auth/register'),
            data={'username': username, 'password': password, 'confirm_password': password},
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)

    def test_auth_register_failed(self):
        # 注册已存在用户
        resp = self.client.post(
            reverse_lazy('api:account/auth/register'),
            data={'username': 'test', 'password': 'test', 'confirm_password': 'test'},
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)

        # 密码不一致
        username = uuid.uuid4().hex
        password = uuid.uuid4().hex
        resp = self.client.post(
            reverse_lazy('api:account/auth/register'),
            data={'username': username, 'password': password, 'confirm_password': 'another-password'},
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)

        # 手机号格式错误
        resp = self.client.post(
            reverse_lazy('api:account/auth/register'),
            data={'username': username, 'password': password, 'confirm_password': password, 'phone': '1234'},
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)

        # 注册已存在手机号的用户
        resp = self.client.post(
            reverse_lazy('api:account/auth/register'),
            data={'username': username, 'password': password, 'confirm_password': password, 'phone': '13812341234'},
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400)

    def test_auth_get_current_user(self):
        resp = self.client.post(
            reverse_lazy('api:account/auth/login'),
            data={'username': 'test', 'password': 'test'},
            content_type='application/json'
        )

        token = resp.json()['data']['token']

        resp = self.client.get(
            reverse_lazy('api:account/auth/current_user'),
            content_type='application/json',
            headers={'authorization': f'Bearer {token}'},
        )
        self.assertEqual(resp.json()['data']['username'], 'test')
