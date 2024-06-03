from django.contrib import admin
from .models import UserClaim


@admin.register(UserClaim)
class UserClaimAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'value']
