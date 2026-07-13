---
tags:
  - deployment
  - vmware
  - vxrail
search:
  boost: 1.5
description: "End-to-end deployment guide for a new VxRail cluster. Covers pre-deployment readiness, the First Run Wizard, vCenter integration, vSAN validation, OMIVV..."
---
# VxRail — Deploy

<div class="kb-summary">
End-to-end deployment guide for a new VxRail cluster. Covers pre-deployment readiness, the First Run Wizard, vCenter integration, vSAN validation, OMIVV plugin setup, and Day 1 post-deployment hardening.

*Applies to: VxRail 7.x / 8.x*
</div>

---

```d2
direction: right

plan: "Plan" {shape: oval}
phase_1_physical_readiness: "Phase 1: Physical Readiness" {shape: rectangle}
phase_2_first_run_wizard: "Phase 2: First Run Wizard" {shape: rectangle}
phase_3_vsan_configuration: "Phase 3: vSAN Configuration" {shape: rectangle}
phase_4_network_validation: "Phase 4: Network Validation" {shape: rectangle}
phase_5_supportassist_and_omivv: "Phase 5: SupportAssist and OMIVV" {shape: rectangle}
phase_6_postdeploy_hardening_and_bas: "Phase 6: Post-Deploy Hardening and Baseline" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> phase_1_physical_readiness
phase_1_physical_readiness -> phase_2_first_run_wizard
phase_2_first_run_wizard -> phase_3_vsan_configuration
phase_3_vsan_configuration -> phase_4_network_validation
phase_4_network_validation -> phase_5_supportassist_and_omivv
phase_5_supportassist_and_omivv -> phase_6_postdeploy_hardening_and_bas
phase_6_postdeploy_hardening_and_bas -> validate
```

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Phase 1: Physical Readiness

VxRail nodes ship pre-racked or are racked on-site. Before running the First Run Wizard every prerequisite below must pass — the wizard does not retry failed DNS or NTP lookups gracefully.

**Racking and cabling**

- Follow the Dell VxRail Network Planning Guide for your appliance model (E/P/V/S series)
- Each node needs: 2 × 25GbE (or 100GbE) data NICs to ToR switches + 1 × dedicated iDRAC port
- Dual switch uplinks required for HA — active/standby or LACP (VxRail supports both)
- iDRAC port on a dedicated OOB management VLAN or shared management VLAN (separate from vmk0)

**iDRAC IP assignment per node (DCUI)**

On each node, at the physical console (or iDRAC front-panel LCD):

```text
iDRAC Settings (F2 at POST or iDRAC front panel)
  → Network Settings
    → Static IP: <idrac-ip>
    → Subnet: <mask>
    → Gateway: <gateway>
    → DNS: <dns-server>
```

Verify iDRAC is reachable before proceeding:

```bash
# From jump host on OOB management VLAN
ping -c 3 <node1-idrac-ip>
ping -c 3 <node2-idrac-ip>
ping -c 3 <node3-idrac-ip>
```


```text title="Expected output"
PING 192.168.1.101 (192.168.1.101) 56(84) bytes of data.
64 bytes from 192.168.1.101: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 192.168.1.101: icmp_seq=2 ttl=64 time=2.18 ms
64 bytes from 192.168.1.101: icmp_seq=3 ttl=64 time=2.41 ms

--- 192.168.1.101 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/stddev = 2.18/2.31/2.41/0.10 ms

PING 192.168.1.102 (192.168.1.102) 56(84) bytes of data.
64 bytes from 192.168.1.102: icmp_seq=1 ttl=64 time=1.89 ms
64 bytes from 192.168.1.102: icmp_seq=2 ttl=64 time=2.05 ms
64 bytes from 192.168.1.102: icmp_seq=3 ttl=64 time=1.97 ms

--- 192.168.1.102 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 1.89/1.97/2.05/0.07 ms

PING 192.168.1.103 (192.168.1.103) 56(84) bytes of data.
64 bytes from 192.168.1.103: icmp_seq=1 ttl=64 time=3.12 ms
64 bytes from 192.168.1.103: icmp_seq=2 ttl=64 time=3.28 ms
64 bytes from 192.168.1.103: icmp_seq=3 ttl=64 time=3.05 ms

--- 192.168.1.103 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
rtt min/avg/max/stddev = 3.05/3.15/3.28/0.11 ms
```

