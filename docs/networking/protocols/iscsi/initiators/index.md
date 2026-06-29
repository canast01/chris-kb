---
tags:
  - networking
---
# iSCSI Initiators

<div class="kb-summary">
An iSCSI initiator is the client-side component — typically software on a server OS or a hardware iSCSI HBA — that sends SCSI commands over an IP network to iSCSI targets.
</div>

## IQN Format

![iSCSI Initiators — Diagram](../../../../assets/networking-protocols-iscsi-initiators-diagram.svg)

## Linux Software Initiator (open-iscsi)

```bash
# Install
dnf install iscsi-initiator-utils      # RHEL/Rocky
apt install open-iscsi                 # Ubuntu

# Find your initiator IQN
cat /etc/iscsi/initiatorname.iscsi

# Set a custom IQN (edit file, then restart)
echo "InitiatorName=iqn.2024-01.com.example:server01" > /etc/iscsi/initiatorname.iscsi
systemctl restart iscsid

# Configure CHAP (optional, in /etc/iscsi/iscsid.conf)
node.session.auth.authmethod = CHAP
node.session.auth.username = <initiator-username>
node.session.auth.password = <initiator-password>

# Start and enable daemon
systemctl enable --now iscsid
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Wed Jan 10 14:22:15 2024.
Dependencies resolved.
================================================================================
 Package                    Arch       Version              Repository    Size
================================================================================
Installing:
 iscsi-initiator-utils      x86_64     6.2.1.4-15.el9       appstream    420 kB

Transaction Summary
================================================================================
Install  1 Package

Total download size: 420 kB
Installed size: 1.2 MB
Is this ok? [y/N]: y
Downloading Packages:
iscsi-initiator-utils-6.2.1.4-15.el9.x86_64.rpm          100% |====| 420 kB
Running transaction
  Preparing        :                                                        1/1
  Installing       : iscsi-initiator-utils-6.2.1.4-15.el9.x86_64           1/1
  Verifying        : iscsi-initiator-utils-6.2.1.4-15.el9.x86_64           1/1

Installed:
  iscsi-initiator-utils-6.2.1.4-15.el9.x86_64

Complete!
## DO NOT EDIT OR REMOVE THE FOLLOWING LINE
InitiatorName=iqn.2024-01.com.example:server01
(no output — command completes silently)
Created symlink /etc/systemd/system/multi-user.target.wants/iscsid.service → /usr/lib/systemd/system/iscsid.service.
```

!!! warning "Common errors"
    **`cat: /etc/iscsi/initiatorname.iscsi: No such file or directory`** — Install iscsi-initiator-utils or open-iscsi first before attempting to read the initiator configuration file.
    **`Failed to restart iscsid.service: Unit iscsid.service not found.`** — Ensure the iSCSI package is fully installed and the systemd daemon is reloaded with `systemctl daemon-reload`.
## Windows iSCSI Initiator

```powershell
# Enable initiator service
Start-Service MSiSCSI
Set-Service MSiSCSI -StartupType Automatic

# View initiator IQN
(Get-WmiObject -Namespace root\wmi -Class MSiSCSIInitiator_MethodClass).iSCSINodeName

# Discover targets
iscsicli ListTargets
iscsicli AddTargetPortal <target-ip>
iscsicli QAddTargetPortal <target-ip>

# Connect to a target
iscsicli PersistentLoginTarget <IQN> <...>
```

## VMware ESXi Software iSCSI

```bash
# Enable software iSCSI adapter
esxcli iscsi software set --enabled=true

# Get initiator IQN
esxcli iscsi adapter list

# Add target portal (send target discovery)
esxcli iscsi adapter discovery sendtarget add \
  --adapter vmhba65 --address <target-ip>

# Rescan
esxcli storage core adapter rescan --adapter vmhba65
```


```text title="Expected output"
(no output — command completes silently)

Adapter  Driver     State   Type  Model
-------  ---------  ------  ----  -----
vmhba65  iscsi_vmk  online  iscsi iSCSI Software Adapter

iSCSI Initiator IQN: iqn.1998-01.com.vmware:esx-prod-01-12345678

(no output — command completes silently)

Rescan of adapter vmhba65 completed successfully.
```

!!! warning "Common errors"
    **`Error: Unknown option --enabled=true`** — Use `--enabled true` (space-separated, not equals sign) in older ESXi versions.
    **`Error: Discovery address already exists`** — Remove the duplicate target portal first with `esxcli iscsi adapter discovery sendtarget remove --adapter vmhba65 --address <target-ip>`.
    **`Error: Could not find adapter vmhba65`** — Verify the adapter name with `esxcli iscsi adapter list` and use the correct vmhba identifier.
## Initiator Standards

- One initiator IQN per HBA port — do not share IQNs across hosts
- Register initiator IQNs in CMDB at provisioning time
- Use CHAP in environments where iSCSI traverses shared networks
- Bind software initiators to dedicated storage NICs — never use management interfaces

## Common Issues

| Symptom | Cause | Check |
|---|---|---|
| Initiator not seen by array | Discovery not run or wrong target IP | Run `iscsiadm -m discovery` |
| CHAP authentication failure | Mismatched credentials | Compare username/password on initiator and target |
| Session drops | MTU mismatch or jumbo frames not end-to-end | Verify MTU on NIC, switch, and storage port |
| IQN rejected by array | IQN not added to host group | Add IQN to storage host group / initiator group |
