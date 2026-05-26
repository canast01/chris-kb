# PowerScale — Troubleshooting

┌─────────────────────────────────── Dell PowerScale Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Common faults: SyncIQ policy failure, node degraded, quota exceeded, auth errors       │   │
│   │       SyncIQ: check isi sync job; stalled replication causes RPO gap; check network path      │   │
│   │    Node degraded: drive failure triggers FlexProtect restripe; do not remove until complete   │   │
│   │       Quota: full hard quota blocks all writes; raise limit or archive data immediately       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Alert fires → isi status + event log → identify fault layer → remediate → verify health            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        SyncIQ Issues        │  │        Cluster Issues       │  │        Client Issues        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Policy stalled       │  │        Node degraded        │  │         Auth failure        │   │
│   │         RPO exceeded        │  │        Drive failure        │  │        Quota exceeded       │   │
│   │       Network blocked       │  │        FlexProt stall       │  │        NFS mount fail       │   │
│   │       Target cert err       │  │        Pool 100% full       │  │       SMB access deny       │   │
│   │        Failover stuck       │  │        Slow restripe        │  │           Slow I/O          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    isi status → event log filter → isi sync job list → isi quota list → targeted fix                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Symptom      │   First check    │      Command      │       Fix        │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   SyncIQ stall   │   Network path   │    isi sync job   │    Fix route     │  Policy errors   │   │
│   │  Node degraded   │   Drive state    │     isi status    │  Replace drive   │   Node offline   │   │
│   │    Quota full    │ Usage vs. limit  │   isi quota list  │ Raise or archive │ App writes fail  │   │
│   │   Auth failure   │  AD join state   │  isi auth status  │    Rejoin AD     │ KDC unreachable  │   │
│                                                                                                       │
│    Physical: check drive bay LEDs for failed drives; verify back-end cable for degraded node          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Policy stalled = SyncIQ job in Error or Needs Attention state; check isi sync job list             │
│    RPO exceeded   = Last successful sync older than RPO target; data loss risk if source fails        │
│    FlexProt stall = FlexProtect restripe paused; pool too full to complete; free capacity first       │
│    Pool 100% full = All usable space consumed; SmartPool migration and FlexProtect both stall         │
│    isi auth status= Show AD/LDAP provider join state and Kerberos ticket validity                     │
│    KDC unreachable= Kerberos Key Distribution Center offline; all Kerberos auth fails                 │
│    Target cert err= SyncIQ TLS cert mismatch between source and target; regenerate cert               │
│    NFS mount fail = Check export policy in access zone; confirm client IP in export client list       │
│    SMB access deny= Check share permissions and ACL in access zone; confirm AD group membership       │
│    Slow restripe  = FlexProtect running; I/O throttled; normal behavior after node/drive event        │
│    Failover stuck = SyncIQ failover did not complete; check allow_writes on target policy             │
│    isi quota list = Show quota usage; -v for details; identify directory exceeding hard limit         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────── Dell PowerScale Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Common faults: SyncIQ policy failure, node degraded, quota exceeded, auth errors       │   │
│   │       SyncIQ: check isi sync job; stalled replication causes RPO gap; check network path      │   │
│   │    Node degraded: drive failure triggers FlexProtect restripe; do not remove until complete   │   │
│   │       Quota: full hard quota blocks all writes; raise limit or archive data immediately       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Alert fires → isi status + event log → identify fault layer → remediate → verify health            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        SyncIQ Issues        │  │        Cluster Issues       │  │        Client Issues        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Policy stalled       │  │        Node degraded        │  │         Auth failure        │   │
│   │         RPO exceeded        │  │        Drive failure        │  │        Quota exceeded       │   │
│   │       Network blocked       │  │        FlexProt stall       │  │        NFS mount fail       │   │
│   │       Target cert err       │  │        Pool 100% full       │  │       SMB access deny       │   │
│   │        Failover stuck       │  │        Slow restripe        │  │           Slow I/O          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    isi status → event log filter → isi sync job list → isi quota list → targeted fix                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Symptom      │   First check    │      Command      │       Fix        │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   SyncIQ stall   │   Network path   │    isi sync job   │    Fix route     │  Policy errors   │   │
│   │  Node degraded   │   Drive state    │     isi status    │  Replace drive   │   Node offline   │   │
│   │    Quota full    │ Usage vs. limit  │   isi quota list  │ Raise or archive │ App writes fail  │   │
│   │   Auth failure   │  AD join state   │  isi auth status  │    Rejoin AD     │ KDC unreachable  │   │
│                                                                                                       │
│    Physical: check drive bay LEDs for failed drives; verify back-end cable for degraded node          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Policy stalled = SyncIQ job in Error or Needs Attention state; check isi sync job list             │
│    RPO exceeded   = Last successful sync older than RPO target; data loss risk if source fails        │
│    FlexProt stall = FlexProtect restripe paused; pool too full to complete; free capacity first       │
│    Pool 100% full = All usable space consumed; SmartPool migration and FlexProtect both stall         │
│    isi auth status= Show AD/LDAP provider join state and Kerberos ticket validity                     │
│    KDC unreachable= Kerberos Key Distribution Center offline; all Kerberos auth fails                 │
│    Target cert err= SyncIQ TLS cert mismatch between source and target; regenerate cert               │
│    NFS mount fail = Check export policy in access zone; confirm client IP in export client list       │
│    SMB access deny= Check share permissions and ACL in access zone; confirm AD group membership       │
│    Slow restripe  = FlexProtect running; I/O throttled; normal behavior after node/drive event        │
│    Failover stuck = SyncIQ failover did not complete; check allow_writes on target policy             │
│    isi quota list = Show quota usage; -v for details; identify directory exceeding hard limit         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Quick reference for common problems and resolutions.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic procedures and log analysis.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Vendor escalation procedures and support contacts.</span>
</a>

</div>
