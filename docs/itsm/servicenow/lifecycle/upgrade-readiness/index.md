---
tags:
  - servicenow
---
# Upgrade Readiness Checklist

<div class="kb-summary">
Validates that infrastructure is in a safe state before any upgrade or patching activity begins. Complete all checks and obtain explicit go/no-go sign-off before proceeding.

*Applies to: ServiceNow*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
preupgrade_gate_criteria: "Pre-Upgrade Gate Criteria" {shape: rectangle}
4_network_and_connectivity: "4. Network and Connectivity" {shape: rectangle}
5_vendor_compatibility_matrix: "5. Vendor Compatibility Matrix" {shape: rectangle}
6_preupgrade_snapshot_vms: "6. Pre-Upgrade Snapshot (VMs)" {shape: rectangle}
7_rollback_plan: "7. Rollback Plan" {shape: rectangle}
go_nogo_signoff: "Go / No-Go Sign-Off" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> preupgrade_gate_criteria
preupgrade_gate_criteria -> 4_network_and_connectivity
4_network_and_connectivity -> 5_vendor_compatibility_matrix
5_vendor_compatibility_matrix -> 6_preupgrade_snapshot_vms
6_preupgrade_snapshot_vms -> 7_rollback_plan
7_rollback_plan -> go_nogo_signoff
go_nogo_signoff -> validate
```

## Pre-Upgrade Gate Criteria

| Health Check | Pass Criteria |
|---|---|
| CPU load | < 80% sustained |
| Memory free | > 20% |
| Disk free | > 20% on all volumes |
| Failed services | None |
| Error log (last 1h) | No critical / hardware errors |
| HW alarms | No active hardware alerts |
| Replication lag | Within SLA |

## 4. Network and Connectivity

```bash
ping -c 3 <gateway>
ping -c 3 <dns-server>
ping -c 3 <ntp-server>

# NTP sync (drift < 1s)
chronyc tracking | grep "System time"

# DNS resolution
nslookup <hostname>.example.com
```


```text title="Expected output"
PING 10.0.1.1 (10.0.1.1) 56(84) bytes of data.
64 bytes from 10.0.1.1: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 10.0.1.1: icmp_seq=2 ttl=64 time=2.41 ms
64 bytes from 10.0.1.1: icmp_seq=3 ttl=64 time=2.38 ms
--- 10.0.1.1 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 2.34/2.38/2.41/0.03 ms

PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=18.92 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=19.07 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=18.99 ms
--- 8.8.8.8 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/stddev = 18.92/19.00/19.07/0.07 ms

PING 91.189.89.198 (91.189.89.198) 56(84) bytes of data.
64 bytes from 91.189.89.198: icmp_seq=1 ttl=54 time=42.18 ms
64 bytes from 91.189.89.198: icmp_seq=2 ttl=54 time=42.31 ms
64 bytes from 91.189.89.198: icmp_seq=3 ttl=54 time=42.25 ms
--- 91.189.89.198 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
rtt min/avg/max/stddev = 42.18/42.25/42.31/0.06 ms

System time   : 0.000000123 seconds slow of NTP time

Server          Address
Name:   app-server-01.example.com
Address: 192.168.1.45
```

!!! warning "Common errors"
    **`ping: <gateway>: Name or service not known`** — Replace `<gateway>` with the actual IP address or hostname of your gateway (e.g., `10.0.1.1`).
    **`chronyc: command not found`** — Install chrony with `sudo apt install chrony` or `sudo yum install chrony` depending on your distribution.
    **`** server can't find <hostname>.example.com: NXDOMAIN`** — Verify the hostname is correct and that DNS is properly configured; check `/etc/resolv.conf` for valid nameserver entries.
## 5. Vendor Compatibility Matrix

```bash
# VMware HCL — check driver/firmware compatibility before ESXi upgrade
esxcli software vib list | grep -E "bnx|igb|i40e|lpfc|nfnic|enic"
esxcli hardware firmware get
```


