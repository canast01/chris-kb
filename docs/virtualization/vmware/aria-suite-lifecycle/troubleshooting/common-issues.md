---
tags:
  - aria-lcm
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Suite Lifecycle — Common Issues

<div class="kb-summary">
Common Issues reference covering Upgrade Gets Stuck or Times Out, NFS Mount Lost During Operation, Locker Certificate Import Fails, VIDM Authentication Failure After Password Change, Product Shows Red Health in LCM Dashboard and 1 more sections.

*Applies to: Aria LCM 8.x*
</div>
![Aria Suite Lifecycle — Common Issues](../../../../assets/virtualization-vmware-aria-suite-lifecycle-troubleshooting-c.svg)

  LCM Triage Decision Tree

If the upgrade is truly stuck (no log activity for 30+ minutes):
1. Do NOT power off product VMs — this risks split-brain state
2. Open a Broadcom SR with the LCM log bundle and the request ID
3. LCM may offer a **Retry** option for some stuck states — use only if advised by support

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
nfs_mount_lost_during_operation: "NFS Mount Lost During Operation" {shape: rectangle}
locker_certificate_import_fails: "Locker Certificate Import Fails" {shape: rectangle}
vidm_authentication_failure_after_pa: "VIDM Authentication Failure After Password Change" {shape: rectangle}
product_shows_red_health_in_lcm_dash: "Product Shows Red Health in LCM Dashboard" {shape: rectangle}
checking_request_history: "Checking Request History" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> nfs_mount_lost_during_operation: investigate
symptom -> locker_certificate_import_fails: investigate
symptom -> vidm_authentication_failure_after_pa: investigate
symptom -> product_shows_red_health_in_lcm_dash: investigate
symptom -> checking_request_history: investigate
diagnostic_flow -> resolution
nfs_mount_lost_during_operation -> resolution
locker_certificate_import_fails -> resolution
vidm_authentication_failure_after_pa -> resolution
product_shows_red_health_in_lcm_dash -> resolution
checking_request_history -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
B1: "Product upgrade failed mid-way" {shape: rectangle}
B2: "Certificate sync error" {shape: rectangle}
B3: "Environment health check red" {shape: rectangle}
B4: "Locker credential or cert import fails" {shape: rectangle}
B5: "NFS mount lost during operation" {shape: rectangle}
B6: "vIDM authentication failure" {shape: rectangle}
D1: "D1" {shape: rectangle}
R1: "Open Broadcom SR with LCM Log Bundle\n→ Product Shows Red Health in LCM Dashboard" {shape: rectangle}
R2: "Review installer.log · Use Retry if Offered\n→ Product Shows Red Health in LCM Dashboard" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Re-import Correct Cert · Run Replace Cert Action in LCM\n→ Locker Certificate Import Fails" {shape: rectangle}
R4: "Check Product Cert Trust Chain · Verify openssl verify\n→ Locker Certificate Import Fails" {shape: rectangle}
R5: "Click Red Card · Check Service Status · Run Health Check\n→ Product Shows Red Health in LCM Dashboard" {shape: rectangle}
R6: "Verify Key Matches Cert · Confirm No Passphrase on Key\n→ Locker Certificate Import Fails" {shape: rectangle}
R7: "Remount NFS · Verify Write Access · Remap Binary Mapping\n→ NFS Mount Lost During Operation" {shape: rectangle}
R8: "Re-register vIDM in LCM Settings · Update Credentials\n→ VIDM Authentication Failure After Password Change" {shape: rectangle}

S -> B1
S -> B2
S -> B3
S -> B4
S -> B5
S -> B6
D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
B3 -> R5
B4 -> R6
B5 -> R7
B6 -> R8
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## NFS Mount Lost During Operation

If the NFS share becomes unavailable while LCM is running:

```bash
# Check mount status
mount | grep /data
df -h /data

# Attempt remount
mount -a
# or explicitly:
mount -t nfs <nfs-server>:/lcm-repo /data

# Verify write access
touch /data/.write-test && echo "OK" && rm /data/.write-test

# Check for NFS errors in syslog
grep -i "nfs\|mount" /var/log/messages | tail -30
```


```text title="Expected output"
/dev/mapper/vg0-lv_data on /data type ext4 (rw,relatime,errors=remount-ro)
Filesystem     Size  Used Avail Use% Mounted on
/data          500G  245G  255G  49% /data
OK
nfs-server.corp.local:/lcm-repo on /data type nfs4 (rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.1.42,local_lock=none,addr=192.168.1.10)
Dec 12 14:23:01 aria-lcm-01 kernel: NFS: Server 192.168.1.10 not responding, still trying
Dec 12 14:24:15 aria-lcm-01 kernel: NFS: Server 192.168.1.10 OK
Dec 12 14:25:42 aria-lcm-01 kernel: nfs4: state manager: lease expired
Dec 12 14:26:08 aria-lcm-01 systemd: Mounted /data.
Dec 12 14:27:33 aria-lcm-01 kernel: NFS: Server 192.168.1.10 not responding, still trying
Dec 12 14:28:01 aria-lcm-01 kernel: NFS: Server 192.168.1.10 OK
```

