# Nexus Dashboard — How It Works (Monitoring)


<div class="kb-summary">
How It Works (Monitoring) reference covering Cluster Architecture, Node Communication, Network Interfaces.
</div>

```
┌─────────────────────────────────── Nexus Dashboard — How It Works ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Step 1: Onboarding — add APIC or NX-OS fabric to Nexus Dashboard with credentials       │   │
│   │          Step 2: Telemetry — switches stream metrics via MDT/gRPC to NDI continuously         │   │
│   │       Step 3: Analysis — NDI ML models score health, detect anomalies, and analyse flows      │   │
│   │          Step 4: Alert — health score drops or anomaly detected triggers event in NDI         │   │
│   │     Step 5: Notification — email or webhook sent; ServiceNow integration creates incident     │   │
│   │        Step 6: Remediation — engineer reviews event; NDI shows affected objects and fix       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Switches stream telemetry to ND data network IP · APIC queried via REST · ND cluster processes       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Onboarding = Adding fabric to ND; requires APIC IP/credentials or switch SSH access                  │
│  MDT = Model-Driven Telemetry; NX-OS sensor push to NDI for real-time data                            │
│  gRPC = Transport for MDT streaming; port 9339 from switch to ND data IP                              │
│  Health score = NDI composite score per site/fabric/object from telemetry analysis                    │
│  Anomaly = NDI ML deviation from learned baseline in fabric metrics                                   │
│  Flow analysis = NDI tracking actual IP flows for EPG connectivity verification                       │
│  Event = NDI alert for health drop, anomaly, or assurance violation                                   │
│  Assurance = NDI verifying actual fabric state matches ACI policy intent                              │
│  Notification = Email or webhook from ND when event fires                                             │
│  ServiceNow = NDI integration creating ITSM incidents from fabric events                              │
│  Affected objects = NDI identifying specific switch, interface, or EPG causing health drop            │
│  Fabric site = Single ACI fabric or DCNM/NDFC managed NX-OS domain added to ND                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────── Nexus Dashboard — How It Works ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Step 1: Onboarding — add APIC or NX-OS fabric to Nexus Dashboard with credentials       │   │
│   │          Step 2: Telemetry — switches stream metrics via MDT/gRPC to NDI continuously         │   │
│   │       Step 3: Analysis — NDI ML models score health, detect anomalies, and analyse flows      │   │
│   │          Step 4: Alert — health score drops or anomaly detected triggers event in NDI         │   │
│   │     Step 5: Notification — email or webhook sent; ServiceNow integration creates incident     │   │
│   │        Step 6: Remediation — engineer reviews event; NDI shows affected objects and fix       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Switches stream telemetry to ND data network IP · APIC queried via REST · ND cluster processes       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Onboarding = Adding fabric to ND; requires APIC IP/credentials or switch SSH access                  │
│  MDT = Model-Driven Telemetry; NX-OS sensor push to NDI for real-time data                            │
│  gRPC = Transport for MDT streaming; port 9339 from switch to ND data IP                              │
│  Health score = NDI composite score per site/fabric/object from telemetry analysis                    │
│  Anomaly = NDI ML deviation from learned baseline in fabric metrics                                   │
│  Flow analysis = NDI tracking actual IP flows for EPG connectivity verification                       │
│  Event = NDI alert for health drop, anomaly, or assurance violation                                   │
│  Assurance = NDI verifying actual fabric state matches ACI policy intent                              │
│  Notification = Email or webhook from ND when event fires                                             │
│  ServiceNow = NDI integration creating ITSM incidents from fabric events                              │
│  Affected objects = NDI identifying specific switch, interface, or EPG causing health drop            │
│  Fabric site = Single ACI fabric or DCNM/NDFC managed NX-OS domain added to ND                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Cisco Nexus Dashboard (ND) is a centralised operations platform for Cisco ACI and NX-OS data centre fabrics. It provides unified management, health monitoring, policy orchestration, and network insights through a microservices-based architecture. Services including Nexus Dashboard Fabric Controller (NDFC) and Nexus Dashboard Insights (NDI) run on top of the ND platform and are independently licensed and deployed.

---

## Cluster Architecture

A Nexus Dashboard cluster consists of 3 or 5 nodes. All nodes are peers in a Raft-based cluster consensus model. A virtual IP (VIP) provides a single management entry point.



---

## Node Communication

| Path | Protocol | Port | Purpose |
|---|---|---|---|
| ND cluster nodes (internal) | HTTPS | TCP 2379, 2380, 9200 | etcd / Elasticsearch cluster |
| Browser → ND VIP | HTTPS | TCP 443 | Web UI and REST API |
| ND → ACI APIC | HTTPS | TCP 443 | Policy management |
| ND → NX-OS switches | SSH | TCP 22 | Configuration and telemetry |
| ND → NX-OS switches | SNMP | UDP 161/162 | Fault and telemetry |
| ND → Syslog target | Syslog | UDP/TCP 514 | Event forwarding |

---

## Network Interfaces

Each ND node requires two network interfaces:

- **Management interface**: used for admin access and communication with managed devices
- **Data / cluster interface**: used for inter-node cluster communication (dedicated subnet recommended)