!!! warning "Common errors"
    **`ping: sendto: No route to host`** — Verify the jump host is on the OOB management VLAN and routing to the iDRAC subnet is configured.
    **`ping: unknown host <node1-idrac-ip>`** — Confirm the iDRAC IP addresses are correct and resolvable, or use explicit IP addresses instead of hostnames.
    **`100% packet loss`** — Check that iDRAC interfaces are powered on, network cables are connected, and firewall rules allow ICMP on the OOB management network.
**DNS pre-creation**

Create A and PTR records for ALL of the following FQDNs before starting the wizard. Missing DNS records cause wizard failure or post-deploy vCenter join errors.

| Record | Example FQDN | Type |
|---|---|---|
| VxRail Manager | vxrail-manager.example.local | A + PTR |
| vCenter (embedded) | vcenter.example.local | A + PTR |
| Node 01 | vxrail-node-01.example.local | A + PTR |
| Node 02 | vxrail-node-02.example.local | A + PTR |
| Node 03 | vxrail-node-03.example.local | A + PTR |

```bash
# Verify DNS resolves forward and reverse before wizard
nslookup vxrail-manager.example.local
nslookup node-01.example.local

# Verify reverse lookup for vCenter IP
nslookup 10.0.1.20
```


```text title="Expected output"
Server:		10.0.1.10
Address:	10.0.1.10#53

Name:	vxrail-manager.example.local
Address: 10.0.1.50

Server:		10.0.1.10
Address:	10.0.1.10#53

Name:	node-01.example.local
Address: 10.0.1.51

Server:		10.0.1.10
Address:	10.0.1.10#53

10.0.1.20.in-addr.arpa	name = vcenter.example.local.
```

!!! warning "Common errors"
    **`** server can't find vxrail-manager.example.local: NXDOMAIN`** — Verify the hostname exists in DNS and check the domain suffix matches your environment (use `nslookup vxrail-manager.example.local <dns-server-ip>` to test against the correct nameserver).
    **`** server can't find 10.0.1.20.in-addr.arpa: NXDOMAIN`** — Confirm reverse DNS zones are configured on your DNS server and the PTR record exists for the vCenter IP address.
**NTP reachability**

```bash
# From jump host on management VLAN — NTP must be reachable from this VLAN
ntpdate -q ntp1.example.local
ntpdate -q ntp2.example.local
```


```text title="Expected output"
server 10.20.50.12, stratum 3, offset 0.002341, delay 0.045123
server 10.20.50.13, stratum 3, offset -0.001876, delay 0.041567
```

!!! warning "Common errors"
    **`no server suitable for synchronization found`** — Verify NTP servers are reachable from the management VLAN by running `ping ntp1.example.local` and check firewall rules allow UDP port 123.
    **`getaddrinfo: Name or service not known`** — Confirm DNS resolution works on the jump host with `nslookup ntp1.example.local` and verify the NTP server hostnames are correct in your environment.
**Switch VLAN and MTU configuration**

| Network | VLAN ID | MTU | Notes |
|---|---|---|---|
| Management | 100 | 1500 | vmk0; iDRAC OOB may share or use dedicated VLAN |
| vMotion | 101 | 9000 | vmk1; jumbo frames required |
| vSAN | 102 | 9000 | vmk2; jumbo frames required — verify on both switch ports |
| VM traffic | 200–299 | 1500 | VM port groups; trunk on host uplinks |

Verify MTU is set to 9000 on all switch ports carrying vSAN and vMotion traffic before the wizard runs. Mismatched MTU causes vSAN build failures that are difficult to diagnose post-deploy.

**Exit criterion:** All nodes iDRAC reachable. All FQDNs resolve forward and reverse. NTP reachable. Switch VLANs and MTU confirmed by network team.

---

## Phase 2: First Run Wizard

The First Run Wizard is a browser-based workflow that runs before vCenter exists. It discovers nodes, collects network configuration, deploys VxRail Manager, and (for embedded deployments) deploys the vCenter VCSA — all automatically.

**Access the wizard**

```bash
# Navigate from a browser on the management VLAN
# The wizard is served from the VxRail bootstrap agent on node 1
https://<node1-management-ip>/
```