!!! warning "Common errors"
    **`mount: mount point /data does not exist`** — Create the mount point with `mkdir -p /data` before attempting to mount.
    **`mount.nfs: access denied by server while mounting nfs-server:/lcm-repo`** — Verify NFS export permissions on the server and ensure the client IP is listed in `/etc/exports` with appropriate read-write flags.
    **`touch: cannot touch '/data/.write-test': Read-only file system`** — Remount with write permissions using `mount -o remount,rw /data` or check NFS server export settings for `ro` restrictions.
After restoring the NFS mount, any in-progress upgrade will need to be resumed or retried via LCM. If the upgrade failed due to missing binaries, re-map the product binaries in **Lifecycle Operations → Settings → Binary Mapping** before retrying.

---

## Locker Certificate Import Fails

```bash
# Verify certificate chain validity before importing
openssl verify -CAfile chain.pem leaf.pem
# Expected: leaf.pem: OK

# Check that the private key matches the certificate
openssl x509 -noout -modulus -in leaf.pem | md5sum
openssl rsa -noout -modulus -in private.key | md5sum
# Both MD5 hashes must match

# Verify SANs in the certificate
openssl x509 -noout -text -in leaf.pem | grep -A5 "Subject Alternative Name"

# Confirm no passphrase on the private key (LCM requires unencrypted key)
openssl rsa -in private.key -check 2>&1 | head -1
# Must output: RSA key ok (not: Enter pass phrase)
```


```text title="Expected output"
leaf.pem: OK
8f7c2d9e1a4b5c6f3e2d1a9b8c7f6e5d  -
8f7c2d9e1a4b5c6f3e2d1a9b8c7f6e5d  -
        X509v3 Subject Alternative Name: 
            DNS:aria-lcm.internal.corp, DNS:*.internal.corp, IP Address:10.42.18.55
RSA key ok
```

!!! warning "Common errors"
    **`leaf.pem: CN = aria-lcm.internal.corp, error 20 at 0 depth lookup: unable to get local issuer certificate`** — Ensure the intermediate CA certificate is included in chain.pem in the correct order (root last).
    **`8f7c2d9e1a4b5c6f3e2d1a9b8c7f6e5d  - (certificate hash)` does not match private key hash** — Regenerate the certificate and private key pair together, or verify you are using the correct matching files.
    **`Enter PEM pass phrase:`** — Remove the passphrase from the private key using `openssl rsa -in private.key -out private.key.nopass` before importing into LCM.
---

## VIDM Authentication Failure After Password Change

If the VIDM admin password is changed externally, LCM loses its registration credentials.

```bash
# Verify VIDM health from LCM appliance
curl -sk https://vidm.example.local/SAAS/API/1.0/REST/system/health
# If health is UP but login fails, re-register VIDM:
```


```text title="Expected output"
{
  "status": "UP",
  "timestamp": "2024-01-15T09:42:33.847Z",
  "components": {
    "database": "UP",
    "cache": "UP",
    "messaging": "UP",
    "ldap": "UP"
  },
  "version": "8.10.2.1234",
  "build": "20240110-143022"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in the example, but ensure it's lowercase `-sk` not `-Sk`).
    **`curl: (7) Failed to connect to vidm.example.local port 443: Connection refused`** — Verify VIDM appliance is running and network connectivity exists; check firewall rules and DNS resolution with `nslookup vidm.example.local`.
    **`{"error":"Unauthorized","code":401}`** — Ensure the LCM appliance service account has valid credentials and VIDM trust relationship is intact; re-register VIDM in LCM as indicated in the documentation.
Re-register VIDM: **LCM → Settings → Identity Manager → Edit → update credentials → Save**.

After re-registration, verify that all AD-backed users can still log into LCM via the VIDM login button.

---

## Product Shows Red Health in LCM Dashboard

1. Click the red product card — LCM shows the specific component or service that is unhealthy
2. SSH to the product appliance and check service status:

```bash
ssh admin@<product-fqdn>
vracli status
systemctl status <failing-service>
journalctl -u <failing-service> --since "1 hour ago" | tail -100
```


```text title="Expected output"
admin@aria-lcm-prod-01.corp.local's password: 
Welcome to VMware Aria Suite Lifecycle 8.14.2
Last login: Wed Jan 15 14:32:18 2025 from 192.168.1.45

