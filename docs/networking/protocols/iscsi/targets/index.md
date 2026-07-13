---
tags:
  - networking
description: "An iSCSI target is the storage-side endpoint — a port on an array, NAS gateway, or software target — that presents LUNs to initiators."
---
# iSCSI Targets

<div class="kb-summary">
An iSCSI target is the storage-side endpoint — a port on an array, NAS gateway, or software target — that presents LUNs to initiators.
</div>

        iSCSI TARGET STRUCTURE

```d2
direction: down

target_address_format: "Target Address Format" {shape: rectangle}
target_portal_groups: "Target Portal Groups" {shape: rectangle}
discovery_methods: "Discovery Methods" {shape: rectangle}
host_initiator_group_mapping: "Host / Initiator Group Mapping" {shape: rectangle}
verifying_target_connectivity: "Verifying Target Connectivity" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}

target_address_format -> target_portal_groups: uses
target_portal_groups -> discovery_methods: uses
discovery_methods -> host_initiator_group_mapping: uses
host_initiator_group_mapping -> verifying_target_connectivity: uses
verifying_target_connectivity -> common_issues: uses
```

## Target Address Format

```text
iqn.2020-01.com.purestorage:flasharray-m70-ct0   (target IQN)
192.168.10.10:3260                                 (portal — IP:port)
```

TCP port 3260 is the standard iSCSI port.

## Target Portal Groups

A **Target Portal Group (TPG)** is a set of IP addresses (portals) through which a target is reachable. Arrays typically present multiple portals for load distribution and redundancy.

```bash
# Linux — show discovered targets and their portals
iscsiadm -m node -o show

# Show all portal addresses for a discovered target
iscsiadm -m node --targetname <IQN> -o show | grep portal
```


```text title="Expected output"
Node [192.168.1.100:3260,1 iqn.2020-04.com.example:storage.disk1.sys1] {
	iface.iscsi_ifacename = default
	iface.net_ifacename = <empty>
	iface.ipaddress = <empty>
	iface.hwaddress = <empty>
	iface.transport_name = tcp
	iface.initiator_name = iqn.1993-08.org.debian:01.a1b2c3d4e5f6
	iface.state = <empty>
	node.name = iqn.2020-04.com.example:storage.disk1.sys1
	node.tpgt = 1
	node.startup = manual
	node.leading_login = No
	node.session.auth.authmethod = None
	node.conn[0].address = 192.168.1.100
	node.conn[0].port = 3260
	node.conn[0].startup = manual
}
Node [192.168.1.101:3260,2 iqn.2020-04.com.example:storage.disk2.sys1] {
	node.conn[0].address = 192.168.1.101
	node.conn[0].port = 3260
	node.conn[0].startup = manual
}

portal.address = 192.168.1.100
portal.port = 3260
portal.address = 192.168.1.101
portal.port = 3260
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `iscsiadm: No records found` | Run `iscsiadm -m discovery -t st -p <portal_ip>` to discover targets before querying nodes. |
    | `iscsiadm: Invalid IQN format` | Verify the target IQN syntax matches `iqn.YYYY-MM.reverse.domain:identifier` and use quotes if it contains special characters. |
## Discovery Methods

| Method | How it works | Use case |
|---|---|---|
| **SendTargets** | Initiator queries a portal; portal returns all targets | Most common — use for dedicated storage networks |
| **iSNS** | Central iSNS server registers and serves target info | Large environments with many targets |
| **Static** | Targets entered manually | Simple/lab environments |

```bash
# Linux — SendTargets discovery
iscsiadm -m discovery -t sendtargets -p <target-ip>:3260

# Linux — list discovered targets
iscsiadm -m node

# Linux — remove stale target record
iscsiadm -m node -o delete -T <IQN> -p <ip>:3260
```


```text title="Expected output"
# Linux — SendTargets discovery
iscsiadm -m discovery -t sendtargets -p 192.168.1.50:3260
192.168.1.50:3260,1 iqn.2019-05.com.example:storage.disk1
192.168.1.50:3260,1 iqn.2019-05.com.example:storage.disk2

# Linux — list discovered targets
iscsiadm -m node
192.168.1.50:3260,1 iqn.2019-05.com.example:storage.disk1
192.168.1.50:3260,1 iqn.2019-05.com.example:storage.disk2
192.168.1.51:3260,1 iqn.2019-05.com.example:storage.disk3

# Linux — remove stale target record
iscsiadm -m node -o delete -T iqn.2019-05.com.example:storage.disk3 -p 192.168.1.51:3260
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `iscsiadm: cannot connect to discovery address 192.168.1.50:3260` | Verify the target IP is reachable and the iSCSI daemon (iscsid) is running with `systemctl status iscsid`. |
    | `iscsiadm: No records found` | Run discovery first with the sendtargets command before attempting to list or delete nodes. |
    | `iscsiadm: Error: cannot find record for node` | Ensure the IQN and IP:port combination exactly match an existing record; verify with `iscsiadm -m node` first. |
## Host / Initiator Group Mapping

All storage arrays require the initiator IQN to be registered in a host or initiator group before a LUN is visible:

| Array | Where to configure |
|---|---|
| Pure FlashArray | Storage → Hosts → Add Host (iSCSI IQN) |
| NetApp ONTAP | `igroup create -protocol iscsi -ostype vmware` |
| Dell PowerStore | Hosts → Create Host → iSCSI Initiators |
| Dell Unity | Hosts → Create Host → iSCSI Initiators |

## Verifying Target Connectivity

```bash
# Check target portal is reachable (TCP handshake)
nc -zv <target-ip> 3260

# Discover targets
iscsiadm -m discovery -t sendtargets -p <target-ip>

# Show active sessions to a target
iscsiadm -m session -P 3 | grep -A10 <IQN>
```


```text title="Expected output"
Connection to 192.168.1.50 3260 port [tcp/iscsi] succeeded!
Target: iqn.2024-01.com.storage:target.disk1
	Current Portal: 192.168.1.50:3260,1
	Persistent Portal: 192.168.1.50:3260,1

iSCSI Transport: tcp
Initiator Name: iqn.1993-08.org.debian:01.a1b2c3d4e5f6
Initiator Alias: debian-host-01
...
	Attached scsi disk sdb	State: running
	Current Portal: 192.168.1.50:3260,1
	Persistent Portal: 192.168.1.50:3260,1
	Iface Name: default
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nc: connect to 192.168.1.50 port 3260 (tcp) failed: Connection refused` | Verify the iSCSI target service is running on the target server with `systemctl status iscsid` and check firewall rules allow port 3260. |
    | `iscsiadm: No records found` | Ensure the target IP is correct, the target portal is listening, and run `iscsiadm -m discovery -t sendtargets -p <target-ip>` to refresh discovery records. |
    | `iscsiadm: No active sessions` | Log in to the target first using `iscsiadm -m node -T <IQN> -p <target-ip> --login` before querying session details. |
## Common Issues

| Symptom | Cause | Action |
|---|---|---|
| No targets returned from discovery | Wrong portal IP or TCP 3260 blocked | `nc -zv <ip> 3260` — check firewall |
| Target visible but LUN not seen | Initiator IQN not in host group | Add IQN to storage host/initiator group |
| Target disappears after reboot | Non-persistent login | Use `iscsiadm -m node -l -o automatic` |
| Multiple targets seen unexpectedly | iSNS or SendTargets returning unrelated targets | Scope discovery to dedicated storage VLAN |
