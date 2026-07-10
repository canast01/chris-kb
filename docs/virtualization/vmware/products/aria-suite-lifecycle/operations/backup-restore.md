---
tags:
  - aria-lcm
  - operations
  - vmware
---
# Aria Suite Lifecycle — Backup & Restore

<div class="kb-summary">
Backup & Restore reference covering Option 2 — VADP-Compatible Backup (Preferred for Production), Backing Up the NFS Binary Repository, Exporting LCM Environment Configuration via API, Restore Procedure, Backup Verification Checklist.

*Applies to: Aria LCM 8.x*
</div>
![Aria Suite Lifecycle — Backup & Restore](../../../../../assets/virtualization-vmware-aria-suite-lifecycle-operations-backup.svg)

  LCM Backup Strategy

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Option 2 — VADP-Compatible Backup (Preferred for Production)

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


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
nfs-server-01:/export/lcm-data
              500G  287G  213G  57% /data

/data/lcm-backups          145G
/data/lcm-logs             89G
/data/lcm-temp             34G
/data/lcm-config           12G
/data/lost+found          8.0K

Export list for 192.168.10.45:
/export/lcm-data          192.168.10.0/24
/export/lcm-shared        192.168.10.0/24
```

!!! warning "Common errors"
    **`mount.nfs: access denied by server while mounting 192.168.10.45:/export/lcm-data`** — Verify the NFS server firewall allows port 2049 from the LCM appliance IP and check /etc/exports permissions on the NFS server.
    **`showmount: clnt_create: RPC: Port mapper failure - Unable to receive`** — Ensure the NFS server's portmapper (rpcbind) is running with `systemctl status rpcbind` and that port 111 is accessible.
Backup options:
- **NFS server snapshot**: if the NFS server supports snapshots (NetApp, Pure, vSAN File Services), schedule daily snapshots of the export volume
- **rsync to secondary storage**:

```bash
# Run from NFS server or a jump host with access to both locations
rsync -avz --progress /exports/lcm-repo/ /backup/lcm-repo-$(date +%Y%m%d)/
```


```text title="Expected output"
sending incremental file list
created directory /backup/lcm-repo-20240315
lcm-repo/
lcm-repo/manifest.json
         1,245 100%    2.34MB/s    0:00:00 (xfr#1, to-chk=847/849)
lcm-repo/bundles/
lcm-repo/bundles/aria-suite-8.14.0.tar.gz
       2,847,361,024 100%   18.92MB/s    0:02:15 (xfr#2, to-chk=846/848)
lcm-repo/bundles/vrealize-operations-8.14.0.tar.gz
       1,562,048,512 100%   21.45MB/s    0:01:12 (xfr#3, to-chk=845/847)
lcm-repo/config/
lcm-repo/config/lcm-config.yaml
         8,932 100%   15.67MB/s    0:00:00 (xfr#4, to-chk=844/846)
...
sent 4,421,847,293 bytes  received 12,847 bytes  32.18MB/s
total size is 4,421,834,156  speedup is 1.00
```

!!! warning "Common errors"
    **`rsync: change_dir "/exports/lcm-repo" failed: No such file or directory (2)`** — Verify the source path exists and is mounted on the current host with `ls -la /exports/lcm-repo`.
    **`Permission denied (13)`** — Ensure the user running rsync has read permissions on the source directory and write permissions on the destination with `chmod 755 /exports/lcm-repo` and `chmod 755 /backup/`.
    **`No space left on device (28)`** — Check available disk space on the destination with `df -h /backup/` and ensure sufficient free space exists for the full backup.
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


```text title="Expected output"
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBsb2NhbCIsImV4cCI6MTcwOTMxNjgwMH0.abc123xyz"}
{
  "documentSelfLink": "/lcm/lcmservice/api/v2/environments",
  "documentCount": 3,
  "documents": [
    {
      "documentSelfLink": "/lcm/lcmservice/api/v2/environments/env-prod-001",
      "name": "Production-vSphere-8.0",
      "type": "VSPHERE",
      "version": "8.0.1"
    },
    {
      "documentSelfLink": "/lcm/lcmservice/api/v2/environments/env-staging-002",
      "name": "Staging-vSphere-7.0",
      "type": "VSPHERE",
      "version": "7.0.3"
    },
    {
      "documentSelfLink": "/lcm/lcmservice/api/v2/environments/env-dev-003",
      "name": "Dev-vSphere-7.0",
      "type": "VSPHERE",
      "version": "7.0.2"
    }
  ]
}
{
  "documentSelfLink": "/lcm/lcmservice/api/v2/environments/env-prod-001",
  "name": "Production-vSphere-8.0",
  "type": "VSPHERE",
  "version": "8.0.1",
  "vcenterHostname": "vcenter-prod.example.local",
  "vcenterVersion": "8.0.0.10000",
  "clusterName": "Cluster-01",
  "nodeCount": 4
}
{
  "documentSelfLink": "/lcm/locker/api/v2/certificates",
  "documentCount": 12,
  "certificates": [
    {"alias":"vcenter-prod-cert","issuer":"CN=VMware-Root-CA","expiryDate":"2026-03-15T00:00:00Z","thumbprint":"a1b2c3d4e5f6..."},
    {"alias":"nsx-manager-cert","issuer":"CN=VMware-Root-CA","expiryDate":"2025-09-22T00:00:00Z","thumbprint":"f6e5d4c3b2a1..."},
    {"alias":"aria-ops-cert","issuer":"CN=VMware-Root-CA","expiryDate":"2027-01-10T00:00:00Z","thumbprint":"9z8y7x6w5v4u..."}
  ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl commands to skip SSL verification, or import the LCM server's CA certificate into your system trust store.
    **`jq: parse error: (null) is not defined at line 1, column 0`** — Verify the authentication token is valid by checking the login response; the API likely returned an error
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


```text title="Expected output"
admin@lcm-prod-01.example.local's password: 
● lcm.service - VMware Aria Suite Lifecycle Manager
     Loaded: loaded (/etc/systemd/system/lcm.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:42:33 UTC; 2 days ago
   Main PID: 4521 (java)
      Tasks: 47 (limit: 4915)
     Memory: 2.3G
     CGroup: /system.slice/lcm.service
             └─4521 /usr/lib/jvm/java-11-openjdk-11.0.18.0.10-1.el7_9.x86_64/bin/java -Xmx4g...

● nginx.service - The NGINX HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
     Active: active (running) since Mon 2024-01-15 09:43:12 UTC; 2 days ago
   Main PID: 4687 (nginx)
      Tasks: 3 (limit: 4915)
     Memory: 45.2M

LCM Status: RUNNING
Database Status: CONNECTED
Appliance Health: HEALTHY
Build: 8.13.1.20240110-1
```

!!! warning "Common errors"
    **`sudo: no tty present and no -S option was specified`** — Add `-t` flag to ssh command: `ssh -t admin@lcm-prod-01.example.local`
    **`Connection refused`** — Verify LCM appliance is reachable and SSH service is running; check firewall rules and DNS resolution for lcm-prod-01.example.local
    **`vracli: command not found`** — Source the vracli environment or use full path `/opt/vmware/vracli/bin/vracli status`
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


```text title="Expected output"
/dev/mapper/vg0-lv_root  50G   12G   38G  24% /
tmpfs                    16G      0   16G   0% /dev/shm
nfs-server.corp.local:/lcm-repo  500G  245G  255G  49% /data
```

!!! warning "Common errors"
    **`mount.nfs: mount point /data does not exist`** — Create the mount point directory with `mkdir -p /data` before running `mount -a`.
    **`mount.nfs: access denied by server while mounting nfs-server.corp.local:/lcm-repo`** — Verify NFS server exports the path and firewall allows NFS traffic (ports 111, 2049); check `/etc/exports` on the NFS server.
    **`mount: /etc/fstab: parse error at line X`** — Ensure the fstab entry has exactly 6 whitespace-separated fields with no trailing characters.
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

---

## See also

- [Aria Suite Lifecycle — Procedures](../procedures/)
- [Aria Suite Lifecycle — Common Issues](../../troubleshooting/common-issues/)
- [Aria Suite Lifecycle — Health Checks](../health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
