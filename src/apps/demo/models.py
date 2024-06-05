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


import uuid


class TestModel(models.Model):
    char_field = models.CharField(max_length=255)
    text_field = models.TextField()
    integer_field = models.IntegerField()
    float_field = models.FloatField()
    boolean_field = models.BooleanField()
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    email_field = models.EmailField()
    url_field = models.URLField()
    decimal_field = models.DecimalField(max_digits=10, decimal_places=2)
    slug_field = models.SlugField(max_length=50)
    uuid_field = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    binary_field = models.BinaryField(max_length=100)
    duration_field = models.DurationField()
    ip_address_field = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    json_field = models.JSONField()

    def __str__(self):
        return self.char_field
