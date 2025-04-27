from django.contrib import admin
from unfold.admin import StackedInline
from django_starter.contrib.admin.admin import UserAdmin as BaseUserAdmin
from .models import *


# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "用户资料"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
