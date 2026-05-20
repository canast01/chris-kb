# VxRail — Troubleshooting

<div class="kb-summary">
Troubleshooting guide for VxRail in the VMware product context. Covers VxRail plugin unavailability, LCM pre-check failures, vSAN degraded states, and node rejoin procedures.
</div>

```
┌────────────────────────────────────── VxRail — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          VxRail plugin unavailable in vCenter; LCM pre-check failure blocking upgrade         │   │
│   │              vSAN object degraded or resync stuck; iDRAC hardware alert on a node             │   │
│   │  Node not rejoining cluster after maintenance; network mismatch causing VxRail Manager issues │   │
│   │        Diagnostics: VxRail API debug, LCM logs, vSAN health UI, iDRAC system event log        │   │
│   │    Escalation: support bundle export, Dell GSS P1, TAM contact, log archive for ProSupport    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define triage path · diagnostics isolate root cause · escalation engages Dell support│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │        Plugin unavail       │  │       VxRail API debug      │  │         VxRail bndl         │   │
│   │       LCM pre-chk fail      │  │        LCM log files        │  │      Dell support case      │   │
│   │        vSAN degraded        │  │        vSAN health UI       │  │        GSS escalation       │   │
│   │         iDRAC alert         │  │       iDRAC sys event       │  │         TAM contact         │   │
│   │       Node not rejoin       │  │       get-tech-support      │  │       P1 Dell ProSupp       │   │
│   │         Net mismatch        │  │       vm-support bndl       │  │         Log archive         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics pinpoint root cause · escalation gets Dell support engaged│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │  Plugin unavail  │  VxRail API dbg  │  VxRail Mgr logs  │  Bundle export   │  Restart VxRail  │   │
│   │ LCM pre-chk fail │  LCM log files   │  /var/log/vmware  │   Dell support   │   Fix + retry    │   │
│   │  vSAN degraded   │  vSAN health UI  │   /var/log/vsan   │   GSS P1 case    │   Replace disk   │   │
│   │ Node not rejoin  │  iDRAC sys evt   │     iDRAC /log    │   TAM contact    │   Re-add node    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · NVMe/SSD/HDD · iDRAC OOB · 25GbE NICs · ToR switches                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VxRail plugin     = vCenter plugin provided by VxRail Manager; shows cluster health and LCM status   │
│  LCM pre-check     = Validation run before upgrade; fails if vSAN resync, network, or health issues   │
│  vSAN object health = vSAN tracks each VM object; degraded = FTT violated; resync = rebuilding copies │
│  iDRAC SEL         = System Event Log on iDRAC; hardware faults (disk, PSU, fan, NIC) recorded here   │
│  get-tech-support  = VxRail CLI command collecting full diagnostic bundle for Dell GSS cases          │
│  Support bundle    = Compressed log archive from VxRail Manager, ESXi hosts, and iDRAC for escalation │
│  TAM               = Technical Account Manager; Dell named support contact for critical escalations   │
│  Dell ProSupport   = Dell premium support tier; P1 = production down, response in under 4 hours       │
│  Node rejoin       = Process of ESXi host re-entering vSAN cluster after maintenance or failure       │
│  Network mismatch  = VLAN or MTU misconfiguration preventing VxRail Manager from reaching ESXi hosts  │
│  VxRail Mgr restart = Restarting Mystic service on VxRail Manager VM to recover plugin or API issues  │
│  GSS escalation    = Global Support Services; Dell/VMware support organisation for P1/P2 incidents    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Quick Reference

| Symptom | First Check | Action |
|---|---|---|
| VxRail Plugin not loading in vCenter | VxRail Manager VM running? | SSH to VxRail Manager; check services |
| Node shows Offline in VxRail Plugin | iDRAC connectivity? | `ping <idrac-ip>` from VxRail Manager |
| LCM upgrade stuck | VxRail Manager logs | Check `/var/log/mystic/` and vCenter tasks |
| vSAN health warning | Specific check failing | Review per-check in vCenter → Monitor → vSAN → Health |
| vSAN object degraded | Component on failed disk/host | Check disk group health; replace failed disk |
| Node won't join cluster during expansion | Network config mismatch | Verify VLAN tagging and IP addressing on new node |
| iDRAC hardware alarm | Hardware fault | Review iDRAC SEL; identify failed component |
| vSAN resync not completing | Cluster capacity, network | Check capacity utilisation; verify vSAN network MTU |

---

## Incident Triage

Work through this triage sequence for any VxRail cluster issue:

1. **Check VxRail Plugin** — Is the plugin loading? Is the cluster health red/yellow?
2. **Check vSAN health** — vCenter → Cluster → Monitor → vSAN → Health. Identify which specific checks are failing.
3. **Check node status** — All nodes Online? Any in maintenance mode unexpectedly?
4. **Check vCenter tasks and events** — Recent tasks pane; any failed tasks related to VxRail?
5. **Check VxRail Manager logs** — SSH to VxRail Manager VM; review service logs
6. **Check iDRAC hardware health** — VxRail Plugin → Hardware, or directly via iDRAC UI
7. **Check ESXi host alarms** — Any hardware health or storage path alarms on hosts?
8. **Check vSAN resync** — Any active resyncing? Resync can take hours after a node or disk returns.

```bash
# Quick triage commands from any ESXi host in the cluster
esxcli vsan health cluster get | grep -v "Green"
esxcli vsan debug resync list | head -20
esxcli vsan storage list | grep -E "Disk Group|Is Capacity|Device:"
esxcli storage core path list | grep -c "State: dead"
```

---

## VxRail Manager Service Issues

### VxRail Manager VM Not Responding

```bash
# SSH to VxRail Manager VM
ssh mystic@<vxrail-manager-ip>

