# FlashArray — Design Standards


<div class="kb-summary">
FlashArray — Design Standards reference.
</div>

FlashArray Design Checklist — Key Areas
```text
```
```
┌────────────────────────────────── Pure FlashArray Design Standards ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          FlashArray Design Standards — Naming, Zoning, Host Config, Capacity Planning         │   │
│   │    Naming: array-name, volume, host, hgroup follow site-consistent lowercase-hyphen scheme    │   │
│   │       FC zoning: single-initiator / single-target; each HBA port zoned to one array port      │   │
│   │        Host connect: create host, add WWN/IQN, add to hgroup, connect volume to hgroup        │   │
│   │     Capacity: provision at 2x data-reduction estimate; alert threshold 80% array capacity     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Standards ensure consistent deployments across sites and reduce operational errors                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Naming and Zoning Standards          │  │       Capacity and Performance Design       │   │
│   │        Volume: appname-function-lun01        │  │         Target data reduction: 4:1+         │   │
│   │          Host: hostname matches DNS          │  │          Provision: 2x DR estimate          │   │
│   │         hgroup: cluster or app group         │  │        Alert: 80% capacity threshold        │   │
│   │         FC zone: SI-ST per HBA port          │  │         QoS: bandwidth + IOPS limits        │   │
│   │        iSCSI: CHAP + portal per port         │  │         Snap retention: 24h/7d/4w/1y        │   │
│   │           PG: one PG per app tier            │  │        Volume size: multiples of 1 TB       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Consistent naming and single-initiator zoning are the two most impactful design decisions          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Volume Design   │   Host Design    │     FC Zoning     │    PG Design     │    Monitoring    │   │
│   │ 512-byte aligned │1 host per hgroup │  SI-ST mandatory  │   1 PG per app   │ Pure1 DR metric  │   │
│   │ Thin: no reserve │WWNs per HBA port │  Zone activation  │ Hourly schedule  │ Capacity alerts  │   │
│   │ Limit QoS shared │iSCSI: 2+ portals │ Alias hostname_p1 │ Retain: 24 snaps │  Latency < 1 ms  │   │
│   │LUN ID consistent │  MPIO multipath  │    Verify login   │Target: remote PG │purearray monitor │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FlashArray pair · FC director switches · iSCSI ToR switches · ESXi/bare-metal hosts · Pure1 portal   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SI-ST zoning  = Single-Initiator/Single-Target; best practice FC zoning reduces blast radius         │
│  hgroup        = Host group; collection of hosts sharing access to the same volumes                   │
│  Protection Group= PG; volumes/hosts replicated together on schedule; one PG per application          │
│  Data reduction= Ratio of written logical data to physical flash used; 4:1 typical on VMs             │
│  QoS limits    = Per-volume IOPS/bandwidth cap; set with purevolume setattr --iops-limit              │
│  CHAP          = Challenge Handshake Auth Protocol; iSCSI authentication between host and array       │
│  MPIO          = Multipath I/O; host multipath driver balances I/O across multiple array ports        │
│  Thin provision= Volume allocated on demand; no physical flash reserved until data is written         │
│  Snap retention= Schedule of snapshots kept: hourly, daily, weekly, monthly, yearly counts            │
│  Portal        = iSCSI target endpoint; IP:port on array for iSCSI initiator discovery                │
│  WWN           = World Wide Name; 64-bit FC identifier for initiator HBA port and target port         │
│  Pure1 DR      = Pure1 shows data-reduction ratio per array; used to validate design targets          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

For Linux DM-Multipath, use the Pure Storage recommended `multipath.conf` settings (available from Pure Support): `path_grouping_policy multibus`, `path_checker tur`, `failback immediate`, `no_path_retry 18`.
