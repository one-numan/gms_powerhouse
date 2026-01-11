from django.db import models


class Member(models.Model):
    """
    Member represents a gym client/customer.
    Members do NOT have login access (POC scope).
    All member-related actions are performed by gym staff users.
    """

    # --- Ownership & Scope ---
    # Each member belongs to one organization and one branch
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='members',
        db_index=True  
    )

    branch = models.ForeignKey(
        'organizations.Branch',
        on_delete=models.CASCADE,
        related_name='members',
        db_index=True  
    )

    # --- Personal Information ---
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20,db_index=True  )
    email = models.EmailField(blank=True, null=True)

    # --- Status ---
    # Used to quickly enable/disable a member without deleting data
    is_active = models.BooleanField(default=True,db_index=True  )

    # --- Audit Fields ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Soft Delete ---
    # Members are never hard-deleted to preserve history
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_members'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()