```text title="Expected output"
Name                           Version                        Vendor  Acceptance Level  Install Date
net-bnx2-2.2.5f-1OEM.670.0.0.8169922  2.2.5f                         Broadcom  PartnerSupported  2024-01-15
net-igb-5.4.6-1OEM.670.0.0.8169922    5.4.6                          Intel     PartnerSupported  2024-01-15
net-i40e-2.18.6-1OEM.670.0.0.8169922  2.18.6                         Intel     PartnerSupported  2024-01-15
lpfc-12.8.405.3-1OEM.670.0.0.8169922  12.8.405.3                     Broadcom  PartnerSupported  2024-01-15

System UUID: 4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d
BIOS Version: DELL A13 12/18/2023
Firmware Version: 2.11.2
```

!!! warning "Common errors"
    **`esxcli: Unknown option or subcommand 'software vib list' under 'software'`** — Verify ESXi version supports the command; use `esxcli software vib list --help` to confirm syntax.
    **`Unable to retrieve firmware information: Connection refused`** — Ensure you are connected to the ESXi host via SSH or vSphere Client with proper credentials.
| Dependency | Current Version | Compatible With Upgrade | Checked |
|---|---|---|---|
| Hypervisor version | | | ☐ |
| Driver versions | | | ☐ |
| Firmware versions | | | ☐ |
| Application compatibility | | | ☐ |
| Storage array interop | | | ☐ |

## 6. Pre-Upgrade Snapshot (VMs)

```bash
# Take quiesced snapshot immediately before change
New-Snapshot -VM "HOSTNAME" \
  -Name "pre-upgrade-CHG-XXXX-$(Get-Date -Format yyyyMMdd)" \
  -Description "Pre-upgrade snapshot — CHG-XXXX" \
  -Quiesce \
  -Memory:$false

# Verify
Get-VM -Name "HOSTNAME" | Get-Snapshot | Select-Object Name, Created, SizeMB
```


```text title="Expected output"
Name                                    Created              SizeMB
----                                    -------              ------
pre-upgrade-CHG-0047291-20250114        1/14/2025 2:34:15 PM 12847
pre-upgrade-CHG-0047290-20250113        1/13/2025 9:12:08 AM 12802
base-golden-image-v8.2                  1/10/2025 4:47:22 PM 0
```

!!! warning "Common errors"
    **`New-Snapshot : The operation is not valid for the current state of the object.`** — Ensure the VM is powered on and not already in a snapshot operation; check vCenter for any pending tasks.
    **`Get-VM : The object 'HOSTNAME' was not found.`** — Verify the exact VM name matches vCenter inventory and that you have sufficient vSphere permissions.
!!! note "Snapshot retention"
    Remove pre-upgrade snapshots within 48 hours of successful completion. Stale snapshots degrade VM performance and consume datastore space.

## 7. Rollback Plan

```text
Rollback Plan — CHG-XXXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
System:           <hostname>
Upgrade:          <from version> → <to version>
Rollback method:  [ ] Snapshot  [ ] Backup restore  [ ] Config revert
Snapshot name:    pre-upgrade-CHG-XXXX-YYYY-MM-DD
Estimated time:   <X> minutes
Rollback trigger: Service fails to start / error rate > 5% / app team reports failures
Decision authority: <name / role>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Go / No-Go Sign-Off

| Category | Status | Signed Off By |
|---|---|---|
| Change approved | ☐ Go / ☐ No-Go | |
| Backup verified | ☐ Go / ☐ No-Go | |
| Rollback plan documented | ☐ Go / ☐ No-Go | |
| System health passing | ☐ Go / ☐ No-Go | |
| Vendor compatibility confirmed | ☐ Go / ☐ No-Go | |
| Maintenance window active | ☐ Go / ☐ No-Go | |
| **Final Decision** | ☐ **GO** / ☐ **NO-GO** | |
