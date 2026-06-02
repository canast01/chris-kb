# NetApp Keystone Security

<div class="kb-summary">
NetApp Keystone Security reference covering Shared Responsibility, Keystone Collector Security, Storage Security, Access Control, Compliance.
</div>
```text
┌───────────────────────────────────── NetApp Keystone — Security ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Keystone security: access control, authentication, encryption, and hardening guide      │   │
│   │          Principle of least privilege applied to all admin roles and service accounts         │   │
│   │          Encryption at rest and in transit enforced; key rotation on defined schedule         │   │
│   │            Annual security review and audit; logs forwarded to SIEM for correlation           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Define roles → enforce MFA → enable encryption → harden → audit                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Hardware          │  │       AFF/FAS on-prem       │  │         NetApp-owned        │   │
│   │        Service level        │  │       Extreme/Perf/Std      │  │         Latency SLA         │   │
│   │          Collector          │  │         Telemetry VM        │  │        ONTAP polling        │   │
│   │          Dashboard          │  │            BlueXP           │  │       Usage visibility      │   │
│   │           Billing           │  │       Committed+burst       │  │       Monthly invoice       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │Keystone Collecto │  Usage metering  │     ONTAP REST    │ Service account  │    On-prem VM    │   │
│   │      BlueXP      │   SaaS portal    │       HTTPS       │    OAuth2/SSO    │   NetApp SaaS    │   │
│   │   AFF Extreme    │  NVMe perf tier  │    FC/iSCSI/NFS   │  Kerberos/CHAP   │  Sub-ms latency  │   │
│   │   AutoSupport    │ Telemetry relay  │       HTTPS       │   Certificate    │    Call-home     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: NetApp AFF/FAS arrays on-prem · Keystone Collector VM · BlueXP cloud portal              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Keystone           = NetApp STaaS; fixed-term subscription for ONTAP or StorageGRID capacity       │
│    Service level      = tiered SLA: Extreme (NVMe), Performance (SSD), Standard (HDD)                 │
│    Committed capacity = minimum contracted TiB; billed monthly even if below threshold                │
│    Burst capacity     = usage above committed; available without pre-ordering; billed monthly         │
│    Keystone Collector = on-prem VM that gathers usage metrics and sends to NetApp Keystone            │
│    BlueXP             = NetApp SaaS control plane; Keystone dashboard, DRaaS, and cloud integrations  │
│    AFF                = All Flash FAS; ONTAP-based NVMe/SSD array used for Extreme and Performance ...│
│    FAS                = Fabric Attached Storage; ONTAP hybrid HDD/SSD for Standard service level      │
│    StorageGRID        = NetApp S3 object storage; Object service level in Keystone subscriptions      │
│    AutoSupport        = ONTAP telemetry relay; sends call-home data and log bundles to NetApp         │
│    Service request    = NetApp SR; support ticket opened via mysupport.netapp.com portal              │
│    SKU                = Keystone service SKU identifies the service level and raw or usable capacity  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Shared Responsibility

Keystone operates on a shared responsibility model between NetApp and the customer.

| Responsibility | NetApp | Customer |
|---|---|---|
| Hardware physical security | Manages | — |
| Firmware and OS patching | Manages | — |
| Storage controller hardening | Manages | — |
| RBAC on the data layer | — | Configures |
| Volume and share permissions | — | Configures |
| Encryption of customer data | — | Configures (NVE/NAE) |
| Network access to storage | — | Configures |
| Application security | — | Manages |
| Keystone Collector VM security | — | Manages (OS patching, access) |

## Keystone Collector Security

The Keystone Collector VM collects consumption telemetry only — no customer data is transmitted to NetApp. The Collector sends capacity metrics (volume sizes, used capacity, service level assignments) over TLS-encrypted HTTPS.

- Collector is outbound only; no inbound ports are required or opened
- TLS encryption for all data transmission to NetApp endpoints
- Collector VM is customer-managed; apply OS security patches and access controls per your standard server hardening baseline
- Restrict SSH access to the Collector VM to authorized infrastructure administrators

## Storage Security

The underlying storage is standard ONTAP or StorageGRID — all ONTAP security controls apply regardless of whether the hardware is Keystone-owned or customer-owned. The customer configures:

- NetApp Volume Encryption (NVE) or NetApp Aggregate Encryption (NAE) for data at rest
- RBAC via ONTAP roles for storage administration access
- NFS/CIFS export policies and share permissions
- iSCSI/FC initiator group (igroup) access controls for SAN LUNs
- Audit logging for file and volume access (FPolicy for NFS/CIFS, ONTAP audit framework)

## Access Control

- NetApp SRE has access to the storage management plane only (ONTAP System Manager, cluster admin CLI); NetApp SRE does not have access to customer data volumes
- An access log of NetApp SRE activity is available on request via the support portal
- Customers are notified before any scheduled maintenance access by NetApp; emergency access for P1 incidents is performed with notification at time of access
- Request a formal access log audit via the Keystone Success Manager if required for compliance purposes

## Compliance

- Keystone service is ISO 27001 certified at the service delivery level
- SOC 2 Type II attestation available — request the report via the Keystone Success Manager or NetApp trust portal
- Data residency is guaranteed on-premises (or at the agreed colocation facility); customer data does not leave the contracted location

---

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Identity sources, MFA, and service account configuration.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC roles, least-privilege, and tenant access boundaries.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data-at-rest and in-transit encryption for Keystone services.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baseline, audit logging, and compliance controls.</span>
</a>

</div>
- For regulated workloads, confirm compliance scope with NetApp legal and the KSM — Keystone's compliance certifications cover the infrastructure service, not the customer's data processing activities
