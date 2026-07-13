---
tags:
  - nsx
  - nsx-4
  - operations
  - vmware
---
# NSX — Install and Upgrade

*Applies to: VMware NSX-T 3.x / 4.x*
![NSX — Install and Upgrade](../../../../../assets/virtualization-vmware-nsx-operations-install-upgrade.svg)

```bash
# SSH to node 2
nsxcli

# Join to the cluster (provide node 1's IP and certificate thumbprint)
join management-plane <node1-ip> username admin thumbprint <node1-thumbprint>

# Get node 1's thumbprint from node 1 CLI:
get certificate api thumbprint
```

```yaml
Name: pool-tep-compute
Subnet: 192.168.200.0/24
Gateway: 192.168.200.1
IP Ranges: 192.168.200.10–192.168.200.254
```
```bash
# Verify from Manager CLI after preparation
nsxcli
get transport-nodes
get transport-node-status
# All hosts should show "UP"
```
```text
1. NSX Manager (all 3 nodes) — control plane first
2. Edge Nodes — north-south gateway impact; BGP reconverges
3. ESXi Transport Nodes (host-by-host) — data plane impact; rolling
```
```text
Upgrade node 1 → node 1 reboots (cluster VIP on node 2 or 3)
Upgrade node 2 → node 2 reboots
Upgrade node 3 → node 3 reboots
```
```bash
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/upgrade/status-summary"
```

```text title="Expected output"
{
  "upgrade_status": "READY",
  "current_version": "3.2.1.0",
  "target_version": "3.2.2.0",
  "upgrade_progress": 0,
  "upgrade_start_time": null,
  "upgrade_end_time": null,
  "upgrade_duration": null,
  "upgrade_error": null,
  "upgrade_error_details": null,
  "node_upgrade_status": [
    {
      "node_id": "nsx-mgr-01",
      "node_ip": "192.168.1.50",
      "upgrade_status": "READY",
      "current_version": "3.2.1.0"
    },
    {
      "node_id": "nsx-mgr-02",
      "node_ip": "192.168.1.51",
      "upgrade_status": "READY",
      "current_version": "3.2.1.0"
    },
    {
      "node_id": "nsx-mgr-03",
      "node_ip": "192.168.1.52",
      "upgrade_status": "READY",
      "current_version": "3.2.1.0"
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip SSL verification, or import the NSX Manager's certificate into your system trust store. |
    | `{"error_code":401,"error_message":"Invalid credentials"}` | Verify the admin username and password are correct and the account has not been locked after failed login attempts. |
    | `curl: (7) Failed to connect to <nsx-manager> port 443: Connection refused` | Confirm the NSX Manager hostname/IP is correct, reachable on the network, and the management service is running with `systemctl status nsx-manager`. |
```bash
# On Edge node CLI
get version
get bgp neighbor summary
# All peers should be Established
```

```text title="Expected output"
NSX Edge> get version
NSX Edge version: 6.4.13.1 Build 21589934
NSX Edge> get bgp neighbor summary
BGP router identifier 192.168.100.1, local AS number 65001

Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
10.0.0.1        4 65002    1247    1251        0    0    0 5d12h34m Established
10.0.0.2        4 65002    1248    1250        0    0    0 5d12h34m Established
10.0.0.3        4 65003     892     895        0    0    0 2d08h12m Established
10.0.0.4        4 65003     156     159        0    0    0 00h47m23s Connect
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `State/PfxRcd: Connect` | Verify BGP neighbor configuration and network connectivity; check firewall rules allowing TCP 179 between Edge and peer. |
    | `State/PfxRcd: Idle` | Confirm BGP neighbor IP address is reachable and the remote AS number matches the configuration on both sides. |
```bash
# Verify backup is restorable before the upgrade window
# Check backup files are present on SFTP server
# Confirm the passphrase is stored and accessible
```
```bash
# NSX Manager cluster health
nsxcli
get cluster status
get managers
get services

# Transport node health
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/transport-nodes/status"
# Check: up_count equals total_count

# Edge cluster health and BGP
# SSH to each Edge node
get version                    # Confirm new version
get bgp neighbor summary        # All peers Established
get edge-cluster status         # Active/Standby state confirmed

# Open alarms
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL"
# Should return result_count: 0

# DFW rule push
# Verify a test VM can still communicate as expected after upgrade
```


```text title="Expected output"
nsx-manager-01> get cluster status
Cluster Status: STABLE
Leader: nsx-manager-01 (192.168.1.10)
Follower: nsx-manager-02 (192.168.1.11)
Follower: nsx-manager-03 (192.168.1.12)

nsx-manager-01> get managers
UUID                                   Hostname            IP              Status
550e8400-e29b-41d4-a716-446655440001   nsx-manager-01      192.168.1.10    UP
550e8400-e29b-41d4-a716-446655440002   nsx-manager-02      192.168.1.11    UP
550e8400-e29b-41d4-a716-446655440003   nsx-manager-03      192.168.1.12    UP

nsx-manager-01> get services
Service Name              Status    PID
nsx-manager              UP        2847
policy-service          UP        3156
search-service          UP        3421
cluster-service         UP        2934

{
  "result_count": 24,
  "results": [
    {
      "node_id": "tn-edge-01",
      "status": "UP",
      "up_count": 2,
      "total_count": 2
    },
    {
      "node_id": "tn-host-01",
      "status": "UP",
      "up_count": 4,
      "total_count": 4
    }
  ]
}

edge-node-01> get version
Product: NSX-T
Version: 3.2.1.0
Build: 19480675

edge-node-01> get bgp neighbor summary
BGP router identifier 10.0.0.1, local AS number 65001
Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
10.0.0.254      4 65000    1247    1251        8    0    0 00:42:18 Established
10.0.1.254      4 65000    1248    1252        8    0    0 00:42:15 Established

edge-node-01> get edge-cluster status
Edge Cluster: edge-cluster-01
Member: edge-node-01 (Active)
Member: edge-node-02 (Standby)

{
  "result_count": 0,
  "results": []
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip certificate verification, or import the NSX Manager certificate into your CA bundle. |
    | `401 Unauthorized` | Verify the admin credentials in the curl command are correct and the user has API access permissions in NSX Manager. |
    | `Cluster Status: UNSTABLE` | Check the NSX Manager node connectivity and logs with `get log follow` to identify which manager is down, then restart the failed node's services. |
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

- [NSX — Health Checks](../health-checks/)
- [NSX — Common Issues](../../troubleshooting/common-issues/)
- [NSX — Standard Procedures](../procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
