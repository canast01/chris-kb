# vRNI Escalation

```bash
ssh ubuntu@vrni.example.local

# Generate support bundle from CLI
sudo /etc/init.d/support-bundle.sh

# Bundle is placed in:
ls /data/support-bundles/
# Transfer via SCP:
scp ubuntu@vrni.example.local:/data/support-bundles/<bundle>.tar.gz /local/path/
```

```text
┌─────────────────────────────────────────── vRNI Escalation ───────────────────────────────────────────┐
│                                                                                                       │
│  Escalation triggers, Support Request process, and TAM engagement for vRNI.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │              SR Severity Levels             │   │
│   │           Platform UI unreachable            │  │           P1: platform fully down           │   │
│   │          All flows missing >2 hours          │  │          P2: flows missing/degraded         │   │
│   │            Upgrade fails or loops            │  │             P3: feature/UI issue            │   │
│   │          Data corruption suspected           │  │            P4: how-to / question            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Triggers determine severity; SR opened with bundle; TAM engaged for P1/P2.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SR Process                  │  │                TAM Engagement               │   │
│   │          1. Generate support bundle          │  │             Notify TAM for P1/P2            │   │
│   │         2. Open GSS SR with severity         │  │           TAM escalates internally          │   │
│   │         3. Attach bundle + timeline          │  │           Provide change timeline           │   │
│   │            4. Follow GSS guidance            │  │              Bridge call for P1             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM; support bundle generated via SSH or VAMI; GSS portal for SR                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Support Bundle      = Compressed log archive; mandatory attachment for any SR                        │
│  GSS                 = Global Support Services; VMware/Broadcom support portal                        │
│  SR                  = Support Request; formal case opened with GSS                                   │
│  P1 Severity         = Production down; requires 24/7 response and bridge call                        │
│  P2 Severity         = Major degradation; business-hours priority response                            │
│  TAM                 = Technical Account Manager; escalation point for P1/P2                          │
│  Bridge Call         = Live conference with GSS, TAM, and customer for P1 issues                      │
│  Change Timeline     = Log of recent changes provided to GSS to narrow root cause                     │
│  Data Corruption     = Suspected invalid flow data; always P1 or P2 severity                          │
│  Upgrade Loop        = PAK upgrade repeatedly fails or rolls back; escalate to GSS                    │
│  Internal Escalation = TAM routes SR to engineering or BU team for complex issues                     │
│  RCA                 = Root Cause Analysis; provided by GSS after P1/P2 resolution                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
