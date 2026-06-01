# RecoverPoint — Encryption


<div class="kb-summary">
Encryption reference covering Journal Encryption, Network Segmentation, Certificate Management.
</div>

```
┌────────────────────────────────────── RecoverPoint — Encryption ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            RecoverPoint — Encryption Configuration                            │   │
│   │   AES-256 WAN compression+encryption; data at rest on journal volumes unencrypted by default  │   │
│   │              In-transit: TLS 1.2+ for all management; data channel also encrypted             │   │
│   │              At-rest: AES-256 on repository or vault storage; key managed by KMS              │   │
│   │               Key lifecycle: generate → use → rotate (annual) → retire → destroy              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  In-Transit                  │  │                   At-Rest                   │   │
│   │              TLS 1.2+ (minimum)              │  │              AES-256 encryption             │   │
│   │            443 (mgmt HTTPS) HTTPS            │  │              KMS key management             │   │
│   │             Mutual TLS internal              │  │               WORM / immutable              │   │
│   │             Cert rotation annual             │  │             Key rotation annual             │   │
│   │             No plain-text admin              │  │               Audit key access              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites           │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication          │
│  Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA                  │
│  Journal       = write-order-consistent storage capturing all writes for point-in-time access         │
│  Consistency Group= set of volumes protected together; writes are applied in order across all         │
│  Bookmark      = named marker in journal; enables deterministic recovery to a known state             │
│  Image Access  = mounting a journal point-in-time image to a host for testing or recovery             │
│  Failover      = activating the replica at the recovery site; breaks replication relationship         │
│  Test Copy     = non-disruptive image access for validation without breaking replication              │
│  RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero          │
│  RTO           = Recovery Time Objective; time from failover to service restored                      │
│  Reverse       = after failover, replicates from recovery site back to re-sync production             │
│  Splitter Lag  = delay between host write and journal commit; monitor for replication health          │
│  CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps          │
│  Distributed CG= consistency group spanning volumes on multiple storage arrays                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── RecoverPoint — Encryption ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            RecoverPoint — Encryption Configuration                            │   │
│   │   AES-256 WAN compression+encryption; data at rest on journal volumes unencrypted by default  │   │
│   │              In-transit: TLS 1.2+ for all management; data channel also encrypted             │   │
│   │              At-rest: AES-256 on repository or vault storage; key managed by KMS              │   │
│   │               Key lifecycle: generate → use → rotate (annual) → retire → destroy              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  In-Transit                  │  │                   At-Rest                   │   │
│   │              TLS 1.2+ (minimum)              │  │              AES-256 encryption             │   │
│   │            443 (mgmt HTTPS) HTTPS            │  │              KMS key management             │   │
│   │             Mutual TLS internal              │  │               WORM / immutable              │   │
│   │             Cert rotation annual             │  │             Key rotation annual             │   │
│   │             No plain-text admin              │  │               Audit key access              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites           │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication          │
│  Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA                  │
│  Journal       = write-order-consistent storage capturing all writes for point-in-time access         │
│  Consistency Group= set of volumes protected together; writes are applied in order across all         │
│  Bookmark      = named marker in journal; enables deterministic recovery to a known state             │
│  Image Access  = mounting a journal point-in-time image to a host for testing or recovery             │
│  Failover      = activating the replica at the recovery site; breaks replication relationship         │
│  Test Copy     = non-disruptive image access for validation without breaking replication              │
│  RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero          │
│  RTO           = Recovery Time Objective; time from failover to service restored                      │
│  Reverse       = after failover, replicates from recovery site back to re-sync production             │
│  Splitter Lag  = delay between host write and journal commit; monitor for replication health          │
│  CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps          │
│  Distributed CG= consistency group spanning volumes on multiple storage arrays                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [RecoverPoint](../../index.md) > [Security](../index.md) reference.

---

## Journal Encryption

Journal volumes hold continuous copies of production data — protect them:

- At-rest encryption is managed at the storage array level (not in RecoverPoint itself)
- Ensure journal volume LUNs are on encrypted arrays or datastores
- For PowerMax: verify journal vols are in an encrypted Storage Group
- For vSphere (RP4VM): place journal VMDKs on vSAN encrypted datastore or array-encrypted NFS

---

## Network Segmentation

| Traffic Type | Recommended Isolation |
|---|---|
| Production-to-replica replication | Dedicated WAN circuit or MPLS path; no internet traversal |
| RPA management | Dedicated management VLAN, accessible only from management jump hosts |
| RPA-to-array communication | SAN fabric or dedicated NFS management network |
| SRM ↔ RecoverPoint SRA | Management network; port 7225 |

---

## Certificate Management

Replace the default self-signed management certificate:

1. Generate CSR on each RPA node
2. Sign with internal CA
3. Import via Management Console → System Settings → TLS Certificates

Track certificate expiry — RecoverPoint management console becomes inaccessible if the cert expires.
