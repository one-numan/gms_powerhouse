"""
RBAC utility helpers.

Contains role detection and scope helpers.
All RBAC decisions should use these helpers.
"""

def is_superadmin(user):
    return user.is_superuser


def is_org_manager(user):
    return getattr(user, "role", None) == "ORG_MANAGER"


def is_branch_manager(user):
    return getattr(user, "role", None) == "BRANCH_MANAGER"


def is_gym_staff(user):
    return getattr(user, "role", None) == "GYM_STAFF"


def get_user_organization(user):
    return getattr(user, "organization", None)


def get_user_branch(user):
    return getattr(user, "branch", None)
