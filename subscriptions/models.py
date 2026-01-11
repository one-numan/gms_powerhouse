from django.db import models
from django.db.models import Q
from django.utils import timezone


class Plan(models.Model):
    """
    Plan defines the membership offering of a gym.
    Example: 1 Month, 3 Months, 6 Months, 1 Year
    """

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='plans',
        db_index=True
    )

    name = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True, db_index=True)

    # --- Audit ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Soft Delete ---
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_plans'
    )

    def __str__(self):
        return f"{self.name} ({self.amount})"


# class Subscription(models.Model):
#     """
#     Subscription represents a member's membership.
#     A member can have multiple subscriptions over time,
#     but ONLY ONE active subscription at a time.
#     """

#     STATUS_CHOICES = (
#         ('active', 'Active'),
#         ('expired', 'Expired'),
#         ('cancelled', 'Cancelled'),
#     )

#     organization = models.ForeignKey(
#         'organizations.Organization',
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#         db_index=True
#     )

#     member = models.ForeignKey(
#         'members.Member',
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#         db_index=True
#     )

#     plan = models.ForeignKey(
#         Plan,
#         on_delete=models.PROTECT,
#         related_name='subscriptions'
#     )

#     start_date = models.DateField(db_index=True)
#     end_date = models.DateField(db_index=True)

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='active',
#         db_index=True
#     )

#     # --- Audit ---
#     created_by = models.ForeignKey(
#         'accounts.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='created_subscriptions'
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # --- Soft Delete ---
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     deleted_by = models.ForeignKey(
#         'accounts.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='deleted_subscriptions'
#     )

#     class Meta:
#         indexes = [
#             models.Index(fields=['member', 'status']),
#             models.Index(fields=['end_date']),
#         ]
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['member'],
#                 condition=Q(status='active', deleted_at__isnull=True),
#                 name='one_active_subscription_per_member'
#             )
#         ]

#     def is_expired(self):
#         return self.end_date < timezone.now().date()

#     def __str__(self):
#         return f"{self.member} → {self.plan.name} ({self.status})"



# class Subscription(models.Model):
#     """
#     Subscription represents a member's membership.
#     A member can have multiple subscriptions over time,
#     but ONLY ONE active subscription at a time.
#     """

#     STATUS_CHOICES = (
#         ('active', 'Active'),
#         ('expired', 'Expired'),
#         ('cancelled', 'Cancelled'),
#     )

#     organization = models.ForeignKey(
#         'organizations.Organization',
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#         db_index=True
#     )

#     member = models.ForeignKey(
#         'members.Member',
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#         db_index=True
#     )

#     plan = models.ForeignKey(
#         'subscriptions.Plan',
#         on_delete=models.PROTECT,
#         related_name='subscriptions'
#     )

#     start_date = models.DateField(db_index=True)
#     end_date = models.DateField(db_index=True)

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='active',
#         db_index=True
#     )

#     # --- Audit ---
#     created_by = models.ForeignKey(
#         'accounts.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='created_subscriptions'
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # --- Soft Delete ---
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     deleted_by = models.ForeignKey(
#         'accounts.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='deleted_subscriptions'
#     )

#     class Meta:
#         indexes = [
#             models.Index(fields=['member', 'status']),
#             models.Index(fields=['end_date']),
#         ]
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['member'],
#                 condition=Q(status='active', deleted_at__isnull=True),
#                 name='one_active_subscription_per_member'
#             )
#         ]

#     def is_expired(self):
#         return self.end_date < timezone.now().date()

#     def __str__(self):
#         return f"{self.member} → {self.plan.name} ({self.status})"

from django.db import models
from django.db import transaction
from django.db.models import Q
from django.utils import timezone


class Subscription(models.Model):
    """
    Subscription represents a member's membership.
    A member can have multiple subscriptions over time,
    but ONLY ONE active subscription at a time.
    """

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        db_index=True
    )

    member = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        db_index=True
    )

    plan = models.ForeignKey(
        'subscriptions.Plan',
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )

    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        db_index=True
    )

    # --- Audit ---
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_subscriptions'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Soft Delete ---
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_subscriptions'
    )

    class Meta:
        indexes = [
            models.Index(fields=['member', 'status']),
            models.Index(fields=['end_date']),
        ]
        # ⚠️ MariaDB does NOT enforce conditional unique constraints
        # This constraint is kept only for documentation / future DBs
        constraints = [
            models.UniqueConstraint(
                fields=['member'],
                condition=Q(status='active', deleted_at__isnull=True),
                name='one_active_subscription_per_member'
            )
        ]

    # ✅ MARIA DB SAFE ENFORCEMENT
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.status == 'active' and self.deleted_at is None:
                Subscription.objects.filter(
                    member=self.member,
                    status='active',
                    deleted_at__isnull=True
                ).exclude(pk=self.pk).update(
                    status='expired',
                    updated_at=timezone.now()
                )
            super().save(*args, **kwargs)

    def is_expired(self):
        return self.end_date < timezone.now().date()

    def __str__(self):
        return f"{self.member} → {self.plan.name} ({self.status})"

class Payment(models.Model):
    """
    Payment stores money received for a subscription.
    Payments are immutable financial records.
    """

    PAYMENT_MODE_CHOICES = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('debit_card', 'Debit Card'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
    )

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='payments',
        db_index=True
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    member = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES,
        db_index=True
    )

    payment_ref = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_date = models.DateField(db_index=True)

    received_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_payments',
        db_index=True
    )

    # --- Accounting Safety ---
    is_void = models.BooleanField(default=False, db_index=True)
    voided_at = models.DateTimeField(null=True, blank=True)
    voided_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voided_payments'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount} ({self.payment_mode})"
