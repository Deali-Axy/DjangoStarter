from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField()
    rating = models.IntegerField()
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'demo_movie'
        ordering = ['title']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        unique_together = (('title', 'year'),)
        index_together = (('title', 'year'),)


class Actor(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'demo_actor'
        ordering = ['name']
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'
        unique_together = (('name', 'name'),)
        index_together = (('name', 'name'),)


class MusicAlbum(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'demo_music_album'
        ordering = ['name']
        verbose_name = 'MusicAlbum'
        verbose_name_plural = 'MusicAlbums'


class Music(models.Model):
    name = models.CharField(max_length=100)
    singer = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    rating = models.IntegerField()
    album = models.ForeignKey('MusicAlbum', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'demo_music'
        ordering = ['name']
        verbose_name = 'Music'
        verbose_name_plural = 'Music'