```text title="Expected output"
(no output — this is a browser navigation URL, not a bash command)

The VxRail bootstrap wizard loads in your browser at:
- URL: https://192.168.1.100/
- Page title: "VxRail Deployment Wizard"
- Status: Bootstrap agent listening on port 443
- Node 1 management IP: 192.168.1.100
- Session established with TLS 1.2
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to 192.168.1.100 port 443: Connection refused`** — Verify node 1 is powered on, bootstrap agent is running, and the management VLAN network is correctly configured on your client.
    **`SSL_ERROR_BAD_CERT_DOMAIN`** — The certificate is self-signed during bootstrap; add a security exception in your browser or use `curl -k` if testing via CLI.
    **`ERR_NAME_NOT_RESOLVED` or `nodename nor servname provided`** — Ensure the node1 management IP is reachable from your client and DNS/hosts file is configured if using a hostname instead of an IP address.
Accept the self-signed certificate warning. Default credentials at first access: no login required — the wizard prompts for all passwords as part of setup.

**Wizard input sequence**

| Step | Input | Notes |
|---|---|---|
| 1. Welcome | Accept EULA | Review Dell and VMware license agreements |
| 2. Network discovery | Auto-discovers all nodes on management VLAN | Confirm all expected nodes are listed |
| 3. Node network config | Management, vMotion, vSAN IPs per node | Enter static IPs for all VMkernel ports |
| 4. DNS / NTP | VxRail Manager FQDN, DNS servers, NTP servers | Must match pre-created DNS records exactly |
| 5. vCenter type | Embedded or External | See table below |
| 6. SSO domain | e.g. `vsphere.local` | Cannot be changed post-deploy without full reinstall |
| 7. Passwords | vCenter admin, SSO admin, VxRail Manager mystic | Document securely — not recoverable without reset |
| 8. Review + Deploy | Summary screen | Wizard runs 30–60 min unattended |

**Embedded vs External vCenter**

| Factor | Embedded | External |
|---|---|---|
| vCenter location | Deployed inside the VxRail cluster automatically | Pre-existing vCenter you provide FQDN for |
| Use case | Single-cluster or small deployments | Multi-cluster, multi-site, existing vCenter infrastructure |
| Recovery complexity | Higher — vCenter VM is on vSAN it manages | Lower — vCenter is independent of this cluster |
| Supported from | All VxRail versions | VxRail 4.7+ |

**Wizard deploys automatically:**
- VxRail Manager VM on node 1 (4 vCPU, 12 GB RAM, 60 GB disk minimum)
- Embedded vCenter VCSA (if selected)
- Configures all VMkernel ports on all nodes
- Creates the vSphere cluster object with DRS + HA enabled

**Exit criterion:** Wizard completes without errors. VxRail Manager UI accessible at `https://<vxm-ip>`. vCenter accessible at `https://<vcenter-fqdn>`.

---

## Phase 3: vSAN Configuration

VxRail Manager automatically claims disks and configures vSAN during and after the First Run Wizard. Manual disk claiming is not required or recommended on VxRail — the wizard handles it.

**OSA vs ESA architecture**

| Architecture | Cache tier | Capacity tier | Minimum VxRail |
|---|---|---|---|
| OSA (Original Storage Architecture) | NVMe or SSD (10–20% of total) | SSD or HDD | All versions |
| ESA (Express Storage Architecture) | None — single tier | NVMe only | VxRail 8.0+ |

OSA creates disk groups (1 cache device + 1–7 capacity devices per node). ESA uses all NVMe as a single pool with no explicit cache assignment.

**Verify vSAN health post-deploy**

```bash
# From any ESXi node SSH session
esxcli vsan health cluster get

# Summary view — check for any red or yellow items
esxcli vsan health summary get
```


```text title="Expected output"
Cluster Health Status:
  Cluster Status: healthy
  Hosts Participating: 4
  Hosts Healthy: 4
  Hosts Unhealthy: 0
  Hosts Disconnected: 0
  Data Health: Healthy
  Memory Health: Healthy
  Network Health: Healthy
  Physical Disk Health: Healthy
  Capacity Health: Healthy

Summary Health Status:
  Overall Cluster Status: green
  Cluster Capacity: 87% used
  Rebalance Progress: 100%
  Resync Activity: None
  Component Limit Status: green
  Network Connectivity: green
  Host Health: green
```

