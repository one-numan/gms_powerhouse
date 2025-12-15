from django.contrib import admin
from .models import Plan, Subscription, Payment


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    Admin for Membership Plans
    """

    list_display = ('name', 'duration_days', 'amount', 'is_active')
    list_filter = ('is_active',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin for Member Subscriptions
    """

    list_display = ('member', 'plan', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'plan')
    search_fields = ('member__first_name', 'member__mobile')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin for Payments
    """

    list_display = ('member', 'amount', 'payment_mode', 'payment_date', 'received_by')
    list_filter = ('payment_mode',)
