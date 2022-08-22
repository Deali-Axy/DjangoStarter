from django.contrib import admin
from .models import *

admin.site.site_header = 'DjangoStart 管理后台'
admin.site.site_title = 'DjangoStart 管理后台'
admin.site.index_title = 'DjangoStart 管理后台'

# 一些默认配置
admin.ModelAdmin.list_per_page = 20
