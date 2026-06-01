# vCenter — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Service Health, Log Locations, DNS and NTP Validation, Certificate Checks, SSO and Identity Source Diagnostics and 4 more sections.
</div>

```text
Diagnostic Chain — Priority Order
════════════════════════════════════════════════════════

  ┌─────┐
  │  1  │  df -h
  │     │  /storage/log · /storage/db · /storage/core
  │     │  Full partition = root cause (stop here, fix disk first)
  └──┬──┘
     │
  ┌──▼──┐
  │  2  │  service-control --status --all
  │     │  Identify stopped services → check dependency order
  └──┬──┘
     │
  ┌──▼──┐
  │  3  │  DNS + NTP
  │     │  nslookup <vcenter-fqdn>  ·  timedatectl
  │     │  Skew >5 min = Kerberos/SSO breaks
  └──┬──┘
     │
  ┌──▼──┐
  │  4  │  Certificates
  │     │  VAMI → Certificate Management (expiry dates)
  │     │  openssl s_client -connect <vcenter>:443
  └──┬──┘
     │
  ┌──▼──┐
  │  5  │  SSO / STS health
  │     │  service-control --status vmware-stsd
  │     │  vmafd-cli get-domain-name / get-ls-location
  └──┬──┘
     │
  ┌──▼──┐
  │  6  │  Log review
  │     │  tail -f /var/log/vmware/vpxd/vpxd.log
  │     │  tail -f /var/log/vmware/sso/vmware-sts-idmd.log
  └──┬──┘
     │
  ┌──▼──┐
  │  7  │  vm-support bundle
  │     │  /usr/bin/vm-support  →  upload to Broadcom case
  └─────┘
```
┌──────────────────────────────────── vCenter Server — Diagnostics ─────────────────────────────────────┐
│                                                                                                       │
│  vCenter diagnostics use log bundles, service status checks, and database queries                     │
│  to identify root causes of connectivity, performance, and auth failures.                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Collection                │  │             Service Diagnostics             │   │
│   │            Support bundle: VC UI             │  │             vmon-cli -l (status)            │   │
│   │          vc-support.sh on appliance          │  │            journalctl -u vmware-*           │   │
│   │              Key logs: vpxd.log              │  │           service-control --status          │   │
│   │           SSO: ssoAdminServer.log            │  │           Check port 443/9443 open          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Collect support bundle first; vpxd.log and SSO logs cover 90% of issues.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            DB & Performance Diag             │  │             Network Diagnostics             │   │
│   │      Postgres: select pg_stat_activity       │  │            Ping VC from ESXi host           │   │
│   │          DB size: /storage/db usage          │  │           nslookup: VC FQDN + PTR           │   │
│   │           Slow UI: vpxd CPU usage            │  │         traceroute: management path         │   │
│   │          Stats rollup: latency logs          │  │           Port test: nc -zv vc 443          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  All diagnostic access is via SSH to VCSA appliance or via browser to vSphere Client;                 │
│  support bundles are downloaded via browser UI.                                                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vc-support.sh = generates support bundle on VCSA; exports to /tmp                                    │
│  vpxd.log      = main vCenter Server log; task, event, error messages                                 │
│  ssoAdminServer= SSO authentication service log; login failures here                                  │
│  pg_stat_activity= Postgres view; shows active DB queries                                             │
│  vmon-cli      = service monitor; RUNNING/STOPPED states                                              │
│  journalctl    = systemd log; vmware-* services write here                                            │
│  /storage      = VCSA data partition; contains DB, logs, stats                                        │
│  nc -zv        = netcat; test TCP port reachability                                                   │
│  nslookup PTR  = reverse DNS check; must match forward A record                                       │
│  Support bundle= ZIP of all VCSA logs + config; send to GSS                                           │
│  Stats rollup  = scheduled job; aggregates perf metrics; latency = problem                            │
│  vpxd CPU      = high vCenter process CPU = query storm or stuck tasks                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## Service Health

### Appliance Management Interface (VAMI)

Log into `https://<vcenter>:5480` to get an immediate overview:
- **Summary** tab — CPU, memory, disk usage per partition
- **Services** tab — status of every vCenter service (started/stopped)
- **Monitor** tab — resource utilisation graphs
- **Networking** tab — confirm IP, DNS, and hostname

### Service Status from Shell

```bash
# SSH to VCSA as root or as a user with shell access

# Summary of all services
service-control --status --all

# Individual service checks
service-control --status vpxd              # core vCenter daemon
service-control --status vmware-vpostgres  # embedded PostgreSQL
service-control --status vmware-stsd       # SSO token service
service-control --status vmware-sts-idmd   # SSO identity management daemon
service-control --status vmware-lookupsvc  # service registry / lookup service
service-control --status applmgmt          # VAMI (port 5480)
service-control --status vsphere-ui        # vSphere Client (HTML5 UI)
service-control --status vmware-eam        # ESX Agent Manager

# Alternative — vmon-cli (more granular)
vmon-cli --list
vmon-cli --status vpxd
```

### Disk Partition Usage

