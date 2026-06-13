---
tags:
  - aria-networks
  - deployment
  - vmware
---
# Aria Operations for Networks — Deploy

<div class="kb-summary">
End-to-end deployment guide for Aria Operations for Networks (AON). Covers pre-flight checks, platform node OVA deployment, proxy/collector node registration, data source configuration (vCenter, NSX, physical switches), IPFIX flow collection setup, and post-deployment validation.

*Applies to: Aria Networks 6.x*
</div>

```text
┌────────────────────────── Aria Operations for Networks — Deployment Phases ───────────────────────────┐
│                                                                                                       │
│  Six phases from bare metal to operational flow-collection and topology mapping.                      │
│  Complete each phase validation check before proceeding to the next phase.                            │
│                                                                                                       │
│  ┌──────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────────────┐     │
│  │  Phase 1: Pre-Flight     │  │  Phase 2: Platform OVA   │  │   Phase 3: Proxy/Collector OVA   │     │
│  │  DNS A + PTR records     │  │  Deploy Platform OVA     │  │   Deploy Collector OVA           │     │
│  │  NTP reachable           │  │  Set IP/FQDN/NTP         │  │   Enter platform FQDN + key      │     │
│  │  vCenter svc account     │  │  Initial setup wizard    │  │   Proxy registers to platform    │     │
│  │  NSX credentials ready   │  │  Accept EULA + licence   │  │   Verify green status in UI      │     │
│  │  Datastore ≥ 200 GB      │  │  Platform Running state  │  │   Deploy more proxies if needed  │     │
│  └──────────────────────────┘  └──────────────────────────┘  └──────────────────────────────────┘     │
│                                                                                                       │
│               ▼                             ▼                                ▼                        │
│                                                                                                       │
│  ┌──────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────────────┐     │
│  │  Phase 4: Data Sources   │  │  Phase 5: Flow (IPFIX)   │  │     Phase 6: Validation          │     │
│  │  Add vCenter + thumbprt  │  │  NSX IPFIX → proxy IP    │  │   Services: nginx, cassandra     │     │
│  │  Add NSX Manager creds   │  │  VDS: collector UDP 2055 │  │   All data sources green         │     │
│  │  Add physical switches   │  │  Physical switch NetFlow │  │   Flows arriving on flow map     │     │
│  │  SNMP community/v3 creds │  │  Verify flows in UI      │  │   Topology visible (VM→phys)     │     │
│  │  Topology sync begins    │  │  Application discovery   │  │   Path analysis functional       │     │
│  └──────────────────────────┘  └──────────────────────────┘  └──────────────────────────────────┘     │
│                                                                                                       │
│  Physical Infrastructure: Platform VM (≥200 GB datastore, static IP) + Collector VMs per site;        │
│  SNMP access to physical switches; IPFIX/NetFlow export from ESXi hosts and NSX.                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Platform VM    = Central AON node: UI, analytics engine, cassandra/kafka/elasticsearch data store    │
│  Collector VM   = Remote proxy VM: receives IPFIX/NetFlow; connects outbound to platform TCP 443      │
│  IPFIX          = IP Flow Information Export; standard flow telemetry from NSX-T and VDS              │
│  Data source    = vCenter, NSX Manager, physical switch, or firewall added to AON for collection      │
│  PAK file       = Product upgrade bundle; uploaded via VAMI on port 5480 for in-place upgrade         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Pre-Flight Checks

**Exit criterion:** DNS resolves forward and reverse for all AON VMs; NTP is reachable; all service account credentials prepared.

### DNS

Create A and PTR records before deploying any OVA. AON will fail to start if PTR records are missing.

| Record | Example |
|---|---|
| Platform VM A record | `aon-platform.example.local → 10.10.10.50` |
| Platform VM PTR record | `50.10.10.10.in-addr.arpa → aon-platform.example.local` |
| Collector VM A record | `aon-collector-dc1.example.local → 10.10.10.51` |
| Collector VM PTR record | `51.10.10.10.in-addr.arpa → aon-collector-dc1.example.local` |

```bash
# Verify from a host on the same management network
nslookup aon-platform.example.local
nslookup 10.10.10.50
```

### Service Accounts

| System | Required Permission |
|---|---|
| vCenter | Read-only at datacenter level (for topology); or Global Read |
| NSX Manager | Auditor role (read-only; AON does not need write unless pushing DFW rules) |
| Physical switches | SNMP v2 read community string or SNMPv3 credentials |

### Resource Requirements

| Component | vCPU | RAM | Disk | Notes |
|---|---|---|---|---|
| Platform VM (medium) | 8 | 32 GB | 200 GB | Production; 1 per deployment |
| Collector VM | 4 | 12 GB | 100 GB | 1 per site or per NSX Manager |

---

## Phase 2 — Platform Node OVA Deployment

**Exit criterion:** AON platform UI accessible at `https://aon-platform.example.local`; initial setup wizard complete; platform shows Running state.

