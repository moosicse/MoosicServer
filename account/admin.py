from django.contrib import admin

from account.models import UserGroup, UserProfile


@admin.register(UserProfile, UserGroup)
class AccountAdmin(admin.ModelAdmin):
    pass
