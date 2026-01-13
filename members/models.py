from django.db import models

INDIAN_STATES = [
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CG', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OD', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TS', 'Telangana'),
    ('TR', 'Tripura'),
    ('UK', 'Uttarakhand'),
    ('UP', 'Uttar Pradesh'),
    ('WB', 'West Bengal'),
    ('DL', 'Delhi'),
    ('JK', 'Jammu & Kashmir'),
    ('LA', 'Ladakh'),
    ('AN', 'Andaman & Nicobar Islands'),
    ('CH', 'Chandigarh'),
    ('DN', 'Dadra & Nagar Haveli and Daman & Diu'),
    ('PY', 'Puducherry'),
]



# class Member(models.Model):
#     """
#     Member represents a gym client/customer.
#     Members do NOT have login access (POC scope).
#     All member-related actions are performed by gym staff users.
#     """

#     # --- Ownership & Scope ---
#     # Each member belongs to one organization and one branch
#     organization = models.ForeignKey(
#         'organizations.Organization',
#         on_delete=models.CASCADE,
#         related_name='members',
#         db_index=True  
#     )

#     branch = models.ForeignKey(
#         'organizations.Branch',
#         on_delete=models.CASCADE,
#         related_name='members',
#         db_index=True  
#     )

#     # --- Personal Information ---
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100, blank=True, null=True)
#     mobile = models.CharField(max_length=20,db_index=True  )
#     email = models.EmailField(blank=True, null=True)

#     # --- Status ---
#     # Used to quickly enable/disable a member without deleting data
#     is_active = models.BooleanField(default=True,db_index=True  )

#     # --- Audit Fields ---
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # --- Soft Delete ---
#     # Members are never hard-deleted to preserve history
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     deleted_by = models.ForeignKey(
#         'accounts.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='deleted_members'
#     )

#     def __str__(self):
#         return f"{self.first_name} {self.last_name or ''}".strip()


from django.db import models


class Member(models.Model):
    """
    Member represents a gym client/customer.
    Members do NOT have login access.
    Profile-only information (India-friendly).
    """

    # --------------------------------------------------
    # Ownership & Scope
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Personal Information
    # --------------------------------------------------
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        blank=True,
        null=True,
        db_index=True
    )

    mobile = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(blank=True, null=True)

    # --------------------------------------------------
    # Address (India Optimized)
    # --------------------------------------------------
    address_line = models.TextField(
        blank=True,
        null=True,
        help_text="House no, street, landmark"
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
        null=True,
        db_index=True
    )

    state = models.CharField(
        max_length=2,
        choices=INDIAN_STATES,
        blank=True,
        null=True,
        db_index=True
    )

    country = models.CharField(
        max_length=50,
        default="India",
        editable=False
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------
    is_active = models.BooleanField(default=True, db_index=True)

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
        related_name='deleted_members'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()
