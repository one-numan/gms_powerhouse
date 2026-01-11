from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for gym staff.
    Includes role-based access and profile information.
    """

    ROLE_CHOICES = (
        ('owner', 'Gym Owner'),
        ('site_manager', 'Site Manager'),
        ('gym_manager', 'Gym Manager'),
        ('staff', 'Staff'),
    )

    STAY_STATUS_CHOICES = (
        ('pg', 'PG'),
        ('rent', 'Rented Room/House'),
        ('hostel', 'Hostel'),
        ('college', 'School / College'),
        ('other', 'Other'),
    )

    # --- Role & Access ---
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff',
        db_index=True  # ✅ RBAC checks,
    )

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True  
    )

    branch = models.ForeignKey(
        'organizations.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True  # ✅ RBAC checks
    )

    # --- Contact & Location ---
    mobile = models.CharField(max_length=20, blank=True, null=True,db_index=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # --- Personal Info ---
    current_stay_status = models.CharField(
        max_length=20,
        choices=STAY_STATUS_CHOICES,
        blank=True,
        null=True
    )

    # --- System Fields ---
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

