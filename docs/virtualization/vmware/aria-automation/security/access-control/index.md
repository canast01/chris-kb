# Aria Automation — Access Control

## RBAC Model

Aria Automation uses a **project-based access control** model. All resource provisioning is scoped to a project.

### Project-Level Roles

| Role | Permissions |
|---|---|
| **Owner** | Full control over the project — manage members, cloud zones, quotas, and all deployments |
| **Member** | Can request from catalog and manage own deployments within the project |
| **Viewer** | Read-only access to deployments and catalog items in the project |

### Organisation-Level Roles

| Role | Permissions |
|---|---|
| **Administrator** | Full platform access — all projects, all infrastructure, all administration |
| **Member** | Can access projects they are assigned to |
