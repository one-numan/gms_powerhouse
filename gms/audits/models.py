from django.db import models


class AuditLog(models.Model):
    """
    AuditLog stores critical system activities for traceability.
    This helps in accountability, debugging, and future compliance.
    """

    ACTION_CHOICES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    )

    # --- Who performed the action ---
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )

    # --- Context ---
    # organization = models.ForeignKey(
    #     'organizations.Organization',
    #     on_delete=models.CASCADE,
    #     related_name='audit_logs'
    # )
    organization = models.ForeignKey(
        'organizations.Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
)

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )

    table_name = models.CharField(max_length=100)
    record_id = models.PositiveIntegerField()

    # --- Data snapshot (optional, POC-level) ---
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action.upper()} on {self.table_name} by {self.user}"
