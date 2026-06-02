# Nexus Dashboard — Backup & Restore


<div class="kb-summary">
> Part of the [Nexus Dashboard](../../index.md) reference.
</div>

---

## Overview

Nexus Dashboard backup captures the full cluster state:
- Platform configuration (users, LDAP, certificates, site registrations)
- NDFC database (fabrics, zones, device aliases, inventory, events)
- NDI configuration and anomaly history (optional — large)
- Application configuration and state

Backups are critical for cluster recovery after node failure and as pre-upgrade snapshots. ND backup uses an external SCP or SFTP target — local-only backups are insufficient for DR.

---

## Backup Configuration

### Configure Remote Backup Destination

Navigate to **Admin Console > Operations > Backup & Restore > Settings**:

| Setting | Recommended Value |
|---|---|
| Backup type | SCP or SFTP |
| Remote host | `backup-server.corp.example.com` |
| Remote path | `/backups/nexus-dashboard/dc1/` |
| Username | `nd-bkp` (write permission on target path) |
| Authentication | SSH key (preferred) or password |
| Encryption | Enabled — set a strong passphrase (store in vault) |
| Retention count | 4 (keep last 4 backups) |

Test the remote destination by clicking **Test Connection** before relying on it.

### Schedule Automated Backups

Navigate to **Admin Console > Operations > Backup & Restore > Schedule**:

| Field | Value |
|---|---|
| Frequency | Weekly |
| Day | Sunday |
| Time | 02:00 (local appliance time) |
| Include app data | Yes for NDFC; optional for NDI (large) |

### Manual Backup (GUI)

1. Navigate to **Admin Console > Operations > Backup & Restore**.
2. Click **Backup Now**.
3. Select: include or exclude NDI telemetry data (exclude for faster backup unless telemetry history is required).
4. Click **Start Backup**.
5. Monitor progress — backup status updates in the UI. Completion time depends on data size: 10-30 minutes typical.

### Manual Backup (CLI)

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Trigger manual backup to remote SCP target
acs backup create \
  --remote-server backup-server.corp.example.com \
  --remote-path /backups/nexus-dashboard/dc1/ \
  --remote-user nd-bkp \
  --encryption-passphrase-file /home/ndadmin/.nd-backup-pass

# Check backup status
acs backup status

# List available backups
acs backup list
```
```
┌───────────────────────── Cisco Nexus Dashboard — Operations Backup & Restore ─────────────────────────┐
│                                                                                                       │
│  Cluster configuration backup to remote storage; restore via UI or CLI for DR recovery.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Backup Configuration             │  │                 Backup Scope                │   │
│   │          Remote: SCP or NFS target           │  │        Cluster config: all node data        │   │
│   │         Schedule: daily/weekly cron          │  │            App data: NDFC/NDI/NDO           │   │
│   │         Encryption: AES-256 at rest          │  │         Secrets: encrypted in backup        │   │
│   │          Retention: keep N backups           │  │        Sites: site credentials incl.        │   │
│   │          Alert: backup success/fail          │  │          Certificates: not included         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Schedule backup before any upgrade; verify remote target is writable                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Restore Process                │  │              Disaster Recovery              │   │
│   │         Bootstrap new cluster first          │  │          DR: rebuild cluster nodes          │   │
│   │          Upload backup file via UI           │  │          Same software version req.         │   │
│   │          Validate: checksum verify           │  │           IP/hostnames must match           │   │
│   │         Restore: node-by-node apply          │  │        Certs re-issued after restore        │   │
│   │          Post-restore: verify sites          │  │            RTO: ~2-4 hrs typical            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · remote SCP/NFS server · management network · spare hardware for DR                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SCP            = Secure Copy Protocol; encrypted file transfer to remote backup target               │
│  NFS            = Network File System; shared storage mount for backup destination                    │
│  AES-256        = Advanced Encryption Standard 256-bit; encrypts backup archive                       │
│  Bootstrap      = Initial cluster bring-up before restoring configuration                             │
│  Checksum       = SHA hash validating backup file integrity before restore                            │
│  RTO            = Recovery Time Objective; target time to restore service                             │
│  DR             = Disaster Recovery; rebuilding ND cluster at alternate site                          │
│  Secrets        = Passwords and API keys stored encrypted within backup bundle                        │
│  Retention      = Policy defining how many backup files are kept before purging                       │
│  Site credentials= Per-site username/password ND uses to reach APIC/switches                          │
│  Certs re-issued= SSL certificates are regenerated fresh on restore; not restored                     │
│  Version match  = Restore requires identical ND software version as backup source                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Backup Retention Policy

| Backup Type | Frequency | Retention | Storage |
|---|---|---|---|
| ND cluster full backup | Weekly | 4 copies | Remote SCP/SFTP |
| Pre-upgrade ND backup | Before every upgrade | Indefinite | Remote SCP/SFTP |
| NDFC zone export | Before every zone change | 90 days | Change management system |
| VM snapshots | Before each upgrade | Delete within 48h post-upgrade | vCenter datastore |

Do not rely on VM snapshots as the primary recovery mechanism. Snapshots held longer than 48 hours degrade VM I/O performance and should be deleted after confirming the upgrade is stable.

---

## Backup Verification

Test the backup restore procedure at least annually:

1. Deploy a temporary ND cluster (in a test environment or a dedicated DR environment).
2. Restore the most recent production backup.
3. Validate NDFC fabric inventory, zone databases, and user accounts.
4. Document the test results (time to restore, any issues encountered).
5. Delete the test cluster after validation.

A restore that has never been tested in practice is not a reliable recovery plan.
