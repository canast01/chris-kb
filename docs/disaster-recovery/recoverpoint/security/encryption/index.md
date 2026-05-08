# RecoverPoint — Encryption

> Part of the [RecoverPoint](../../) > [Security](../) reference.

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
