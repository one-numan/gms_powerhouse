from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from audits.models import AuditLog


@receiver(post_save, sender=User)
def create_or_update_user_audit(sender, instance, created, **kwargs):
    """
    Automatically create audit logs when a User is created or updated.
    """

    # 🚫 Skip raw saves (fixtures, migrations, loaddata)
    if kwargs.get('raw', False):
        return

    # Determine action type
    action = 'create' if created else 'update'

    # Organization context (may be None for superusers)
    organization = instance.organization

    AuditLog.objects.create(
        user=instance,
        organization=organization,
        action=action,
        table_name='accounts_user',
        record_id=instance.id,
        new_data={
            'username': instance.username,
            'role': instance.role,
            'is_active': instance.is_active,
        }
    )
