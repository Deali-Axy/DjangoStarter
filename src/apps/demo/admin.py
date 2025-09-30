from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django_starter.contrib.admin.tags import html_tags

from .models import *


@admin.register(Movie)
class MovieAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ['id', 'title', 'year', 'rating', 'genre', 'director', 'actors', 'description', ]
    list_display_links = ['id', 'title', 'description', 'year', 'rating', 'genre', 'director', 'actors', ]
    readonly_fields = ['id', 'created_time', 'updated_time', 'is_deleted', ]
    fieldsets = (
        ('电影', {'fields': ('id', 'title', 'description', 'year', 'rating', 'genre', 'director', 'actors',)}),

        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )


@admin.register(Actor)
class ActorAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'birth_date', 'country', 'city', ]
    list_display_links = ['id', 'name', 'birth_date', 'country', 'city', ]
    readonly_fields = ['id', 'created_time', 'updated_time', 'is_deleted', ]
    fieldsets = (
        ('演员', {'fields': ('id', 'name', 'birth_date', 'country', 'city',)}),

        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )


@admin.register(MusicAlbum)
class MusicAlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', ]
    list_display_links = ['id', 'name', 'year', ]
    readonly_fields = ['id', 'created_time', 'updated_time', 'is_deleted', ]
    fieldsets = (
        ('音乐专辑', {'fields': ('id', 'name', 'year',)}),

        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'singer', 'genre', 'rating', 'album', ]
    list_display_links = ['id', 'name', 'singer', 'genre', 'rating', ]
    readonly_fields = ['id', 'created_time', 'updated_time', 'is_deleted', ]
    fieldsets = (
        ('音乐', {'fields': ('id', 'name', 'singer', 'genre', 'rating', 'album',)}),

        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )
