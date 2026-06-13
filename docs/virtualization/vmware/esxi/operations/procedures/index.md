---
tags:
  - esxi
  - operations
  - vmware
  - vsphere-8
---
# ESXi — Procedures


<div class="kb-summary">
Procedures reference covering Change Readiness, Maintenance Window, Post-Change Validation, Incident Triage, Networking, Storage, Security and Hardening, and Lifecycle and Patching.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌───────────────────────────────────── ESXi — Standard Procedures ──────────────────────────────────────┐
│                                                                                                       │
│  Maintenance mode, change control, and host decommission standard procedures.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Maintenance Mode Procedure          │  │              Change Management              │   │
│   │          Drain VMs via vMotion/DRS           │  │          Raise change request (CR)          │   │
│   │        Enter maintenance: vCenter UI         │  │          Pre-change health snapshot         │   │
│   │        esxcli system maintenanceMode         │  │          Maintenance window agreed          │   │
│   │         Verify no VMs remain on host         │  │            Post-change validation           │   │
│   │        Perform task, exit maintenance        │  │            Close CR with evidence           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Maintenance mode drains VMs; change control wraps every host-level change.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Host Decommission               │  │             Emergency Procedures            │   │
│   │           Migrate all VMs off host           │  │           Force maintenance if HA           │   │
│   │         Remove from vSAN disk group          │  │          PSOD: capture vmkernel log         │   │
│   │           Disconnect from vCenter            │  │          Isolate host from network          │   │
│   │             Remove from cluster              │  │            Power off affected VMs           │   │
│   │           Deregister from vCenter            │  │            Escalate to VMware GSS           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 host, iDRAC/IPMI for OOB control, management network, vCenter appliance                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Maintenance mode = host state; vCenter stops VM placement; drains existing                           │
│  vMotion     = live VM migration; used to drain host before maintenance                               │
│  PSOD        = Purple Screen Of Death; ESXi kernel panic / crash dump                                 │
│  CR          = Change Request; ITSM ticket authorising planned changes                                │
│  DRS         = Distributed Resource Scheduler; auto-migrates VMs                                      │
│  HA          = High Availability; restarts VMs on remaining hosts                                     │
│  Decommission= formal process to remove host from inventory and cluster                               │
│  iDRAC       = Dell OOB management; power control when host unresponsive                              │
│  vmkernel log= /var/log/vmkernel.log; primary diagnostic log on ESXi                                  │
│  vSAN evac   = removes host disks from vSAN before decommission                                       │
│  Force maint = maintenance without VM evacuation; HA failure scenario only                            │
│  Health snap = pre/post change comparison of alarms/metrics/log tail                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Change Readiness

- [ ] vMotion tested and working between affected hosts before any maintenance
- [ ] Host not in maintenance mode — no other concurrent work on same host
- [ ] HA admission control checked: cluster has capacity to tolerate host loss
- [ ] All storage paths healthy and no dead paths: `esxcli storage core path list | grep dead`
- [ ] vCenter backup is current (file-based backup or VAMI snapshot taken recently)
- [ ] DRS is enabled and configured to fully automated — VMs will migrate automatically
- [ ] Change window approved and communicated; storage and compute teams notified

| Item | Status | Notes |
|---|---|---|
| vMotion tested | | Test migration successful |
| HA admission control OK | | Cluster has failover capacity |
| Storage paths healthy | | `grep dead` returns 0 |
| vCenter backup current | | Backup timestamp |
| Change window approved | | Ticket reference |

## Maintenance Window

1. Confirm host is healthy and not already in maintenance mode: `Get-VMHost | Select Name,ConnectionState`
2. Check HA admission control — ensure cluster can tolerate one less host during maintenance
3. Put host into maintenance mode: `Set-VMHost -VMHost <hostname> -State Maintenance`
4. Wait for all VMs to vMotion off the host — monitor via vCenter Tasks pane
5. Confirm zero VMs running on the host: `Get-VM -Location <host> | Where-Object {$_.PowerState -eq "PoweredOn"}`
6. Perform the required maintenance work (patching, hardware replacement, config change)
7. Exit maintenance mode: `Set-VMHost -VMHost <hostname> -State Connected`
8. Validate host is Connected, all storage paths active, NTP in sync, and VMs have migrated back

## Post-Change Validation

- [ ] Host shows Connected and PoweredOn in vCenter
- [ ] No hardware health alarms triggered: `esxcli hardware health get`
- [ ] All storage paths active, no dead paths: `esxcli storage core path list | grep dead`
- [ ] All vmnic uplinks connected: `esxcli network nic list`
- [ ] VMs running correctly on the host or successfully migrated back
- [ ] NTP synchronized: `esxcli system ntp get` confirms `Running: true`
- [ ] No new vCenter alarms or vmkernel errors introduced by the change
- [ ] Close change ticket with validation evidence attached

