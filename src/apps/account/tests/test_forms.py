from django.contrib.auth.models import User
from django.test import TestCase

from apps.account.forms import LoginForm, RegisterForm, UserProfileForm


class AccountFormsTestCase(TestCase):
    """
    account app 表单测试：
    - LoginForm：长度/必填校验
    - RegisterForm：email/用户名/密码基础校验（两次密码一致性在 view 中处理）
    - UserProfileForm：基于 ModelForm 更新 profile 字段
    """

    def test_login_form_validation(self):
        form = LoginForm(data={"username": "ab", "password": "cd"})
        self.assertFalse(form.is_valid())

        form = LoginForm(data={"username": "test", "password": "test"})
        self.assertTrue(form.is_valid())

    def test_register_form_validation(self):
        form = RegisterForm(data={"username": "test", "password": "test", "confirm_password": "test"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

        form = RegisterForm(
            data={
                "email": "name@example.com",
                "username": "test",
                "password": "test",
                "confirm_password": "test",
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_profile_form_updates_instance(self):
        user = User.objects.create_user(username="u1", email="u1@example.com", password="pass1234")

        form = UserProfileForm(
            data={"full_name": "李四", "gender": "male", "phone": "13800000000"},
            instance=user.profile,
        )
        self.assertTrue(form.is_valid())
        form.save()

        user.refresh_from_db()
        self.assertEqual(user.profile.full_name, "李四")
        self.assertEqual(user.profile.gender, "male")
        self.assertEqual(user.profile.phone, "13800000000")

