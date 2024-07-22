from django.contrib import admin

from .models import *


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'year', 'rating', 'genre', 'director', 'actors', ]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'birth_date', 'country', 'city', ]


@admin.register(MusicAlbum)
class MusicAlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', ]


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'singer', 'genre', 'rating', 'album', ]

