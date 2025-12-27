from django.contrib import admin
from .models import Plan, Subscription, Payment
from core.rbac.admin_mixins import RBACQuerysetMixin, RBACPermissionMixin


@admin.register(Plan)
class PlanAdmin(RBACQuerysetMixin, RBACPermissionMixin, admin.ModelAdmin):
    list_display = ('name', 'duration_days', 'amount', 'is_active')
    list_filter = ('is_active',)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == "organization_manager"


@admin.register(Subscription)
class SubscriptionAdmin(RBACQuerysetMixin, RBACPermissionMixin, admin.ModelAdmin):
    list_display = ('member', 'plan', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'plan')

    def has_add_permission(self, request):
        return request.user.role in ["organization_manager", "branch_manager"]

    def has_change_permission(self, request, obj=None):
        return request.user.role in ["organization_manager", "branch_manager"]


@admin.register(Payment)
class PaymentAdmin(RBACQuerysetMixin, RBACPermissionMixin, admin.ModelAdmin):
    list_display = ('member', 'amount', 'payment_mode', 'payment_date', 'received_by')
    list_filter = ('payment_mode',)

    def has_add_permission(self, request):
        return request.user.role in ["branch_manager", "staff"]

    def has_change_permission(self, request, obj=None):
        return request.user.role == "branch_manager"

    def has_delete_permission(self, request, obj=None):
        return request.user.role == "organization_manager"
