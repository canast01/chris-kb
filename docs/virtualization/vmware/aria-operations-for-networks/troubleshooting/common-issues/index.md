---
tags:
  - aria-networks
  - troubleshooting
  - vmware
---
# vRNI Common Issues

```bash
# From Collector VM — test connectivity to Platform VM
curl -sk https://<platform-vm-ip>/api/ni/auth/token
nc -vz <platform-vm-ip> 443

# Check Collector services
ssh admin@<collector-vm-ip>
sudo systemctl status hms
sudo systemctl start hms   # restart if stopped

# Check Collector disk usage (stops uploading when >85% full)
df -h
sudo journalctl --vacuum-size=1G   # free journal space
```
```text
┌───────────────────────────────────────── vRNI Common Issues ──────────────────────────────────────────┐
│                                                                                                       │
│  Common issues: data source red, no flows, LDAP login failure, and collector offline.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Data Source Red                │  │                No Flows in UI               │   │
│   │            Check API reachability            │  │            Verify IPFIX target IP           │   │
│   │         Validate credentials in vRNI         │  │            Check collector online           │   │
│   │         Cert error: re-accept or fix         │  │           Check UDP 2055 firewall           │   │
│   │           Service account locked?            │  │           proxy.log: flow receipt?          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Source and flow issues are most common; LDAP and collector are next in frequency.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              LDAP Login Failure              │  │              Collector Offline              │   │
│   │           Test LDAP in Settings UI           │  │           Check collector VM power          │   │
│   │         Validate bind DN + password          │  │          service collector restart          │   │
│   │          Check LDAPS cert validity           │  │           Verify platform TCP 443           │   │
│   │            Try LDAP browser tool             │  │         Re-register collector in UI         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform + collector VMs; AD/LDAP server; NSX-T and physical switches as sources                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Data Source Red     = vRNI cannot reach or authenticate to the configured source                     │
│  No Flows            = Flow Map empty; IPFIX not reaching collector or platform                       │
│  IPFIX Target        = Device setting pointing flow export to the collector IP                        │
│  proxy.log           = Collector log; confirms flow packets received and forwarded                    │
│  LDAP Bind Failure   = vRNI cannot authenticate to directory with stored credentials                  │
│  Collector Offline   = Collector VM unreachable or service stopped; check VM health                   │
│  Service Account Lock= AD account lockout caused by repeated vRNI auth attempts                       │
│  Cert Error          = TLS cert mismatch; re-accept thumbprint or upload correct CA                   │
│  Re-register         = Remove and re-add collector in vRNI UI to reset association                    │
│  UDP 2055 Firewall   = NetFlow/IPFIX port; blocked firewall = no flows received                       │
│  LDAP Browser        = Tool like ldp.exe to manually test LDAP bind and search                        │
│  Test Connection     = vRNI built-in source test; confirms API reachability and auth                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1[NSX data source collection failed]
    S --> B2[Flow data missing in UI]
    S --> B3[Path analysis shows no path]
    S --> B4[Physical device not discovered]
    S --> B5[Metric gap in timeline]
    S --> B6[LDAP login failure]

    B1 --> D1{API reachable\nand credentials valid?}
    D1 -->|No| R1[Fix API Connectivity · Update Credentials · Re-accept Cert\n→ Data Source Red]
    D1 -->|Yes| R2[Check Service Account Lock · Run Test Connection\n→ Data Source Red]

    B2 --> D2{IPFIX configured\non source?}
    D2 -->|No| R3[Set IPFIX Target to Collector IP · Enable on vDS\n→ No Flows in UI]
    D2 -->|Yes| R4[Check UDP 2055 Firewall · Review proxy.log\n→ No Flows in UI]

    B3 --> R5[Verify All Source Devices Discovered · Check NSX Data Source\n→ No Flows in UI]

    B4 --> R6[Add Device via SNMP · Verify Credentials · Check Collector Reachability\n→ Data Source Red]

    B5 --> D3{Collector\nonline?}
    D3 -->|No| R7[Restart Collector Service · Re-register in UI\n→ Collector Offline]
    D3 -->|Yes| R8[Check Collector Disk Usage · Clear Journal Space\n→ Collector Offline]

    B6 --> R9[Test LDAP Bind DN · Check LDAPS Cert · Use LDAP Browser Tool\n→ LDAP Login Failure]

    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8,R9 section
    class D1,D2,D3 decision
    class S start
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
