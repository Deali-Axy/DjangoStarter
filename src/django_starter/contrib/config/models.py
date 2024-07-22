from django.db import models
from django_starter.db.models import ModelExt
from django_starter.utilities import table_name_wrapper


class ConfigItem(ModelExt):
    key = models.CharField('配置项名称', unique=True, max_length=200)
    value = models.CharField('配置项的值', max_length=5000)
    display_name = models.TextField('显示名称', default='')

    def __str__(self):
        return self.key

    class Meta:
        db_table = table_name_wrapper('config')
        verbose_name = '通用配置'
        verbose_name_plural = verbose_name
