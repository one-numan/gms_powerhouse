"""
RBAC (Role-Based Access Control) utilities.

This module centralizes all permission logic for the system.
Rules are based on:
- User role
- Organization scope
- Branch scope

DO NOT put permission logic in views/admin directly.
Always call these helpers.
"""

from typing import Optional
from accounts.models import User
from organizations.models import Organization, Branch


# ---------------------------------------------------------
# ROLE CHECK HELPERS
# ---------------------------------------------------------

def is_superadmin(user: User) -> bool:
    """
    SuperAdmin = Django superuser.
    Has unrestricted access across the system.
    """
    return user.is_superuser


def is_org_manager(user: User) -> bool:
    return user.role == "org_manager"


def is_branch_manager(user: User) -> bool:
    return user.role == "branch_manager"


def is_gym_staff(user: User) -> bool:
    return user.role == "staff"


# ---------------------------------------------------------
# ORGANIZATION & BRANCH SCOPE HELPERS
# ---------------------------------------------------------

def same_organization(user: User, organization: Organization) -> bool:
    """
    Check if user belongs to the same organization.
    """
    return user.organization_id == organization.id


def same_branch(user: User, branch: Branch) -> bool:
    """
    Check if user belongs to the same branch.
    """
    return user.branch_id == branch.id


# ---------------------------------------------------------
# USER (STAFF) MANAGEMENT PERMISSIONS
# ---------------------------------------------------------

def can_view_user(request_user: User, target_user: User) -> bool:
    """
    Who can VIEW users:
    - SuperAdmin: All users
    - Org Manager: Users in same organization
    - Branch Manager: Users in same organization
    - Gym Staff: Users in same organization
    """
    if is_superadmin(request_user):
        return True

    return (
        request_user.organization_id
        and request_user.organization_id == target_user.organization_id
    )


def can_create_user(request_user: User, branch: Branch) -> bool:
    """
    Who can CREATE users:
    - SuperAdmin: Anywhere
    - Org Manager: Any branch in own org
    - Branch Manager: Only own branch
    - Gym Staff: Only own branch
    """
    if is_superadmin(request_user):
        return True

    if is_org_manager(request_user):
        return same_organization(request_user, branch.organization)

    if is_branch_manager(request_user) or is_gym_staff(request_user):
        return same_branch(request_user, branch)

    return False


def can_delete_user(request_user: User, target_user: User) -> bool:
    """
    Who can DELETE users (SOFT DELETE ONLY):
    - SuperAdmin: Any user
    - Org Manager: Users in same organization
    """
    if is_superadmin(request_user):
        return True

    if is_org_manager(request_user):
        return (
            request_user.organization_id
            == target_user.organization_id
        )

    return False


# ---------------------------------------------------------
# MEMBER (GYM CLIENT) PERMISSIONS
# ---------------------------------------------------------

def can_add_member(request_user: User, branch: Branch) -> bool:
    """
    Who can ADD members:
    - SuperAdmin: Anywhere
    - Org Manager: Any branch in org
    - Branch Manager: Own branch
    - Gym Staff: Own branch
    """
    if is_superadmin(request_user):
        return True

    if is_org_manager(request_user):
        return same_organization(request_user, branch.organization)

    if is_branch_manager(request_user) or is_gym_staff(request_user):
        return same_branch(request_user, branch)

    return False


def can_update_member(request_user: User) -> bool:
    """
    Member personal details are IMMUTABLE (POC decision).
    No one can update member details after creation.
    """
    return False


# ---------------------------------------------------------
# SUBSCRIPTION PERMISSIONS
# ---------------------------------------------------------

def can_create_subscription(request_user: User, branch: Branch) -> bool:
    """
    Who can CREATE subscriptions:
    - SuperAdmin
    - Org Manager (any branch in org)
    - Branch Manager (own branch)
    """
    if is_superadmin(request_user):
        return True

    if is_org_manager(request_user):
        return same_organization(request_user, branch.organization)

    if is_branch_manager(request_user):
        return same_branch(request_user, branch)

    return False


def can_update_subscription(request_user: User, branch: Branch) -> bool:
    """
    Staff CANNOT update subscriptions.
    """
    return can_create_subscription(request_user, branch)


# ---------------------------------------------------------
# PAYMENT PERMISSIONS
# ---------------------------------------------------------

def can_create_payment(request_user: User, branch: Branch) -> bool:
    """
    Who can COLLECT payment:
    - Branch Manager (own branch)
    - Gym Staff (own branch)
    """
    if is_branch_manager(request_user) or is_gym_staff(request_user):
        return same_branch(request_user, branch)

    return False


def can_update_payment(request_user: User, branch: Branch) -> bool:
    """
    Only Branch Manager can UPDATE payment.
    """
    if is_branch_manager(request_user):
        return same_branch(request_user, branch)

    return False


def can_soft_delete_payment(request_user: User) -> bool:
    """
    Only Org Manager can SOFT DELETE payments.
    """
    return is_org_manager(request_user)


# ---------------------------------------------------------
# AUDIT LOG PERMISSIONS
# ---------------------------------------------------------

def can_view_audit_logs(request_user: User) -> bool:
    """
    Audit logs visibility:
    - SuperAdmin
    - Org Manager
    - Branch Manager
    """
    return (
        is_superadmin(request_user)
        or is_org_manager(request_user)
        or is_branch_manager(request_user)
    )
