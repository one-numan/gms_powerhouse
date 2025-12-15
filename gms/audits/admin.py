from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Admin for Audit Logs
    """

    list_display = ('action', 'table_name', 'record_id', 'user', 'created_at')
    list_filter = ('action', 'table_name')
