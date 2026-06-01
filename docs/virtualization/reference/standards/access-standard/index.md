# Access Standard


<div class="kb-summary">
Access Standard reference covering Overview, Core Principles, vCenter Role Definitions, AD Group Mapping, Service Accounts and 5 more sections.
</div>

```
┌────────────────────────────────────── vSphere — Access Standard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Access standard governing authentication, authorisation, and audit for the vSphere platform  │   │
│   │  All management access via vCenter SSO backed by Active Directory; direct host access blocked │   │
│   │ Three-tier RBAC: Administrator / Operator (custom role) / Read-only; no built-in admin sharing│   │
│   │     Service accounts: one per integration, least-privilege, vault-stored, rotated 90 days     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gate → authorisation scope → audit trail for all management actions                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Authorisation        │  │            Audit            │   │
│   │       vCenter SSO + AD      │  │      Administrator role     │  │        vCenter events       │   │
│   │       MFA enforcement       │  │      Operator (custom)      │  │       iDRAC audit log       │   │
│   │        Lockdown mode        │  │        Read-only role       │  │        Syslog to SIEM       │   │
│   │       Service accounts      │  │      Scope: DC/cluster      │  │        Login attempts       │   │
│   │       Break-glass acct      │  │       Least privilege       │  │         Role changes        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All three pillars required: no auth without logging, no access without defined role                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Access tier    │   Auth method    │    vCenter role   │      Scope       │   Review freq    │   │
│   │  Administrator   │  SSO + AD + MFA  │   Administrator   │    Datacenter    │    Quarterly     │   │
│   │     Operator     │  SSO + AD + MFA  │  Custom ops role  │     Cluster      │    Quarterly     │   │
│   │    Read-only     │     SSO + AD     │     Read-only     │    Datacenter    │      Annual      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ESXi hosts in lockdown mode; iDRAC on OOB VLAN; vCenter on management cluster            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    vCenter SSO   = Single Sign-On; authentication broker for vCenter and connected services           │
│    Lockdown mode = ESXi blocks direct SSH/shell; all access via vCenter API path only                 │
│    RBAC          = Role-Based Access Control; vCenter permissions assigned via role+scope             │
│    Administrator = Full vCenter access; restricted to named infra team members only                   │
│    Operator role = Custom role with write permissions scoped to specific operations                   │
│    Read-only     = No changes; appropriate for monitoring and helpdesk triage access                  │
│    Service acct  = Non-human account for tool integration; one per tool, least-privilege              │
│    Break-glass   = Emergency admin stored in vault; retrieved on MFA failure or lockout               │
│    Least priv.   = Grant only the minimum permissions required for the role to function               │
│    Propagate     = vCenter permission flag that applies a role to all child objects too               │
│    Scope         = vCenter object level where permission is assigned: DC, cluster, folder             │
│    SIEM          = Security Information and Event Management; receives vSphere syslog events          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Standards](../index.md) reference.

---

## Overview

This standard defines how access to the vSphere environment is granted, managed, and reviewed. The principle of least privilege applies. All access is granted via AD group membership mapped to vCenter roles — no direct user-to-object permission assignments.

## Core Principles

- **No direct ESXi host logins in production.** All administration is performed through vCenter. ESXi SSH access is break-glass only.
- **No shared accounts.** All access is tied to individual named accounts.
- **AD group mapping only.** Do not assign permissions directly to individual users in vCenter.
- **Least privilege.** Grant the minimum role required for the task.
- **Regular audit.** Access is reviewed quarterly.

## vCenter Role Definitions

| Role Name | Permissions | Assigned To |
|---|---|---|
| `vcenter-admin` | Full vCenter Administrator | AD group: `grp-vsphere-admins` |
| `vcenter-vm-operator` | Power on/off, console, snapshot management | AD group: `grp-vsphere-vm-operators` |
| `vcenter-read-only` | View all objects, no changes | AD group: `grp-vsphere-readonly` |
| `vcenter-network-admin` | Manage port groups and vDS | AD group: `grp-vsphere-network` |
| `vcenter-storage-admin` | Manage datastores and storage policies | AD group: `grp-vsphere-storage` |
| `vcenter-backup-operator` | Role required by backup service account (Veeam) | Service account only |

Use the built-in `Administrator` role only for the vCenter appliance itself. Do not map AD groups to the built-in Administrator role.

## AD Group Mapping

Map AD groups to vCenter in: **vCenter** → **Administration** → **Access Control** → **Global Permissions**

Or at the vCenter object level for scoped permissions:
**vCenter** → **Hosts and Clusters** → select object → **Permissions** tab → **Add**

Always propagate permissions to child objects unless there is a specific reason not to.

## Service Accounts

| Service Account | Purpose | Role | Password Rotation |
|---|---|---|---|
| `svc-veeam-vcenter` | Veeam backup integration | `vcenter-backup-operator` | Annual, stored in CyberArk |
| `svc-ariaops-vcenter` | Aria Operations vCenter adapter | Read-Only + additional stats | Annual, stored in CyberArk |
| `svc-automation-vcenter` | Aria Automation / Terraform | Limited admin (scoped) | Annual, stored in CyberArk |

All service account passwords are stored in CyberArk. Service accounts do not have interactive login rights to any system other than their target service.

## ESXi Host Access

| Access Type | Policy |
|---|---|
| Root account | Password set per standard, stored in CyberArk. Used for break-glass only. |
| SSH | Disabled by default. Enable only with a change record. Disable immediately after use. |
| ESXi Shell (console) | Disabled by default. Same policy as SSH. |
| Lockdown Mode | Normal Lockdown Mode enabled on all production hosts. |
| Direct host login | Not permitted in production without a change record. |

Lockdown Mode prevents direct host access and routes all management through vCenter. ESXi Shell and SSH must be re-disabled within 1 hour of use.

## Break-Glass Access

For critical incidents where vCenter is unavailable and direct ESXi access is required:

1. Raise a P1 incident or emergency change record
2. Retrieve root credentials from CyberArk (requires approval workflow)
3. Enable SSH via DCUI (if no console access, use iDRAC/iLO)
4. Perform required recovery steps
5. Disable SSH immediately after
6. Document all actions in the incident record
7. Rotate root credentials after break-glass use

## NSX Access

| Role | Description | AD Group |
|---|---|---|
| Enterprise Admin | Full NSX administration | `grp-nsx-admins` |
| Network Engineer | Network configuration (no security policies) | `grp-nsx-network` |
| Security Engineer | Security policies and firewall rules | `grp-nsx-security` |
| Auditor | Read-only access | `grp-nsx-readonly` |

## Access Review Cadence

| Review | Frequency | Owner |
|---|---|---|
| vCenter role membership (AD groups) | Quarterly | Infra Team Lead |
| Service account permissions | Semi-annual | Infra + Security Team |
| Break-glass account rotation | Annual (or after each use) | Infra Team |
| NSX role membership | Quarterly | Network Team Lead |

Access review findings must be documented. Unused accounts or excessive permissions must be remediated within 14 days.

## Access Request Process

1. Requestor submits a ServiceNow access request with justification and required role
2. Team lead approves
3. AD group membership updated by the AD team
4. Access confirmed in vCenter
5. Request record closed with evidence