!!! warning "Common errors"
    **`Error: Could not connect to VSAN cluster`** — Ensure VSAN is enabled on the cluster and the host is part of a valid VSAN cluster; run `esxcli vsan cluster get` to verify cluster membership.
    **`Error: Permission denied`** — Log in with root credentials or an account with VSAN administration privileges; use `esxcli system permission list` to verify your role.
**Create production SPBM policy**

The default vSAN storage policy (FTT=0) provides no redundancy. Always create and apply a production policy before placing any workload VMs.

In vCenter: Policies and Profiles → VM Storage Policies → Create:
- Name: `VxRail-RAID1-FTT1`
- Failures to tolerate: 1
- RAID method: RAID-1 (Mirroring)
- Apply to: VxRail Manager VM, vCenter VM, and all production VMs

**Verify vSAN health via PowerCLI**

```powershell
Connect-VIServer vcenter.example.local
Get-VsanClusterHealthSummary -Cluster "VxRail-Cluster" | Select-Object OverallHealth
```

Expected output: `green`

**Check VxRail Manager version and cluster status**

```bash
curl -sk -u 'mystic:password' https://<vxm-ip>/rest/vxm/v1/system | python3 -m json.tool
```


```text title="Expected output"
{
  "id": "vxm-01.lab.local",
  "version": "7.0.410-28915276",
  "build": "28915276",
  "productName": "VxRail Manager",
  "serialNumber": "VXM123456789ABC",
  "systemStatus": "Healthy",
  "clusterStatus": "Online",
  "nodeCount": 4,
  "totalCapacity": {
    "cpu": 384,
    "memory": 3072,
    "storage": 614400
  },
  "lastUpdated": "2024-01-15T14:32:18Z",
  "licenseStatus": "Valid",
  "supportStatus": "Active"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification (already present in the example, so ensure it's not being removed).
    **`curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused`** — Verify the VxRail Manager IP address is correct and the management interface is reachable with `ping <vxm-ip>`.
    **`jq: parse error: Invalid JSON at line 1`** — Ensure `python3 -m json.tool` is installed; if unavailable, use `jq` instead or remove the formatter to see the raw response.
**Exit criterion:** vSAN health all green. VxRail Manager reports cluster healthy. Production SPBM policy created and applied to VxRail Manager and vCenter VMs.

---

## Phase 4: Network Validation

VxRail Manager configures VMkernel ports automatically, but you must validate that all ports are present and functioning on every node after the wizard completes.

**Expected VMkernel ports per node**

| VMkernel | Traffic type | VLAN | MTU | Service tag |
|---|---|---|---|---|
| vmk0 | Management | Management VLAN | 1500 | Management |
| vmk1 | vMotion | vMotion VLAN | 9000 | vMotion |
| vmk2 | vSAN | vSAN VLAN | 9000 | vSAN |

**Verify VMkernel ports on all nodes via PowerCLI**

```powershell
Connect-VIServer vcenter.example.local
Get-VMHost -Location (Get-Cluster "VxRail-Cluster") | Select-Object Name, ConnectionState
```

Expected output: all nodes `Connected`.

**Verify all VMkernel IPs from a specific host**

```bash
# SSH to any VxRail node
esxcli network ip interface list
esxcli network ip interface ipv4 get
```


```text title="Expected output"
Name  Enabled  Connected  MTU  MAC Address        IPV4 Address      Netmask         Broadcast
----  -------  ---------  ---  -----------------  ----------------  --------------  ----------------
vmk0  true     true       1500  00:50:56:c0:00:01  192.168.1.45      255.255.255.0   192.168.1.255
vmk1  true     true       1500  00:50:56:c0:00:02  192.168.100.45    255.255.255.0   192.168.100.255
vmk2  false    false      1500  00:50:56:c0:00:03  0.0.0.0           0.0.0.0         0.0.0.0
vmk3  true     true       9000  00:50:56:c0:00:04  10.20.30.45       255.255.255.0   10.20.30.255

