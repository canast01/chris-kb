---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
---
# Network Connectivity Issues


<div class="kb-summary">
Troubleshooting VM network connectivity failures — vSwitch/vDS configuration, portgroup VLAN mismatches, VMkernel routing, NSX segment issues, and physical uplink failures.
</div>
```text
┌────────────────────────────── Virtualization Operations Troubleshooting ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 Operations: Virtualization Operations Troubleshooting platform                │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │            Management: Virtualization Operations Troubleshooting management console           │   │
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
│    Physical: Virtualization Operations Troubleshooting infrastructure · management network · monitor  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Operations         = Virtualization Operations Troubleshooting platform overview and core concept  │
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


---
## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## vMotion Fails

**Step 1 — Check the VMkernel adapter tagged for vMotion:**

```bash
# From ESXi — verify VMkernel adapters and their tags
esxcli network ip interface list
esxcli network ip interface tag get -i vmk1  # vmk1 is typically the vMotion vmk

# Check vMotion is enabled on the vmk
esxcli network ip interface list | grep -A5 vmk1
```

**Step 2 — Verify MTU consistency** — vMotion requires jumbo frames (MTU 9000) if configured; a mismatch between the VMkernel adapter, vSwitch, and physical switch will cause failures:

```bash
# Check VMkernel MTU
esxcli network ip interface list | grep -E "Name|MTU"

# Test vMotion network reachability with correct MTU
vmkping -I vmk1 -d -s 8972 <destination-esxi-vmotion-ip>
# -d = don't fragment, -s 8972 = payload size (8972 + 28 byte header = 9000 MTU)
```

**Step 3 — Check error details in vCenter Tasks:**

- "The migration was not attempted because no valid network is available" → No vMotion vmk on the destination
- "The host is not licensed for vMotion" → Check host licensing
- "EVC mismatch" → CPU feature compatibility; EVC cluster mode may need updating
- "The VM is using a device or file that is not accessible on the target host" → Local VMDK, local ISO, or CD-ROM still attached

---

## VM Network Outage

**Step 1 — Confirm the VM can ping its gateway** from inside the guest. If not, check the virtual NIC is still connected:

```powershell
# PowerCLI — check VM network adapter connection state
Get-VM "VMName" | Get-NetworkAdapter | Select Name, NetworkName, ConnectionState
```

**Step 2 — Check the port group:**

```bash
# From ESXi — list port groups and VLAN IDs
esxcli network vswitch standard portgroup list
esxcli network vswitch dvs vmware portgroup list  # For distributed vSwitch
```

Confirm the port group VLAN ID matches the upstream switch configuration. A recent switch-side VLAN change will strand all VMs on that port group.

**Step 3 — Check physical uplinks:**

```bash
# Check vmnic link state
esxcli network nic list | grep -E "Name|Link"

# Check which vmnics back the vSwitch
esxcli network vswitch standard list
```

**Step 4 — Check NIC teaming policy** — if an uplink failed and the teaming policy does not failover correctly:

```bash
esxcli network vswitch standard policy failover get -v vSwitch0
```

---

## Host Management Network Issue

If the host management network goes down, vCenter loses the host and SSH stops working.

**Recovery path using DCUI (Direct Console User Interface):**

1. Connect to iDRAC/iLO virtual console → open host console.
2. Press F2 to enter DCUI.
3. Go to **Configure Management Network** → verify IP, subnet, gateway, DNS.
4. Press **Escape** and select "Test Management Network" — this runs ping and DNS tests from the host.
5. If the configuration was changed, confirm the management VLAN setting on the physical switch port.

```bash
# Once SSH access is restored — verify management vmk
esxcli network ip interface ipv4 get -i vmk0
esxcli network ip route list
```

---

## NSX Issues

| Symptom | Check |
|---|---|
| VMs on NSX segments cannot communicate | TEP (Tunnel Endpoint) connectivity; VTEP MTU |
| Edge gateway unreachable | Edge node health; BGP peering state |
| Distributed firewall blocking unexpected traffic | DFW rule order; service tag definitions |
| Transport node status red in NSX Manager | Host preparation state; NSX agent on the ESXi host |

```bash
# From ESXi — check NSX VTEP interface
esxcli network ip interface list | grep vmk

# Check TEP ping between two hosts
vmkping -I vmk10 -d -s 1572 <remote-tep-ip>

# Check NSX agent status on ESXi host
/etc/init.d/nsx-opsagent status
/etc/init.d/nsx-mpa status
```

From NSX Manager UI:
- System → Fabric → Hosts — check each transport node status
- System → Fabric → Edges — check edge node status and tunnel state
- Networking → Tier-0 Gateways → check BGP neighbor state

---

## Packet Loss on a VM or Host

```bash
# From ESXi — check vmnic error counters
esxcli network nic stats get -n vmnic0
# Look for: rx_errors, tx_errors, rx_dropped, tx_dropped

# Check for CRC errors on physical switch port (from switch CLI)
# Cisco: show interface GigabitEthernetX/X counters errors

# Test with vmkping to rule out congestion vs physical errors
vmkping -I vmk0 -c 100 <destination-ip>
```

Common causes:

| Cause | Indicator | Fix |
|---|---|---|
| Duplex mismatch | Incrementing rx/tx errors on vmnic | Force speed/duplex on switch port to match NIC; or set both to auto |
| MTU mismatch | Large packets dropped silently | Set MTU consistently end-to-end |
| Physical cable / transceiver | CRC errors on switch | Reseat or replace cable/SFP |
| NIC teaming imbalance | One vmnic handling all traffic | Review load balancing policy (Route Based on IP hash requires LACP) |
| Congestion on shared path | High latency and drops under load | Check QoS settings; consider storage traffic isolation to a separate vmnic |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
