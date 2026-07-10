---
tags:
  - operations
  - vmware
  - vsphere-replication
---
# vSphere Replication — CLI Reference

<div class="kb-summary">
CLI Reference reference covering VRA Appliance SSH Access, VRA REST API Authentication, Get Replication Status via REST API, PowerCLI — Replication Status, VRA Health API and 2 more sections.

*Applies to: vSphere Replication 8.x*
</div>
![vSphere Replication — CLI Reference](../../../../../assets/virtualization-vmware-vsphere-replication-operations-cli-ref.svg)

  VR CLI and API Access

---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## VRA Appliance SSH Access

```bash
# SSH to VRA appliance (admin user)
ssh admin@vra-london.example.local
# Or: admin user → use appliance shell

# Check VRA service status
systemctl status hms        # Home Management Server — core VRA service
systemctl status vrms       # vSphere Replication Management Service
systemctl status nginx      # HTTPS proxy

# Restart VRA services (use with care — interrupts active replications briefly)
systemctl restart hms
systemctl restart vrms
```


```text title="Expected output"
admin@vra-london.example.local's password: 
Last login: Wed Mar 13 14:22:18 2024 from 10.45.12.89
vra-london:~ # systemctl status hms
● hms.service - Home Management Server
   Loaded: loaded (/etc/systemd/system/hms.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2024-03-13 14:18:33 UTC; 4min 12s ago
   Main PID: 2847 (java)
   Memory: 487.3M
   CGroup: /system.slice/hms.service
           └─2847 /usr/lib/jvm/java-11-openjdk/bin/java -Xmx1024m...

vra-london:~ # systemctl status vrms
● vrms.service - vSphere Replication Management Service
   Loaded: loaded (/etc/systemd/system/vrms.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2024-03-13 14:18:45 UTC; 4min 5s ago
   Main PID: 3156 (java)
   Memory: 312.8M

vra-london:~ # systemctl status nginx
● nginx.service - NGINX HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2024-03-13 14:18:22 UTC; 4min 23s ago
   Main PID: 1924 (nginx)
   Memory: 18.2M

vra-london:~ # systemctl restart hms
vra-london:~ # systemctl restart vrms
vra-london:~ #
```

!!! warning "Common errors"
    **`Unit hms.service not found.`** — Verify the VRA appliance version supports systemd; older versions may use service hms restart instead.
    **`Failed to restart vrms.service: Access denied`** — Ensure you are logged in as the admin user with sudo privileges, or use sudo systemctl restart vrms.
    **`Job for hms.service failed because the control process exited with error code.`** — Check /var/log/hms/hms.log for Java heap memory errors and increase -Xmx value if needed.
---

## VRA REST API Authentication