Name  IPV4 Address      Netmask         Broadcast           DHCP   DefaultGateway
----  ----------------  --------------  ------------------  -----  ----------------
vmk0  192.168.1.45      255.255.255.0   192.168.1.255       false  192.168.1.1
vmk1  192.168.100.45    255.255.255.0   192.168.100.255     false  192.168.100.1
vmk2  0.0.0.0           0.0.0.0         0.0.0.0             false  0.0.0.0
vmk3  10.20.30.45       255.255.255.0   10.20.30.255        false  10.20.30.1
```

!!! warning "Common errors"
    **`Could not connect to the host. The host may not be running, or a network error may have occurred.`** — Verify SSH connectivity to the VxRail node and confirm the ESXi host is powered on and responsive.
    **`Unknown command or namespace.`** — Ensure you are connected to an ESXi host with esxcli enabled; this command does not work on vCenter or management appliances.
**MTU test on vSAN network**

Run from each node to each peer node vSAN VMkernel IP. All tests must succeed (0% packet loss) before the cluster is considered production-ready.

```bash
# SSH to node 1 — test vSAN MTU to node 2 vSAN VMkernel IP
# 8972 = 9000 MTU minus 28 bytes IP+ICMP header
vmkping -I vmk2 -d -s 8972 <node2-vsan-vmk-ip>

# Repeat for all node pairs
vmkping -I vmk2 -d -s 8972 <node3-vsan-vmk-ip>
```


```text title="Expected output"
PING 192.168.100.12 (192.168.100.12): 8972 data bytes
8980 bytes from 192.168.100.12: icmp_seq=0 ttl=64 time=0.456 ms
8980 bytes from 192.168.100.12: icmp_seq=1 ttl=64 time=0.423 ms
8980 bytes from 192.168.100.12: icmp_seq=2 ttl=64 time=0.441 ms
8980 bytes from 192.168.100.12: icmp_seq=3 ttl=64 time=0.438 ms
--- 192.168.100.12 statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 0.423/0.439/0.456 ms

PING 192.168.100.13 (192.168.100.13): 8972 data bytes
8980 bytes from 192.168.100.13: icmp_seq=0 ttl=64 time=0.512 ms
8980 bytes from 192.168.100.13: icmp_seq=1 ttl=64 time=0.498 ms
8980 bytes from 192.168.100.13: icmp_seq=2 ttl=64 time=0.505 ms
8980 bytes from 192.168.100.13: icmp_seq=3 ttl=64 time=0.489 ms
--- 192.168.100.13 statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
```

!!! warning "Common errors"
    **`PING 192.168.100.12 (192.168.100.12): 8972 data bytes (100% packet loss)`** — Verify vSAN VMkernel interface MTU is set to 9000 on both nodes using `esxcli network ip interface list`.
    **`sendto() failed (Message too long)`** — Reduce packet size or confirm physical switch and vSAN portgroup MTU settings match 9000 bytes across all uplinks.
    **`Unable to route to host`** — Verify vSAN VMkernel IP is correct and the vSAN network is properly isolated and routable between nodes.
**Verify OMIVV plugin in vCenter**

After wizard: vCenter → Menu → OpenManage Integration for VMware vCenter should appear. If the plugin is not present, see Phase 5 for manual installation.

**Exit criterion:** All nodes connected in vCenter. vmk0/vmk1/vmk2 present and correct on all nodes. MTU tests pass across all node pairs. OMIVV plugin visible in vCenter menu.

---

## Phase 5: SupportAssist and OMIVV

OMIVV (OpenManage Integration for VMware vCenter) surfaces Dell hardware alerts, firmware inventory, and warranty data directly in vCenter. SupportAssist enables Dell cloud-based proactive diagnostics. Both should be enabled before the cluster goes to production.

**Install OMIVV plugin (if not auto-installed)**

The OMIVV OVA is available from the Dell support portal. Deploy via vCenter:

1. vCenter → Deploy OVF Template → provide OMIVV OVA path
2. Configure OMIVV appliance: IP, hostname, admin password
3. After deploy: navigate to `https://<omivv-ip>` → register with vCenter
4. In vCenter → Menu → OpenManage Integration → Configure → Add vCenter connection

**Enable SupportAssist via VxRail Plugin**

1. vCenter → Menu → VxRail → Support → SupportAssist
2. Enable SupportAssist → enter Dell support account credentials (or create account)
3. Configure contact info and preferred support language
4. Test connection → confirm status shows "Connected"