## Incident Triage

- [ ] Check host connection state in vCenter — Connected, Disconnected, or Not Responding?
- [ ] Run `esxcli hardware health get` — identify any hardware component in Warning or Error state
- [ ] Check storage paths: `esxcli storage core path list | grep dead`
- [ ] Check network uplinks: `esxcli network nic list` — look for down links
- [ ] Review vmkernel log: `tail -500 /var/log/vmkernel.log`
- [ ] Check NTP status — a drifted clock can cause certificate and auth failures
- [ ] Review vCenter events for the affected host around the incident time
- [ ] If host is Not Responding, attempt IPMI/iDRAC/iLO console access

| Question | Answer |
|---|---|
| Host connection state? | Connected / Disconnected / Not Responding |
| Hardware health alerts? | `esxcli hardware health get` |
| Dead storage paths? | `esxcli storage core path list \| grep dead` |
| vmnic uplinks down? | `esxcli network nic list` |
| vmkernel.log at incident time? | `/var/log/vmkernel.log` — SCSI, NMP, network errors |

---

## Add a VMkernel Adapter (vmk)

A VMkernel adapter (vmk) carries ESXi management, vMotion, vSAN, or NFS traffic. Add a new vmk when you are separating traffic types onto dedicated VLANs or adding a second vMotion path.

**Prerequisites:** target vSwitch or dvSwitch port group already exists; IP subnet and VLAN confirmed with the network team.

1. Identify the target vSwitch and port group:

    ```bash
    esxcli network vswitch standard list
    esxcli network vswitch standard portgroup list
    ```

2. Add the VMkernel adapter with a static IP:

    ```bash
    esxcli network ip interface add --interface-name vmk1 --portgroup-name "vMotion"
    esxcli network ip interface ipv4 set --interface-name vmk1 --ipv4 192.168.10.11 --netmask 255.255.255.0 --type static
    ```

3. Enable the appropriate traffic tag (vMotion in this example):

    ```bash
    esxcli network ip interface tag add --interface-name vmk1 --tagname VMotion
    ```

    Valid tag names: `Management`, `VMotion`, `vSAN`, `faultToleranceLogging`, `vSphereReplication`.

4. Verify the adapter is up and the IP is set:

    ```bash
    esxcli network ip interface list
    esxcli network ip interface ipv4 get --interface-name vmk1
    ```

5. Test connectivity from the host to a remote vmk on the same subnet:

    ```bash
    vmkping -I vmk1 192.168.10.12
    ```

---

## Configure a vSS Port Group

A standard switch (vSS) port group defines the VLAN tag and policy that VMs or VMkernel adapters on that switch use. Add or modify port groups to extend VLAN access or change security policy without touching the uplinks.

1. List existing port groups and switches:

    ```bash
    esxcli network vswitch standard portgroup list
    ```

2. Add a new port group to the target vSwitch:

    ```bash
    esxcli network vswitch standard portgroup add --vswitch-name vSwitch0 --portgroup-name "VLAN20-App"
    ```

3. Set the VLAN ID:

    ```bash
    esxcli network vswitch standard portgroup set --portgroup-name "VLAN20-App" --vlan-id 20
    ```

4. (Optional) Override security policy on the port group:

    ```bash
    esxcli network vswitch standard portgroup policy security set \
      --portgroup-name "VLAN20-App" \
      --allow-promiscuous false \
      --allow-mac-change false \
      --allow-forged-transmits false
    ```

5. Verify the port group is visible:

    ```bash
    esxcli network vswitch standard portgroup list | grep "VLAN20-App"
    ```

---

## Change vSwitch MTU (Jumbo Frames)

Raising MTU to 9000 (jumbo frames) reduces CPU overhead for vSAN and NFS workloads. The physical switches and all vmk adapters on that vSwitch must also be set to 9000 before enabling — a mismatch causes silent packet fragmentation.

**Prerequisites:** physical switch ports already configured for MTU 9000; change window in place.

1. Check the current MTU on all vSwitches:

    ```bash
    esxcli network vswitch standard list | grep -E "Name|MTU"
    ```

2. Set the vSwitch MTU to 9000:

    ```bash
    esxcli network vswitch standard set --vswitch-name vSwitch1 --mtu 9000
    ```

3. Update each VMkernel adapter on that vSwitch to match:

    ```bash
    esxcli network ip interface set --interface-name vmk2 --mtu 9000
    ```

