---
tags:
  - operations
  - vmware
  - vsphere-replication
description: "Install and Upgrade reference covering Prerequisites, VRA OVA Deployment, Register VRA with vCenter, Deploy VRS (Scale-Out Server), Pair Sites and 3 more..."
---
# vSphere Replication — Install and Upgrade

<div class="kb-summary">
Install and Upgrade reference covering Prerequisites, VRA OVA Deployment, Register VRA with vCenter, Deploy VRS (Scale-Out Server), Pair Sites and 3 more sections.

*Applies to: vSphere Replication 8.x*
</div>
![vSphere Replication — Install and Upgrade](../../../../../assets/virtualization-vmware-vsphere-replication-operations-install.svg)

  VR Deployment and Upgrade Workflow

---

## Before you begin

- **Access:** vCenter Administrator at both protected and recovery sites; access to the VR appliance VAMI (`https://<vra-ip>:5480`)
- **Timing:** VRS deployment is non-disruptive; site pairing requires a brief VR service restart — safe during business hours
- **Dependencies:** vCenter deployed and healthy at both sites; TCP 31031 open between sites (replication traffic); TCP 443 between VR appliances (management); DNS resolves VR FQDN from both sites
- **Logging:** record VR appliance IPs and FQDNs; capture the site pairing confirmation and certificate fingerprints

---

!!! warning "Host enters maintenance mode"
    ESXi remediation puts hosts into maintenance mode, triggering DRS evacuation. Confirm DRS is Fully Automated and HA admission control is satisfied before starting.
## Prerequisites

| Requirement | Detail |
|---|---|
| vCenter | Supported version (check interopmatrix.vmware.com) |
| DNS | FQDN for VRA resolvable from both sites |
| Network | TCP 31031 (source ESXi → target VRA), TCP 44046 (VRA-to-VRA), TCP 443 (VRA → vCenter) |
| NTP | VRA and vCenter time synchronized (±5 seconds) |
| Storage | Sufficient datastore space at target site for replica VMDKs |
| License | vSphere Replication included with vSphere Essentials Plus and higher |

---

## VRA OVA Deployment

Deploy a VRA at each site (protected site and recovery site):

```yaml
vCenter → Deploy OVF Template
  Source: VMware-vSphere-Replication-<version>.ovf

  Step 1: Name and folder
    Name: vra-london
    Folder: Infrastructure VMs

  Step 2: Compute resource
    Select: host or cluster for VRA VM

  Step 3: Storage
    Storage policy: default (VRA needs minimal disk)
    Datastore: management datastore

  Step 4: Network
    Network: Management portgroup

  Step 5: Customize template
    IP Address: 10.10.10.50 (static)
    Subnet Mask: 255.255.255.0
    Gateway: 10.10.10.1
    DNS: 10.10.10.10
    NTP: ntp.example.local
    Admin password: <set strong password>
    Root password: <set strong password>

  → Deploy (takes ~5 minutes)
```

---

## Register VRA with vCenter

After deployment, register VRA with vCenter:

```text
VRA VAMI UI: https://vra-london.example.local:5480
  Configuration → vCenter Server
    vCenter Address: vcenter-london.example.local
    Username: administrator@vsphere.local
    Password: <password>
    Accept certificate
    → Register
```

After registration, VRA appears in vCenter → Site Recovery as a Replication Appliance.

---

## Deploy VRS (Scale-Out Server)

For environments with >500 replicated VMs, deploy additional VRS appliances:

```text
vCenter → Site Recovery → vSphere Replication → Replication Servers → Deploy

  Same OVF as VRA, but select: Deploy as Replication Server
  Configure: same network settings
  After deploy: it auto-registers with the VRA
```

---

## Pair Sites

```text
vCenter (Protected Site) → Site Recovery → New Site Pair
  Remote vCenter: vcenter-amsterdam.example.local
  SSO credentials for remote vCenter: administrator@vsphere.local
  Remote VRA: vra-amsterdam.example.local
  Accept certificate thumbprints for both VRA appliances
  → Pair
```

