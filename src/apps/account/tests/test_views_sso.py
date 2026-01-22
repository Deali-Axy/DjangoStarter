from django.test import TestCase
from django.urls import reverse


class AccountSsoViewTestCase(TestCase):
    """
    login_sso 视图测试：
    - 无 code 时应直接回到登录页
    - 有 code 但 SSO 未实际接入时，不应 500，应返回明确的安全降级行为
    """

    def test_login_sso_without_code_redirects_to_login(self):
        resp = self.client.get(reverse("account:login-sso"))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith(reverse("account:login")))

    def test_login_sso_with_code_does_not_500(self):
        resp = self.client.get(reverse("account:login-sso"), data={"code": "dummy", "state": reverse("account:index")})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].endswith(reverse("account:login")))

