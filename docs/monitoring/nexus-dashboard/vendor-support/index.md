# Nexus Dashboard Vendor Support

```
┌────────────────────────────────── Nexus Dashboard — Vendor Support ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Support Model — Cisco TAC                                   │   │
│   │             Nexus Dashboard covered by Cisco DNA Advantage or ACI Premier license             │   │
│   │                    Open TAC case: cisco.com/support or call 1-800-553-2447                    │   │
│   │             Sev-1: production fabric unreachable or ND cluster down; 24x7 response            │   │
│   │                        Collect: acs logs download → attach to TAC case                        │   │
│   │             Smart Call Home: auto-opens TAC case on critical events if configured             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ND on-prem · logs bundle collected locally · uploaded to TAC case portal                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cisco TAC = Technical Assistance Centre; 24x7 for Sev-1 production issues                            │
│  DNA Advantage = Cisco licensing tier required for Nexus Dashboard                                    │
│  ACI Premier = ACI licensing tier including NDI and NDO                                               │
│  acs logs download = Log bundle command; required attachment for ND support cases                     │
│  Smart Call Home = ND feature auto-opening Cisco TAC case on critical cluster events                  │
│  Severity 1 = Fabric unreachable or ND cluster failed; 24x7 phone response                            │
│  Severity 2 = NDI not collecting or major feature down; 4-hour response                               │
│  Contract check = Cisco TAC requires valid SMARTNET or DNA/ACI contract                               │
│  Bug search = Cisco Bug Search Tool (bst.cisco.com); search by ND version + symptom                   │
│  Release notes = Per-version Cisco ND release notes; check before upgrade                             │
│  Interop matrix = Cisco compatibility matrix for ND vs NX-OS/ACI versions                             │
│  TAM = Technical Account Manager; proactive Cisco contact for enterprise customers                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Nexus Dashboard support is provided by Cisco TAC via the Cisco Support Portal (support.cisco.com). A valid SmartNet contract covering the ND cluster (physical) or Cisco software subscription (virtual) is required to open SRs. When raising an SR, collect a support bundle from the ND Admin UI (Admin > System Settings > Tech Support) and include details of the fabric type and fault description. For ACI-specific issues, also collect an APIC tech support bundle.

**Information to collect before opening an SR**

- Nexus Dashboard version and service versions (NDFC, NDI)
- Cluster size and node deployment type (physical or virtual)
- Fabric type (ACI or NX-OS) and number of fabrics
- Fault or error details with timestamps
- Support bundle from ND Admin > System Settings > Tech Support
- SmartNet contract number

| Resource | Details |
|---|---|
| Cisco TAC Portal | support.cisco.com |
| Software Downloads | software.cisco.com |
| ND Documentation | developer.cisco.com/docs/nexus-dashboard |
| EOL / EOS Notices | cisco.com/go/eos |
| Community | community.cisco.com |
