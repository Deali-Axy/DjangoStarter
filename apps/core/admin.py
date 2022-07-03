from django.contrib import admin
from .models import *

admin.site.site_header = 'DjangoStart 管理后台'
admin.site.site_title = 'DjangoStart 管理后台'
admin.site.index_title = 'DjangoStart 管理后台'


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'phone']
