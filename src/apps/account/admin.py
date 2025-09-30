from django.contrib import admin
from django.contrib.auth.models import User
from django.forms.models import BaseInlineFormSet
from django_starter.contrib.admin.admin import UserAdmin
from .models import UserProfile


class UserProfileInlineFormSet(BaseInlineFormSet):
    """防止重复创建 UserProfile"""

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        obj.user = self.instance  # instance 就是 User
        if commit:
            obj.save()
        return obj


# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "用户资料"
    extra = 1
    max_num = 1  # 只允许一个 profile
    formset = UserProfileInlineFormSet
    ordering = []


# Define a new User admin
class UserAdminWithProfile(UserAdmin):
    inlines = [UserProfileInline]


# 替换默认的 User admin
admin.site.unregister(User)
admin.site.register(User, UserAdminWithProfile)
