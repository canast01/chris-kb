---
tags:
  - powershell
  - security
description: "PowerShell access control: execution policy enforcement, JEA (Just Enough Administration) configuration, module signing requirements, and constrained..."
---
# PowerShell — Access Control

<div class="kb-summary">
PowerShell access control: execution policy enforcement, JEA (Just Enough Administration) configuration, module signing requirements, and constrained language mode.

*Applies to: PowerShell 7.x*
</div>

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## PowerShell Access Control Architecture

```d2
direction: right

user: "User / Script\n(caller" {shape: rectangle}
execPolicy: "Execution Policy\n(RemoteSigned / AllSigned" {shape: rectangle}
jea: "JEA Endpoint\n(Register-PSSessionConfiguration" {shape: rectangle}
sessionConfig: "Session Configuration\n(.pssc — restricted" {shape: rectangle}
roleCapability: "Role Capability File\n(.psrc — allowed cmdlets" {shape: rectangle}
adGroup: "AD Group Membership\n(RBAC check in code" {shape: rectangle}
svcAccount: "Service Account\n(least privilege" {shape: rectangle}
transcript: "Start-Transcript\n(audit log" {shape: rectangle}

user -> execPolicy
execPolicy -> jea
jea -> sessionConfig
sessionConfig -> roleCapability
user -> adGroup
adGroup -> svcAccount
svcAccount -> transcript
```

## Least Privilege Reference

| Principle | Implementation |
|---|---|
| Use `RemoteSigned` execution policy | Prevent unsigned remote scripts |
| Run scripts as a service account | Not as a local admin or domain admin |
| Use JEA for constrained remoting | Limit cmdlets available in remote sessions |
| Audit with `Start-Transcript` | Log all script activity |
| Check group membership in scripts | Enforce RBAC in code |

---

## See also

- [PowerShell — Authentication](../authentication/)
- [PowerShell — Hardening](../hardening/)
- [PowerShell — Encryption](../encryption/)
