# vCenter Outage Runbook

```bash
ping <vcenter-ip>
nslookup <vcenter-fqdn>
```
```text
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
