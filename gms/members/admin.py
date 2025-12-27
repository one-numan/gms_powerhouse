from django.contrib import admin
from django.utils.timezone import now
from datetime import timedelta

from .models import Member
from subscriptions.models import Subscription
from core.rbac.admin_mixins import RBACQuerysetMixin, RBACPermissionMixin


class FeeStatusFilter(admin.SimpleListFilter):
    title = 'Fee Status'
    parameter_name = 'fee_status'

    def lookups(self, request, model_admin):
        return (
            ('no_active', 'No Active Subscription'),
            ('expired_7', 'Expired in last 7 days'),
            ('expired_old', 'Expired more than 7 days'),
        )

    def queryset(self, request, queryset):
        today = now().date()
        seven_days_ago = today - timedelta(days=7)

        active_member_ids = Subscription.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
            status='active'
        ).values_list('member_id', flat=True)

        if self.value() == 'no_active':
            return queryset.exclude(id__in=active_member_ids)

        if self.value() == 'expired_7':
            return queryset.filter(
                subscriptions__end_date__lt=today,
                subscriptions__end_date__gte=seven_days_ago
            ).distinct()

        if self.value() == 'expired_old':
            return queryset.filter(
                subscriptions__end_date__lt=seven_days_ago
            ).distinct()

        return queryset


@admin.register(Member)
class MemberAdmin(RBACQuerysetMixin, RBACPermissionMixin, admin.ModelAdmin):
    """
    RBAC-enforced Member Admin
    """

    list_display = (
        'first_name',
        'last_name',
        'mobile',
        'branch',
        'subscription_expiry_status',
        'is_active',
    )

    list_filter = ('branch', 'is_active', FeeStatusFilter)
    search_fields = ('first_name', 'last_name', 'mobile')

    def subscription_expiry_status(self, obj):
        today = now().date()
        latest = obj.subscriptions.order_by('-end_date').first()

        if not latest:
            return "No Subscription"

        days = (latest.end_date - today).days
        if days > 0:
            return f"Expires in {days} days"
        if days == 0:
            return "Expires Today"
        return f"Expired {abs(days)} days ago"

    subscription_expiry_status.short_description = "Expiry Status"
