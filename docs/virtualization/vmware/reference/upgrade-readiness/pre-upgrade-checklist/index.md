---
tags:
  - reference
---
# Pre-Upgrade Checklist


<div class="kb-summary">
Complete all items before starting any vSphere upgrade (vCenter, ESXi, vSAN, NSX).
</div>
```text
┌───────────────────────────── Virtualization Reference Upgrade Readiness ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 Reference: Virtualization Reference Upgrade Readiness platform                │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │           Management: Virtualization Reference Upgrade Readiness management console           │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Reference Upgrade Readiness infrastructure · management network · monito  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Reference          = Virtualization Reference Upgrade Readiness platform overview and core concep  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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
  for fqdn in vcenter.example.local nsx.example.local esxi01.example.local; do
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
  openssl s_client -connect vcenter.example.local:443 -showcerts 2>/dev/null | openssl x509 -noout -dates
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
