from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_organizations'
    )

    def __str__(self):
        return self.name

# class Branch(models.Model):
#     organization = models.ForeignKey(
#         Organization,
#         on_delete=models.CASCADE,
#         related_name='branches'
#     )

#     name = models.CharField(max_length=255)
#     address = models.TextField(blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)

#     is_active = models.BooleanField(default=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # Soft delete
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     deleted_by = models.ForeignKey(
#         'accounts.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='deleted_branches'
#     )

#     def __str__(self):
#         return f"{self.name} ({self.organization.name})"

class Branch(models.Model):
    # --------------------------------------------------
    # Ownership
    # --------------------------------------------------
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='branches'
    )

    # --------------------------------------------------
    # Branch Manager
    # --------------------------------------------------
    manager = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_branches',
        limit_choices_to={'role__in': ['site_manager', 'gym_manager']}
    )

    # --------------------------------------------------
    # Basic Info
    # --------------------------------------------------
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    # --------------------------------------------------
    # Address (India Optimized)
    # --------------------------------------------------
    address_line = models.TextField(
        blank=True,
        null=True,
        help_text="Building, street, landmark"
    )
    area = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Area / locality"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    pincode = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=50,
        default="India"
    )

    # --------------------------------------------------
    # Contact & Operations
    # --------------------------------------------------
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    # --------------------------------------------------
    # Location (Optional – for advanced use)
    # --------------------------------------------------
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    # --------------------------------------------------
    # Audit Fields
    # --------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --------------------------------------------------
    # Soft Delete
    # --------------------------------------------------
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_branches'
    )

    google_map_url = models.TextField(null=True,blank=True)

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def full_address(self):
        """
        Returns formatted full address (email & map friendly)
        """
        parts = [
            self.name,
            self.address_line,
            self.area,
            self.city,
            self.state,
            self.pincode,
        ]
        return "\n".join(filter(None, parts))


    def working_hours(self):
        if self.opening_time and self.closing_time:
            return f"{self.opening_time.strftime('%I:%M %p')} – {self.closing_time.strftime('%I:%M %p')}"
        return None

    def __str__(self):
        return f"{self.name} ({self.organization.name})"
