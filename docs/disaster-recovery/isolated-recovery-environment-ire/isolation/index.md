# IRE — Isolation

The Isolated Recovery Environment (IRE) is a network-isolated, air-gapped environment used for recovering from ransomware and other destructive attacks. Isolation is the foundational control: the IRE must never share network paths, credentials, or management planes with the production environment.

## Why Isolation Matters

Ransomware that has compromised a production environment may still be active during a recovery attempt. If the IRE shares any network connectivity with production, the threat actor can:
- Detect and destroy clean recovery copies.
- Pivot from production into the IRE.
- Re-encrypt or corrupt systems being restored.

Isolation eliminates these lateral movement paths.

## Network Isolation Architecture

```mermaid
graph TB
    PROD["Production Environment\n(potentially compromised)"]
    JUMP["Jump Host\n(IRE management access\nMFA required)"]
    IRE["Isolated Recovery Environment\n(dedicated VLANs / VNet)"]
    STORE["Immutable Backup Copy\n(air-gapped or vault-locked)"]
    FW["Perimeter Firewall\n(default deny from PROD)"]

    PROD -.->|No direct access| IRE
    JUMP --> FW
    FW --> IRE
    STORE --> IRE
    IRE -.->|No route back to PROD| PROD
```

## Credential Isolation

| Requirement | Rationale |
|---|---|
| Dedicated IRE admin accounts | Production accounts may be compromised |
| No shared service accounts | Compromised service account credentials span both environments |
| Separate AD/IdP | IRE domain controllers are not replicas of production AD |
| Break-glass accounts | Dedicated, MFA-protected, stored offline (sealed envelope / PAW) |
| No domain trust | IRE domain has no trust relationship with production domain |

```powershell
# Check for domain trusts in IRE AD (should return nothing)
Get-ADTrust -Filter *

# Verify IRE domain controller has no replication partners outside IRE
Get-ADReplicationPartnerMetadata -Target (hostname) -Scope Server
```

## Storage Isolation

Backup copies used for IRE restoration must be:

- **Immutable** — write-once, cannot be deleted or modified by any account including backup admins.
- **Isolated** — stored in a separate cloud tenant, offline media, or vault-locked object storage.
- **Access-controlled** — no production system has read or write access to the backup store.

```bash
# Azure: enable immutable blob storage for backup container
az storage container immutability-policy create \
  --account-name <backup-storage-account> \
  --container-name <container-name> \
  --period 30 \
  --allow-protected-append-writes false

az storage container immutability-policy lock \
  --account-name <backup-storage-account> \
  --container-name <container-name>
```

## Isolation Verification Checklist

| Check | Command / Test | Pass condition |
|---|---|---|
| No network route from IRE to production | `traceroute <prod-host>` from IRE | Route fails or hits default deny |
| No route from production to IRE | `ping <ire-host>` from prod | No response |
| No shared AD | `nltest /dsgetdc:<prod-domain>` from IRE | Returns error |
| No shared credentials | Verify IRE accounts do not exist in prod AD | Enumeration returns nothing |
| Immutable backups | Check immutability lock state | Locked, cannot be deleted |
| Firewall ACL | Review firewall ruleset | Default deny between prod and IRE |

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| IRE VM can ping production host | Missing ACL or VLAN trunk leak | Check firewall ACLs and switch port VLAN configuration |
| Restore fails because backup store is unreachable | Backup store IP not whitelisted in IRE firewall | Add firewall rule: IRE → backup store IP, port 443 only |
| Cannot manage IRE systems remotely | Jump host not in allowed source list | Update IRE NSG/firewall to allow traffic from jump host subnet only |
| AD join required for IRE workloads | App requires domain membership | Build dedicated IRE domain; never join production domain |
