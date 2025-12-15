from django.db import models


class Plan(models.Model):
    """
    Plan defines the membership offering of a gym.
    Example: 1 Month, 3 Months, 6 Months, 1 Year
    """

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='plans'
    )

    name = models.CharField(max_length=100)          # e.g. "3 Months"
    duration_days = models.PositiveIntegerField()    # e.g. 90
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)

    # --- Audit Fields ---
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
        return f"{self.name} - {self.amount}"


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

    member = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT
    )

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
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

    def __str__(self):
        return f"{self.member} → {self.plan.name} ({self.status})"


class Payment(models.Model):
    """
    Payment stores money received for a subscription.
    Payments are financial records and must NEVER be deleted.
    """

    PAYMENT_MODE_CHOICES = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('debit_card', 'Debit Card'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
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
        choices=PAYMENT_MODE_CHOICES
    )

    payment_ref = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_date = models.DateField()

    received_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_payments'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount} ({self.payment_mode})"