### Deploy Platform OVA

```bash
# Download OVA from Broadcom Support Portal:
# My Downloads → Aria Operations for Networks → VMware-Aria-Operations-for-Networks-6.14.0-Platform.ova
```

Deploy via vCenter UI: Actions → Deploy OVF Template, then configure OVF properties:

| Property | Example Value |
|---|---|
| IP Address | `10.10.10.50` |
| Subnet Mask | `255.255.255.0` |
| Default Gateway | `10.10.10.1` |
| DNS Server 1 | `10.10.0.1` |
| DNS Server 2 | `10.10.0.2` |
| Hostname (FQDN) | `aon-platform.example.local` |
| NTP Server | `ntp.example.local` |
| Admin Password | *(set initial password)* |

Power on the VM. First boot initialises cassandra, kafka, elasticsearch, and nginx — allow 10–15 minutes.

### Verify Platform Is Ready

```bash
# HTTPS reachable
curl -sk https://aon-platform.example.local -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200

# Services running on platform VM
ssh ubuntu@aon-platform.example.local
sudo systemctl status vrni-platform nginx cassandra kafka elasticsearch postgres
```

### Initial Setup Wizard

1. Browse to `https://aon-platform.example.local`.
2. Accept EULA.
3. Enter licence key (from Broadcom portal).
4. Confirm platform shows **Running** in Admin → Infrastructure.

---

## Phase 3 — Proxy / Collector Node Deployment

**Exit criterion:** All collector VMs registered to the platform and showing green health in Admin → Infrastructure.

### Deploy Collector OVA

Download: `VMware-Aria-Operations-for-Networks-6.14.0-Collector.ova`

Deploy via vCenter (same steps as Platform OVA) using the Collector OVA. During the wizard, enter:

| Property | Value |
|---|---|
| IP Address | `10.10.10.51` |
| Hostname (FQDN) | `aon-collector-dc1.example.local` |
| Platform VM FQDN | `aon-platform.example.local` |
| Shared Secret | *(pairing key from platform UI)* |

**Retrieve the pairing key from platform UI:**  
Admin → Infrastructure → Add Proxy → copy the shared secret.

### Register Collector to Platform

The Collector auto-registers on first boot using the platform FQDN and shared secret entered during OVA deploy. Monitor from the platform UI:

Admin → Infrastructure → Proxies — the new collector should appear within 5 minutes.

```bash
# Verify collector service on collector VM
ssh ubuntu@aon-collector-dc1.example.local
sudo systemctl status vrni-collector

# Verify collector registered via API
TOKEN=$(curl -sk -X POST "https://aon-platform.example.local/api/ni/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"PASSWORD"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk "https://aon-platform.example.local/api/ni/collectors" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "import sys,json; [print(c.get('nickname'), c.get('status')) for c in json.load(sys.stdin).get('results',[])]"
```

---

## Phase 4 — Data Source Configuration

**Exit criterion:** vCenter, NSX Manager, and physical switch data sources all show green collection status in Infrastructure → Data Sources.

### Add vCenter as Data Source

In the AON UI: Infrastructure → Data Sources → Add Source → VMware vCenter

```text
vCenter FQDN:   vcenter.example.local
Username:       svc-aon@vsphere.local
Password:       ********
Accept thumbprint when prompted
```

Topology sync starts immediately. VMs and host objects appear in the flow map within minutes.

### Add NSX Manager as Data Source

Infrastructure → Data Sources → Add Source → VMware NSX-T Manager

```text
NSX Manager FQDN:   nsxmgr.example.local
Username:           svc-aon@vsphere.local
Password:           ********
```

NSX adds DFW rule context to flow records and enables security group visibility.

### Add Physical Switches (SNMP)

