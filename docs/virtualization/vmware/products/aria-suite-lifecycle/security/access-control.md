---
tags:
  - aria-lcm
  - security
  - vmware
description: "Access Control reference covering Service Account for API Automation, Separation of Duties, Auditing Access."
---
# Aria Suite Lifecycle — Access Control

<div class="kb-summary">
Access Control reference covering Service Account for API Automation, Separation of Duties, Auditing Access.

*Applies to: Aria LCM 8.x*
</div>
![Aria Suite Lifecycle — Access Control](../../../../../assets/virtualization-vmware-aria-suite-lifecycle-security-access-c.svg)

  LCM RBAC — AD Groups → LCM Roles

Assign the minimum role required for the automation task — use `LCM_CONTENT_DEVELOPER` for scripts that only query health; use `LCM_ADMIN` only for scripts that trigger upgrades or certificate replacements.

---

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Separation of Duties

Apply the principle of least privilege across team functions:

| Function | Required Role | Team |
|---|---|---|
| Deploy/upgrade Aria products | LCM Admin | Platform team lead |
| Manage Locker certificates | LCM Admin | Platform team / PKI team |
| Rotate Locker passwords | LCM Admin | Platform team |
| View environment health | Viewer | Any team |
| Extract/deploy content packs | LCM Content Developer | Operations team |
| API health monitoring | LCM Content Developer | Monitoring team (service account) |

---

## Auditing Access

LCM logs all write operations (deploy, upgrade, certificate import) to the application log. Parse for audit records:

```bash
# List all login events
grep -i "login\|authenticated\|logout" /var/log/vmware/vrlcm/lcm-app.log | \
  grep -v "health\|ping" | tail -100

# List all Locker write operations (certificate/password imports and updates)
grep -i "locker\|certificate\|password" /var/log/vmware/vrlcm/lcm-app.log | \
  grep -i "import\|update\|delete\|create" | tail -100

# List all upgrade/deploy requests with user attribution
grep -i "upgrade\|deploy\|install" /var/log/vmware/vrlcm/lcm-app.log | \
  grep -i "user\|request" | tail -100
```


```text title="Expected output"
2024-01-15T09:23:47.123Z INFO [AuthenticationManager] User 'admin@vsphere.local' authenticated successfully from 192.168.1.45
2024-01-15T09:24:12.456Z INFO [SessionManager] Login event for user 'svc-automation' - Session ID: a7f3e9c2-1b4d-4e8f-9a2c-5d6e7f8g9h0i
2024-01-15T09:45:33.789Z WARN [AuthenticationManager] Failed login attempt for user 'operator' from 192.168.1.102 - Invalid credentials
2024-01-15T10:12:05.234Z INFO [SessionManager] Logout event for user 'admin@vsphere.local' - Session duration: 1847 seconds
2024-01-15T10:33:22.567Z INFO [LockerService] Certificate import operation initiated by user 'admin@vsphere.local' - Cert ID: vmware-root-ca-2024
2024-01-15T10:33:45.891Z INFO [LockerService] Password update for credential 'vcenter-sso-bind' completed successfully
2024-01-15T10:34:12.123Z INFO [LockerService] Certificate delete operation for expired cert 'old-intermediate-ca' by user 'admin@vsphere.local'
2024-01-15T11:02:18.456Z INFO [DeploymentManager] Upgrade request submitted by user 'svc-automation' - Target version: 8.12.1, Request ID: req-2024-001847
2024-01-15T11:15:33.789Z INFO [DeploymentManager] Deploy operation for product 'vRealize Automation' initiated - User: 'admin@vsphere.local', Environment: production
2024-01-15T11:45:22.234Z INFO [InstallationService] Install request processed - Component: 'Identity Manager', User attribution: svc-automation, Status: in-progress
2024-01-15T12:03:11.567Z WARN [DeploymentManager] Upgrade rollback initiated for failed deployment req-2024-001847 by user 'admin@vsphere.local'
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /var/log/vmware/vrlcm/lcm-app.log: No such file or directory` | Verify the log file path is correct and the vRealize Lifecycle Manager service is running with `systemctl status vrlcm`. |
    | `grep: (standard input): line 1234 is too long (exceeding 32767 bytes)` | Pipe the output through `sed 's/.\{32000\}/&\n/g'` to handle extremely long log lines, or check for corrupted log entries. |
    | `tail: cannot open '/var/log/vmware/vrlcm/lcm-app.log' for reading: Permission denied` | Run the command with `sudo` or ensure your user is in the appropriate group with `groups $USER`. |
For formal audit trails, forward the LCM syslog to Aria Operations for Logs or a SIEM:

```bash
# Configure syslog forwarding from LCM appliance
# Edit /etc/rsyslog.d/lcm-remote.conf (create if not present)
echo '*.* @@vrli-prod-01.example.local:514' > /etc/rsyslog.d/lcm-remote.conf
systemctl restart rsyslog
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Failed to restart service rsyslog: Unit rsyslog.service not found.` | Verify rsyslog is installed with `apt-get install rsyslog` or `yum install rsyslog` depending on your OS. |
    | `Permission denied` | Run the commands with `sudo` or as root user since `/etc/rsyslog.d/` requires elevated privileges. |
    | `Name or service not known` | Ensure the syslog server hostname `vrli-prod-01.example.local` is resolvable; test with `nslookup vrli-prod-01.example.local` or update `/etc/hosts`. |
## See also

- [Aria Suite Lifecycle — Authentication](../authentication/)
- [Aria Suite Lifecycle — Hardening](../hardening/)
