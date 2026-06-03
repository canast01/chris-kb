# Cisco Nexus Dashboard — Operations Backup & Restore

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

```text
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