**Configure Dell Connect (outbound HTTPS only)**

SupportAssist requires outbound HTTPS (port 443) from VxRail Manager to `esrs.emc.com` and `supportassist.emc.com`. No inbound connections are required.

```bash
# Verify outbound connectivity from VxRail Manager VM SSH
curl -sk https://esrs.emc.com
curl -sk https://supportassist.emc.com
```


```text title="Expected output"
<!DOCTYPE html>
<html>
<head>
<title>EMC ESRS Portal</title>
</head>
<body>
<h1>Welcome to ESRS</h1>
</body>
</html>
<!DOCTYPE html>
<html>
<head>
<title>Dell EMC SupportAssist</title>
</head>
<body>
<h1>SupportAssist Online</h1>
</body>
</html>
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to esrs.emc.com port 443: Connection timed out`** — Verify network connectivity from VxRail Manager VM, check firewall rules allow outbound HTTPS to EMC domains, and confirm DNS resolution with `nslookup esrs.emc.com`.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Remove the `-k` flag if you need strict certificate validation, or ensure the VxRail Manager VM has current CA certificates installed via `update-ca-certificates` or equivalent.
    **`curl: (6) Could not resolve host: esrs.emc.com`** — Verify DNS servers are configured correctly on the VxRail Manager VM with `cat /etc/resolv.conf` and test with `nslookup 8.8.8.8`.
If a proxy is required, configure it in VxRail Manager: Settings → Network → Proxy.

**Verify hardware monitoring**

In vCenter → Menu → OpenManage Integration → Hosts and Clusters: all nodes should show hardware health green with firmware inventory populated.

**Exit criterion:** OMIVV shows all nodes with green hardware health. SupportAssist shows Connected status. Dell hardware alerts are visible in vCenter alarms.

---

## Phase 6: Post-Deploy Hardening and Baseline

**Change VxRail Manager mystic password**

The `mystic` account is the local service account for VxRail Manager REST API and CLI access. Change the default password immediately after deployment.

In VxRail Manager UI: Settings → System → Change Password (mystic account)

Or via REST API:

```bash
curl -sk -X PUT -u 'mystic:currentpassword' \
  -H "Content-Type: application/json" \
  -d '{"password":"<NewPassword>"}' \
  https://<vxm-ip>/rest/vxm/v1/system/credentials/mystic
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification (already present in the example, so ensure you're using the exact command provided).
    **`curl: (401) Unauthorized`** — Verify the current password is correct and the mystic user exists; check VxRail Manager credentials in your environment.
    **`curl: (7) Failed to connect to <vxm-ip> port 443: Connection refused`** — Confirm the VxRail Manager IP address is correct and reachable, and that the REST API service is running on the target node.
**Change iDRAC default passwords on all nodes**

Default iDRAC credentials (root / Calvin) must be changed on every node. Do this via RACADM from each node's ESXi SSH session or from a jump host with RACADM installed.

```bash
# Change iDRAC root password via RACADM (run on each node or via iDRAC IP remotely)
racadm set idrac.users.2.password <NewPassword>

# Verify the change took effect
racadm get idrac.users.2.username
```


```text title="Expected output"
RACADM.2.1 -- Dell EMC RACADM CLI Tool, Version 2.1.1.0
Copyright (C) 2009-2023 Dell Inc. All rights reserved.

Object value modified successfully.
root
```

!!! warning "Common errors"
    **`RACADM.1.1 -- Unexpected EOF while processing command`** — Ensure the iDRAC IP is reachable and RACADM is authenticated; add `-r <iDRAC_IP> -u root -p <current_password>` flags if running remotely.
    **`Error: IPMI command failed: Insufficient privilege`** — Verify you are running RACADM as root or with sudo, or that the current iDRAC user has administrator privileges.
Alternatively use the iDRAC web UI: iDRAC Settings → User Authentication → Local Users → root → Change Password.

**Enable lockdown mode on all hosts**

```powershell
# Enable normal lockdown on all VxRail nodes via PowerCLI
Connect-VIServer vcenter.example.local
foreach ($h in Get-VMHost -Location (Get-Cluster "VxRail-Cluster")) {
    $view = Get-View $h
    $view.EnterLockdownMode()
    Write-Host "$($h.Name) lockdown enabled"
}
```

**Configure vCenter VAMI file-based backup**

vCenter VCSA (for embedded deployments) should be backed up via the VAMI backup facility.

1. Navigate to `https://<vcenter-fqdn>:5480` → Backup → Configure
2. Backup location: SFTP or FTPS target (not on the vSAN datastore the VCSA manages)
3. Schedule: daily, retain 3 copies minimum
4. Encryption password: set and document securely

