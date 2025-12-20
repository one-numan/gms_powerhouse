from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for gym staff users.
    """

    list_display = (
        'username',
        'email',
        'mobile',
        'role',
        'city',
        'is_active',
    )

    list_filter = ('role', 'city', 'state', 'current_stay_status')
    search_fields = ('username', 'email', 'mobile')

    fieldsets = (
        ('Login Info', {
            'fields': ('username', 'password')
        }),
        ('Role & Organization', {
            'fields': ('role', 'organization', 'branch')
        }),
        ('Contact Details', {
            'fields': ('email', 'mobile', 'city', 'state', 'country')
        }),
        ('Personal Info', {
            'fields': ('current_stay_status',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )
