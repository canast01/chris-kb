# vCenter Security — Hardening

## Hardening Baseline

Follow the **VMware vSphere Security Configuration Guide (SCG)** published by Broadcom for the specific vSphere version. Key controls:

| Control | Setting |
|---|---|
| Restrict Shell access | Disable ESXi Shell except during maintenance |
| Lockdown Mode | Enable Normal or Strict Lockdown on all ESXi hosts |
| vCenter admin accounts | Named accounts only; no shared `administrator@vsphere.local` |
| API access | Restrict API access to management jump hosts (firewall rules) |
| NTP | Synchronised on all vCenter and ESXi nodes |
| Unused services | Disable unused vCenter plugins (e.g., legacy Web Client if not needed) |
| VAMI access | Restrict port 5480 access to admin subnets |
| TLS minimum | 1.2 enforced; verify with `tls-reconfigurator` tool if upgrading from older versions |

## Audit Logging

### vCenter Events and Tasks

All configuration changes in vCenter generate events viewable at **Monitor → Events**. Default retention: 30 days for tasks, 30 days for events.

### Syslog Forwarding to SIEM

```
VAMI (https://<vcenter>:5480) → Syslog → Add Syslog Server
Protocol: TLS (preferred) / UDP / TCP
Port: 514 (UDP), 6514 (TLS)
```

Events forwarded include: login/logout, permission changes, VM creation/deletion, host add/remove.

### Alarms for Security Events

Create vCenter alarms for:
- Failed login attempts (event: `com.vmware.sso.LoginFailure`)
- Permission additions/removals
- Certificate expiry (< 30 days)
- SSH enabled on ESXi host

## SSO Password Policy

Configure at **Administration → Single Sign On → Configuration → Policies → Password Policy**:

| Parameter | Recommended Value |
|---|---|
| Maximum lifetime | 90 days |
| Minimum length | 16 characters |
| Complexity | Uppercase + lowercase + digits + special |
| Lockout (failed attempts) | 5 attempts |
| Lockout duration | 5 minutes |

## vCenter Configuration Checklist

- [ ] NTP configured (at least 2 sources, matching ESXi host NTP)
- [ ] DNS forward/reverse resolution working for all hosts
- [ ] Syslog forwarding configured to log aggregator
- [ ] SMTP relay configured for alarm notifications
- [ ] vCenter backup schedule configured and validated
- [ ] Certificate validity checked (>90 days remaining)
- [ ] SSO lockout policy set (5 failed attempts, 5-minute lockout)
- [ ] Default admin account password rotated per policy
- [ ] Alarm definitions reviewed and recipients set
- [ ] vSphere tags applied to all VMs (env, tier, owner)
- [ ] Resource pools created; default pool empty
- [ ] DRS and HA enabled on all production clusters

## ESXi Host Hardening (Managed via vCenter)

| Control | Action |
|---|---|
| Lockdown Mode | Enable Normal Lockdown on all production hosts |
| SSH | Disable when not in use; enable only for break-glass |
| ESXi Shell | Disable when not in use |
| UEFI Secure Boot | Enable in BIOS before ESXi install |
| Firewall rules | Restrict management access to admin subnets |
| Host profiles | Use to enforce consistent security settings across cluster |

Apply hardening consistently across all hosts using Host Profiles: **vCenter → Policies and Profiles → Host Profiles**.
