# Aria Suite Lifecycle — Backup & Restore

```text
  LCM Backup Strategy
┌─────────────────────────────────────────────────────────────────┐
│  What to Back Up              Method                            │
│  ┌───────────────────────┐    ┌─────────────────────────────┐   │
│  │ LCM appliance VM      │───►│ VADP backup (Veeam etc.)    │   │
│  │  /var/lib/vrlcm/      │    │  nightly + quiesce          │   │
│  │  /opt/vmware/vrlcm/   │    │ OR VM snapshot pre-change   │   │
│  │  (DB + Locker)        │    │  (delete within 48h)        │   │
│  └───────────────────────┘    └─────────────────────────────┘   │
│  ┌───────────────────────┐    ┌─────────────────────────────┐   │
│  │ NFS Binary Repo       │───►│ NFS snapshot (NetApp/Pure)  │   │
│  │  /data (.pak files)   │    │ OR rsync to secondary       │   │
│  └───────────────────────┘    └─────────────────────────────┘   │
│  ┌───────────────────────┐    ┌─────────────────────────────┐   │
│  │ Environment config    │───►│ LCM API export to JSON      │   │
│  │  (deploy manifests)   │    │  stored version-controlled  │   │
│  └───────────────────────┘    └─────────────────────────────┘   │
│                                                                 │
│  Locker Master Password → offline vault (required for restore)  │
└─────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────── Aria Suite LCM Backup & Restore ───────────────────────────────────┐
│                                                                                                       │
│  LCM database backup, logscraper archive, and environment product backup steps.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               What to Back Up                │  │                Backup Method                │   │
│   │         LCM database (appliance DB)          │  │             VAMI: backup to NFS             │   │
│   │          Cert store and trust certs          │  │           vSphere snapshot LCM VM           │   │
│   │          Environment configuration           │  │           Export environment JSON           │   │
│   │         Product: each product backup         │  │           Each product: own backup          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  LCM backup covers its own DB; each managed product must be backed up separately.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Restore Procedure               │  │           Post-Restore Validation           │   │
│   │           1. Deploy fresh LCM OVA            │  │              LCM UI accessible?             │   │
│   │         2. Restore from VAMI backup          │  │            Environments visible?            │   │
│   │         3. Reconnect vCenter + vIDM          │  │             Products: health OK?            │   │
│   │          4. Validate product health          │  │             Cert store: intact?             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM on vSphere; NFS for backup target; vCenter and vIDM must be reachable                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM Database        = Internal PostgreSQL DB storing environments, products, certs                   │
│  VAMI Backup         = LCM built-in backup to NFS at port 5480                                        │
│  vSphere Snapshot    = Full LCM VM checkpoint; use before upgrades                                    │
│  Environment JSON    = Export of LCM environment definition for reference                             │
│  Cert Store          = LCM-internal trusted CA and product cert repository                            │
│  Product Backup      = Each Aria product (vROps, vRLI, vRA) needs own backup                          │
│  Logscraper          = LCM diagnostic tool; not a backup tool but useful for SR                       │
│  Restore             = VAMI-driven LCM DB restore from backup file on NFS                             │
│  Reconnect vCenter   = After restore, re-add vCenter connection in LCM settings                       │
│  Post-restore Check  = Validate environment, product health, and cert store                           │
│  NFS Target          = Backup storage; LCM writes backup archive to NFS share                         │
│  Backup Schedule     = Automate daily LCM backup via VAMI scheduler                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

Remove the snapshot within 48 hours of a successful upgrade:

```bash
Get-Snapshot -VM (Get-VM "lcm-prod-01") -Name "pre-upgrade-*" |
  Remove-Snapshot -Confirm:$false
```

### Option 2 — VADP-Compatible Backup (Preferred for Production)

Use your enterprise backup solution (Veeam, Commvault, Veritas) to back up the LCM appliance VM with application-consistent quiesce. Schedule nightly full or incremental backups. Retain at least 14 daily restore points.

Requirements:
- VMware Tools must be running on the LCM appliance (verify: `vmware-toolsd --version` from SSH)
- Backup job should quiesce the guest filesystem
- LCM services do not need to be stopped for VADP backup — quiesce handles this

---

## Backing Up the NFS Binary Repository

The `/data` NFS share contains all downloaded product bundles (`.pak` files). These are large and re-downloadable from Broadcom, but backing them up avoids re-downloading during disaster recovery.

```bash
# Check NFS mount and size from LCM appliance
df -h /data
du -sh /data/*

# On the NFS server — verify export path
showmount -e <nfs-server-ip>
```

Backup options:
- **NFS server snapshot**: if the NFS server supports snapshots (NetApp, Pure, vSAN File Services), schedule daily snapshots of the export volume
- **rsync to secondary storage**:

```bash
# Run from NFS server or a jump host with access to both locations
rsync -avz --progress /exports/lcm-repo/ /backup/lcm-repo-$(date +%Y%m%d)/
```

---

## Exporting LCM Environment Configuration via API

The LCM API can export environment inventory, which documents deployed product configurations for rebuild reference.

```bash
# Authenticate
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.example.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

# List all environments
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/environments" | \
  jq '.' > lcm-environments-$(date +%Y%m%d).json

# Export a specific environment (replace <env-id> with actual ID)
ENV_ID="<env-id>"
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/environments/$ENV_ID" | \
  jq '.' > lcm-env-${ENV_ID}-$(date +%Y%m%d).json

# Export Locker certificate inventory (metadata only — not private keys)
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/locker/api/v2/certificates" | \
  jq '.' > lcm-locker-certs-$(date +%Y%m%d).json
```

Store these JSON exports alongside the backup job output in a version-controlled location.

---

## Restore Procedure

### Restoring the LCM Appliance from VM Backup

1. Power off the LCM appliance VM (coordinate with teams — LCM UI will be unavailable)
2. Restore the VM from the backup job or revert to snapshot
3. Power on the restored appliance
4. Verify LCM services are running:

```bash
ssh admin@lcm-prod-01.example.local
sudo systemctl status lcm
sudo systemctl status nginx
vracli status
```

5. Open the LCM UI and verify:
   - Environments show correct products and versions
   - Locker contains all expected certificates and passwords
   - vCenter and VIDM integrations show green

6. If restoring from a snapshot that predates a completed upgrade, the product appliances may be at a newer version than LCM expects. In this case, open a Broadcom SR — do not attempt manual re-registration without guidance.

### Restoring After NFS Data Loss

If the `/data` NFS mount is lost but the LCM appliance is intact:

1. Re-provision or restore the NFS export
2. Remount on LCM:

```bash
# Edit /etc/fstab if the NFS entry is missing
echo "<nfs-server>:/lcm-repo /data nfs defaults,_netdev 0 0" >> /etc/fstab
mount -a
df -h /data
```

3. Re-download required product bundles from Broadcom Support Portal
4. Re-map binaries: **Lifecycle Operations → Settings → Binary Mapping → Map Binaries**

---

## Backup Verification Checklist

Run monthly or after every restore test:

- [ ] LCM appliance VM backup job succeeded within last 24 hours
- [ ] Backup restore test performed: restore to isolated network, verify LCM UI accessible
- [ ] NFS backup or snapshot current (within 24 hours)
- [ ] API export JSON files archived and stored off-appliance
- [ ] Locker Master Password documented in offline vault (required for decryption after restore)
- [ ] All Locker certificate private keys have source copies in secure offline storage (PEM files)