vracli status
Service Status Report - aria-lcm-prod-01.corp.local
================================================
vra-server                    RUNNING (PID: 2847)
vra-config-server             RUNNING (PID: 2851)
vra-iaas-service              RUNNING (PID: 2856)
vra-orchestrator              RUNNING (PID: 2862)
vra-dsc-service               STOPPED
vra-gateway                   RUNNING (PID: 2871)

systemctl status vra-dsc-service
● vra-dsc-service.service - VMware Aria DSC Service
     Loaded: loaded (/etc/systemd/system/vra-dsc-service.service; enabled; vendor preset: disabled)
     Active: inactive (dead) since Wed 2025-01-15 13:47:22 UTC; 47min ago
     Process: 2156 ExecStart=/opt/vmware/vra/bin/dsc-service.sh (code=exited, status=1)
     Main PID: 2156 (code=exited, status=1)

journalctl -u vra-dsc-service --since "1 hour ago" | tail -100
Jan 15 13:47:18 aria-lcm-prod-01 vra-dsc-service[2156]: ERROR: Failed to connect to database host db-cluster-01.corp.local:5432
Jan 15 13:47:19 aria-lcm-prod-01 vra-dsc-service[2156]: Connection timeout after 30 seconds
Jan 15 13:47:22 aria-lcm-prod-01 systemd[1]: vra-dsc-service.service: Main process exited, code=exited, status=1/FAILURE
Jan 15 13:47:22 aria-lcm-prod-01 systemd[1]: vra-dsc-service.service: Unit entered failed state.
Jan 15 13:47:23 aria-lcm-prod-01 systemd[1]: vra-dsc-service.service: Failed with result 'exit-code'.
```

!!! warning "Common errors"
    **`Connection timeout after 30 seconds`** — Verify database connectivity from the Aria appliance with `telnet db-cluster-01.corp.local 5432` and confirm the PostgreSQL service is running on the database host.
    **`vra-dsc-service.service: Main process exited, code=exited, status=1/FAILURE`** — Check the service configuration file at `/etc/systemd/system/vra-dsc-service.service` for correct environment variables and restart with `systemctl restart vra-dsc-service`.
3. Common causes: disk full on the product appliance, internal service crash, or expired certificate
4. If the product health does not self-recover after the root cause is resolved: **LCM → Environments → product card → Run Health Check** to force a re-evaluation

---

## Checking Request History

All LCM operations are tracked as requests with full audit logs:

```bash
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.example.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<password>"}' | jq -r '.token')

# List last 20 requests
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/requests?size=20" | \
  jq -r '.[] | "\(.state)\t\(.requestType)\t\(.requestId)\t\(.startTime)"'

# Get detail of a failed request
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/requests/<request-id>" | \
  jq '.tasks[] | {name: .taskName, state: .taskState, message: .message}'
```


```text title="Expected output"
SUCCEEDED	ClusterUpgrade	req-2024-01-15-001	2024-01-15T09:23:45.123Z
SUCCEEDED	ProductPatch	req-2024-01-14-042	2024-01-14T14:52:12.456Z
FAILED	ClusterUpgrade	req-2024-01-14-038	2024-01-14T11:18:33.789Z
IN_PROGRESS	ProductPatch	req-2024-01-15-003	2024-01-15T10:05:22.234Z
SUCCEEDED	EnvironmentRefresh	req-2024-01-13-091	2024-01-13T16:41:09.567Z
SUCCEEDED	ClusterUpgrade	req-2024-01-13-087	2024-01-13T15:33:44.890Z
FAILED	ProductPatch	req-2024-01-12-065	2024-01-12T08:19:51.012Z
...
{
  "name": "ValidateClusterHealth",
  "state": "FAILED",
  "message": "Health check failed: Node lcm-prod-02.example.local unreachable (timeout after 30s)"
}
{
  "name": "PreUpgradeBackup",
  "state": "SUCCEEDED",
  "message": null
}
{
  "name": "ApplyPatches",
  "state": "FAILED",
  "message": "Insufficient disk space on /var/lib/lcm: 2.1GB available, 5GB required"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification (already present in the example, but ensure it's not removed).
    **`jq: parse error: Cannot index string with string "token"`** — Verify the login credentials are correct and the LCM service is responding with valid JSON; check the password doesn't contain special characters that need escaping.
    **`curl: (7) Failed to connect to lcm-prod-01.example.local port 443: Connection refused`** — Confirm the LCM appliance hostname/IP is correct and the service is running with `systemctl status lcm` on the LCM host.
---

## See also

- [Aria Suite Lifecycle — Diagnostics](../diagnostics/)
- [Aria Suite Lifecycle — Escalation](../escalation/)
- [Aria Suite Lifecycle — Health Checks](../../operations/health-checks/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
