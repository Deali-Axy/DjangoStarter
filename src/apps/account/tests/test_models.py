from django.contrib.auth.models import User
from django.test import TestCase


class UserProfileModelTestCase(TestCase):
    """
    UserProfile 的核心行为测试：
    - 创建 User 时应自动创建 profile（post_save 信号）
    - profile 应包含基础字段与软删字段（由 ModelExt 提供）
    """

    def test_profile_is_created_on_user_creation(self):
        user = User.objects.create_user(username="u1", email="u1@example.com", password="pass1234")
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.user_id, user.id)

    def test_profile_is_not_duplicated_on_user_save(self):
        user = User.objects.create_user(username="u2", email="u2@example.com", password="pass1234")
        profile_id = user.profile.id

        user.first_name = "changed"
        user.save()

        user.refresh_from_db()
        self.assertEqual(user.profile.id, profile_id)

    def test_profile_fields_and_soft_delete_flag(self):
        user = User.objects.create_user(username="u3", email="u3@example.com", password="pass1234")
        user.profile.full_name = "张三"
        user.profile.gender = "male"
        user.profile.phone = "13800000000"
        user.profile.save()

        user.refresh_from_db()
        self.assertEqual(user.profile.full_name, "张三")
        self.assertEqual(user.profile.gender, "male")
        self.assertEqual(user.profile.phone, "13800000000")

        self.assertTrue(hasattr(user.profile, "is_deleted"))
        self.assertIn(user.profile.is_deleted, (False, 0))