```bash
# Authenticate to VRA REST API
TOKEN=$(curl -sk -X POST \
  "https://vra-london.example.local/api/rest/vr/authentication/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}' | \
  python3 -c "import json,sys; print(json.load(sys.stdin).get('token',''))")

HEADERS="-H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json'"
```


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwOTMxNjU0MCwiZXhwIjoxNzA5MzIwMTQwfQ.kL9mN2pQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYz
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification (already present in example, but ensure it's not removed).
    **`jq: command not found` or `python3: command not found`** — Install the required JSON parser (`apt-get install python3` or `yum install python3`) or replace the Python one-liner with `jq '.token'`.
    **`{"error":"Invalid credentials","code":401}`** — Verify the username and password are correct and the VRA service is running and accessible at the specified hostname.
---

## Get Replication Status via REST API

```bash
# List all replications on this VRA
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-london.example.local/api/rest/vr/replications" | python3 -m json.tool

# Get replication status for a specific VM (by replication ID)
REPL_ID="<replication-id>"
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-london.example.local/api/rest/vr/replications/$REPL_ID" | python3 -m json.tool
```


```text title="Expected output"
{
  "replications": [
    {
      "id": "repl-4a8c9f2e-b1d3-47e2-9c5a-2f8e1b3d4c6a",
      "sourceVm": "prod-web-01",
      "targetVm": "prod-web-01-replica",
      "sourceVcenter": "vcenter-us-east.example.local",
      "targetVcenter": "vcenter-eu-west.example.local",
      "state": "SYNCED",
      "progress": 100,
      "lastSync": "2024-01-15T14:32:18Z",
      "rpo": 3600
    },
    {
      "id": "repl-7b2d1e4f-c9a8-41d6-8e3b-5a7c2f9d1b4e",
      "sourceVm": "prod-db-02",
      "targetVm": "prod-db-02-replica",
      "sourceVcenter": "vcenter-us-east.example.local",
      "targetVcenter": "vcenter-eu-west.example.local",
      "state": "SYNCING",
      "progress": 67,
      "lastSync": "2024-01-15T14:28:45Z",
      "rpo": 1800
    }
  ],
  "totalCount": 2
}
{
  "id": "repl-4a8c9f2e-b1d3-47e2-9c5a-2f8e1b3d4c6a",
  "sourceVm": "prod-web-01",
  "targetVm": "prod-web-01-replica",
  "sourceVcenter": "vcenter-us-east.example.local",
  "targetVcenter": "vcenter-eu-west.example.local",
  "state": "SYNCED",
  "progress": 100,
  "lastSync": "2024-01-15T14:32:18Z",
  "rpo": 3600,
  "bytesTransferred": 524288000,
  "estimatedTimeRemaining": 0,
  "networkCompression": 0.42
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or import the VRA's certificate into your system trust store.
    **`curl: (7) Failed to connect to vra-london.example.local port 443: Connection refused`** — Verify the VRA hostname/IP is correct, the VRA service is running, and network connectivity exists from your client to the VRA appliance.
    **`jq: error (at <stdin>:1): Cannot index object with string "replications"`** — Ensure the API token in `$TOKEN` is valid and has not expired; re-authenticate and export a fresh token.
---

## PowerCLI — Replication Status

```powershell
# Connect to vCenter
Connect-VIServer -Server vcenter.example.local

# Get all VMs with replication configured
$replicatedVMs = Get-VM | Where-Object {
    (Get-VIObjectByVIView -MORef $_.ExtensionData.MoRef |
     Get-View).Config.Hardware.Device |
    Where-Object { $_.GetType().Name -eq "VirtualDisk" } |
    Where-Object { $_.Backing.ChangeId }
}

# Using SRM module for VR-managed replications:
Import-Module VMware.VimAutomation.Srm
$srm = Connect-SrmServer -SrmServerAddress srm-london.example.local

# List protection groups with VR replications
$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()
foreach ($pg in $pgs) {
    $vms = $srm.ExtensionData.Protection.ListProtectedVms($pg)
    foreach ($vm in $vms) {
        Write-Host "$($vm.Vm.Name): $($vm.ReplicationState)"
    }
}
```

---

## VRA Health API

```bash
# Check VRA health (no auth required for health endpoint)
curl -sk https://vra-london.example.local/api/rest/vr/health | python3 -m json.tool

# Check VRA API version
curl -sk https://vra-london.example.local/api/rest/vr/deployment | python3 -m json.tool
```


```text title="Expected output"
{
  "state": "RUNNING",
  "build": "8.7.0.21260",
  "version": "8.7.0",
  "site_name": "London-DC",
  "site_id": "site-42a8c9d1-5e3f",
  "paired_sites": 1,
  "replication_pairs": 247,
  "healthy_pairs": 247,
  "unhealthy_pairs": 0,
  "uptime_seconds": 2592000
}
{
  "deployment_id": "vra-london-prod-01",
  "api_version": "8.7.0",
  "build_number": "21260",
  "deployment_type": "embedded",
  "node_count": 3,
  "cluster_status": "healthy",
  "last_sync": "2024-01-15T09:42:17Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in the example, but ensure it's included if removed).
    **`curl: (7) Failed to connect to vra-london.example.local port 443: Connection refused`** — Verify the VRA appliance is running and the hostname/IP is correct with `ping vra-london.example.local` or check network connectivity.
    **`json.tool: error: JSON document is empty`** — Confirm the VRA API service is fully initialized; wait 2-3 minutes after appliance startup and retry the health check.
---

## Test Connectivity from Source ESXi to Target VRA

```bash
# From ESXi host shell (SSH to ESXi host)
nc -vz vra-amsterdam.example.local 31031
# Must succeed for replication data transfer

nc -vz vra-amsterdam.example.local 44046
# VRA management port

# Or using vmkping from ESXi:
vmkping -I vmk1 vra-amsterdam.example.local
```


```text title="Expected output"
Connection to vra-amsterdam.example.local 31031 port [tcp/*] succeeded!
Connection to vra-amsterdam.example.local 44046 port [tcp/*] succeeded!
PING vra-amsterdam.example.local (192.168.42.108): 56 data bytes
64 bytes from 192.168.42.108: icmp_seq=0 time=2.341 ms
64 bytes from 192.168.42.108: icmp_seq=1 time=2.156 ms
64 bytes from 192.168.42.108: icmp_seq=2 time=2.289 ms
64 bytes from 192.168.42.108: icmp_seq=3 time=2.401 ms

--- vra-amsterdam.example.local statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 2.156/2.296/2.401 ms
```

!!! warning "Common errors"
    **`nc: getaddrinfo: Name or service not known`** — Verify the VRA hostname resolves correctly by running `nslookup vra-amsterdam.example.local` on the ESXi host.
    **`Connection refused`** — Confirm the VRA appliance is powered on and the replication service is running by checking VRA status in the vSphere Client.
    **`No route to host`** — Ensure the ESXi host has network connectivity to the VRA subnet and check firewall rules allow traffic on ports 31031 and 44046.
---

## Force Replication Sync (Immediate Sync)

When you need a VM to sync immediately regardless of scheduled interval:

```text
vCenter → Site Recovery → Replications → [VM] → Sync Now
```

There is no CLI for immediate sync — use the vCenter UI or the VRA REST API:

```bash
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://vra-london.example.local/api/rest/vr/replications/$REPL_ID/sync"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present; if error persists, verify the hostname matches the certificate CN).
    **`curl: (7) Failed to connect to vra-london.example.local port 443: Name or service not known`** — Ensure the vRA hostname is resolvable and reachable; check DNS or update `/etc/hosts` with the correct IP address.
    **`{"error":"Invalid or expired token","code":401}`** — Regenerate the Bearer token by re-authenticating to vRA and ensure `$TOKEN` variable is set correctly with `echo $TOKEN`.
---

## See also

- [vSphere Replication — Procedures](../procedures/)
- [vSphere Replication — Scripts](../scripts/)
- [vSphere Replication — Health Checks](../health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
