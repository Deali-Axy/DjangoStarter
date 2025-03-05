from django.contrib import admin
from .models import About


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
        ('联系方式', {
            'fields': ['email', 'phone', 'address']
        }),
        ('时间信息', {
            'fields': ['created_time', 'updated_time']
        }),
    ]
