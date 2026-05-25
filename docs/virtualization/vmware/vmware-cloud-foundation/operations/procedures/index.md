# VCF — Procedures

```text
VCF Operational Procedures — Decision Map
┌─────────────────────────────────────────────────────┐
│  Routine Operations                                 │
└──────┬───────────────┬────────────────┬─────────────┘
       │               │                │
       ▼               ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌────────────────┐
│ Patching /   │ │ Password     │ │ Certificate       │
│ Upgrading    │ │ Management   │ │ Management        │
│              │ │              │ │                   │
│ SDDC Mgr     │ │ SDDC Mgr     │ │ SDDC Mgr          │
│ → LCM        │ │ → Security   │ │ → Security        │
│ → Upgrade    │ │ → Password   │ │ → Certificate     │
│              │ │   Management │ │   Management      │
│ Order:       │ │              │ │                   │
│ SDDC Mgr     │ │ Rotate via   │ │ Generate CSR      │
│ → vCenter    │ │ SDDC Mgr     │ │ → sign → import   │
│ → ESXi       │ │ (not direct  │ │                   │
│ → NSX → vSAN │ │ in product)  │ │ Order:            │
│              │ │              │ │ SDDC Mgr          │
│ Pre-check    │ │ Update vault │ │ → vCenter         │
│ first!       │ │ after rotate │ │ → NSX → ESXi      │
└──────────────┘ └──────────────┘ └────────────────┘
```

## Lifecycle Management (Patching)

All VCF component upgrades must go through SDDC Manager LCM. Patching components independently breaks the BOM alignment and can block future LCM upgrades.

**Pre-upgrade checklist:**

- [ ] All workload domains healthy in SDDC Manager
- [ ] No active critical alarms in vCenter or NSX Manager
- [ ] vSAN Skyline Health shows no critical issues
- [ ] SDDC Manager backup completed successfully within 24 hours
- [ ] BOM compatibility confirmed — check VCF release notes for target version
- [ ] Maintenance window scheduled with change management

**Upgrade order within a VCF release:**

1. SDDC Manager itself (if being upgraded)
2. Management domain: vCenter → ESXi → vSAN → NSX (in BOM order)
3. Workload domains (in order)

```text
SDDC Manager → Lifecycle Management → Upgrade → select target bundle → run pre-check → schedule
```

## SDDC Manager Backup

```text
SDDC Manager → Administration → Backup → Configure (SFTP target recommended)
```

- Schedule: daily; retain at least 7 restore points
- On-demand: `SDDC Manager → Administration → Backup → Backup Now`

## Password Management

```text
SDDC Manager → Security → Password Management
```

**Break-glass rotation procedure:**

1. Retrieve the break-glass account password from the enterprise vault
2. Rotate in SDDC Manager → Password Management
3. Update the vault entry immediately
4. Log the rotation in the change management system

## Useful Log Locations

| Component | Log Path |
|---|---|
| SDDC Manager | `/var/log/vmware/vcf/sddc-manager/` |
| LCM service | `/var/log/vmware/vcf/lcm/` |
| Domain manager | `/var/log/vmware/vcf/domainmanager/` |
| NSX Manager | NSX Manager UI → System → Support Bundle |
| ESXi (per host) | `/var/log/hostd.log`, `/var/log/vmkernel.log` |
