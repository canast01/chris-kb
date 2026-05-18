# SRM — Escalation

```
  Escalation Path
┌──────────────────────────────────────────────────────────────┐
│  Collect (both sites):                                       │
│  SRM bundle + VR bundle + SRA logs + Recovery Plan history   │
│  + vCenter events + SRM/vSphere versions                     │
│                    │                                         │
│                    ▼                                         │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ Severity Assessment                                  │     │
│  │  Sev 1 — DR failover failing ──► SR + call now      │     │
│  │  Sev 2 — DR capability degraded ──► SR 24x7         │     │
│  │  Sev 3 — One VM / test issue ──► SR biz hours       │     │
│  └─────────────────────────────────────────────────────┘     │
│                    │                                         │
│                    ▼                                         │
│  If SRA involved: open SR with VMware AND storage vendor     │
│  TAM / Critical Escalation if Sev 1 unresolved > 2 hours    │
└──────────────────────────────────────────────────────────────┘
```

---

## Before Opening a Support Case

Collect from both protected and recovery sites:

| Item | How to Collect |
|---|---|
| SRM support bundle (both sites) | Site Recovery → Summary → Download SRM Support Bundle |
| vSphere Replication bundle (both sites) | VRA VAMI → Support → Download Support Bundle |
| SRA logs (both SRM Servers) | Array-vendor specific log path (see Diagnostics page) |
| Recovery Plan execution logs | Site Recovery → Recovery Plans → [plan] → History → export |
| vCenter events for affected VMs | vCenter → Monitor → Events → filter by VM name and DR time |
| SRM version | Settings → About SRM |
| vSphere version | vCenter → About |
| SRA version | Site Recovery → Storage → Adapters |
| Array firmware version | Storage array admin UI / CLI |
| Symptom timeline | When issue started, what action triggered it, what was expected |

---

## Severity Definitions

| Severity | Condition |
|---|---|
| Sev 1 | Active DR failover in progress and SRM is failing — production systems down |
| Sev 2 | DR capability degraded — protection groups in error, replication failing, cannot run recovery |
| Sev 3 | Configuration issue, test recovery failed, one VM not protected |
| Sev 4 | General how-to question, cosmetic issue |

For Sev 1 during an active DR event: open case AND call VMware Support immediately.

---

## If SRA Vendor is Involved

If the failure involves the Storage Replication Adapter or array-side replication:
1. Open a case with VMware for SRM itself
2. **Also open a case with the storage vendor** (Pure, Dell, NetApp) for the SRA
3. Provide SRA logs to both vendors
4. VMware and the storage vendor may need to collaborate — share case numbers cross-vendor

---

## Support Portal

1. **VMware/Broadcom Support Portal:** support.broadcom.com
   - Product: VMware Site Recovery Manager
   - Version: [current version]
   - Attach: SRM support bundles from both sites, SRA logs, symptom description

2. **Call Support directly for Sev 1** — reference case number on call

---

## Escalation Path

| Escalation Level | Trigger |
|---|---|
| Technical Account Manager | Recurring issues, SLA breach |
| Critical Escalation Team | Sev 1 not resolved within 2 hours — request escalation via portal |
| SRM Engineering | Suspected SRM bug — TAM or support can escalate to engineering |
| Storage Vendor Engineering | Suspected SRA bug — escalate via storage vendor support case |

---

## Useful Resources

- SRM Documentation: docs.vmware.com/site-recovery-manager
- SRM Compatibility Matrix: interopmatrix.vmware.com
- SRM KB articles: kb.vmware.com (search "Site Recovery Manager")
- vSphere Replication KB: kb.vmware.com (search "vSphere Replication")
- Pure Storage SRA documentation: support.purestorage.com