# Check all VxRail services
systemctl list-units --state=failed
systemctl status mystic-server    # Main VxRail Manager service
systemctl status mystic-mariadb   # Database backend
systemctl status mystic-rabbitmq  # Message queue

# Restart the VxRail Manager service
sudo systemctl restart mystic-server

# Check logs
sudo journalctl -u mystic-server -n 100 --no-pager
sudo tail -500 /var/log/mystic/mystic.log
```

### VxRail Plugin Not Loading in vCenter

1. Verify the VxRail Manager VM is powered on and reachable from vCenter
2. SSH to VxRail Manager and check services (above)
3. In vCenter: **Administration → Client Plugins** — verify the VxRail plugin is enabled and not in an error state
4. If the plugin is in error state, re-register it:
   - SSH to VxRail Manager
   - Run the plugin registration script (location varies by version — check Dell documentation for the VxRail version)

### Re-register vCenter Credentials in VxRail Manager

If VxRail Manager loses its connection to vCenter (e.g., after vCenter password change):

**VxRail Plugin → System → vCenter Credentials → Update**

Or via API:

```bash
curl -sk -X PUT \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "vc_admin_user": {
      "username": "administrator@vsphere.local",
      "password": "vCenterPassword!"
    }
  }' \
  "https://<vxrail-manager-ip>/rest/vxm/v1/system/initialize/vcenter"
```

---

## LCM Upgrade Issues

### LCM Stuck or Failed

```bash
# SSH to VxRail Manager — check LCM logs
sudo tail -200 /var/log/mystic/lcm.log | grep -i "error\|fail\|exception"

# Check the upgrade status via API
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/lcm/upgrade" | python3 -m json.tool
```

### Common LCM Failure Points

| Failure | Likely Cause | Resolution |
|---|---|---|
| Pre-check fails: vSAN health | vSAN health not green | Resolve vSAN health issues before retrying |
| Pre-check fails: resync active | vSAN resyncing in progress | Wait for resync to complete |
| Node firmware update fails | iDRAC connectivity lost | Check iDRAC IP; restart iDRAC |
| ESXi VIB install fails | VIB acceptance level mismatch | Check `esxcli software acceptance get` on node |
| vCenter upgrade fails | VAMI access issue | Verify vCenter VAMI at port 5480 is accessible |
| Upgrade hangs at maintenance mode | DRS not migrating VMs | Verify DRS is Fully Automated; check for DRS rules blocking migration |

### Resume a Failed LCM Upgrade

LCM upgrades can often be retried after fixing the root cause:

**VxRail Plugin → LCM → Resume Upgrade**

If resume fails repeatedly, open a Dell support case — do not attempt to manually upgrade ESXi or firmware on VxRail nodes.

---

## vSAN Issues

### vSAN Health Checks — Common Failures

| Health Check | Failure Meaning | Resolution |
|---|---|---|
| vSAN Build Recommendation | Component versions don't match | Run LCM upgrade |
| vSAN Disk Balance | Disks heavily unbalanced | Trigger vSAN rebalance |
| MTU Check | Jumbo frames not end-to-end | Verify physical switch MTU 9000 on vSAN ports |
| vSAN Network Connectivity | Node cannot reach peers on vSAN network | Check vSAN vmkernel IP; verify network |
| Capacity — Space Utilisation > 70% | Cluster filling up | Add nodes or reduce VM footprint |
| Component State | One or more components degraded/absent | Check disk health; replace failed disk |

### vSAN MTU Verification

```bash
# Test jumbo frames between nodes on vSAN network
vmkping -I vmk2 -d -s 8972 <remote-node-vsan-vmkernel-ip>
# -d = don't fragment, -s 8972 = 9000 MTU payload

# If ping fails: check physical switch MTU on vSAN-facing ports
# Switch port MTU must be 9000 or higher
```

### vSAN Network Connectivity Failure

```bash
# Verify vSAN vmkernel is on the correct port group
esxcli network ip interface list | grep vmk

