from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class AccountSettingsViewTestCase(TestCase):
    """
    settings 相关视图测试：
    - 修改密码后会话保持有效（update_session_auth_hash）
    - 退出其它设备 / 退出全部设备 的 session 清理逻辑
    - developer token 生成需要二次校验密码
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@example.com", password="oldpass1234")

    def test_change_password_keeps_session(self):
        self.client.login(username="test", password="oldpass1234")

        resp = self.client.post(
            reverse("account:settings"),
            data={
                "action": "change_password",
                "old_password": "oldpass1234",
                "new_password1": "newpass1234",
                "new_password2": "newpass1234",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith(reverse("account:settings")))

        resp = self.client.get(reverse("account:settings"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("_auth_user_id" in self.client.session)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass1234"))

    def test_logout_others_deletes_other_sessions(self):
        client1 = Client()
        client2 = Client()

        self.assertTrue(client1.login(username="test", password="oldpass1234"))
        self.assertTrue(client2.login(username="test", password="oldpass1234"))

        resp = client1.post(reverse("account:settings"), data={"action": "logout_others"})
        self.assertEqual(resp.status_code, 302)

        resp = client1.get(reverse("account:settings"))
        self.assertEqual(resp.status_code, 200)

        resp = client2.get(reverse("account:settings"))
        self.assertEqual(resp.status_code, 302)

    def test_logout_all_logs_out_current_session(self):
        self.client.login(username="test", password="oldpass1234")

        resp = self.client.post(reverse("account:settings"), data={"action": "logout_all"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith(reverse("account:login")))

        resp = self.client.get(reverse("account:settings"))
        self.assertEqual(resp.status_code, 302)

    def test_settings_developer_token_requires_password(self):
        self.client.login(username="test", password="oldpass1234")

        resp = self.client.post(reverse("account:settings-developer-token"), data={"password": "wrong"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", resp.context)
        self.assertIsNone(resp.context["token"])

        resp = self.client.post(reverse("account:settings-developer-token"), data={"password": "oldpass1234"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", resp.context)
        self.assertIn("token", resp.context["token"])
        self.assertIn("exp", resp.context["token"])