Infrastructure → Data Sources → Add Source → Switch (SNMP)

```text
Switch IP:          10.10.0.254
SNMP Version:       v2c
Community String:   public-ro
```

For SNMPv3:

```text
SNMP Version:      v3
Username:          snmpuser
Auth Protocol:     SHA
Auth Password:     ********
Privacy Protocol:  AES
Privacy Password:  ********
```

Physical topology appears in the network map after the first SNMP poll cycle (~5 minutes).

### Verify Data Source Health

```bash
curl -sk "https://aon-platform.example.local/api/ni/data-sources" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "import sys,json; [print(ds.get('alias'), ds.get('status')) for ds in json.load(sys.stdin).get('results',[])]"
# All sources should report: ENABLED
```

---

## Phase 5 — IPFIX Flow Collection

**Exit criterion:** Flow records visible in the Flow Map for at least one VM-to-VM conversation; application discovery active.

### Enable IPFIX on NSX-T

In NSX Manager: Networking → Flow Monitoring → IPFIX Profiles → Add Profile

```text
Collector IP:    10.10.10.51   (Collector VM management IP)
Collector Port:  2055
Active Timeout:  60
Idle Timeout:    15
```

Assign the profile to NSX segments or transport nodes.

### Enable IPFIX on VDS

In vCenter: dvSwitch → Configure → NetFlow → Edit

```text
Collector IP:   10.10.10.51
Collector Port: 2055
Active Flow Timeout:   60
Idle Flow Timeout:     15
```

Apply to the distributed switch. Flow export begins immediately.

### Configure Physical Switch NetFlow

On Cisco IOS switches (example):

```bash
# Define flow exporter toward the Collector VM
ip flow-export destination 10.10.10.51 2055
ip flow-export version 9
ip flow-export source Vlan10

# Enable on interfaces
interface GigabitEthernet1/0/1
 ip flow ingress
 ip flow egress
```

On Arista EOS (example):

```bash
flow tracking hardware
   tracker IPFIX
      record format ipfix
      exporter VRNI-COLLECTOR
         destination 10.10.10.51
         local interface Management1
         template interval 300
```

### Verify Flows Arriving

In the AON UI: Network Map → select a VM entity → Flows tab — recent flow records should appear within 5 minutes of enabling export.

```bash
# Check collector is receiving UDP 2055 traffic
ssh ubuntu@aon-collector-dc1.example.local
sudo tcpdump -i eth0 udp port 2055 -c 20
# Should see packets from ESXi hosts and switches
```

---

## Phase 6 — Post-Deployment Validation

**Exit criterion:** All service health checks green; topology visible end-to-end (VM → logical → physical); path analysis returns results.

### Service Health Check

```bash
ssh ubuntu@aon-platform.example.local
sudo systemctl status vrni-platform nginx cassandra kafka elasticsearch postgres
# All services: Active (running)

# Check for errors in platform log
sudo tail -50 /var/log/vrni-platform/platform.log | grep -i error
```

### Topology and Flow Map

- Network Map → browse to any VM → confirm VMs, segments, and physical switches are visible.
- Network Map → select two VMs → Path Analysis → confirm path traces through NSX DFW rules.

### Run Path Analysis

In the AON UI: Plan & Assess → Path Analysis

```text
Source:       VM or IP (e.g. web-01.example.local)
Destination:  VM or IP (e.g. db-01.example.local)
Port:         3306/TCP
→ Analyse
```

Expected result: full hop-by-hop path including NSX DFW rule that allows or denies the flow.

### Post-Deployment Checklist

| Check | Expected Result |
|---|---|
| Platform UI accessible on HTTPS 443 | Login page loads; no certificate errors |
| All collector VMs registered | Admin → Infrastructure → Proxies: all green |
| vCenter data source green | VMs and hosts visible in flow map |
| NSX data source green | DFW rules visible on path analysis hops |
| Physical switch topology visible | Switch and port objects in network map |
| IPFIX flows arriving | Flows visible on VM entities within 5 min |
| Path analysis returns results | Full path from source to destination shown |
| Application discovery active | Plan & Assess → Applications shows candidates |
| No errors in platform.log | `grep -i error /var/log/vrni-platform/platform.log` returns nothing critical |
| NTP synchronised on all AON VMs | `chronyc tracking` shows < 1 s offset |