**Configure LCM upgrade baseline**

1. vCenter → Menu → Lifecycle Manager → Baselines
2. Create a VxRail-aware upgrade baseline (VxRail Manager integrates with LCM for coordinated upgrades)
3. VxRail upgrades must go through VxRail Manager → not directly through LCM baselines
4. In VxRail Manager UI: LCM → Upload Bundle → initiate from VxRail Manager, not vCenter LCM directly

**Take VxRail Manager VM backup**

```powershell
# Snapshot VxRail Manager VM as a baseline post-deploy snapshot
Connect-VIServer vcenter.example.local
$vm = Get-VM "VxRail-Manager"
New-Snapshot -VM $vm -Name "Post-Deploy-Baseline" -Description "Clean post-deploy state before production use"
```

Also integrate VxRail Manager VM into any existing VM backup solution (Avamar, VBEM, etc.).

**Disable SSH on all ESXi hosts post-hardening**

```bash
# From each ESXi host SSH session
vim-cmd hostsvc/disable_ssh
vim-cmd hostsvc/disable_esx_shell
```


```text title="Expected output"
SSH has been disabled.
ESX Shell has been disabled.
```

!!! warning "Common errors"
    **`vim-cmd: command not found`** — Ensure you are logged into an ESXi host directly via SSH, not a vCenter or management appliance where vim-cmd is not available.
    **`Error: Permission denied`** — Verify you are logged in as root or a user with administrative privileges on the ESXi host.
Or via PowerCLI:

```powershell
foreach ($h in Get-VMHost -Location (Get-Cluster "VxRail-Cluster")) {
    Get-VMHostService -VMHost $h | Where-Object {$_.Key -eq "TSM-SSH"} | Stop-VMHostService -Confirm:$false
}
```

**Exit criterion:** All passwords changed. Lockdown mode active on all nodes. SSH disabled. VAMI backup scheduled and tested. VxRail Manager VM snapshot taken.

---

## Post-Deployment Checklist

| Check | Command / Location | Expected |
|---|---|---|
| All nodes connected | vCenter → Hosts and Clusters | Connected |
| vSAN health | `esxcli vsan health cluster get` | All green |
| vSAN MTU test | `vmkping -I vmk2 -d -s 8972 <peer>` | 0% packet loss |
| VMkernel ports present | `esxcli network ip interface list` | vmk0, vmk1, vmk2 on all nodes |
| VxRail Manager accessible | `https://<vxm-ip>` → cluster health | Healthy |
| VxRail Manager version | `curl -sk -u mystic:pw https://<vxm-ip>/rest/vxm/v1/system` | Current release |
| OMIVV hardware health | vCenter → Menu → OpenManage Integration | All nodes green |
| SupportAssist status | vCenter → Menu → VxRail → Support | Connected |
| mystic password changed | VxRail Manager → Settings → Credentials | Non-default |
| iDRAC passwords changed | iDRAC web UI or `racadm get idrac.users.2` | Non-default (not Calvin) |
| Lockdown mode enabled | vCenter → Host → Configure → Security Profile | Normal |
| SSH disabled | vCenter → Host → Configure → Security Profile → Services | Stopped |
| SPBM policy applied | vCenter → Policies and Profiles | RAID-1 FTT=1 on mgmt VMs |
| VAMI backup configured | `https://<vcenter-fqdn>:5480` → Backup | Scheduled, last run success |
| VxRail Manager VM backup | Snapshot or backup job | Post-deploy baseline exists |
| DNS all records resolve | `nslookup <fqdn>` for each component | Forward + reverse match |
| NTP synced on all nodes | `esxcli system ntp get` | NTP enabled, synced |

---

## See also

- [VxRail — How It Works (VMware Platform)](../architecture/how-it-works/)
- [VxRail — Health Checks](../operations/health-checks/)
- [VxRail — Common Issues](../troubleshooting/common-issues/)

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
