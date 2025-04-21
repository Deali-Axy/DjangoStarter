from django.contrib import admin
from django_starter.contrib.admin.tags import html_tags

from .models import *


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','title','year','rating','genre','director','actors','description',]
    list_display_links = ['id','title','description','year','rating','genre','director','actors',]
    readonly_fields = ['id','created_time', 'updated_time', 'is_deleted',]
    fieldsets = (
        ('Movie', {'fields': ('id','title','description','year','rating','genre','director','actors',)}),
        
        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )

    

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['id','name','birth_date','country','city',]
    list_display_links = ['id','name','birth_date','country','city',]
    readonly_fields = ['id','created_time', 'updated_time', 'is_deleted',]
    fieldsets = (
        ('Actor', {'fields': ('id','name','birth_date','country','city',)}),
        
        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )

    

@admin.register(MusicAlbum)
class MusicAlbumAdmin(admin.ModelAdmin):
    list_display = ['id','name','year',]
    list_display_links = ['id','name','year',]
    readonly_fields = ['id','created_time', 'updated_time', 'is_deleted',]
    fieldsets = (
        ('MusicAlbum', {'fields': ('id','name','year',)}),
        
        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )

    

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['id','name','singer','genre','rating','album',]
    list_display_links = ['id','name','singer','genre','rating',]
    readonly_fields = ['id','created_time', 'updated_time', 'is_deleted',]
    fieldsets = (
        ('Music', {'fields': ('id','name','singer','genre','rating','album',)}),
        
        ('通用信息', {'fields': ('created_time', 'updated_time', 'is_deleted')}),
    )

    

