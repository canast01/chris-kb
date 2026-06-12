# ESXi — Health Checks


<div class="kb-summary">
Daily and weekly health runbook for ESXi hosts: hardware sensors, service status, storage paths, network uplinks, NTP sync, VIB compliance, and capacity thresholds — with a runnable command sequence and per-area deep-dive checks.
</div>

```text
┌──────────────────────────────────────── ESXi — Health Checks ─────────────────────────────────────────┐
│                                                                                                       │
│  Daily/weekly health runbook: hardware sensors, alarms, capacity, and storage.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Hardware Health                │  │            vSphere Cluster Health           │   │
│   │           IPMI/iDRAC sensor status           │  │          HA master elected & green          │   │
│   │            CPU/mem/fan/PSU alarms            │  │            DRS balance score < 2            │   │
│   │           esxcli hardware ipmi sdr           │  │          vMotion network reachable          │   │
│   │            HBA/NIC link state up             │  │            No disconnected hosts            │   │
│   │         Boot media health S.M.A.R.T.         │  │             EVC mode consistent             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Hardware sensors → vSphere alarms → storage health → capacity review.                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Storage Health                │  │               Capacity Review               │   │
│   │           All paths active per LUN           │  │           Host CPU util < 70% avg           │   │
│   │           No APD/PDL events today            │  │           Host mem util < 80% avg           │   │
│   │             Datastore free > 20%             │  │             VM balloon/swap = 0             │   │
│   │          VMFS no ATS heartbeat err           │  │           vSAN disk capacity < 70%          │   │
│   │            vSAN health: all green            │  │          Trend forecast 30/60 days          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 hosts with IPMI/iDRAC BMC, SAN/NAS/vSAN storage, 10/25 GbE NICs                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IPMI     = Intelligent Platform Mgmt Interface; OOB hardware sensor access                           │
│  iDRAC    = Dell Remote Access Controller; OOB management BMC                                         │
│  S.M.A.R.T = Self-Monitoring Analysis; disk health from boot media                                    │
│  APD      = All Paths Down; storage unreachable but PDL not declared                                  │
│  PDL      = Permanent Device Loss; device signals loss is permanent                                   │
│  ATS      = Atomic Test & Set; VMFS locking primitive; heartbeat mechanism                            │
│  DRS score= 1-5 imbalance rating; 1=balanced, 5=critical imbalance                                    │
│  Balloon  = VMware memory mgmt; guest driver returns idle pages to host                               │
│  EVC      = Enhanced vMotion Compat; consistent CPU flags across cluster                              │
│  fdm      = Fault Domain Manager; HA agent; must run on all hosts                                     │
│  vSAN health = Skyline Health dashboard in vCenter; 60+ automated checks                              │
│  BMC      = Baseboard Management Controller; embedded OOB management chip                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Run This Routine

Run these commands in sequence for a complete ESXi health snapshot. Each block can be pasted directly into an SSH session on the host or run via PowerCLI.

```bash
# 1. Verify ESXi version and build
vmware -vl

# 2. Host hardware summary — vendor, model, serial
esxcli hardware platform get

# 3. Network adapter (vmnic) status — check link state and speed
esxcli network nic list

# 4. VMkernel adapter list — IPs, MTU, enabled services
esxcli network ip interface list

# 5. Storage adapter health — HBAs, iSCSI, NVMe controllers
esxcli storage core adapter list

# 6. Storage paths — look for 'dead' state
esxcli storage core path list | grep -i dead

# 7. Datastore accessibility — mount state and capacity
esxcli storage filesystem list

# 8. NTP sync status
esxcli system ntp get
esxcli system time get

# 9. Host services — verify hostd, vpxa, fdm running
esxcli system process stats load get
/etc/init.d/hostd status
/etc/init.d/vpxa status
/etc/init.d/fdm status

# 10. Recent syslog errors
tail -100 /var/log/syslog.log | grep -iE "error|critical|warning"

# 11. Installed VIB count — baseline for patch drift detection
esxcli software vib list | wc -l
```

## Hardware Health

### Sensor Status

```bash
# Full hardware health summary (CPU, memory, fan, PSU, temperature)
esxcli hardware ipmi sdr list | grep -iE "critical|warning|nc"

# Specific component checks
esxcli hardware cpu list          # CPU package info
esxcli hardware memory get        # RAM installed
esxcli hardware pci list | grep -i "hba\|nic\|nvme"   # PCI devices

# Boot media S.M.A.R.T. check (USB/SD boot media or local SSD)
esxcli storage core device smart get -d <device-name>
```

| Sensor category | Alert threshold | Action |
|---|---|---|
| CPU temperature | > 80°C | Check datacenter cooling, BIOS throttling |
| Memory ECC errors | Any correctable/uncorrectable | Replace DIMM; plan maintenance |
| Fan failure | Any fan speed = 0 or critical | Replace fan, monitor temperature |
| PSU redundancy | Redundancy lost | Replace failed PSU before primary fails |
| Boot media health | S.M.A.R.T. reallocated sectors > 0 | Schedule boot media replacement |

### Host Connection and Service Health

```bash
# Check hostd (management daemon) — restart if unresponsive
/etc/init.d/hostd status
/etc/init.d/hostd restart        # only if genuinely unresponsive

