from django.contrib import admin
from .models import *


@admin.register(DemoDepartment)
class DemoDepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'created_time', 'updated_time', 'is_deleted']
    list_filter = ['created_time', 'updated_time', 'is_deleted']
