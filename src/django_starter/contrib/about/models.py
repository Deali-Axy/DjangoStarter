from django.db import models
from django_starter.db.models import ModelExt
from django_starter.utilities import table_name_wrapper


class About(ModelExt):
    """关于我们页面内容"""
    title = models.CharField('标题', max_length=200)
    story = models.TextField('我们的故事')
    mission = models.TextField('我们的使命')
    values = models.JSONField('价值观', default=list)
    milestones = models.JSONField('发展历程', default=list)
    metrics = models.JSONField('关键数据', default=dict)
    email = models.EmailField('联系邮箱', max_length=100)
    phone = models.CharField('联系电话', max_length=20)
    address = models.TextField('地址')

    class Meta:
        db_table = table_name_wrapper('about')
        verbose_name = '关于我们'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Contact(ModelExt):
    """联系我们表单提交记录"""
    name = models.CharField('姓名', max_length=100)
    email = models.EmailField('邮箱', max_length=100)
    phone = models.CharField('电话', max_length=20)
    message = models.TextField('留言内容')

    class Meta:
        db_table = table_name_wrapper('contact')
        verbose_name = '联系我们'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} - {self.email}'
