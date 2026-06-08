# Storage — Operations

```text
┌──────────────────────────── Storage — Operations Overview ────────────────────────────────────────────┐
│                                                                                                       │
│  Operational Domain                                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐                │
│  │  Provisioning           │  │  Capacity Management    │  │  Replication Health     │                │
│  │  LUN/volume creation    │  │  pool utilisation %     │  │  lag monitoring         │                │
│  │  host registration      │  │  thin provisioning ovr  │  │  link state checks      │                │
│  │  masking / zoning       │  │  capacity forecasting   │  │  consistency group sync │                │
│  └─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘                │
│                                                                                                       │
│  Daily Operational Checks                                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Array health: check vendor management UI (Unisphere, Purity, ONTAP System Manager) — all green       │
│  Capacity: review pools > 70% used; flag any within 30 days of projected full                         │
│  Replication: confirm lag within RPO target; check for any suspended consistency groups               │
│  Snapshots: confirm scheduled snapshots ran; review retention policy compliance                       │
│  Alerts: review and triage any outstanding array event log entries from overnight                     │
│                                                                                                       │
│  GLOSSARY                                                                                             │
│  LUN        — Logical Unit Number; a block storage volume presented to a host via FC or iSCSI         │
│  Masking    — restricting which hosts can see which LUNs via host groups and masking views            │
│  Thin prov  — allocating capacity on demand rather than upfront; risk = overcommit                    │
│  RPO        — Recovery Point Objective; maximum data loss tolerance (drives replication schedule)     │
│  Consistency group — set of volumes replicated as a unit to ensure write-order consistency            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-summary">
Cross-platform storage operations — provisioning, replication health, capacity management, and operational runbooks.
</div>

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="runbooks/"><strong>Runbooks</strong><span>Operational runbooks for storage procedures.</span></a>

</div>
