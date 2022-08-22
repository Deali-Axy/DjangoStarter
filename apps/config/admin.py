from django.contrib import admin

from .models import *


@admin.register(CommonConfig)
class CommonConfigAdmin(admin.ModelAdmin):
    list_editable = ['value']
    list_display = ['display_name', 'key', 'value']
    list_display_links = None
