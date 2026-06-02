# Cisco DCNM — Backup & Restore


<div class="kb-summary">
> Part of the [Cisco DCNM](../../index.md) reference.
</div>

---

## Overview

DCNM does not have a built-in one-click backup GUI comparable to SANnav. Backup is a combination of:
- **Database backup** (PostgreSQL) — all inventory, zones, events, users, and configuration
- **File-based backup** — DCNM configuration files, TLS certificates, custom scripts
- **VM snapshot** — a hypervisor-level recovery point (for upgrades only; not a substitute for DB backup)

---

## Database Backup

### Manual Backup

```bash
ssh root@dcnm-dc1.corp.example.com

# Full database dump (all DCNM databases)
pg_dumpall -U postgres -f /var/backup/dcnm/dcnm-db-$(date +%Y%m%d-%H%M).sql

# Compress the dump
gzip /var/backup/dcnm/dcnm-db-$(date +%Y%m%d-%H%M).sql

# Transfer to remote backup server
scp /var/backup/dcnm/dcnm-db-$(date +%Y%m%d-%H%M).sql.gz \
    bkp@backup-server.corp.example.com:/backups/dcnm/db/

# List backups
ls -lh /var/backup/dcnm/
```
```text
┌─────────────────────────────────── Cisco DCNM — Backup and Restore ───────────────────────────────────┐
│                                                                                                       │
│  DCNM backup covers the config DB, zone snapshots, NX-OS configs, and topology data.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             DCNM Platform Backup             │  │             Switch Config Backup            │   │
│   │           Nightly: NFS destination           │  │           copy run startup on MDS           │   │
│   │         Includes: DB + topology data         │  │         DCNM: archive config per sw         │   │
│   │        Schedule: DCNM Admin → Backup         │  │           Pre-change zone snapshot          │   │
│   │            Retention: 30 days min            │  │          Export zone set: text file         │   │
│   │            Test restore quarterly            │  │         SCP to central backup store         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DCNM DB backup and switch zone snapshots are both required for full recovery.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            DCNM Restore Procedure            │  │            Switch Config Restore            │   │
│   │           1. Deploy fresh DCNM OVA           │  │          copy tftp: startup-config          │   │
│   │        2. Restore DB from NFS backup         │  │          Restore zone: import file          │   │
│   │          3. Verify switch discovery          │  │           zoneset activate in VSAN          │   │
│   │           4. Re-validate ISE auth            │  │         Verify: show zoneset active         │   │
│   │           5. Test alert forwarding           │  │         Test: host I/O after restore        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM VM · NFS backup server · Cisco MDS switch chassis · vSphere host                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NFS backup      = DCNM configuration and DB exported to NFS mount point                              │
│  copy run startup= NX-OS command; saves running config to startup-config (NVRAM)                      │
│  DCNM archive    = per-switch config archive stored in DCNM; viewable in GUI                          │
│  Zone snapshot   = show zoneset active output saved before any zone change                            │
│  Zone set export = zone set saved to text file for offline backup and audit                           │
│  SCP             = Secure Copy; transfer config archives to central backup server                     │
│  DCNM OVA        = fresh DCNM VM from Cisco-provided OVA; base for restore                            │
│  copy tftp       = NX-OS; copies startup-config from TFTP server for restore                          │
│  zoneset activate= NX-OS command; applies restored zone set to VSAN                                   │
│  show zoneset    = verifies zone set is active and matches expected configuration                     │
│  Retention 30d   = keep 30 days of DCNM backups; prune older ones to save storage                     │
│  Restore test    = quarterly test of full DCNM restore to validate backup integrity                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Configuration File Backup

Back up the DCNM configuration files (these contain server settings not stored in the DB):

```bash
# Key configuration directories
tar -czf /var/backup/dcnm/dcnm-config-$(date +%Y%m%d).tar.gz \
  /usr/local/cisco/dcm/dcnm/conf/ \
  /etc/ssl/dcnm/ \
  /var/dcnm/

scp /var/backup/dcnm/dcnm-config-$(date +%Y%m%d).tar.gz \
    bkp@backup-server.corp.example.com:/backups/dcnm/config/
```

---

## Zone Configuration Export

Export zone databases before every zone change:

### GUI Export

1. Navigate to **SAN > Zoning > [Fabric] > Export**.
2. Select format: **DCNM** (native) or **Text** (human-readable).
3. Save with timestamp: `DC1-FABRIC-A-zones-20260506.txt`.
4. Attach to the change management ticket.

### CLI Export via REST API

```bash
# Get auth cookie
curl -sk -c dcnm-cookie.txt -X POST \
  https://dcnm-dc1.corp.example.com/rest/logon \
  -H "Content-Type: application/json" \
  -d '{"expirationTime": 3600}' \
  -u "svc-automation:<password>"

# Export zone configuration for a fabric
curl -sk -b dcnm-cookie.txt \
  "https://dcnm-dc1.corp.example.com/rest/san/zoning?fabricName=DC1-FABRIC-A" \
  -o DC1-FABRIC-A-zones-$(date +%Y%m%d).json

curl -sk -b dcnm-cookie.txt -X POST \
  https://dcnm-dc1.corp.example.com/rest/logout
```

---

## Restore Procedures

### Restore Database to Same Appliance

```bash
ssh root@dcnm-dc1.corp.example.com

# Stop DCNM services first
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server stop

# Drop and recreate databases
psql -U postgres -c "DROP DATABASE IF EXISTS sane;"
psql -U postgres -c "CREATE DATABASE sane;"
psql -U postgres -c "DROP DATABASE IF EXISTS pmdb;"
psql -U postgres -c "CREATE DATABASE pmdb;"

# Restore from full dump
gunzip -c /var/backup/dcnm/dcnm-db-20260506-0200.sql.gz | psql -U postgres

# Start DCNM services
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server start

# Monitor startup
tail -f /var/log/dcnm/server.log
```

### Restore to New Appliance (DR Recovery)

1. Deploy a fresh DCNM OVA with the **same version** as the backup.
2. Configure the same management IP, hostname, and NTP.
3. Stop DCNM services on the new appliance.
4. Transfer the database backup to the new appliance.
5. Restore as above.
6. If the DCNM IP changed: update SNMP trap destinations on all managed switches to point to the new IP.

### Post-Restore Validation

| Check | Method |
|---|---|
| Fabric inventory populated | SAN > Fabrics — all switches visible |
| Zone sets intact | SAN > Zoning — all zones and zone sets present |
| Device aliases intact | SAN > Device Alias |
| Events history present | Monitor > Events |
| User accounts restored | Administration > Security > Users |
| Performance data (PM) | Monitor > Performance — historical data present |

---

## Backup Retention Policy

| Backup Type | Frequency | Retention |
|---|---|---|
| Full DB backup (pg_dumpall) | Daily | 7 days locally, 30 days remote |
| Config file backup | Weekly | 4 copies |
| Zone set export | Before each zone change | 90 days |
| VM snapshot | Before each upgrade | Delete within 48h post-upgrade |