Full partitions are the most common cause of cascading vCenter failures. Check before and after any service restart.

```bash
df -h
```

Key partitions:

| Partition | Purpose | Alert Threshold |
|---|---|---|
| `/storage/log` | vCenter and service logs | 80% |
| `/storage/db` | vCenter PostgreSQL database | 80% |
| `/storage/core` | Core appliance data, config | 80% |
| `/storage/seat` | Stats, events, alarms, and tasks DB | 80% |
| `/` | Root filesystem | 85% |

Clearing `/storage/log`:
```bash
# Find large log files
du -sh /var/log/vmware/*/
du -sh /storage/log/*/

# Remove compressed old logs (safe to delete)
find /var/log/vmware -name "*.gz" -mtime +30 -delete
find /storage/log -name "*.gz" -mtime +30 -delete

# Do NOT delete active .log files — truncate if critically full
> /var/log/vmware/vpxd/vpxd.log   # last resort; only if vpxd is stopped
```

---

## Log Locations

All logs are on the VCSA appliance at `/var/log/vmware/` or in `/storage/log/vmware/`.

| Component | Primary Log Path |
|---|---|
| vpxd (core vCenter) | `/var/log/vmware/vpxd/vpxd.log` |
| vpxd-profiler | `/var/log/vmware/vpxd/vpxd-profiler.log` |
| vSphere Client | `/var/log/vmware/vsphere-ui/logs/vsphere_client_virgo.log` |
| SSO identity daemon | `/var/log/vmware/sso/vmware-sts-idmd.log` |
| SSO admin server | `/var/log/vmware/sso/ssoAdminServer.log` |
| vAPI endpoint | `/var/log/vmware/vapi/endpoint.log` |
| Appliance mgmt (VAMI) | `/var/log/vmware/applmgmt/applmgmt.log` |
| Upgrade / patching | `/var/log/vmware/applmgmt/software-packages.log` |
| Certificate manager | `/var/log/vmware/vmcad/certificate-manager.log` |
| PostgreSQL | `/var/log/vmware/vpostgres/postgresql-*.log` |
| vmdird (LDAP/vmdir) | `/var/log/vmware/vmdird/vmdird-syslog.log` |
| Lookup service | `/var/log/vmware/lookupsvc/lookup-service.log` |
| ESX Agent Manager | `/var/log/vmware/eam/eam.log` |
| rhttpproxy (reverse proxy) | `/var/log/vmware/rhttpproxy/rhttpproxy.log` |

### Tailing Logs in Real Time

```bash
# Watch vpxd for errors during a service restart or incident
tail -f /var/log/vmware/vpxd/vpxd.log

# Filter for error-level messages only
tail -f /var/log/vmware/vpxd/vpxd.log | grep -i "error\|fatal\|panic"

# SSO login failures
tail -f /var/log/vmware/sso/vmware-sts-idmd.log | grep -i "fail\|error\|bind"

# Certificate operations
tail -f /var/log/vmware/vmcad/certificate-manager.log
```

---

## DNS and NTP Validation

DNS and NTP failures cascade into certificate, SSO, and agent failures. Validate these first during any incident.

```bash
# Forward DNS — vCenter must resolve its own FQDN
nslookup vcenter.example.local
dig vcenter.example.local

# Reverse DNS — must resolve back to the FQDN
nslookup <vcenter-ip>

# Test ESXi host resolution from vCenter
nslookup esxi-01.example.local

# NTP status on the appliance
timedatectl
chronyc sources -v    # if chrony is the NTP client
chronyc tracking

# Check time offset against NTP servers
chronyc makestep      # force immediate sync (use carefully in production)
```

NTP drift over 5 minutes breaks Kerberos authentication, causing SSO login failures for AD-backed accounts. If clocks are skewed, fix NTP and allow time to resync before investigating SSO issues.

---

## Certificate Checks

```bash
# Check Machine SSL certificate expiry from outside the VCSA
echo | openssl s_client -connect vcenter.example.local:443 \
    -servername vcenter.example.local 2>/dev/null \
    | openssl x509 -noout -dates

# Check VAMI certificate
echo | openssl s_client -connect vcenter.example.local:5480 2>/dev/null \
    | openssl x509 -noout -dates

# List all certificate stores on VCSA
/usr/lib/vmware-vmafd/bin/vecs-cli store list

# List certificates in the Machine SSL store with expiry
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text \
    | grep -E "Alias|Subject|Not After"

# List VMCA root certificate
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store TRUSTED_ROOTS --text \
    | grep -E "Alias|Subject|Not After"

# List solution user certificates
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store vpxd-extension --text \
    | grep -E "Alias|Not After"
```

Check certificate expiry in VAMI: **`https://<vcenter>:5480` → Certificate Management**. The UI shows all certificates with expiry dates and a renewal button.

---

## SSO and Identity Source Diagnostics

