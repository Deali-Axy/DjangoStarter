from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountAuthViewsTestCase(TestCase):
    """
    account app 的 Web 认证相关视图测试（不包含 2FA 分支）：
    - login_view / signup_view / logout_view
    - 受保护页面的登录重定向
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@example.com", password="test")

    def test_protected_pages_redirect_to_login_when_anonymous(self):
        resp = self.client.get(reverse("account:index"))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(reverse("account:profile"))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(reverse("account:settings"))
        self.assertEqual(resp.status_code, 302)

    def test_login_get_renders_page(self):
        resp = self.client.get(reverse("account:login"))
        self.assertEqual(resp.status_code, 200)

    def test_login_failed_shows_page(self):
        resp = self.client.post(reverse("account:login"), data={"username": "test", "password": "wrong"})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_login_success_redirects(self):
        resp = self.client.post(reverse("account:login"), data={"username": "test", "password": "test"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_signup_creates_user_and_logs_in(self):
        resp = self.client.get(reverse("account:signup"))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse("account:signup"),
            data={
                "email": "new@example.com",
                "username": "newuser",
                "password": "pass1234",
                "confirm_password": "pass1234",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser", email="new@example.com").exists())
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_signup_duplicate_username_or_email(self):
        resp = self.client.post(
            reverse("account:signup"),
            data={
                "email": "another@example.com",
                "username": "test",
                "password": "pass1234",
                "confirm_password": "pass1234",
            },
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse("account:signup"),
            data={
                "email": "test@example.com",
                "username": "another",
                "password": "pass1234",
                "confirm_password": "pass1234",
            },
        )
        self.assertEqual(resp.status_code, 200)

    def test_logout_clears_session(self):
        self.client.login(username="test", password="test")
        resp = self.client.get(reverse("account:logout"))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse("_auth_user_id" in self.client.session)

