from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

admin.site.site_header = settings.DJANGO_STARTER['admin']['site_header']
admin.site.site_title = settings.DJANGO_STARTER['admin']['site_title']
admin.site.index_title = settings.DJANGO_STARTER['admin']['index_title']

admin.ModelAdmin.list_per_page = settings.DJANGO_STARTER['admin']['list_per_page']

# 覆盖默认登录页面，实现验证码
# admin.AdminSite.login_template = 'django_starter/admin/login.html'

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    warn_unsaved_form = True


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, admin.ModelAdmin):
    warn_unsaved_form = True

