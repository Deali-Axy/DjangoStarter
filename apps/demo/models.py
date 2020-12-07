from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=20)
    money = models.IntegerField()

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = verbose_name


class Article(models.Model):
    name = models.CharField(max_length=20)
    content = models.TextField()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
