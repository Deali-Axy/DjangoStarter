from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User

from django_starter.contrib.auth.models import UserProfileAbstract


# Create your models here.
class UserProfile(UserProfileAbstract):
    class Meta:
        db_table = 'user_profile'


# 创建用户的时候自动创建 profile
@receiver(signals.post_save, sender=User, dispatch_uid='django_user_post_save')
def create_user_profile(sender: User, instance: User, created, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=instance)
