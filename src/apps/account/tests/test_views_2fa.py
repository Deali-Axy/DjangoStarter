from unittest import mock

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice


class AccountTwoFactorTestCase(TestCase):
    """
    2FA 流程测试（TOTP + 恢复码）：
    - 启用：/accounts/2fa/setup/
    - 登录触发二次验证：/accounts/login/
    - 验证：/accounts/2fa/verify/
    - 关闭：/accounts/2fa/disable/

    说明：
    - 为避免依赖二维码图片生成库的差异，这里会 mock 掉 _qr_data_uri。
    - TOTP token 的正确性在 django-otp 内部较依赖时间与密钥；这里通过 mock TOTPDevice.verify_token
      来验证“流程与状态变更”而不是算法正确性（算法由 django-otp 自身保障）。
    - 恢复码（StaticToken）采用真实 verify_token 行为，验证一次性消费。
    """

    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@example.com", password="pass1234")

    def test_two_factor_setup_get_creates_unconfirmed_device(self):
        self.client.login(username="test", password="pass1234")

        with mock.patch("apps.account.views._qr_data_uri", return_value="data:image/png;base64,stub"):
            resp = self.client.get(reverse("account:2fa-setup"))

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(TOTPDevice.objects.filter(user=self.user, name="default").exists())
        self.assertFalse(TOTPDevice.objects.filter(user=self.user, confirmed=True).exists())

    def test_two_factor_setup_post_confirms_and_generates_recovery_codes(self):
        self.client.login(username="test", password="pass1234")

        with (
            mock.patch("apps.account.views._qr_data_uri", return_value="data:image/png;base64,stub"),
            mock.patch.object(TOTPDevice, "verify_token", return_value=True),
        ):
            resp = self.client.post(reverse("account:2fa-setup"), data={"token": "123456"})

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(TOTPDevice.objects.filter(user=self.user, confirmed=True).exists())

        static_device = StaticDevice.objects.filter(user=self.user, name="recovery", confirmed=True).first()
        self.assertIsNotNone(static_device)
        self.assertEqual(StaticToken.objects.filter(device=static_device).count(), 10)
        self.assertIsNotNone(resp.context.get("recovery_codes"))
        self.assertEqual(len(resp.context["recovery_codes"]), 10)

    def test_login_view_redirects_to_2fa_verify_when_enabled(self):
        TOTPDevice.objects.create(user=self.user, name="default", confirmed=True)

        resp = self.client.post(reverse("account:login"), data={"username": "test", "password": "pass1234"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith(reverse("account:2fa-verify")))

        session = self.client.session
        self.assertEqual(session.get("pre_2fa_user_id"), self.user.id)
        self.assertTrue(session.get("pre_2fa_next"))
        self.assertFalse("_auth_user_id" in session)

    def test_two_factor_verify_consumes_recovery_code_and_logs_in(self):
        static_device = StaticDevice.objects.create(user=self.user, name="recovery", confirmed=True)
        token = "87654321"
        StaticToken.objects.create(device=static_device, token=token)

        anon = Client()
        session = anon.session
        session["pre_2fa_user_id"] = self.user.id
        session["pre_2fa_next"] = reverse("account:index")
        session.save()

        resp = anon.post(reverse("account:2fa-verify"), data={"token": token})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith(reverse("account:index")))

        resp = anon.get(reverse("account:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(StaticToken.objects.filter(device=static_device, token=token).count(), 0)

        anon.logout()
        session = anon.session
        session["pre_2fa_user_id"] = self.user.id
        session["pre_2fa_next"] = reverse("account:index")
        session.save()

        resp = anon.post(reverse("account:2fa-verify"), data={"token": token})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse("_auth_user_id" in anon.session)

    def test_two_factor_disable_deletes_devices(self):
        TOTPDevice.objects.create(user=self.user, name="default", confirmed=True)
        static_device = StaticDevice.objects.create(user=self.user, name="recovery", confirmed=True)
        token = "12345678"
        StaticToken.objects.create(device=static_device, token=token)

        self.client.login(username="test", password="pass1234")

        resp = self.client.post(
            reverse("account:2fa-disable"),
            data={"password": "pass1234", "token": token},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith(reverse("account:settings")))
        self.assertEqual(TOTPDevice.objects.filter(user=self.user).count(), 0)
        self.assertEqual(StaticDevice.objects.filter(user=self.user).count(), 0)