```bash
# SSO service health
service-control --status vmware-stsd
service-control --status vmware-sts-idmd

# SSO domain info
/usr/lib/vmware-vmafd/bin/vmafd-cli get-domain-name --server-name localhost

# Lookup service endpoint
/usr/lib/vmware-vmafd/bin/vmafd-cli get-ls-location --server-name localhost

# Test LDAP connectivity to AD domain controller from VCSA
ldapsearch -x \
    -H ldaps://dc01.example.local:636 \
    -b "DC=corp,DC=local" \
    -D "svc-vcenter-ldap@corp.local" \
    -W \
    "(objectClass=*)" dn

# Check vmdir (embedded LDAP for vsphere.local) health
/usr/lib/vmware-vmafd/bin/dir-cli ssogroup list --login administrator@vsphere.local
```

---

## vCenter API Health Check

```bash
# Authenticate and get a session token
TOKEN=$(curl -sk -u 'administrator@vsphere.local:<password>' \
    -X POST https://vcenter.example.local/api/session | tr -d '"')

# Get system health
curl -sk -H "vmware-api-session-id: $TOKEN" \
    https://vcenter.example.local/api/vcenter/health/system

# List all hosts via API
curl -sk -H "vmware-api-session-id: $TOKEN" \
    https://vcenter.example.local/api/vcenter/host | python3 -m json.tool

# List all VMs via API
curl -sk -H "vmware-api-session-id: $TOKEN" \
    https://vcenter.example.local/api/vcenter/vm | python3 -m json.tool

# Delete the session when done
curl -sk -H "vmware-api-session-id: $TOKEN" \
    -X DELETE https://vcenter.example.local/api/session
```

---

## PowerCLI Diagnostics

```powershell
# Connect
Connect-VIServer -Server vcenter.example.local

# Host connection states — result should be empty in a healthy environment
Get-VMHost | Where-Object { $_.ConnectionState -ne "Connected" } |
    Select-Object Name, ConnectionState, PowerState

# Cluster HA and DRS state
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel, HAAdmissionControlEnabled

# Datastore accessibility and capacity
Get-Datastore | Select-Object Name,
    @{N="Accessible";E={$_.ExtensionData.Summary.Accessible}},
    @{N="CapGB";E={[math]::Round($_.CapacityGB,1)}},
    @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}},
    @{N="FreePct";E={[math]::Round($_.FreeSpaceGB/$_.CapacityGB*100,1)}} |
    Sort-Object FreePct

# Recent error-level events (last 6 hours)
Get-VIEvent -Start (Get-Date).AddHours(-6) |
    Where-Object { $_.GetType().Name -match "Error|Fault|Warning" } |
    Select-Object CreatedTime, UserName, FullFormattedMessage |
    Format-Table -Wrap

# Recent tasks with failures
Get-Task -Status Error | Select-Object -First 20 |
    Select-Object Name, State, StartTime, FinishTime, Description

# Active alarms across all objects
Get-VM | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="Alarms";E={$_.ExtensionData.TriggeredAlarmState.Count}}

# vCenter version and build
$global:DefaultVIServer | Select-Object Name, Version, Build, IsConnected
```

---

## Support Bundle Collection

Collect before escalating to Broadcom/VMware Support. The bundle includes all logs, configuration state, and diagnostic data.

### From VAMI (Recommended)

```text
https://<vcenter>:5480 → Support → Create Support Bundle
```

Wait for the bundle to generate (5–20 minutes depending on environment size), then download via the provided link.

### From VCSA Shell

```bash
# Generate vm-support bundle
/usr/bin/vm-support -n vcenter.example.local

# Output is in /var/core/ — copy to a transfer location
ls -lh /var/core/esx-*.tgz

# SCP the bundle off the appliance
scp /var/core/esx-<timestamp>.tgz user@transfer-host:/path/
```

### From vSphere Client

**Administration → Deployment → System Configuration → Export System Logs**

Select the components to include. For a full incident, include all vCenter server logs and optionally ESXi host logs for affected hosts.

### ESXi Host Log Bundle

```bash
# SSH to ESXi host or use DCUI → Troubleshooting Options → ESXi Shell
vm-support
# Bundle created in /var/core/
```

---

## Evidence to Collect Before Escalation

Before opening a support case or handing off to another team:

| Evidence Item | How to Collect |
|---|---|
| VCSA disk usage | `df -h` output |
| Service status | `service-control --status --all` output |
| VAMI screenshot | Browser screenshot of VAMI → Summary and Services |
| vpxd.log excerpt | `tail -500 /var/log/vmware/vpxd/vpxd.log` |
| SSO log excerpt | `tail -200 /var/log/vmware/sso/vmware-sts-idmd.log` |
| Certificate expiry | VAMI → Certificate Management screenshot |
| Recent events | vCenter → Monitor → Events, last 24 hours, exported |
| Recent tasks | vCenter → Monitor → Tasks, filter by Error state |
| VM-support bundle | `/usr/bin/vm-support` output |
| vCenter build number | `https://<vcenter>/ui` → Help → About |
| Change log | Recent changes from CMDB or change management system |

Timestamp all evidence with the collection time. Upload support bundles directly to the Broadcom case — do not email large files.
