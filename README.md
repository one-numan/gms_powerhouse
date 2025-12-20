# gms_powerhouse

# 🏋️ Gym Fee Management System – POC

## 📌 Overview

This project is a **Proof of Concept (POC)** for a **Gym Fee & Membership Management System** designed as a **future SaaS product**.

The goal of this POC is to **digitize manual fee registers** used by gyms and demonstrate a **clean, scalable architecture** that can later support multiple gyms, branches, and roles.

---

## 🎯 Objectives of the POC

* Replace notebook / register-based fee tracking
* Maintain clear membership & payment history
* Support multi-branch gym structure
* Validate core business workflow
* Keep implementation simple and demo-ready

> ⚠️ This POC focuses on **workflow validation**, not full production security or advanced RBAC.

---

## 👥 User Types (POC Scope)

### Gym Staff Users (Login Enabled)

* Gym Owner
* Site Manager
* Gym Manager
* Staff (Reception / Cashier)

> In POC, all staff roles have **same functional access**, except delete actions.

### Gym Members (Clients)

* Do NOT log in
* Data is managed only by gym staff

---

## 🧱 Core Features (Included in POC)

✅ Add / manage gym members
✅ Define membership plans (1 month, 3 months, etc.)
✅ Assign membership to members
✅ Record payments (Cash / UPI / Card)
✅ Maintain full membership history
✅ Maintain payment history
✅ Soft delete for backup & recovery
✅ Multi-organization & multi-branch ready

---

## 🚫 Features NOT Included (Out of POC Scope)

❌ Online payments
❌ Member login / self-service
❌ Advanced role-based access control
❌ Reports & analytics
❌ GST / invoices
❌ Notifications (SMS / Email)

These are planned for **Phase-2 / Production**.

---

## 🗂️ Data Model (High Level)

```
Organization
 └── Branch
      ├── Users (Gym Owner / Staff)
      ├── Members (Clients)
      │    └── Subscriptions (Memberships)
      │         └── Payments
      └── Plans
```

---

## 🧾 Key Business Rules

* A member can have **multiple subscriptions over time**
* Only **one active subscription** is allowed per member
* Old subscriptions are **never edited**
* Plan change = **new subscription**
* Payments always belong to a subscription
* Records are **soft deleted**, never hard deleted

---

## 💳 Payment Handling (India-Focused)

Supported payment modes:

* Cash
* UPI
* Debit Card
* Credit Card
* Bank Transfer

Only **payment mode & reference ID** are stored
(No sensitive card / UPI details)

---

## 🔐 Access Control (POC Strategy)

* All staff roles have similar permissions
* Only Gym Owner can delete/deactivate records
* Data access is restricted by **branch**
* Full RBAC will be implemented in Phase-2

---

## 🛠️ Tech Stack (POC)

* Backend: Django / Flask
* Database: SQLite (POC) / MySQL (Production-ready)
* Authentication: Staff-only login
* Deployment: Local / Demo environment

---

## 🔄 Soft Delete Strategy

Instead of deleting records:

* `deleted_at` timestamp is used
* Deleted records can be restored
* Financial records (payments) are never deleted

---

## 📈 Future Enhancements (Phase-2)

* Member login & profile update requests
* Strict role-based access control (RBAC)
* Online payments & renewals
* Reports & dashboards
* Notifications & reminders
* SaaS onboarding for new gyms

---

## 🧠 Why This POC Design?

* Simple to build
* Easy to explain
* Matches real gym workflows
* Avoids overengineering
* Scales naturally to SaaS

---

## 📌 Final Note

This POC is intentionally **minimal but correct**.

> “We build the right foundation first, then add complexity only when needed.”






---

# Final Permission Matrix (RBAC)

This document defines the **final, locked Role-Based Access Control (RBAC)** for the system.
These permissions are agreed upon and should be treated as **authoritative for the POC**.

---

## Role Definitions

| Role                     | Scope                        |
| ------------------------ | ---------------------------- |
| **SuperAdmin**           | Entire system                |
| **Organization Manager** | Entire organization          |
| **Branch Manager**       | One branch (read org-wide)   |
| **Gym Staff**            | One branch (limited actions) |

---

## Organization & Branch Permissions

| Action              | SuperAdmin | Org Manager | Branch Manager | Gym Staff |
| ------------------- | ---------- | ----------- | -------------- | --------- |
| Create Organization | ✅          | ❌           | ❌              | ❌         |
| Update Organization | ✅          | ✅           | ❌              | ❌         |
| Create Branch       | ✅          | ❌           | ❌              | ❌         |
| Update Branch       | ✅          | ✅           | ❌              | ❌         |
| Delete Branch       | ✅          | ❌           | ❌              | ❌         |
| View All Branches   | ✅          | ✅           | ✅              | ❌         |

---

## User (Staff) Management

| Action        | SuperAdmin | Org Manager | Branch Manager | Gym Staff |
| ------------- | ---------- | ----------- | -------------- | --------- |
| View Users    | ✅ (All)    | ✅ (Org)     | ✅ (Org)        | ✅ (Org)   |
| Create User   | ✅          | ✅ (Org)     | ✅ (Branch)     | ❌         |
| Update User   | ✅          | ✅ (Org)     | ❌              | ❌         |
| Delete User   | ✅          | ✅ (Org)     | ❌              | ❌         |
| Assign Branch | ✅          | ✅           | ❌              | ❌         |

---

## Members (Gym Clients)

| Action        | SuperAdmin | Org Manager | Branch Manager | Gym Staff  |
| ------------- | ---------- | ----------- | -------------- | ---------- |
| View Members  | ✅          | ✅           | ✅              | ✅ (Branch) |
| Add Member    | ✅          | ✅           | ✅              | ✅ (Branch) |
| Update Member | ❌          | ❌           | ❌              | ❌          |
| Shift Branch  | ❌          | ✅           | ✅              | ❌          |
| Delete Member | ❌          | ❌           | ❌              | ❌          |

**Decision Locked:**
Members are **immutable after creation**. This is intentional and correct for the POC.

---

## Subscriptions

| Action              | SuperAdmin | Org Manager | Branch Manager | Gym Staff  |
| ------------------- | ---------- | ----------- | -------------- | ---------- |
| View Subscriptions  | ✅          | ✅           | ✅              | ✅ (Branch) |
| Create Subscription | ✅          | ✅           | ✅              | ❌          |
| Update Subscription | ✅          | ✅           | ✅              | ❌          |
| Delete Subscription | ❌          | ❌           | ❌              | ❌          |

---

## Payments

| Action              | SuperAdmin | Org Manager | Branch Manager   | Gym Staff  |
| ------------------- | ---------- | ----------- | ---------------- | ---------- |
| View Payments       | ✅          | ✅           | ✅ (All branches) | ❌          |
| Create Payment      | ❌          | ❌           | ✅                | ✅ (Branch) |
| Update Payment      | ❌          | ❌           | ✅                | ❌          |
| Soft Delete Payment | ❌          | ✅           | ❌                | ❌          |
| Hard Delete Payment | ❌          | ❌           | ❌                | ❌          |

---

## Notes

* No role is allowed to **hard delete payments**
* Members cannot be updated or deleted after creation
* Branch Managers have **read-only org visibility**
* Gym Staff actions are **strictly branch-scoped**

---

If you want, I can next:

* Map this to **API permission constants**
* Generate **DB role policies**
* Add **Mermaid RBAC diagrams** to the README
* Create **authorization middleware logic**

Just tell me.
