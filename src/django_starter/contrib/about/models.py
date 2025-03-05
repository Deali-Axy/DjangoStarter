from django.db import models
from django_starter.db.models import ModelExt
from django_starter.utilities import table_name_wrapper


class About(ModelExt):
    """关于我们页面内容"""
    title = models.CharField('标题', max_length=200)
    story = models.TextField('我们的故事')
    mission = models.TextField('我们的使命')
    email = models.EmailField('联系邮箱', max_length=100)
    phone = models.CharField('联系电话', max_length=20)
    address = models.TextField('地址')

    class Meta:
        db_table = table_name_wrapper('about')
        verbose_name = '关于我们'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
