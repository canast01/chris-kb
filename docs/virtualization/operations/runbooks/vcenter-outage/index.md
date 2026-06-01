# vCenter Outage Runbook


<div class="kb-summary">
vCenter Outage Runbook reference covering Confirm Outage Scope, Check VCSA VM Power State, Check VCSA Appliance Management, Check DNS and Network Reachability, Check Disk Partitions and 4 more sections.
</div>

## Confirm Outage Scope

- Can you access the vSphere Client?
- Can you ping the vCenter FQDN and IP?
- Are ESXi hosts still visible and running workloads independently?

## Check VCSA VM Power State

- Confirm the VCSA VM is powered on in vCenter (if a secondary vCenter is available)
- Or verify via iDRAC/IPMI if the VCSA is running on a known host

## Check VCSA Appliance Management

- Access `https://<vcenter>:5480`
- Review service health, disk partitions, and CPU/memory

## Check DNS and Network Reachability

```bash
ping <vcenter-ip>
nslookup <vcenter-fqdn>
```
┌─────────────────────────────────────── vCenter Outage Runbook ────────────────────────────────────────┐
│                                                                                                       │
│    ESXi hosts continue running VMs independently; vCenter is management plane only                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   Diagnose                   │  │                   Restore                   │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │            Ping vCenter FQDN + IP            │  │          Power on VCSA VM via iDRAC         │   │
│   │            Access VAMI port 5480             │  │           Start services via VAMI           │   │
│   │            Review service health             │  │        service-control --start --all        │   │
│   │            Check disk partitions             │  │          Free disk if /storage full         │   │
│   │          Check DNS forward/reverse           │  │         Fix DNS record / hosts file         │   │
│   │          Check VCSA VM power state           │  │           Restore from file backup          │   │
│   │           Check iDRAC / IPMI logs            │  │            Escalate to VMware GSS           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VCSA         = vCenter Server Appliance; Linux-based VM running all vCenter services               │
│    VAMI         = Appliance Management Interface; port 5480; accessible when vCenter UI is not        │
│    service-control = VCSA CLI tool; start/stop/status all vCenter services                            │
│    Management plane = vCenter; losing it does NOT stop running VMs — hosts operate standalone         │
│    File backup  = vCenter native backup; SFTP destination; restore via VCSA installer                 │
│    GSS          = VMware Global Support Services; escalate P1 outages with SR number                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Partitions that commonly cause failures when full:
- `/storage/log`
- `/storage/db`

## Review Recent Changes

- Was a certificate recently replaced?
- Was a patch or upgrade recently applied?
- Was a snapshot taken or deleted on the VCSA VM?

## Restore from Backup if Required

- Use the vCenter file-based backup (VAMI → Backup)
- Confirm the backup date and restore target
- Follow VMware restore documentation

## Validate Services After Recovery

- Confirm all services are running: `service-control --status`
- Confirm vSphere Client is accessible
- Confirm all hosts are reconnecting
- Confirm Aria and other integrations are working

## Communicate Impact

- Notify stakeholders of the outage and recovery status
- Note that ESXi hosts and VMs continue running without vCenter
- Update the incident ticket with timeline and resolution
