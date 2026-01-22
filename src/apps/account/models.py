from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User

from django_starter.contrib.auth.models import UserProfileAbstract
from django_starter.utilities import table_name_wrapper


# Create your models here.
class UserProfile(UserProfileAbstract):
    avatar = models.ImageField('头像', upload_to='avatars/%Y/%m/', blank=True, null=True)
    title = models.CharField('职位/头衔', max_length=100, blank=True, default='')
    bio = models.TextField('个人简介', blank=True, default='')

    class Meta:
        db_table = table_name_wrapper('user_profile')
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name


@receiver(signals.post_save, sender=User, dispatch_uid='account_user_post_save_create_profile')
def create_user_profile(sender: type[User], instance: User, created: bool, **kwargs):
    """
    确保 UserProfile 存在。

    账号体系的多处逻辑依赖 `user.profile`，因此在用户创建时创建 profile，
    并在后续保存时保证其存在。
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
