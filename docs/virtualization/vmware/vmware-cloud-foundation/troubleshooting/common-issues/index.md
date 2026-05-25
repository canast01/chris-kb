# VCF Troubleshooting — Common Issues

```text
VCF Common Failure Points — Quick Reference
┌─────────────────────────────────────────────────────┐
│  Symptom                 → Primary Check            │
├─────────────────────────────────────────────────────┤
│  Domain Warning/Error    → SDDC Mgr Dashboard       │
│                            expand domain view       │
├─────────────────────────────────────────────────────┤
│  LCM upgrade stuck       → SDDC Mgr → Tasks         │
│                            /vcf/lcm/lcm-debug.log   │
├─────────────────────────────────────────────────────┤
│  Certificate expiry warn → SDDC Mgr → Security      │
│                            → Certificate Mgmt       │
├─────────────────────────────────────────────────────┤
│  NSX transport degraded  → NSX Mgr → Fabric/Nodes   │
│                            check NSX agent on ESXi  │
├─────────────────────────────────────────────────────┤
│  BGP peer down           → NSX Mgr → Networking     │
│                            → Tier-0 → BGP           │
├─────────────────────────────────────────────────────┤
│  SDDC Manager disk full  → SSH: df -h               │
│                            archive /nfs/.../bundles  │
├─────────────────────────────────────────────────────┤
│  Password rotation fail  → SDDC Mgr → Security      │
│                            → Credentials → status   │
├─────────────────────────────────────────────────────┤
│  Bundle download fail    → depot.vmware.com reachable│
│                            proxy/firewall check      │
└─────────────────────────────────────────────────────┘
```

## Health Check Triage

VCF health checks across SDDC Manager, vCenter, NSX, ESXi, and workload domains.

### Daily Checks

| Check | Command | Notes |
|---|---|---|
| Review active alarms. |  |  |
| Check recent failed tasks. |  |  |
| Confirm service health. |  |  |
| Confirm capacity and performance are normal. |  |  |
| Check recent changes. |  |  |

### Health Commands

```bash
# Add environment-specific commands here
```

### Common Issues

- Failed or stuck tasks.
- Certificate, DNS, or authentication issues.
- Capacity pressure.
- Service health warnings.
- Version mismatch after maintenance.
- Monitoring gaps.

### Operational Tasks

| Task | Command |
|---|---|
| Review alarms and events. |  |
| Confirm ownership and support notes. |  |
| Validate dependencies. |  |
| Document changes. |  |
| Confirm monitoring coverage. |  |

---

## Technical Deep Dive

VMware Cloud Foundation provides an integrated private cloud stack using SDDC Manager to manage vSphere, vSAN, NSX, workload domains, lifecycle, and credentials.

### Platform Role

VMware Cloud Foundation provides an integrated private cloud stack using SDDC Manager to manage vSphere, vSAN, NSX, workload domains, lifecycle, and credentials.

### Core Components

- SDDC Manager
- Management domain
- Workload domains
- vCenter
- ESXi
- vSAN
- NSX
- Lifecycle Manager
- Password and certificate management
- Bundle repository

### Main Dependencies

- DNS resolution
- NTP/time sync
- Authentication source
- Management network
- Storage access
- Certificate trust
- Monitoring
- Backup/recovery process
- Vendor support access

### Ports and Protocols

| Use | Protocol | Port |
|-----|----------|------|
| SDDC Manager UI/API | HTTPS | 443 |
| vCenter | HTTPS | 443 |
| NSX Manager | HTTPS | 443 |
| ESXi host management | HTTPS | 443 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |

### Key Logs

- SDDC Manager logs
- Lifecycle operation logs
- vCenter logs
- NSX Manager logs
- ESXi host logs
- Bring-up logs

### Health Checks

- Confirm management access.
- Review current alarms.
- Review recent failed tasks.
- Validate DNS and NTP.
- Confirm certificate status.
- Check service health.
- Check capacity and performance.
- Confirm monitoring data is current.
- Review recent changes.

### Useful Commands

```bash
systemctl status lcm
systemctl status domainmanager
systemctl status operationsmanager
systemctl status commonsvcs
df -h
journalctl -xe
```

### Common Failure Points

- Lifecycle bundle issue
- Compatibility mismatch
- Password drift
- Certificate drift
- Workload domain health issue
- SDDC Manager service issue
- NSX/vCenter dependency failure
- DNS/NTP issue

### Troubleshooting Workflow

1. Confirm the impact and scope.
2. Check recent changes.
3. Review alerts, tasks, and events.
4. Validate DNS, NTP, authentication, and certificates.
5. Check service status.
6. Check storage and network dependencies.
7. Review logs.
8. Capture screenshots, timestamps, errors, and task IDs.
9. Escalate with clean evidence if needed.

### Upgrade and Compatibility Notes

- Check product interoperability before upgrades.
- Confirm supported version path.
- Confirm backup or rollback method.
- Confirm maintenance window.
- Run pre-checks before change work.
- Validate health after the change.
- Document version before and after.

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep versions aligned. | Keep versions aligned. |
| Keep certificates tracked. | Keep certificates tracked. |
| Keep DNS and NTP clean. | Keep DNS and NTP clean. |
| Keep alerting actionable. | Keep alerting actionable. |
| Document support ownership. | Document support ownership. |
| Avoid undocumented changes. | Avoid undocumented changes. |
