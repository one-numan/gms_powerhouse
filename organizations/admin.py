from django.contrib import admin
from .models import Organization, Branch
from django.utils.html import format_html

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Admin for Gym Organizations (Companies)
    """

    list_display = ('name', 'email', 'phone', 'is_active')
    search_fields = ('name',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """
    Admin for Gym Branches (Locations)
    """

    # --------------------------------------------------
    # List Page
    # --------------------------------------------------
    list_display = (
        'name',
        'organization',
        'manager',
        'city',
        'state',
        'is_active',    
        'created_at',
        'google_map_url'
    )

    list_filter = (
        'organization',
        'city',
        'state',
        'is_active',
    )

    search_fields = (
        'name',
        'city',
        'state',
        'address_line',
        'manager__first_name',
        'manager__last_name',
    )

    ordering = ('organization', 'name')

    list_editable = ('is_active',)

    # --------------------------------------------------
    # Form Layout
    # --------------------------------------------------

    readonly_fields = (
        'created_at',
        'updated_at',
    )