# Check vpxa (vCenter agent) — needed for vCenter connectivity
/etc/init.d/vpxa status

# Check fdm (HA agent) — needed for vSphere HA
/etc/init.d/fdm status

# Confirm host is Connected in vCenter via PowerCLI
Get-VMHost | Select-Object Name, ConnectionState, PowerState
```

## Network Health

### Uplink and VMkernel

```bash
# Check all vmnic uplinks — Speed/Duplex should show link speed, not 0/Half
esxcli network nic list

# Check for packet errors and drops on each vmnic
esxcli network nic stats get -n vmnic0
esxcli network nic stats get -n vmnic1
# Look for: RX/TX errors > 0 or drops incrementing under load

# VMkernel adapter ping test — verify vMotion and vSAN vmk reachability
vmkping -I vmk1 <vmotion-gateway>
vmkping -I vmk2 -s 8972 <vsan-gateway>   # jumbo frame test for vSAN (MTU 9000)

# Check CDP/LLDP for physical switch confirmation
esxcli network vswitch dvs vmware list     # DVS attached uplinks
esxcli network vswitch standard list       # standard vSwitch uplinks
```

### MTU Validation

```bash
# Test MTU end-to-end on vSAN VMkernel (9000 MTU required)
vmkping -I vmk2 -d -s 8972 <peer-vsan-vmk-ip>
# -d = don't fragment; -s 8972 = payload (8972 + 28 bytes header = 9000 MTU)
# Failure = MTU mismatch somewhere in the path
```

## Storage Health

### Path and Datastore Status

```bash
# List all storage paths — dead paths require immediate attention
esxcli storage core path list | grep -E "State|Name" | grep -B1 -i dead

# Rescan storage adapters (if paths are stale)
esxcli storage core adapter rescan --all

# VMFS datastore health — check for ATS heartbeat errors
esxcli storage vmfs extent list

# Check datastore capacity (alert if < 20% free)
esxcli storage filesystem list | awk '{print $1, $4, $5}'
```

### APD/PDL Detection

```bash
# Check vmkernel log for APD/PDL events in last 24 hours
grep -iE "APD|PDL|LostDevice" /var/log/vmkernel.log | tail -20

# Check for SCSI sense codes (reservation conflicts, path errors)
grep -i "H:0x0 D:0x2\|reservation" /var/log/vmkernel.log | tail -20
```

## Capacity and Performance

### CPU and Memory

```bash
# Host CPU and memory usage via esxtop (batch mode, 1 sample)
esxtop -b -n 1 | head -30

# Via PowerCLI — all hosts in cluster
Get-VMHost | Select-Object Name, CpuUsageMhz, CpuTotalMhz, MemoryUsageGB, MemoryTotalGB |
  Format-Table -AutoSize

# Check for balloon/swap activity across all VMs on host
Get-VM | Get-Stat -Stat mem.balloon.average,mem.swapped.average -MaxSamples 1 |
  Where-Object {$_.Value -gt 0} | Select-Object Entity, MetricId, Value
```

| Metric | Alert threshold | Action |
|---|---|---|
| Host CPU utilization | > 70% sustained (5 min avg) | Migrate VMs via DRS, add capacity |
| Host memory utilization | > 80% | Check balloon/swap; migrate or add RAM |
| VM balloon > 0 | Any VM ballooning | Host under memory pressure; migrate VM |
| VM swap > 0 | Any VM swapping | Critical — immediate VM migration needed |
| Datastore free space | < 20% | Extend datastore or migrate VMs |

## VIB and Patch Compliance

```bash
# List all installed VIBs with version
esxcli software vib list

# Compare against baseline (requires vCenter with vLCM or VUM)
# vCenter → Lifecycle Manager → Hosts → select host → Check Compliance

# Check acceptance level (should be PartnerSupported or higher for production)
esxcli software acceptance get

# Check for any VIBs installed outside of vLCM baseline
esxcli software vib list | grep -v "VMware\|Broadcom\|Dell\|HPE\|Cisco"
```

## Health Checklist

- [ ] All hosts Connected and PoweredOn in vCenter
- [ ] No hardware health warnings or critical sensor alerts
- [ ] All storage paths active — no dead paths (`grep -i dead` returns empty)
- [ ] All vmnic uplinks connected and running at expected speed
- [ ] NTP running and synchronized (`esxcli system ntp get` shows enabled=true, server reachable)
- [ ] No APD/PDL events in vmkernel.log in past 24 hours
- [ ] hostd, vpxa, fdm services all running
- [ ] Host CPU utilization < 70% sustained
- [ ] Host memory utilization < 80%; no VM balloon or swap
- [ ] All datastores > 20% free space
- [ ] No unexpected maintenance mode hosts
- [ ] VIB compliance matches vLCM baseline (no patch drift)
