from django.conf import settings
from django.contrib import admin

admin.site.site_header = settings.DJANGO_STARTER['admin']['site_header']
admin.site.site_title = settings.DJANGO_STARTER['admin']['site_title']
admin.site.index_title = settings.DJANGO_STARTER['admin']['index_title']

admin.ModelAdmin.list_per_page = settings.DJANGO_STARTER['admin']['list_per_page']

# 覆盖默认登录页面，实现验证码
admin.AdminSite.login_template = 'django_starter/admin/login.html'
