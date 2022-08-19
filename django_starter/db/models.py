from django.db import models
from django.utils import timezone


class ModelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_deleted=False)


class ModelExt(models.Model):
    objects = ModelManager()
    is_deleted = models.BooleanField('是否已删除', default=False)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', default=timezone.now)

    class Meta:
        abstract = True
