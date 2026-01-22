from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountProfileViewTestCase(TestCase):
    """
    profile 视图测试：
    - GET 展示页面
    - POST 更新 request.user.profile
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@example.com", password="test")

    def test_profile_get_requires_login(self):
        resp = self.client.get(reverse("account:profile"))
        self.assertEqual(resp.status_code, 302)

    def test_profile_get_and_post_update(self):
        self.client.login(username="test", password="test")

        resp = self.client.get(reverse("account:profile"))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            reverse("account:profile"),
            data={"full_name": "王五", "gender": "male", "phone": "13800000000"},
        )
        self.assertEqual(resp.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.full_name, "王五")
        self.assertEqual(self.user.profile.gender, "male")
        self.assertEqual(self.user.profile.phone, "13800000000")

