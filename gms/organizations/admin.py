from django.contrib import admin
from .models import Organization, Branch


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

    list_display = ('name', 'organization', 'city', 'is_active')
    list_filter = ('organization',)
