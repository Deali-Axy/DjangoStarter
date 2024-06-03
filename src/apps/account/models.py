from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User

from django_starter.contrib.auth.models import UserProfileAbstract
from django_starter.utilities import table_name_wrapper


# Create your models here.
class UserProfile(UserProfileAbstract):
    class Meta:
        db_table = table_name_wrapper('user_profile')
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name


# 创建用户的时候自动创建 profile
@receiver(signals.post_save, sender=User, dispatch_uid='django_user_post_save')
def create_user_profile(sender: User, instance: User, created, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=instance)
