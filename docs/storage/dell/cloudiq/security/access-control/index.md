# CloudIQ — Access Control

> Part of the [CloudIQ](../../) reference.

---

CloudIQ provides role-based access control to limit what each user can view and modify.

| Role | Permissions |
|---|---|
| CloudIQ Admin | Full access: manage users, roles, notification rules, API credentials, and all system data |
| System Admin | Manage and view assigned systems; cannot manage users or global settings |
| Viewer | Read-only access to dashboards, health scores, capacity, and alerts; cannot modify settings or acknowledge alerts |

Assign roles under **Settings > Users**. Apply the principle of least privilege — most operational users should be Viewer or System Admin; CloudIQ Admin should be restricted to a small number of named individuals.
