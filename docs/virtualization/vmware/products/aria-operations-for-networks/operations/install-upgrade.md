---
tags:
  - aria-networks
  - operations
  - vmware
---
# vRNI Install & Upgrade

*Applies to: VMware Aria 8.x*
![vRNI Install & Upgrade](../../../../../assets/virtualization-vmware-aria-operations-for-networks-operation.svg)

```bash
# Check HTTPS is reachable
curl -sk https://aon-platform.example.local -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200 (redirect to login page)

# SSH to platform to verify services
ssh ubuntu@aon-platform.example.local
sudo systemctl status vrni-platform nginx cassandra
```


```text title="Expected output"
HTTP 302
Connected to aon-platform.example.local.
● vrni-platform.service - VMware Aria Operations for Networks Platform
     Loaded: loaded (/etc/systemd/system/vrni-platform.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:42:17 UTC; 2h 34min ago
   Main PID: 2847 (java)
     CGroup: /system.slice/vrni-platform.service
             └─2847 /usr/lib/jvm/java-11-openjdk-amd64/bin/java -Xmx4g...

● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:41:52 UTC; 2h 34min ago
   Main PID: 1204 (nginx)

● cassandra.service - Apache Cassandra
     Loaded: loaded (/etc/systemd/system/cassandra.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:40:33 UTC; 2h 35min ago
   Main PID: 892 (java)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to curl to skip certificate verification (already present in the example, but if removed this is the error). |
    | `Connection refused` | Verify the platform VM is powered on and the hostname resolves correctly with `ndig aon-platform.example.local` or `ping aon-platform.example.local`. |
    | `● vrni-platform.service - VMware Aria Operations for Networks Platform / Active: inactive (dead)` | Restart the service with `sudo systemctl restart vrni-platform` and check logs with `sudo journalctl -u vrni-platform -n 50`. |
```bash
# 1. Take config backup
TOKEN=$(curl -sk -X POST "https://aon.example.local/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk "https://aon.example.local/api/ni/settings/backup" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  --output "aon-backup-pre-upgrade-$(date +%Y%m%d).tar.gz"

# 2. Take vSphere snapshot of Platform VM (via PowerCLI or vCenter UI)
# PowerCLI:
Get-VM "aon-platform-01" | New-Snapshot -Name "Pre-Upgrade-6.14.0" -Description "Before AON upgrade to 6.14.0"

# 3. Note current version
curl -sk "https://aon.example.local/api/ni/system/version" \
  -H "Authorization: NetworkInsight ${TOKEN}" | python3 -m json.tool
```

```text title="Expected output"
{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBsb2NhbCIsImV4cCI6MTcwOTMxNjgwMH0.abc123xyz"}
(no output — command completes silently)
aon-backup-pre-upgrade-20240301.tar.gz saved successfully

Name                 PowerState Cpu MemoryMB
----                 ---------- --- --------
aon-platform-01      PoweredOn   8   32768

New Snapshot created: Pre-Upgrade-6.14.0
SnapshotId: snapshot-1847

{
  "version": "6.13.2",
  "build": "20240228.001",
  "releaseDate": "2024-02-28",
  "productName": "VMware Aria Operations for Networks"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl commands to skip SSL verification for self-signed certificates. |
    | `jq: command not found` | Install `python3-json` or use `python3 -m json.tool` instead of piping to `jq`. |
    | `Get-VM : The term 'Get-VM' is not recognized` | Install VMware PowerCLI module with `Install-Module -Name VMware.PowerCLI -Force` on Windows PowerShell. |
```bash
ssh ubuntu@aon-platform.example.local

# Upload the upgrade bundle to the platform
scp VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak ubuntu@aon-platform.example.local:/tmp/

# On Platform VM
sudo /opt/vmware/bin/upgrade.sh /tmp/VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak

# Monitor upgrade progress
sudo tail -f /var/log/vrni-platform/upgrade.log
```

```text title="Expected output"
ubuntu@aon-platform.example.local's password: 
Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.15.0-86-generic x86_64)

 System load: 0.42             Processes: 187
 Usage of /: 18.3% of 19.53GB  Users logged in: 1

VMware-Aria-Operations-for-Networks-6.14.0-upgrade.pak     100%  2847MB   45.2MB/s   01:03
Verifying upgrade bundle integrity...
Bundle signature verified successfully.
Starting upgrade process for Aria Operations for Networks 6.14.0
[2024-01-15 14:32:18] Pre-upgrade validation: PASSED
[2024-01-15 14:32:45] Stopping services...
[2024-01-15 14:33:12] Backing up database...
[2024-01-15 14:35:22] Upgrading platform components...
[2024-01-15 14:42:18] Starting services...
[2024-01-15 14:43:05] Post-upgrade validation: PASSED
[2024-01-15 14:43:18] Upgrade completed successfully. New version: 6.14.0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied (publickey,password).` | Verify SSH credentials and that the ubuntu user exists on aon-platform.example.local, or use the correct hostname/IP address. |
    | `/opt/vmware/bin/upgrade.sh: No such file or directory` | Confirm the platform VM has Aria Operations for Networks installed in /opt/vmware and that you are running the upgrade script from the correct path. |
    | `Upgrade bundle signature verification failed` | Re-download the upgrade PAK file from VMware and verify its checksum matches the official release documentation. |
```bash
# Check version
curl -sk "https://aon.example.local/api/ni/system/version" \
  -H "Authorization: NetworkInsight ${TOKEN}" | python3 -m json.tool

# Check all services are running
ssh ubuntu@aon-platform.example.local
sudo systemctl status vrni-platform nginx cassandra kafka elasticsearch postgres

# Check Collectors re-connected (they should reconnect automatically)
curl -sk "https://aon.example.local/api/ni/collectors" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "
import sys,json
for c in json.load(sys.stdin).get('results',[]):
    print(c.get('nickname',''), c.get('status',''))
"
```

```text title="Expected output"
{
  "version": "6.10.1",
  "build": "21847392",
  "release_date": "2024-01-15"
}
● vrni-platform.service - Aria Operations for Networks Platform
     Loaded: loaded (/etc/systemd/system/vrni-platform.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:23:47 UTC; 2 days ago
● nginx.service - nginx HTTP and reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:24:12 UTC; 2 days ago
● cassandra.service - Apache Cassandra
     Loaded: loaded (/etc/systemd/system/cassandra.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:25:03 UTC; 2 days ago
● kafka.service - Apache Kafka
     Loaded: loaded (/etc/systemd/system/kafka.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:26:18 UTC; 2 days ago
● elasticsearch.service - Elasticsearch
     Loaded: loaded (/etc/systemd/system/elasticsearch.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:27:05 UTC; 2 days ago
● postgres.service - PostgreSQL Database Server
     Loaded: loaded (/etc/systemd/system/postgres.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 09:28:31 UTC; 2 days ago
dc1-collector-01 CONNECTED
dc2-collector-03 CONNECTED
dc3-collector-02 CONNECTED
edge-collector-01 CONNECTED
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip SSL verification, or import the self-signed certificate into your CA bundle. |
    | `Authorization: NetworkInsight ${TOKEN}: command not found` | Ensure the TOKEN environment variable is set with `export TOKEN=$(cat /path/to/token.txt)` before running the curl command. |
    | `Connection refused` or `ssh: Could not resolve hostname` | Verify the hostname `aon-platform.example.local` resolves correctly with `nslookup` or `ping`, and that SSH is accessible on port 22. |
```bash
# Revert Platform VM snapshot (this is a destructive operation — confirm before proceeding)
Get-VM "aon-platform-01" | Get-Snapshot -Name "Pre-Upgrade-6.14.0" | Set-VM -SnapShot $_ -Confirm:$false

# After revert, Collectors should auto-reconnect to the older Platform
# If not, re-pair manually:
ssh ubuntu@aon-collector-dc1.example.local
sudo /home/ubuntu/support/pairing.sh
```


```text title="Expected output"
Name                      Description                   Created
----                      -----------                   -------
Pre-Upgrade-6.14.0        Platform backup before 6.14   2024-01-15 14:32:18

Reverting to snapshot Pre-Upgrade-6.14.0...
Snapshot revert completed successfully.
aon-platform-01 powered on.

ubuntu@aon-collector-dc1:~$ sudo /home/ubuntu/support/pairing.sh
[sudo] password for ubuntu:
Pairing script v2.1.4 initialized
Attempting to pair with Platform VM at 10.42.8.15...
Connection established. Platform version: 6.13.2
Collector UUID: 550e8400-e29b-41d4-a716-446655440000
Pairing successful. Collector registered.
Restarting collector services...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Get-VM : The term 'Get-VM' is not recognized` | Load the VMware PowerCLI module with `Import-Module VMware.PowerCLI` before running the command. |
    | `Permission denied (publickey,password).` | Verify SSH key is configured or use `ssh -u ubuntu@aon-collector-dc1.example.local` with the correct password, and confirm the collector hostname is reachable. |
    | `pairing.sh: command not found` | Confirm the support directory exists at `/home/ubuntu/support/` and the script has execute permissions with `chmod +x /home/ubuntu/support/pairing.sh`. |
## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

!!! warning "Host enters maintenance mode"
    ESXi remediation puts hosts into maintenance mode, triggering DRS evacuation. Confirm DRS is Fully Automated and HA admission control is satisfied before starting.

---

## See also

- [vRNI Health Checks](../health-checks/)
- [vRNI Common Issues](../../troubleshooting/common-issues/)
- [AON Operational Procedures](../procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