After pairing, configure replications on individual VMs:
```text
vCenter → [VM] → right-click → Configure Replication
```

---

## Upgrade Process

Upgrade VRA by redeploying from new OVA (not in-place):

1. **Take a snapshot of the existing VRA VM** before starting
2. **Redeploy from new OVA** with same IP configuration
3. VRA re-registers with vCenter automatically (if same IP)
4. Existing replications resume without data loss — only the appliance is replaced

> Upgrade Protected Site VRA first (or either order — VRA upgrades are non-disruptive to replications)

```bash
# After redeployment, verify service is up:
ssh admin@vra-london.example.local
systemctl status hms
```


```text title="Expected output"
admin@vra-london.example.local's password: 
● hms.service - VMware vSphere Replication Management Service
     Loaded: loaded (/etc/systemd/system/hms.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2min 45s ago
       Docs: man:hms(8)
    Process: 4521 ExecStart=/opt/vmware/hms/bin/hms.sh start (code=exited, status=0/SUCCESS)
   Main PID: 4538 (java)
      Tasks: 28 (limit: 4915)
     Memory: 512.3M
        CPU: 8s
     CGroup: /system.slice/hms.service
             └─4538 /usr/lib/jvm/java-11-openjdk-11.0.18.10-1.el7_9.x86_64/bin/java -Xmx1024m...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ssh: Could not resolve hostname vra-london.example.local: Name or service not known` | Verify the hostname is correct and resolvable in DNS, or use the IP address directly instead. |
    | `Unit hms.service could not be found.` | Confirm the vSphere Replication appliance was fully deployed and the hms service package is installed; check `/opt/vmware/hms/` directory exists. |
    | `Active: inactive (dead) since Mon 2024-01-15 14:25:03 UTC` | Check service logs with `journalctl -u hms -n 50` to identify startup failures, typically due to port conflicts or insufficient memory. |
Check Site Recovery → Sites → both sites still Connected after upgrade.

---

## Version Compatibility

Check the Interoperability Matrix before upgrading:
- https://interopmatrix.vmware.com
- Key dependencies: VR version ↔ vSphere version ↔ SRM version (if paired with SRM)
- VRA must be same version on both sites before pairing

---

## Post-Install Verification

```bash
# Verify VRA health
curl -sk https://vra-london.example.local/api/rest/vr/health

# Configure a test VM replication:
# vCenter → [any test VM] → Configure Replication
#   Target site: amsterdam, RPO: 1 hour
#   Verify initial sync starts (status: Syncing)
#   Wait for initial sync to complete (status: OK)
```


```text title="Expected output"
{
  "status": "Healthy",
  "version": "8.7.0.1",
  "build": "21624480",
  "uptime_seconds": 2419200,
  "replication_pairs": 847,
  "active_syncs": 12,
  "failed_syncs": 0,
  "last_heartbeat": "2024-01-15T14:32:18Z",
  "storage_usage_percent": 67.3,
  "network_latency_ms": 28.5,
  "components": {
    "database": "Healthy",
    "storage": "Healthy",
    "network": "Healthy"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification, or import the VRA's CA certificate into your system trust store. |
    | `curl: (7) Failed to connect to vra-london.example.local port 443: Connection refused` | Verify the VRA appliance is powered on and the hostname resolves correctly with `nslookup vra-london.example.local`. |
    | `Initial sync stuck at "Syncing" status after 24+ hours` | Check network connectivity and bandwidth between sites using `ping` and `iperf`, and verify the target datastore has sufficient free space. |
---

## See also

- [vSphere Replication — Health Checks](../health-checks/)
- [vSphere Replication — Common Issues](../../troubleshooting/common-issues/)
- [vSphere Replication — Procedures](../procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
