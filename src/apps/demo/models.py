from django.db import models
from django_starter.db.models import ModelExt
from simple_history.models import HistoricalRecords


# Create your models here.
class Movie(ModelExt):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField()
    rating = models.IntegerField()
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=100)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'demo_movie'
        ordering = ['title']
        verbose_name = '电影'
        verbose_name_plural = verbose_name
        unique_together = (('title', 'year'),)
        indexes = [
            models.Index(fields=["title", "year"]),
        ]


class Actor(ModelExt):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'demo_actor'
        ordering = ['name']
        verbose_name = '演员'
        verbose_name_plural = verbose_name


class MusicAlbum(ModelExt):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'demo_music_album'
        ordering = ['name']
        verbose_name = '音乐专辑'
        verbose_name_plural = verbose_name


class Music(ModelExt):
    name = models.CharField(max_length=100)
    singer = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    rating = models.IntegerField()
    album = models.ForeignKey('MusicAlbum', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'demo_music'
        ordering = ['name']
        verbose_name = '音乐'
        verbose_name_plural = verbose_name
