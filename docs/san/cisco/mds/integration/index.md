# Cisco MDS Integration

> Part of the [Cisco MDS](../) reference.

---
## Nexus Dashboard Fabric Controller (NDFC)

NDFC (formerly DCNM) provides centralised zone management, fabric topology visibility, performance monitoring, and firmware orchestration across all MDS switches.

**Key capabilities:**

- Zone provisioning from a single GUI without SSHing to individual switches
- Fabric topology view with ISL health and utilisation
- Per-port performance graphs (IOPS, MB/s, errors)
- Firmware upgrade orchestration

**Setup:**

1. Deploy the NDFC virtual appliance.
2. Discover MDS switches: NDFC → Manage → Inventory → Discover → enter switch IP and credentials.
3. Configure SNMP v3 on each switch for telemetry collection (NDFC requires SNMP and SSH access).

---

## VMware FC Connectivity

ESXi hosts connect to storage via FC HBAs, which log into the MDS fabric and are zoned to storage target ports.

**Zone a new ESXi host:**

```
# Step 1 — Find the host HBA WWPN after it logs in
show flogi database vsan 10 | grep <host-ip-or-note>
# Or check the host HBA WWPNs from the ESXi console:
esxcli storage san fc list

# Step 2 — Create a device alias for each HBA port
device-alias database
  device-alias name esxi-host01_hba0 pwwn 21:00:00:xx:xx:xx:xx:xx
  device-alias name esxi-host01_hba1 pwwn 21:00:00:xx:xx:xx:xx:xx
device-alias commit

# Step 3 — Create zones (one per host-port to storage-port pair)
zone name esxi-host01_hba0-powermax01_fa0 vsan 10
  member device-alias esxi-host01_hba0
  member device-alias powermax01_fa0

# Step 4 — Add zones to the active zone set and activate
zoneset name prod-zoneset vsan 10
  member esxi-host01_hba0-powermax01_fa0

zoneset activate name prod-zoneset vsan 10
```

**Verify the host can see the storage:**

```
show zone member device-alias esxi-host01_hba0 vsan 10
```

---

## Dell PowerMax Integration

PowerMax FA (Front-End Adapter) ports log into the MDS fabric. Each FA port is registered as a device alias.

```
# Show PowerMax FA port registrations
show flogi database vsan 10 | grep <powermax-wwpns>

# Create device aliases for PowerMax FA ports
device-alias database
  device-alias name powermax01_fa0e pwwn 5x:xx:xx:xx:xx:xx:xx:xx
device-alias commit
```

For SRDF/A replication, the SRDF director ports on both arrays are zoned together in the replication VSAN (e.g., VSAN 20/21) — not in the production VSAN.

---

## Pure Storage FlashArray Integration

Pure FlashArray target ports are registered as device aliases and zoned per host.

```
# Pure array target ports (get WWPNs from Pure UI: Settings → SAN)
device-alias database
  device-alias name pure-fa01_ct0.eth4 pwwn 52:4a:xx:xx:xx:xx:xx:xx
device-alias commit

# Zone: one zone per host HBA to one Pure target port
zone name esxi-host01_hba0-pure-fa01_ct0 vsan 10
  member device-alias esxi-host01_hba0
  member device-alias pure-fa01_ct0.eth4
```

Pure recommends at least 2 target ports per host path for redundancy. Zone each host HBA to 2 Pure target ports (one zone per pair).

---

## SNMP and Syslog

```
# Configure SNMP v3 (preferred over v2c)
snmp-server user <username> network-operator auth sha <auth-password> priv aes-128 <priv-password>
snmp-server host <monitoring-server-ip> traps version 3 priv <username>

# Configure syslog forwarding
logging server <siem-ip> 5 facility local7
# Level 5 = notifications (includes port state changes and zone changes)
```

Verify SNMP is reachable from the monitoring server:

```bash
snmpwalk -v3 -u <username> -l authPriv -a SHA -A <auth-pass> -x AES -X <priv-pass> <switch-ip> sysDescr
```
