from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Accounts


class AccountsAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name',
                    'phone', 'department', 'occupation']
    list_display_links = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Accounts, AccountsAdmin)
