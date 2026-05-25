# APEX Storage as a Service — Install & Upgrade

```
┌──────────────────────────────────── Dell Apex STaaS — Onboarding ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Apex onboarding: site preparation, Dell hardware install, host connection, go-live      │   │
│   │       Site prep (customer): rack space, power (kVA), cooling, network drops, OOB access       │   │
│   │     Dell FSE installs hardware, initialises array, deploys SCG; customer does NOT touch HW    │   │
│   │         Customer: configure iSCSI VLANs or FC zoning, install multipath, connect hosts        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Contract → site prep → Dell install → network config → host connect → validate → go-live           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Site Prep          │  │         Dell Install        │  │         Host Connect        │   │
│   │          Rack space         │  │        Rack and cable       │  │          iSCSI VLAN         │   │
│   │         Power (kVA)         │  │          Array init         │  │          FC zoning          │   │
│   │           Cooling           │  │          SCG deploy         │  │          Multipath          │   │
│   │        Network drops        │  │         CloudIQ link        │  │        Initiator reg.       │   │
│   │        OOB management       │  │         Apex Console        │  │           Test I/O          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Apex expands (scale-out) are also Dell-managed; customer opens SR; Dell adds capacity              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Phase       │      Owner       │        Task       │    Milestone     │      Notes       │   │
│   │    Site prep     │     Customer     │     Rack/power    │   Ready cert.    │   Before ship    │   │
│   │     Install      │     Dell FSE     │     HW + init     │    SCG green     │     1–2 days     │   │
│   │     Network      │     Customer     │     VLAN/zone     │   Ping passes    │   iSCSI or FC    │   │
│   │       Host       │     Customer     │    MPIO + test    │   I/O verified   │    All paths     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: 2U or 4U rack space · dedicated 20–30A circuits · 10/25/100GbE or 16/32Gb FC             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Site prep       = Customer prerequisites: power, cooling, rack, network before Dell ships          │
│    Ready cert.     = Customer signs off that site meets Dell physical requirements                    │
│    FSE             = Field Service Engineer; Dell technician performing on-site work                  │
│    Array init      = Dell initialises OS, pools, networking on hardware; customer not involved        │
│    SCG deploy      = Dell installs Secure Connect Gateway VM; enables CloudIQ and SupportAssist       │
│    CloudIQ link    = SCG establishes outbound HTTPS to Dell cloud; confirmed by FSE                   │
│    iSCSI VLAN      = Customer creates dedicated VLAN; configures IP addresses for array ports         │
│    FC zoning       = Customer creates zones in FC fabric: HBA WWN + array port WWN per zone           │
│    Initiator reg.  = Register host IQN/WWN in Apex Console; required before volume mapping            │
│    Multipath test  = Verify active paths; pull one cable; I/O must continue on remaining path         │
│    Scale-out       = Adding capacity to existing Apex subscription via Dell SR; not self-service      │
│    OOB management  = Out-of-band access to array iDRAC/iDRAC9; Dell-managed; not customer access      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [APEX Storage as a Service](../../index.md) reference.

---

Hardware firmware and lifecycle upgrades for APEX STaaS are Dell's responsibility. The customer's role in upgrade events:

| Step | Action |
|---|---|
| 1 | Do not initiate firmware changes on APEX-managed infrastructure without coordination with Dell |
| 2 | Monitor the APEX Console for Dell-initiated maintenance notifications; Dell will schedule maintenance windows and communicate via the Console |
| 3 | Confirm Secure Connect Gateway is at the current recommended version — SCG upgrades can be triggered from the APEX Console or SCG management interface |
| 4 | After any Dell-initiated maintenance, verify all subscriptions show healthy status in APEX Console and confirm on-premises platform availability from the host side |
