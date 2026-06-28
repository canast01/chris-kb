---
tags:
  - netapp
  - security
---
# NetApp Keystone Security

<div class="kb-summary">
NetApp Keystone Security reference covering Shared Responsibility, Keystone Collector Security, Storage Security, Access Control, Compliance.

*Applies to: Keystone STaaS*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

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

- For regulated workloads, confirm compliance scope with NetApp legal and the KSM — Keystone's compliance certifications cover the infrastructure service, not the customer's data processing activities
