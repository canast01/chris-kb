# Cisco DCNM — Install & Upgrade

> Part of the [Cisco DCNM](../../index.md) reference.

---

## Overview

DCNM 11.x is deployed as an OVA (VMware) or ISO (KVM/bare metal). This page covers fresh installation and in-place upgrade procedures. For migration from DCNM to NDFC, see the [Nexus Dashboard](../../../nexus-dashboard/index.md) section.

---

## Pre-Installation Requirements

| Requirement | Detail |
|---|---|
| Hypervisor | VMware ESXi 6.7+ or KVM (RHEL/CentOS 7/8) |
| vCPU | 16 minimum (24 for > 100 switches) |
| RAM | 64 GB minimum |
| Storage | 1 TB (thick provisioned recommended) |
| NIC | 2 NICs: management (DCNM UI/API) and enhanced fabric management (SAN discovery) |
| NTP | Must reach NTP servers |
| DNS | Forward DNS for DCNM management FQDN |
| Ports open | TCP 22, 443 inbound; TCP 22, 161/UDP outbound to switches |

Download DCNM OVA from Cisco Software Download Center. Verify SHA-512 checksum before deployment.

---

## Fresh Installation — VMware ESXi (OVA)

### 1. Deploy OVA

1. In vCenter, select **Actions > Deploy OVF Template**.
2. Browse to the DCNM OVA.
3. Follow the wizard:
   - VM name: `dcnm-dc1-01`
   - Datastore: production datastore with ≥ 1.5 TB free
   - Network: select management port group
4. On **Customize Template**:
   - Management IP / mask / gateway
   - DNS server 1 / 2
   - NTP server
   - Hostname: `dcnm-dc1.corp.example.com`
   - Admin password (set during OVA deploy)
5. Complete and power on.

### 2. Initial Configuration (GUI)

Access `https://<dcnm-ip>` and log in with `admin` and the password set during OVA deployment.

**Setup wizard:**

1. **Licensing** — apply DCNM license key under **Administration > Licensing**.
2. **Network settings** — verify hostname, DNS, NTP under **Administration > Network Preferences**.
3. **SNMP** — configure the SNMP v3 credentials that DCNM will use to poll switches.
4. **SSH** — configure the SSH credentials DCNM will use to manage switches.
5. **Fabric discovery** — navigate to **SAN > Fabrics > Discover** and enter a seed switch IP.

### 3. Discover First Fabric

1. **SAN > Fabrics > New Fabric**
2. Enter fabric name: `DC1-FABRIC-A`
3. Select **Discover** and enter seed switch IP
4. Enter SSH credentials (`dcnm_mgmt` / password)
5. Enter SNMP v3 credentials (`dcnm_poll` / auth+priv)
6. Click **Discover** — DCNM crawls the fabric from the seed switch
7. After discovery completes, navigate to **SAN > Fabrics > DC1-FABRIC-A** to confirm switch count

---

## HA Deployment

### Prerequisites

- Two DCNM VMs deployed with the same version
- A Virtual IP (VIP) reachable by clients
- Both nodes must be in the same subnet (HA uses active/standby with VIP failover)

### HA Configuration

```bash
# On the primary (active) DCNM node
ssh root@dcnm-dc1-active.corp.example.com

# Run HA setup utility
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-setup.sh \
  --primary \
  --vip 10.10.5.15 \
  --peer 10.10.5.11 \
  --password <ha-password>

# On the secondary (standby) node
ssh root@dcnm-dc1-standby.corp.example.com

/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-setup.sh \
  --secondary \
  --vip 10.10.5.15 \
  --peer 10.10.5.10 \
  --password <ha-password>

# Verify HA status from active node
/usr/local/cisco/dcm/dcnm/bin/dcnm-ha-status.sh
# Expected: ACTIVE/STANDBY pair, VIP reachable
```
┌────────────────────────────────── Cisco DCNM — Install and Upgrade ───────────────────────────────────┐
│                                                                                                       │
│  DCNM deployment: OVA/ISO to vSphere, initial config, switch discovery, upgrade path.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Fresh Install Steps              │  │            Initial Configuration            │   │
│   │        1. Download DCNM OVA from CCO         │  │          1. Set hostname + IP + DNS         │   │
│   │           2. Deploy OVA in vSphere           │  │           2. Configure NTP servers          │   │
│   │       3. Boot + initial config wizard        │  │           3. Set admin credentials          │   │
│   │        4. 8 vCPU / 32 GB RAM (large)         │  │           4. Configure ISE TACACS+          │   │
│   │          5. 2 TB datastore for perf          │  │           5. Discover MDS switches          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  OVA deployment is automated; ISE and NTP must be configured before adding switches.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Upgrade Procedure               │  │           Post-Upgrade Validation           │   │
│   │           1. Backup DCNM DB to NFS           │  │         1. Verify all switches shown        │   │
│   │           2. Download new DCNM OVA           │  │         2. Check SNMP alert forward         │   │
│   │        3. Deploy standby; restore DB         │  │         3. Re-test ISE TACACS+ auth         │   │
│   │         4. Validate standby function         │  │        4. Verify NFS backup schedule        │   │
│   │          5. Swing DNS; decom old VM          │  │          5. Confirm zone push works         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere host · 2 TB datastore · management network · NFS backup share                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CCO             = Cisco Connection Online; software download portal (software.cisco.com)             │
│  OVA             = Open Virtual Appliance; DCNM packaged as vSphere-ready VM template                 │
│  Config wizard   = DCNM first-boot setup; sets IP, NTP, credentials interactively                     │
│  ISE             = Cisco Identity Services Engine; provides TACACS+ for DCNM auth                     │
│  NFS backup      = nightly DCNM DB backup; required before any upgrade                                │
│  Swing DNS       = update DNS A record to new DCNM VM IP after validation                             │
│  Standby upgrade = deploy new DCNM version as standby first; validate then swing                      │
│  SNMP forwarding = DCNM forwards switch alerts to NMS; test after every upgrade                       │
│  Zone push test  = verify DCNM can activate zone set on MDS switch after upgrade                      │
│  vCPU / RAM      = DCNM large mode: 8 vCPU / 32 GB; medium: 4 vCPU / 16 GB                            │
│  2 TB datastore  = DCNM storage for 90-day performance data; Elasticsearch store                      │
│  NTP             = Network Time Protocol; timestamps required for event correlation                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Post-Upgrade Validation

```bash
# Verify services
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status

# Check discovery connectivity
# GUI: SAN > Fabrics — all switches should reconnect within 5 minutes

# Check performance manager
# GUI: Monitor > Performance — data should resume within 10 minutes

# Verify event processing
# GUI: Monitor > Alarms — confirm recent events are being received

# Delete VM snapshot (taken pre-upgrade) after 48-hour validation
```

---

## Decommission

1. Export all zone sets and device alias databases.
2. Remove DCNM as SNMP trap receiver on all managed switches:

```bash
# On each MDS switch
no snmp-server host <dcnm-ip> traps version 3 priv dcnm_poll

# Remove syslog forwarding to DCNM
no logging server <dcnm-ip>

# Remove DCNM service account
no username dcnm_mgmt
```

3. Power off and delete the DCNM VM from vCenter.
4. Update DNS to remove DCNM records.
5. If migrating to NDFC: follow Cisco's DCNM-to-NDFC migration guide (cisco.com/go/ndfc).