# Ping the vSAN vmkernel IPs of all other nodes
# From node 1:
vmkping -I vmk2 <node2-vsan-vmk-ip>
vmkping -I vmk2 <node3-vsan-vmk-ip>

# Check vSAN network test tool
esxcli vsan debug network test
```

### Degraded vSAN Object Recovery

If a vSAN object shows `Degraded` (reduced redundancy, still accessible):

1. Identify the affected disk or node
2. vSAN will automatically rebuild onto other nodes/disks as long as capacity exists
3. Monitor resync: `esxcli vsan debug resync list`
4. If the cause is a failed disk, replace it and add the replacement to the disk group

If an object shows `Absent` (offline, inaccessible):

1. Check if the hosting node is powered off or in maintenance mode
2. Return the node to service — vSAN will rehydrate the absent components
3. If the node is lost permanently, remove it and vSAN rebuilds from remaining copies (requires FTT ≥ 1 on the policy)

### vSAN Capacity Issue

```bash
# Check current capacity utilisation
esxcli vsan storage stats get

# Identify which VMs are using the most space
Get-VM | Sort-Object {$_.UsedSpaceGB} -Descending | Select-Object -First 10 Name, UsedSpaceGB, ProvisionedSpaceGB

# Check for snapshot accumulation (large deltas consuming vSAN space)
Get-VM | Get-Snapshot | Select-Object VM, Name, Created, SizeGB | Sort-Object SizeGB -Descending
```

---

## Node Issues

### Node Shows Offline in VxRail Plugin

```bash
# 1. Can you reach the node's iDRAC?
ping <node-idrac-ip>
# If no: check OOB network; check node is powered on

# 2. Can you reach the node's ESXi management IP?
ping <node-mgmt-vmk0-ip>

# 3. SSH to VxRail Manager and check node status via API
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/hosts" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for h in d:
    print(f'{h.get(\"sn\",\"?\")}  {h.get(\"slot\",\"?\")}  state={h.get(\"operational_status\",\"?\")}  health={h.get(\"health\",\"?\")}')
"
```

### Node Hardware Alarm

```bash
# Check iDRAC system event log
# SSH to iDRAC:
ssh root@<node-idrac-ip>
racadm getsel | tail -30

# Check sensors
racadm getsysinfo | grep -i "fault\|warning\|critical"

# From VxRail Plugin: Hardware → select node → Hardware Health
```

Hardware alarms are also visible in vCenter if the iDRAC integration is working — vCenter host → Monitor → Hardware.

---

## Log Collection

### VxRail Manager Logs

```bash
# SSH to VxRail Manager
ssh mystic@<vxrail-manager-ip>

# Main service log
sudo tail -500 /var/log/mystic/mystic.log

# LCM log
sudo tail -500 /var/log/mystic/lcm.log

# API access log
sudo tail -200 /var/log/mystic/access.log

# List all log files
sudo ls -lh /var/log/mystic/
```

### ESXi Host Logs

```bash
# SSH to affected ESXi host
# vSAN-related
tail -100 /var/log/vmkernel.log | grep -i "vsan\|LSOM\|DOM"

# Storage path issues
tail -100 /var/log/vmkernel.log | grep -i "APD\|PDL\|NMP\|path"

# Host management
tail -100 /var/log/hostd.log | grep -i "error\|fail"

# Collect full support bundle
vm-support -n -w /tmp/
```

### Dell VxRail Support Bundle

For Dell support cases, generate the VxRail support bundle:

**VxRail Plugin → Support → Generate Support Bundle**

Or via API:

```bash
curl -sk -X POST \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxrail-manager-ip>/rest/vxm/v1/support/bundle"
# Returns a job ID; poll job status, then download the bundle
```

The bundle includes VxRail Manager logs, node health data, iDRAC logs, and ESXi log excerpts.

---

## Escalation to Dell Support

Open a Dell support case at **https://www.dell.com/support/home** → My Support → Create Service Request.

**Required information:**

| Item | How to Retrieve |
|---|---|
| VxRail cluster serial number | VxRail Plugin → System → Cluster Info |
| VxRail software version | VxRail Plugin → System → Software Version |
| Node service tags (serial numbers) | VxRail Plugin → Hosts → select node → Details |
| Symptom and first occurrence | Timestamps from VxRail Manager logs and vCenter events |
| VxRail support bundle | Generated from VxRail Plugin → Support |
| ESXi support bundles | Generated via `vm-support -n -w /tmp/` on affected hosts |

Set case severity to P1 for production-impacting issues (node down, vSAN degraded with no redundancy). Dell SupportAssist may automatically create a case for critical hardware faults — check whether an automatic case exists before opening a duplicate.

**Dell Support direct lines:**

- Enterprise Support: 1-800-945-3355 (US) — have service tag ready
- VxRail-specific support escalates automatically to the VxRail engineering team if initial triage cannot resolve

For a node with a failed disk and vSAN components becoming absent, request an emergency parts dispatch (next business day or 4-hour response depending on the support contract).