4. Verify the change took effect:

    ```bash
    esxcli network vswitch standard list | grep -A5 "vSwitch1"
    esxcli network ip interface list | grep -E "Name|MTU"
    ```

5. Validate end-to-end with a large-frame ping (do-not-fragment):

    ```bash
    vmkping -I vmk2 -s 8972 -d 192.168.20.12
    ```

    Packet size 8972 = 9000 − 28 bytes (IP + ICMP headers). A successful reply confirms the physical path supports jumbo frames.

---

## Rescan Storage Adapters

Run a rescan after adding new LUNs, zoning changes, or after plugging in a new HBA so ESXi discovers new devices and paths without a reboot.

1. List available storage adapters:

    ```bash
    esxcli storage core adapter list
    ```

2. Rescan all adapters (recommended — covers HBA and software iSCSI):

    ```bash
    esxcli storage core adapter rescan --all
    ```

3. To rescan a specific adapter only:

    ```bash
    esxcli storage core adapter rescan --adapter vmhba1
    ```

4. Verify new devices are visible:

    ```bash
    esxcli storage core device list | grep -E "Display Name|Size"
    ```

5. Check all paths are active:

    ```bash
    esxcli storage core path list | grep -v "active" | grep -v "^$"
    ```

    No output means all paths are active. Dead or standby paths will appear here.

---

## Mount/Unmount a Datastore

Unmount a datastore before decommissioning a LUN or performing storage maintenance. Mount to bring a new NFS share or VMFS volume into inventory.

**Unmount (VMFS or NFS):**

1. Confirm no VMs are registered on the datastore:

    ```bash
    esxcli storage filesystem list
    ```

2. Identify the datastore UUID:

    ```bash
    esxcli storage filesystem list | grep "DatastoreName"
    ```

3. Unmount the datastore:

    ```bash
    esxcli storage filesystem unmount --uuid <datastore-uuid>
    ```

**Mount an NFS datastore:**

1. Mount the NFS share:

    ```bash
    esxcli storage nfs add --host 192.168.30.10 --share /vol/nfs_ds01 --volume-name NFS_DS01
    ```

2. Verify it appears in the filesystem list:

    ```bash
    esxcli storage filesystem list | grep NFS_DS01
    ```

**Mount an existing VMFS volume (after rescan):**

After a rescan the volume usually auto-mounts. If it does not:

```bash
esxcli storage filesystem mount --uuid <datastore-uuid>
```

---

## Enable Lockdown Mode

Lockdown mode prevents direct root login to the ESXi host — all management must go through vCenter. Enable it to reduce the attack surface in production clusters.

**Note:** before enabling, ensure at least one Exception User is configured in DCUI access, and confirm vCenter is reachable and healthy. Lockdown mode cannot be toggled from the host CLI after it is enabled.

1. Enable normal lockdown mode from the DCUI or vCenter:

    - **vCenter UI path:** Host → Configure → Security Profile → Lockdown Mode → Edit → Normal
    - **PowerCLI:**

    ```powershell
    $vmhost = Get-VMHost -Name "esxi01.corp.local"
    $vmhost.ExtensionData.EnterLockdownMode()
    ```

2. Verify lockdown mode is active:

    ```powershell
    Get-VMHost -Name "esxi01.corp.local" | Select Name, @{N="Lockdown";E={$_.ExtensionData.Config.LockdownMode}}
    ```

3. To disable lockdown mode (requires vCenter access or physical DCUI access):

    ```powershell
    $vmhost.ExtensionData.ExitLockdownMode()
    ```

4. Add exception users (accounts that can still log in directly during lockdown):

    - vCenter UI path: Host → Configure → Security Profile → Lockdown Mode → Exception Users → Add

---

## Configure ESXi Firewall Rules

The ESXi firewall controls which services are reachable on the management vmk. Restrict allowed IP ranges on each service to limit exposure.

1. List all firewall rules and their current state:

    ```bash
    esxcli network firewall ruleset list
    ```

2. Enable a specific ruleset (e.g., syslog outbound):

    ```bash
    esxcli network firewall ruleset set --ruleset-id syslog --enabled true
    ```

3. Restrict a ruleset to specific source IPs only:

    ```bash
    esxcli network firewall ruleset allowedip add --ruleset-id syslog --ip-address 192.168.1.50
    esxcli network firewall ruleset set --ruleset-id syslog --allowed-all false
    ```

4. Remove a previously allowed IP:

    ```bash
    esxcli network firewall ruleset allowedip remove --ruleset-id syslog --ip-address 192.168.1.50
    ```

