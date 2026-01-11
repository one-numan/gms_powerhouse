"""
RBAC permission definitions.

This file defines:
- Roles
- High-level permission names
- Central permission matrix

NO Django imports here.
"""

# ---- ROLE CONSTANTS ----
ROLE_SUPERADMIN = "superadmin"
ROLE_ORG_MANAGER = "org_manager"
ROLE_BRANCH_MANAGER = "branch_manager"
ROLE_GYM_STAFF = "gym_staff"


# ---- PERMISSION NAMES ----
PERM_VIEW = "view"
PERM_CREATE = "create"
PERM_UPDATE = "update"
PERM_DELETE = "delete"
PERM_SOFT_DELETE = "soft_delete"
PERM_COLLECT_PAYMENT = "collect_payment"
PERM_UPDATE_PAYMENT = "update_payment"


# ---- PERMISSION MATRIX ----
# Format:
# { role: { resource: [allowed_permissions] } }

RBAC_MATRIX = {
    ROLE_SUPERADMIN: {
        "organization": [PERM_VIEW, PERM_CREATE, PERM_UPDATE, PERM_DELETE],
        "branch": [PERM_VIEW, PERM_CREATE, PERM_UPDATE, PERM_DELETE],
        "user": [PERM_VIEW, PERM_CREATE, PERM_UPDATE, PERM_DELETE],
        "member": [PERM_VIEW, PERM_CREATE],
        "subscription": [PERM_VIEW, PERM_CREATE, PERM_UPDATE],
        "payment": [PERM_VIEW],
        "audit": [PERM_VIEW],
    },

    ROLE_ORG_MANAGER: {
        "organization": [PERM_VIEW, PERM_UPDATE],
        "branch": [PERM_VIEW, PERM_UPDATE],
        "user": [PERM_VIEW, PERM_CREATE, PERM_DELETE],
        "member": [PERM_VIEW, PERM_CREATE],
        "subscription": [PERM_VIEW, PERM_UPDATE],
        "payment": [PERM_VIEW, PERM_SOFT_DELETE],
        "audit": [PERM_VIEW],
    },

    ROLE_BRANCH_MANAGER: {
        "branch": [PERM_VIEW],
        "user": [PERM_VIEW, PERM_CREATE, PERM_DELETE],
        "member": [PERM_VIEW, PERM_CREATE],
        "subscription": [PERM_VIEW, PERM_UPDATE],
        "payment": [PERM_VIEW, PERM_COLLECT_PAYMENT, PERM_UPDATE_PAYMENT],
        "audit": [PERM_VIEW],
    },

    ROLE_GYM_STAFF: {
        "user": [PERM_VIEW],
        "member": [PERM_VIEW, PERM_CREATE],
        "subscription": [PERM_VIEW],
        "payment": [PERM_COLLECT_PAYMENT],
    },
}
