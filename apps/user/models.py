from django_starter.db.models import ModelExt
from django.db import models
from django.contrib.auth.models import User


class UserProfile(ModelExt):
    """用户资料"""

    class GenderChoice(models.TextChoices):
        MALE = 'male', '男'
        FEMALE = 'female', '女'
        UNKNOWN = 'unknown', '未知'

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField('姓名', max_length=200)
    alias = models.CharField('别名', max_length=200, blank=True, null=True)
    gender = models.CharField('性别', max_length=20, choices=GenderChoice.choices, default=GenderChoice.UNKNOWN)
    phone = models.CharField('手机号', max_length=11, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name
