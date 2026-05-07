# Pre-Upgrade Checklist

Complete all items before starting any vSphere upgrade (vCenter, ESXi, vSAN, NSX).
## Backup and Recovery

- [ ] vCenter appliance backup completed and verified (VAMI → Backup → Run Now; confirm backup file exists)
- [ ] Configuration backup for NSX Manager: NSX Manager → System → Backup → Backup Now
- [ ] SDDC Manager backup (VCF): `lcm-tools backup`
- [ ] Aria Suite Lifecycle snapshot taken (for LCM-managed environments)
- [ ] VM snapshots taken of: vCenter, NSX Manager nodes, Platform Services Controllers (if separate)
- [ ] Verify snapshots are visible in vCenter inventory before proceeding

```powershell
# Confirm vCenter snapshot exists
Get-VM -Name vcenter-prod-01 | Get-Snapshot | Select-Object Name, Created, SizeMB
```

## Environment Health

- [ ] Zero critical or red alarms in vCenter (investigate and resolve all before proceeding)
- [ ] All hosts: `ConnectionState = Connected`
- [ ] All clusters: HA Enabled, DRS Enabled
- [ ] vSAN health: no failed disks, no degraded objects, no active resyncs
- [ ] All datastores accessible (no APD/PDL)
- [ ] NSX Manager cluster status: `STABLE` (if NSX deployed)
- [ ] All VMs in expected power state (no stuck power operations in recent tasks)

```powershell
# Quick health check
Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"} | Select-Object Name, ConnectionState
Get-Datastore | Where-Object {$_.State -ne "Available"} | Select-Object Name, State
```

## Compatibility Verification

- [ ] Product Interoperability Matrix checked: [interopmatrix.vmware.com](https://interopmatrix.vmware.com)
  - Target vCenter version compatible with current ESXi versions?
  - Target ESXi version compatible with current hardware (HCL)?
  - NSX version compatible with target vCenter version?
- [ ] Driver and firmware versions on all hosts are on the VCG (vSphere Compatibility Guide)
- [ ] Third-party solutions checked: backup agents, monitoring agents, SAN multipath drivers

## Disk and Capacity

- [ ] vCenter appliance: VAMI → Monitor → Storage — all partitions < 70% full
- [ ] Datastore hosting vCenter VM: > 100 GB free
- [ ] ESXi host scratch partition: > 5 GB free per host (`df -h` on each host's `/scratch`)

## DNS and NTP

- [ ] DNS: forward and reverse resolution for all component FQDNs confirmed
  ```bash
  for fqdn in vcenter.corp.local nsx.corp.local esxi01.corp.local; do
      nslookup $fqdn; nslookup $(nslookup $fqdn | grep Address | tail -1 | awk '{print $2}')
  done
  ```
- [ ] NTP: time drift < 5 seconds between all components
  ```bash
  # On each ESXi host
  esxcli system time get
  ```

## Certificates

- [ ] vCenter Machine SSL certificate not expiring within 30 days
- [ ] NSX Manager cluster certificates not expiring within 30 days
- [ ] STS (Lookup Service) certificate valid
  ```bash
  # Check vCenter cert expiry
  openssl s_client -connect vcenter.corp.local:443 -showcerts 2>/dev/null | openssl x509 -noout -dates
  ```

## Access and Credentials

- [ ] Admin credentials confirmed working (vCenter SSO admin, NSX admin, SDDC Manager admin)
- [ ] Break-glass access procedures documented and tested
- [ ] Service account credentials valid (vcenter → AD authentication test passed)

## Rollback Plan

- [ ] Rollback steps documented and reviewed with team
- [ ] Rollback window agreed (minimum 2 hours after upgrade window)
- [ ] Snapshots confirmed available as rollback point
- [ ] Contact list prepared: vendor support numbers, internal escalation path

## Change Management

- [ ] Change record approved with correct implementation window
- [ ] Application owner notification sent
- [ ] On-call engineer identified for duration of change window
