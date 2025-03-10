from django.contrib import admin
from .models import About, Contact


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'phone', 'updated_time']
    search_fields = ['title', 'story', 'mission']
    list_filter = ['created_time', 'updated_time']
    readonly_fields = ['created_time', 'updated_time']
    fieldsets = [
        ('基本信息', {
            'fields': ['title', 'story', 'mission']
        }),
        ('企业信息', {
            'fields': ['values', 'milestones', 'metrics']
        }),
        ('联系方式', {
            'fields': ['email', 'phone', 'address']
        }),
        ('通用信息', {
            'fields': ['created_time', 'updated_time', 'is_deleted']
        }),
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'updated_time']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['created_time', 'updated_time']
    readonly_fields = ['created_time', 'updated_time']
    fieldsets = [
        ('基本信息', {
            'fields': ['name', 'email', 'phone']
        }),
        ('留言信息', {
            'fields': ['message']
        }),
        ('通用信息', {
            'fields': ['created_time', 'updated_time', 'is_deleted']
        }),
    ]
