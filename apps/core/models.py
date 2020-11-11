from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """用户资料"""
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    phone = models.CharField('手机号', max_length=11, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name