5. Refresh the firewall to apply changes:

    ```bash
    esxcli network firewall refresh
    ```

6. Verify the ruleset's allowed IPs:

    ```bash
    esxcli network firewall ruleset allowedip list --ruleset-id syslog
    ```

---

## Change the Root Password

Rotate the root password after any personnel change, as part of a quarterly credential rotation policy, or after a security incident.

**Via esxcli (SSH session on the host):**

```bash
passwd root
```

Enter the new password twice when prompted. ESXi enforces password complexity — minimum 7 characters with a mix of character classes.

**Via PowerCLI (requires existing vCenter session):**

```powershell
$vmhost = Get-VMHost -Name "esxi01.corp.local"
$esxcli = Get-EsxCli -VMHost $vmhost -V2
$esxcli.system.account.set.Invoke(@{id="root"; password="NewP@ssw0rd!"; passwordconfirmation="NewP@ssw0rd!"})
```

**Post-rotation:**

1. Verify login works with the new password before closing the SSH session.
2. Update the credential vault or password manager entry immediately.
3. If the host is managed by vCenter with stored credentials (e.g., host profile), update the profile or re-enter the password in the host's credential store.
4. Log the rotation in the change management system with timestamp and operator.

---

## Enable and Configure Syslog

Forwarding ESXi logs to a central syslog server (e.g., Syslog-NG, Graylog, vRealize Log Insight) is required for security audit trails and incident investigation across multiple hosts.

1. Set the remote syslog target:

    ```bash
    esxcli system syslog config set --loghost=udp://192.168.1.50:514
    ```

    Supported protocols: `udp://`, `tcp://`, `ssl://`. Use TCP or SSL for reliable delivery.

2. Reload the syslog service to apply the change:

    ```bash
    esxcli system syslog reload
    ```

3. Open the syslog firewall ruleset to allow outbound traffic:

    ```bash
    esxcli network firewall ruleset set --ruleset-id syslog --enabled true
    esxcli network firewall refresh
    ```

4. Verify the configuration:

    ```bash
    esxcli system syslog config get
    ```

5. Send a test message to confirm delivery at the syslog server:

    ```bash
    esxcli system syslog mark --message="ESXi syslog test from esxi01"
    ```

6. On the syslog server, confirm the test message was received. If not, check:
    - UDP/TCP 514 is open between the host management vmk and the syslog server
    - Firewall ruleset `syslog` shows `Enabled: true` and the correct allowed IPs

---

## Apply a Patch Bundle via esxcli (Offline)

Use this procedure when the host has no internet access and patches are delivered as `.zip` bundles from the VMware patch depot or a local repository.

**Prerequisites:** patch bundle `.zip` transferred to a datastore the host can access; host in maintenance mode.

1. Put the host in maintenance mode (see Maintenance Window procedure above).

2. Copy the patch bundle to a local datastore. From a management machine:

    ```bash
    scp VMware-ESXi-7.0U3n-patch.zip root@esxi01:/vmfs/volumes/datastore1/patches/
    ```

3. SSH to the host and verify the bundle:

    ```bash
    esxcli software sources profile list --depot=/vmfs/volumes/datastore1/patches/VMware-ESXi-7.0U3n-patch.zip
    ```

4. Perform a dry run to check for conflicts:

    ```bash
    esxcli software profile update \
      --depot=/vmfs/volumes/datastore1/patches/VMware-ESXi-7.0U3n-patch.zip \
      --profile=ESXi-7.0U3n-20842819-standard \
      --dry-run
    ```

5. Apply the patch:

    ```bash
    esxcli software profile update \
      --depot=/vmfs/volumes/datastore1/patches/VMware-ESXi-7.0U3n-patch.zip \
      --profile=ESXi-7.0U3n-20842819-standard
    ```

6. Reboot the host for the patches to take effect:

    ```bash
    reboot
    ```

7. After reboot, verify the build number matches the expected patch level:

    ```bash
    esxcli system version get
    ```

8. Exit maintenance mode and run Post-Change Validation.

---

## Enable Quick Boot

Quick Boot allows ESXi to restart without a full hardware POST, reducing patch reboot time from ~15 minutes to ~2–3 minutes. It is supported on hardware that passes VMware's compatibility check.

1. Check whether the hardware supports Quick Boot:

    ```bash
    /usr/lib/vmware/loadesx/bin/loadESXCheckCompat
    ```

    A return code of `0` means Quick Boot is supported. Any other code means the hardware is incompatible (often due to BIOS or NIC firmware).

2. Enable Quick Boot:

    ```bash
    esxcli system settings kernel set --setting=quickBoot --value=1
    ```

