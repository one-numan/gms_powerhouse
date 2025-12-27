"""
Reusable Django Admin RBAC mixins.

These mixins enforce:
- Data visibility (querysets)
- Permissions (add/change/delete)

Usage:
class MyAdmin(RBACQuerysetMixin, RBACPermissionMixin, admin.ModelAdmin):
    ...
"""

from django.core.exceptions import PermissionDenied

from core.rbac.utils import (
    is_superadmin,
    is_org_manager,
    is_branch_manager,
    is_gym_staff,
    get_user_organization,
    get_user_branch,
)


class RBACQuerysetMixin:
    """
    Restricts queryset visibility based on user role.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        # SuperAdmin sees everything
        if is_superadmin(user):
            return qs

        # Organization-scoped visibility
        if hasattr(qs.model, "organization_id"):
            return qs.filter(organization=get_user_organization(user))

        # Branch-scoped visibility
        if hasattr(qs.model, "branch_id"):
            return qs.filter(branch=get_user_branch(user))

        return qs.none()


class RBACPermissionMixin:
    """
    Restricts add / change / delete permissions based on role.
    """

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return is_superadmin(request.user) or is_org_manager(request.user) or is_branch_manager(request.user)

    def has_change_permission(self, request, obj=None):
        return is_superadmin(request.user) or is_org_manager(request.user) or is_branch_manager(request.user)

    def has_delete_permission(self, request, obj=None):
        # Only SuperAdmin & Org Manager can delete (soft delete logic later)
        return is_superadmin(request.user) or is_org_manager(request.user)
