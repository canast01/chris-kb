# vSAN — Architecture

<div class="kb-summary">
vSAN pools local NVMe and SSD disks across ESXi hosts into a shared distributed datastore. Storage policies (RAID-1/5/6, FTT) define per-VM resilience. vSAN ESA eliminates the separate cache tier on supported hardware.
</div>

┌───────────────────────────────────────── vSAN — Architecture ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  VMware vSAN — HCI storage pooling local NVMe/SSD/HDD from ESXi hosts into a shared datastore │   │
│   │ FTT policies (RAID-1 mirroring, RAID-5/6 erasure coding) protect objects across hosts/domains │   │
│   │ Dedup and compression available in all-flash OSA; OSA (original) vs ESA (express) architecture│   │
│   │ vSAN ESA uses single-tier NVMe with compression-first; no separate cache/capacity disk groups │   │
│   │  Stretched cluster spans two sites with a witness host; SPBM storage policies enforce per-VM  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    How-it-works defines HCI storage pooling · integrations connect vSphere and management             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │      Disk groups (OSA)      │  │      vCenter: native UI     │  │       Min 3 nodes OSA       │   │
│   │      FTT/RAID policies      │  │        vSphere HA/DRS       │  │       Min 4 nodes ESA       │   │
│   │     Witness: stretch HA     │  │        NSX: microseg        │  │        FTT=1 default        │   │
│   │        Dedup+compress       │  │      File services: NFS     │  │        Cache ≥10% OSA       │   │
│   │        vSAN ESA: NVMe       │  │        HCL: hw compat       │  │       Witness: tiny VM      │   │
│   │      SPBM per-VM policy     │  │       Aria Ops adapter      │  │         25% headroom        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    How-it-works covers pooling and policies · integrations connect vCenter and NSX                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   How It Works   │   Integrations   │    Design Stds    │    Deployment    │     Key Stds     │   │
│   │   Disk groups    │  vCenter native  │    Min 3 nodes    │    All-flash     │    FTT policy    │   │
│   │  FTT/RAID tiers  │   HA/DRS intg    │    Min 4 (ESA)    │    Hybrid OSA    │    Cache 10%     │   │
│   │  Dedup/compress  │   NSX microseg   │    Witness host   │    Stretched     │   HCL required   │   │
│   │  SPBM policies   │  Aria Ops intg   │    25% headroom   │    HCI design    │     SPBM std     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers with NVMe/SSD/HDD · RAM DIMMs · 25GbE NICs · Witness host VM · ToR switches              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OSA           = Original Storage Architecture; vSAN disk groups with separate cache and capacity     │
│  ESA           = Express Storage Architecture; single-tier NVMe; compression-first; vSAN 8.0+         │
│  FTT           = Failures To Tolerate; number of host/disk failures a vSAN object can survive         │
│  RAID-5/6      = Erasure coding in vSAN; RAID-5 requires 4 hosts (1 FTT); RAID-6 needs 6 hosts (2 FTT)│
│  Disk group    = OSA unit of storage; one cache disk + 1-7 capacity disks per ESXi host               │
│  SPBM          = Storage Policy-Based Management; per-VM policy defines FTT, RAID, IOPs limits        │
│  Witness       = Lightweight VM in stretched cluster; holds metadata tie-breaker; no VM data stored   │
│  Dedup+compress = All-flash OSA feature reducing capacity footprint; applied per disk group           │
│  vSAN health   = Built-in health service in vCenter; checks HCL, network, disk, and capacity          │
│  HCL           = Hardware Compatibility List; vSAN requires HCL-certified disks, NICs, and servers    │
│  Stretched cluster = vSAN spanning two fault domains with a witness; tolerates full site failure      │
│  PFTT          = Primary Failures To Tolerate; site-level FTT setting in stretched cluster policy     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
