from django.db import models
from django_starter.db.models import ModelExt


# Create your models here.
class DemoDepartment(ModelExt):
    name = models.CharField('部门名称', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name
