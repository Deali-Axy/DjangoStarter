from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin

from django_starter.db.models import ModelExt
from django_starter.utilities import table_name_wrapper


class UserProfileAbstract(ModelExt):
    """用户资料"""

    class GenderChoice(models.TextChoices):
        MALE = 'male', '男'
        FEMALE = 'female', '女'
        UNKNOWN = 'unknown', '未知'

    user = models.OneToOneField(User, unique=True, on_delete=models.DO_NOTHING, db_constraint=False,
                                related_name='profile')
    full_name = models.CharField('姓名', max_length=200, default='')
    gender = models.CharField('性别', max_length=20, choices=GenderChoice.choices, default=GenderChoice.UNKNOWN)
    phone = models.CharField('手机号', max_length=11, default='')

    def __str__(self):
        return self.full_name

    class Meta:
        abstract = True
        db_table = table_name_wrapper('user_profile')
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name


class UserClaim(models.Model):
    user = models.ForeignKey(User, db_constraint=False, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = table_name_wrapper('user_claims')
        verbose_name = 'UserClaim'
        verbose_name_plural = verbose_name


