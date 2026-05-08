# vCenter Troubleshooting — Common Issues

## Issue Summary

| Symptom | Likely Cause | First Action |
|---|---|---|
| vCenter UI not loading | vpxd stopped or DB down | SSH → `service-control --status vpxd` |
| Certificate error in browser | Machine SSL expired | VAMI → Certificate Management |
| ESXi host shows Disconnected | Agent failure or cert mismatch | Reconnect host; check `/var/log/vmware/vpxd/vpxd.log` |
| SSO login rejected | AD identity source broken or account locked | VAMI → SSO Configuration |
| VAMI inaccessible | `applmgmt` service stopped | SSH → `service-control --start applmgmt` |
| Datastore alarm (Inaccessible) | Storage path failure | Check host storage adapter and SAN/NFS path |
| DRS/HA cluster warning | Admission control violation or host failure | Review cluster Events tab |
| vCenter upgrade failed | Precheck failure or disk space | Review `/var/log/vmware/applmgmt/applmgmt.log` |

---

## vCenter Services Not Starting

### Symptoms
- vSphere Client loads but shows "503 Service Unavailable" or partial UI
- `service-control --status vpxd` returns `stopped`
- Events and tasks pane empty or frozen

### Diagnostic Steps

```bash
# SSH to VCSA

# Check all service statuses at once
service-control --status --all

# Check vpxd specifically
service-control --status vpxd

# Check the Postgres database service
service-control --status vmware-vpostgres

# Tail vpxd log for the root error
tail -200 /var/log/vmware/vpxd/vpxd.log | grep -E "error|fatal|panic" -i

# Check disk space — a full /storage/db partition will kill Postgres
df -h

# Check Postgres log if DB failure suspected
tail -100 /var/log/vmware/vpostgres/postgresql-*.log
```

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

Alarm review, event history, alert tuning, noise reduction, and useful operational signals.

### Daily Checks

| Check | Command | Notes |
|---|---|---|
| Review active alarms. |  |  |
| Check recent failed tasks. |  |  |
| Confirm service health. |  |  |
| Confirm capacity and performance are normal. |  |  |
| Check recent changes. |  |  |

### Health Commands

```bash
# Add environment-specific commands here
```

### Common Issues

- Failed or stuck tasks.
- Certificate, DNS, or authentication issues.
- Capacity pressure.
- Service health warnings.
- Version mismatch after maintenance.
- Monitoring gaps.

### Operational Tasks

| Task | Command |
|---|---|
| Review alarms and events. |  |
| Confirm ownership and support notes. |  |
| Validate dependencies. |  |
| Document changes. |  |
| Confirm monitoring coverage. |  |

### Upgrade Notes

- Confirm compatibility.
- Review known issues.
- Confirm rollback plan.
- Validate health before and after the change.

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Keep versions aligned. | Keep versions aligned. |
| Avoid unsupported version combinations. | Avoid unsupported version combinations. |
| Document exceptions. | Document exceptions. |
| Validate after every change. | Validate after every change. |
