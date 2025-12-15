from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    Admin for Gym Members (Clients)
    """

    list_display = ('first_name', 'last_name', 'mobile', 'branch', 'is_active')
    list_filter = ('branch', 'is_active')
    search_fields = ('first_name', 'last_name', 'mobile')
