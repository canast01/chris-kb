# Version Inventory


<div class="kb-summary">
> Part of the [Inventory](../index.md) reference.
</div>

---

```
┌───────────────────────────────────── VMware — Version Inventory ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Track product versions for all VMware components — required for LCM planning and support   │   │
│   │ Versions must be validated against the VMware Product Interoperability Matrix before upgrades │   │
│   │        HCL status: ESXi build + server model + driver version must appear on VMware HCL       │   │
│   │       Support dates: track EoGS and EoTGS per product for lifecycle and budget planning       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Core platform versions → Aria Suite versions → support and compliance status                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Core Platform        │  │          Aria Suite         │  │          Compliance         │   │
│   │       vCenter version       │  │       Aria Automation       │  │          HCL status         │   │
│   │          ESXi build         │  │       Aria Operations       │  │          EoGS date          │   │
│   │         vSAN version        │  │          Aria Logs          │  │          EoTGS date         │   │
│   │        NSX-T version        │  │           Aria LCM          │  │        Interop matrix       │   │
│   │        VxRail version       │  │         SDDC Manager        │  │         Patch level         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    EoGS components require immediate lifecycle action — unpatched = unsupported risk                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Product      │     Version      │       Build       │       EoGS       │    HCL/Notes     │   │
│   │     vCenter      │      8.0 U3      │      24022515     │     2027-10      │    Compliant     │   │
│   │       ESXi       │      8.0 U3      │      24022510     │     2027-10      │      HCL OK      │   │
│   │      NSX-T       │      4.1.2       │      23287883     │     2026-06      │   Check matrix   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: iDRAC firmware also tracked — updated via VxRail LCM bundle automatically                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    EoGS          = End of General Support; product still supported but no new features added          │
│    EoTGS         = End of Technical Guidance Support; only critical CVE patches provided              │
│    Interop matrix = VMware Product Interoperability Matrix; validates cross-product versions          │
│    HCL           = Hardware Compatibility List; ESXi build + model + driver must be listed            │
│    Build number  = Exact patch build identifier; used for support cases and HCL lookup                │
│    VxRail ver.   = Compound version: bundle includes ESXi + vCenter + iDRAC + VxRail Mgr              │
│    Patch level   = Latest applied patch; may differ from GA release version number                    │
│    SDDC Manager  = VCF LCM; must match supported version for workload domain upgrades                 │
│    LCM bundle    = VxRail single package covering all node components in one upgrade                  │
│    Interop check = Required before any upgrade; prevents incompatible version combinations            │
│    Critical CVE  = High-severity security flaw; drives emergency patching outside LCM cycle           │
│    Upgrade path  = Validated intermediate version sequence needed to reach target version             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### NSX

```text
NSX UI → System → Lifecycle Management → About NSX
```
