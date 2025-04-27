from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

admin.site.site_header = settings.DJANGO_STARTER['admin']['site_header']
admin.site.site_title = settings.DJANGO_STARTER['admin']['site_title']
admin.site.index_title = settings.DJANGO_STARTER['admin']['index_title']

admin.ModelAdmin.list_per_page = settings.DJANGO_STARTER['admin']['list_per_page']

# 覆盖默认登录页面，实现验证码
# admin.AdminSite.login_template = 'django_starter/admin/login.html'

# 为 unfold admin 配置 User & group models
# https://unfoldadmin.com/docs/installation/auth/
# By default, when django.contrib.auth is in INSTALLED_APPS, you are going to have user and group models in admin.
# Both models are going to work but they will look unstyled because they are not inheriting from unfold.admin.ModelAdmin.
# The solution is to unregister default admin classes and then register them back by using unfold.admin.ModelAdmin
# like in the example below. Additionally, we have to override default user forms (UserAdmin class) which are by default
# loaded by Django admin. New, overridden forms are going to have proper styling.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    warn_unsaved_form = True


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    warn_unsaved_form = True