3. Verify the setting:

    ```bash
    esxcli system settings kernel list | grep quickBoot
    ```

4. Quick Boot takes effect on the next restart triggered by `esxcli system shutdown reboot`. It does not apply to cold power cycles (full POST still runs on power-on from off).

5. To disable Quick Boot:

    ```bash
    esxcli system settings kernel set --setting=quickBoot --value=0
    ```

---

## Put Host in Image-Based Management (vLCM)

vSphere Lifecycle Manager (vLCM) image-based management replaces baseline patching with a declarative desired-image model. All hosts in a vLCM-managed cluster must use the same image; the cluster cannot mix baseline and image management.

**Prerequisites:** vCenter 7.0 U1+ with Lifecycle Manager; cluster currently using baselines; all hosts on a compatible hardware/driver matrix for the target image.

1. In vCenter, navigate to: **Menu → Lifecycle Manager → Clusters**.

2. Select the cluster and choose **Manage with a Single Image**.

3. vLCM will import the current host's software profile as the initial desired image. Review and confirm the image components (base ESXi version, vendor add-ons, firmware packages if using Broadcom/Dell/HPE integrations).

4. Remediate all hosts in the cluster to bring them to the desired image:

    - **vCenter UI path:** Cluster → Updates → Image → Remediate All

5. Monitor remediation tasks in the vCenter Tasks pane. Each host will enter maintenance mode, apply the image, and reboot automatically.

6. Verify all hosts show **Compliant** in the Image Compliance column after remediation.

7. Confirm the build version on each host matches the image:

    ```bash
    esxcli system version get
    ```

8. Once all hosts are compliant, the cluster is fully under vLCM image management. Future patching is done by editing the desired image and re-remediating.

---

## Configure NTP

Accurate time is required for SSO Kerberos, vSAN consensus, certificates, and HA heartbeats.

```bash
# Set NTP servers (replace existing config)
esxcli system ntp set --server ntp1.example.local --server ntp2.example.local

# Enable the NTP client service
esxcli system ntp set --enabled true

# Verify NTP sync status
esxcli system ntp get
# Look for: NTP Service: Running, Sync: Yes

# Manual time sync if NTP is syncing but host time has drifted
ntpq -p    # run from ESXi shell; shows stratum and offset
```

Verify from vCenter: **Host → Configure → Time Configuration** — confirm NTP service running and servers listed.

---

## Configure Hostname and DNS

```bash
# Set the hostname
esxcli system hostname set --fqdn esxi-01.example.local

# Set DNS servers
esxcli network ip dns server add --server-address 10.0.0.10
esxcli network ip dns server add --server-address 10.0.0.11

# Set DNS search domain
esxcli network ip dns search add --domain example.local

# Verify hostname and DNS
esxcli system hostname get
esxcli network ip dns server list
esxcli network ip dns search list

# Confirm forward/reverse DNS resolution
nslookup esxi-01.example.local
nslookup 10.0.1.20   # host management IP
```

---

## Join ESXi Host to Active Directory

AD join allows AD users and groups to authenticate to the ESXi host and enables LDAP-based lockdown mode.

```bash
# Join domain from ESXi shell
esxcli system secpolicy domain join --domain EXAMPLE.LOCAL \
    --username administrator --password '<password>'

# Verify domain join status
esxcli system secpolicy domain list
# Expect: Domain: EXAMPLE.LOCAL, Joined: true
```

Assign AD group to ESXi Administrator role after joining:
- vCenter → **Host → Configure → Authentication Services** → confirm domain status
- vCenter → **Host → Configure → Host Users/Groups** → add the AD group

---

## Configure SNMP

```bash
# Enable SNMP service
esxcli system snmp set --enable true

# Set SNMP community string (SNMPv1/v2c)
esxcli system snmp set --communities <community-string>

# Configure trap targets (NMS IP + community)
esxcli system snmp set --targets <nms-ip>@161/<community>

# Verify configuration
esxcli system snmp get

# Test SNMP (send a test trap)
esxcli system snmp test
```

---

## Configure a Coredump Target

Required for support bundle generation and post-crash analysis.

```bash
# List available disk partitions for coredump
esxcli system coredump partition list

# Set the coredump partition (use a small dedicated partition)
esxcli system coredump partition set --partition /vmfs/devices/disks/naa.xxx:9

# Enable coredump to network (coredump collector) — preferred for diskless hosts
esxcli system coredump network set --interface-name vmk0 \
    --server-ip <coredump-collector-ip> --server-port 6500
esxcli system coredump network set --enable true

# Verify coredump configuration
esxcli system coredump partition get
esxcli system coredump network get
```
