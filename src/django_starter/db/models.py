from django.db import models
from django.utils import timezone


class ModelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_deleted=False)


class ModelExt(models.Model):
    objects = ModelManager()
    is_deleted = models.BooleanField('软删除标志', default=False)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
