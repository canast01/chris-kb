# vCenter Troubleshooting — Common Issues


<div class="kb-summary">
Common Issues reference covering Issue Summary, vCenter Services Not Starting, Certificate Errors, ESXi Host Disconnected or Not Responding, SSO / Authentication Failures and 5 more sections.
</div>

```text
Symptom Triage Map
════════════════════════════════════════════════════════

  Start: vCenter issue reported
         │
         ▼
  ┌──────────────────┐   YES   ┌──────────────────────────────┐
  │ Disk partition   │────────▶│ Free /storage/log or /db     │
  │ full? (df -h)    │         │ Remove *.gz files >30 days   │
  └──────┬───────────┘         └──────────────────────────────┘
         │ NO
         ▼
  ┌──────────────────┐   STOP  ┌──────────────────────────────┐
  │ vpxd running?    │────────▶│ Check vpostgres first        │
  │ service-control  │         │ Start DB → then vpxd         │
  │ --status vpxd    │         │ tail vpxd.log for root error  │
  └──────┬───────────┘         └──────────────────────────────┘
         │ RUNNING
         ▼
  ┌──────────────────┐   FAIL  ┌──────────────────────────────┐
  │ SSO login OK?    │────────▶│ Restart vmware-stsd          │
  │ administrator@   │         │ Check AD bind account/LDAPS  │
  │ vsphere.local    │         │ Check NTP skew (>5 min fails) │
  └──────┬───────────┘         └──────────────────────────────┘
         │ OK
         ▼
  ┌──────────────────┐ EXPIRED ┌──────────────────────────────┐
  │ Certificates     │────────▶│ certificate-manager          │
  │ valid?           │         │ (Machine SSL or STS renewal) │
  │ VAMI → Certs     │         │ Maintenance window required  │
  └──────┬───────────┘         └──────────────────────────────┘
         │ OK
         ▼
  ┌──────────────────┐
  │ Check vpxd.log   │  → escalate if DB corrupt or
  │ for root error   │    services unrecoverable
  └──────────────────┘
```
```
┌─────────────────────────────────── vCenter Server — Common Issues ────────────────────────────────────┐
│                                                                                                       │
│  Common vCenter issues: hosts disconnecting, certificate errors, SSO login failure,                   │
│  service crashes, disk space exhaustion, and database performance degradation.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Connectivity Issues              │  │              Certificate Issues             │   │
│   │        Host disconnected: check vpxa         │  │          Login fails: cert expired          │   │
│   │         Reconnect: right-click host          │  │            Error: SEC_E_UNTRUSTED           │   │
│   │         vpxa restart: esxcli on host         │  │           Fix: renew cert via VAMI          │   │
│   │         Network check: ping VC FQDN          │  │          STS cert: scripted renewal         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cert expiry is the most common cause of login/connectivity failures; check first.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Service & Disk Issues             │  │              SSO & Login Issues             │   │
│   │          Service down: vmon-cli -l           │  │            SSO: password lock out           │   │
│   │           Restart: service-control           │  │            Unlock: dir-cli unlock           │   │
│   │        Disk /storage >80%: purge logs        │  │            AD: domain unreachable           │   │
│   │       DB vacuum stuck: kill + restart        │  │           Use local SSO for access          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Most issues trace back to: network (FQDN/DNS), storage (disk full), time (NTP),                      │
│  or certificates (expired); check all four before deep investigation.                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vpxa          = vCenter host agent; handles VC→host communication                                    │
│  vmon-cli -l   = list all VCSA services and their current state                                       │
│  service-control= restart VCSA services; --restart --all (use carefully)                              │
│  dir-cli       = SSO CLI; list users, unlock accounts, set passwords                                  │
│  SEC_E_UNTRUSTED= Windows error: cert chain not trusted; replace cert                                 │
│  STS cert      = Security Token Service cert; 2yr expiry; most common failure                         │
│  /storage      = VCSA data partition; full = service crashes                                          │
│  DB vacuum     = Postgres autovacuum job; kill if stuck; restart postgres                             │
│  NTP skew      = clock drift >5min breaks SSO certificate validation                                  │
│  Reconnect     = right-click disconnected host; re-establishes vpxa link                              │
│  Local SSO     = vsphere.local admin; always works if AD is unreachable                               │
│  Log purge     = /var/log compression/rotation; also rotate stats DB                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

### Resolution

```bash
# If disk space is the cause — clear old logs first, then restart
du -sh /var/log/vmware/*/
find /var/log/vmware -name "*.gz" -mtime +30 -delete

# Restart in dependency order: DB first, then vpxd
service-control --start vmware-vpostgres
service-control --start vpxd
service-control --status vpxd

# If vpxd still fails, attempt a full restart of all services
service-control --stop --all
service-control --start --all
```

**Log location:** `/var/log/vmware/vpxd/vpxd.log`

---

## Certificate Errors

### Symptoms
- Browser shows SSL certificate warning or ERR_CERT_AUTHORITY_INVALID
- ESXi agents cannot connect to vCenter
- PowerCLI `Connect-VIServer` throws certificate-related exceptions
- VAMI shows certificate status as Expired

### Check Certificate Expiry

```bash
# Check Machine SSL certificate expiry from outside VCSA
echo | openssl s_client -connect <vcenter-fqdn>:443 -servername <vcenter-fqdn> 2>/dev/null \
  | openssl x509 -noout -dates

# List certificates in VECS store on VCSA (SSH)
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text \
  | grep -E "Alias|Not After"
```

### Resolution — Renew Machine SSL (VMCA-signed)

```bash
# From VCSA SSH: launch certificate manager
/usr/lib/vmware-vmca/bin/certificate-manager

# Select option 4: Regenerate a New VMCA Root Certificate and replace all certificates
# OR option 6: Replace Machine SSL certificate with VMCA Certificate
```

After renewal, restart services and verify:

```bash
service-control --stop --all
service-control --start --all

# Re-check certificate
echo | openssl s_client -connect <vcenter-fqdn>:443 2>/dev/null \
  | openssl x509 -noout -dates
```

**Log location:** `/var/log/vmware/vmcad/certificate-manager.log`

---

## ESXi Host Disconnected or Not Responding

### Symptoms
- Host shows "Disconnected" or "Not Responding" in vSphere Client
- `Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"}` returns host(s)
- VMs on that host still running but unmanaged

### Diagnostic Steps

```bash
# PowerCLI: list all non-connected hosts
Get-VMHost | Select Name, ConnectionState, PowerState | Where-Object {$_.ConnectionState -ne "Connected"}

# PowerCLI: get recent events for the disconnected host
Get-VIEvent -Entity (Get-VMHost "esxi-hostname") -MaxSamples 50 | Select CreatedTime, FullFormattedMessage

# From VCSA SSH: check vpxd log for host connection errors
grep "esxi-hostname" /var/log/vmware/vpxd/vpxd.log | tail -50

# From ESXi host (SSH): check hostd is running
/etc/init.d/hostd status
/etc/init.d/vpxa status
```

### Resolution

```bash
# PowerCLI: attempt reconnect
(Get-VMHost "esxi-hostname").ExtensionData.ReconnectHost_Task($null)

# If agent is stuck on ESXi host, restart it (SSH to ESXi)
/etc/init.d/vpxa restart
/etc/init.d/hostd restart
```

**Log locations:**
- VCSA: `/var/log/vmware/vpxd/vpxd.log`
- ESXi: `/var/log/vmware/vpxa.log`, `/var/log/vmware/hostd.log`

---

## SSO / Authentication Failures

### Symptoms
- Login to vSphere Client fails with "incorrect credentials" despite correct password
- AD/LDAP users cannot authenticate; local SSO accounts still work (or vice versa)
- `vmware-sts` service stopped
- Audit log shows repeated failed login attempts

### Diagnostic Steps

```bash
# Check SSO/STS service on VCSA
service-control --status vmware-stsd
service-control --status vmware-sts-idmd

# Check SSO log for auth errors
tail -100 /var/log/vmware/sso/vmware-sts-idmd.log | grep -i "error\|fail\|bind"

# Check if the AD identity source is reachable from VCSA
nslookup <ad-domain> <dns-server>
ldapsearch -x -H ldap://<dc-fqdn> -b "dc=domain,dc=com" "(objectClass=*)" -D "bind-user@domain.com" -W
```

### Resolution

```bash
# Restart SSO services if stsd is stopped
service-control --start vmware-stsd
service-control --start vmware-sts-idmd

# Unlock the administrator@vsphere.local account (if locked)
/usr/lib/vmware-vmafd/bin/dir-cli user unlock --account administrator --password <current-admin-pwd>
```

**Log location:** `/var/log/vmware/sso/vmware-sts-idmd.log`, `/var/log/vmware/sso/ssoAdminServer.log`

---

## VAMI Inaccessible (Port 5480)

### Symptoms
- `https://<vcenter>:5480` returns connection refused or times out
- Cannot access appliance management UI for backups, updates, certificates

### Diagnostic Steps

```bash
# SSH to VCSA as root

# Check applmgmt service
service-control --status applmgmt

# Check if port 5480 is listening
ss -tlnp | grep 5480

# Check applmgmt log
tail -50 /var/log/vmware/applmgmt/applmgmt.log
```

### Resolution

```bash
# Start the applmgmt service
service-control --start applmgmt

# Verify port is now open
ss -tlnp | grep 5480
```

If SSH itself is inaccessible, use the VCSA VM console in ESXi direct UI to log in as root.

---

## Datastore Alarms — Inaccessible or Over-Committed

### Symptoms
- Red alarm: "Datastore is inaccessible" or "Thin-provisioned disk overcommitment"
- VMs on affected datastore may pause or fail I/O

### Diagnostic Steps

```bash
# PowerCLI: list all datastores with free space
Get-Datastore | Select Name, CapacityGB, FreeSpaceGB, @{N="UsedPct";E={[math]::Round((1-($_.FreeSpaceGB/$_.CapacityGB))*100,1)}} | Sort UsedPct -Descending

# Check datastore accessibility state
Get-Datastore | Where-Object {$_.State -ne "Available"} | Select Name, State

# For NFS datastores: verify NFS export is reachable from all hosts mounting it
# SSH to ESXi: esxcli storage nfs list
```

---

## DRS / HA Configuration Warnings

### Symptoms
- Cluster shows yellow or red warning icon
- HA configuration issue: "Host has no management network redundancy"

### Diagnostic Steps

```bash
# PowerCLI: check cluster HA and DRS state
Get-Cluster | Select Name, DrsEnabled, DrsAutomationLevel, HAEnabled, HAAdmissionControlEnabled

# Check recent cluster events for HA/DRS errors
Get-Cluster "cluster-name" | Get-VIEvent -MaxSamples 50 | Where-Object {$_.FullFormattedMessage -match "HA|DRS"} | Select CreatedTime, FullFormattedMessage
```

### Resolution

Most HA config warnings are resolved by:
1. Reconfiguring HA on the cluster: right-click cluster → Reconfigure for vSphere HA
2. Checking management network redundancy: each host should have at least two vmknics in the management portgroup

---

## vCenter Upgrade Failures

### Symptoms
- VAMI → Update shows upgrade failed mid-process
- `applmgmt.log` shows precheck failure
- vCenter reverted to previous build (if precheck failed before stage 2)

### Diagnostic Steps

```bash
# Check upgrade log on VCSA
tail -200 /var/log/vmware/applmgmt/applmgmt.log | grep -i "error\|fail\|precheck"

# Check disk space — common precheck failure cause
df -h
```

### Resolution

1. If precheck failed (before stage 2 installs): the system is unchanged. Free disk space, then retry.
2. If stage 2 failed: do not reboot until you understand the state. Review `applmgmt.log` and open a VMware Support request if services are partially upgraded.
3. Restore from VAMI backup or snapshot if the environment is non-functional.

**Log locations:**
- `/var/log/vmware/applmgmt/applmgmt.log`
- `/var/log/vmware/applmgmt/software-packages.log`

## Alarms and Events

### Finding the Right Alarm or Event

vCenter alarms are visible under the **Alarms** tab on any inventory object (datacenter, cluster, host, VM). Triggered alarms surface the affected object, the alarm definition, and the time of the trigger.

```powershell
# List all VMs with active triggered alarms
Get-VM | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="AlarmCount";E={$_.ExtensionData.TriggeredAlarmState.Count}}

# Get alarm details for a specific VM
$vm = Get-VM "app-server-01"
$vm.ExtensionData.TriggeredAlarmState | ForEach-Object {
    [PSCustomObject]@{
        Alarm = $_.Alarm.ToString()
        Status = $_.OverallStatus
        Time = $_.Time
    }
}

# Acknowledge all alarms on a specific host
$host = Get-VMHost "esxi-01.example.local"
$host.ExtensionData.TriggeredAlarmState | ForEach-Object {
    $alarmMgr = Get-View AlarmManager
    $alarmMgr.AcknowledgeAlarm($_.Alarm, $host.ExtensionData.MoRef)
}
```

### Filtering Events by Type and Time

```powershell
# All error-level events in the last 24 hours
Get-VIEvent -Start (Get-Date).AddHours(-24) |
    Where-Object { $_.GetType().Name -match "Error|Fault" } |
    Select-Object CreatedTime, UserName, FullFormattedMessage |
    Sort-Object CreatedTime -Descending

# Events for a specific cluster
Get-VIEvent -Entity (Get-Cluster "CL-LON-PROD") -MaxSamples 200 |
    Select-Object CreatedTime, UserName, FullFormattedMessage

# Login/logout events
Get-VIEvent -MaxSamples 500 |
    Where-Object { $_.GetType().Name -match "Login|Logout" } |
    Select-Object CreatedTime, UserName, FullFormattedMessage
```

### Common Alarm Noise and Tuning

| Alarm | Common False Positive Cause | Tuning Action |
|---|---|---|
| Host memory usage > threshold | Memory balloon during low activity | Raise threshold to 85% or add host-level override |
| Datastore disk usage > threshold | Snapshot growth or thin-provisioning | Set threshold to 80%; alert on trend not point-in-time |
| Virtual machine CPU ready > threshold | Low-vCPU-count VMs in high-density clusters | Tune threshold per workload type |
| SSH enabled on host | Break-glass or maintenance | Add suppression or use alarm action to auto-disable SSH after X hours |

Alarm definitions are managed at **vCenter → Configure → Alarm Definitions**. Each alarm has configurable thresholds, trigger conditions, and actions (send email, run script, send SNMP trap).
