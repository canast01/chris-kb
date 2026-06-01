# VCF Troubleshooting — Common Issues


<div class="kb-summary">
Common Issues reference covering Common Issues, Technical Deep Dive.
</div>

VCF Common Failure Points — Quick Reference
```text
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
┌─────────────────────────────── VMware Cloud Foundation — Common Issues ───────────────────────────────┐
│                                                                                                       │
│  Common VCF issues: upgrade task failures, credential rotation stuck, domain                          │
│  commission failures, certificate expiry, and SDDC Manager service outages.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Upgrade Task Failures             │  │              Credential Issues              │   │
│   │          Pre-check fails: fix first          │  │          Rotation stuck: check logs         │   │
│   │          Upgrade paused: check task          │  │          Service account locked out         │   │
│   │         Remediate: retry failed step         │  │          Fix: unlock in AD + retry          │   │
│   │        Rollback: snapshot (if taken)         │  │          Manual rotation: PowerVCF          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Pre-check failures must be resolved before applying any upgrade bundle.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Commission & Domain Issues          │  │             SDDC Manager Issues             │   │
│   │          Host commission fails: DNS          │  │          UI unreachable: check svc          │   │
│   │       Domain create stuck: check tasks       │  │           Restart: service-control          │   │
│   │        Cert error: renew via SDDC Mgr        │  │           DB issue: check Postgres          │   │
│   │         VCF HCL: hardware not listed         │  │          Disk full: purge old logs          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Most VCF failures trace to DNS, NTP, network connectivity, or certificate expiry;                    │
│  check all four before raising a GSS SR.                                                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Pre-check     = automated validation; fixes required before upgrade                                  │
│  Remediate     = retry a failed upgrade task step in SDDC Mgr                                         │
│  Rollback      = restore snapshot taken before upgrade attempt                                        │
│  Credential rotation= SDDC Mgr updates service passwords; may time out                                │
│  Commission    = add host to free pool; requires DNS + HCL validation                                 │
│  VCF HCL       = VCF-specific HCL; server + NIC + disk must all be listed                             │
│  service-control= restart SDDC Manager services on appliance shell                                    │
│  Postgres      = SDDC Manager embedded DB; full = service crash                                       │
│  Log purge     = delete old SDDC Mgr logs when disk >80%                                              │
│  DNS failure   = most common commission failure; check A + PTR                                        │
│  Task view     = SDDC Mgr Inventory > Tasks; shows stuck operations                                   │
│  Cert expiry   = check SDDC Mgr Certificates tab; renew >30d ahead                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
