---
tags:
  - vxrail
description: "VxRail vendor support: Dell SupportAssist case creation, mystic diagnostic bundle collection, Secure Remote Services (SRS) connectivity, and engineering..."
---
# VxRail Vendor Support

<div class="kb-summary">
VxRail vendor support: Dell SupportAssist case creation, `mystic` diagnostic bundle collection, Secure Remote Services (SRS) connectivity, and engineering escalation path.

*Applies to: VxRail 7.x · 8.x*
</div>

---

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "On-Call Engineer" as ENG
participant "VxRail\nSystem" as SYS
participant "Vendor Support" as SUP

ENG -> SYS: Opening a Support Request
SYS --> ENG: Output
ENG -> SYS: Collecting the VxRail Support Bundle
SYS --> ENG: Output
ENG -> SYS: SRS / SupportAssist
SYS --> ENG: Output
ENG -> SUP: Escalate with diagnostic bundle
SUP --> ENG: Case / resolution path

@enduml
```

## Opening a Support Request

Dell support for VxRail is accessed via the Dell support portal. Service requests are opened against the cluster service tag or an individual node service tag.

1. Navigate to the Dell support portal.
2. Search by service tag (cluster or node) — confirms warranty and support level.
3. Select **VxRail** as the product line.
4. Choose the appropriate category: software (VxRail Manager, ESXi, vSAN), hardware (node failure, disk, PSU), or networking.

**Required information for every VxRail SR:**

- VxRail bundle version (VxRail Manager → System → Software Versions)
- Affected node service tag(s)
- Cluster size and configuration (all-flash, NVMe, etc.)
- Description of the issue with timestamps
- VxRail support bundle (see below)

---

## Collecting the VxRail Support Bundle

The support bundle collects logs from all nodes, vCenter, VxRail Manager, and vSAN traces in a single operation.

```text
VxRail Manager UI → System → Support → Generate Support Bundle
→ Select all nodes → Generate
→ Download the bundle once complete (may take 10–20 minutes for large clusters)
```

**Bundle contents:**

- VxRail Manager application logs
- ESXi host logs (hostd, vmkernel, vpxa) for each node
- vSAN health and trace data
- vCenter events and alarms
- Hardware event logs from iDRAC for each node

**Alternative — individual node bundle via ESXi:**

```bash
# SSH to the ESXi host directly
vm-support -w /tmp
# SCP the output off the host
scp root@<esxi-ip>:/tmp/esx-<hostname>-*.tgz <destination>
```


```text title="Expected output"
Generating support bundle for host esx-vxrail-node01...
Collecting system logs and diagnostics...
Collecting storage information...
Collecting network configuration...
Collecting virtual machine data...
Support bundle created: /tmp/esx-vxrail-node01-2024-01-15-14-32-45.tgz (2.3 GB)
esx-vxrail-node01-2024-01-15-14-32-45.tgz          100%  2.3GB   45.2MB/s   00:51
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Ensure SSH key is loaded in ssh-agent or use `-i` flag to specify the private key file.
    **`No such file or directory`** — Wait for the vm-support command to complete fully before attempting SCP; check `/tmp` on the ESXi host to confirm the .tgz file exists.
---

## SRS / SupportAssist

SupportAssist (formerly Secure Remote Services) auto-generates Dell support cases for hardware faults detected by iDRAC.

**Verify SupportAssist is active:**

```text
VxRail Manager UI → System → Support → SupportAssist
→ Status should show: Connected
→ Check Last Heartbeat timestamp — should be within 24 hours
```

**Test SupportAssist:**

```text
VxRail Manager → System → Support → SupportAssist → Run Test
→ Confirm a test SR appears in the Dell support portal within a few minutes
```

If SupportAssist shows disconnected, check:
1. Outbound HTTPS access from VxRail Manager to Dell SupportAssist endpoints
2. Proxy configuration if applicable (VxRail Manager → System → Network → Proxy)

---

## Escalation Path

| Level | Action |
|---|---|
| Standard SR | Opens automatically (SupportAssist) or via portal |
| Priority escalation | In the open SR → **Request Escalation** → provide business impact |
| Engineering escalation | In the SR → **Request Engineering Escalation** → for bugs blocking production |
| Account team | Contact Dell account team for critical production outages if SR response is insufficient |

---

## Version Compatibility Matrix

Before any lifecycle operation, verify the target VxRail bundle version against the VxRail Compatibility Matrix:

```text
Dell Technologies Interoperability Matrix (IMT)
→ Select VxRail → current version → check compatible vSphere, vSAN, NSX versions
```

Also check for any VxRail-specific release notes or known issues before applying an LCM bundle — some bundles have prerequisites or known issues documented in the release notes.

---

## Useful Support Commands

```bash
# Check VxRail Manager version from the appliance
ssh vcf@<vxrail-manager-ip>
cat /etc/vxrail-release

# Check ESXi version on a node
vmware -v

# Check all node service tags from VxRail Manager CLI
vxrail-system-info --node-list

# Check iDRAC for hardware events on a node
racadm getsel   # System Event Log (hardware alerts)
```


```text title="Expected output"
VxRail Release 7.0.510-26.0.0-20231015
VMware ESXi 7.0.3 build-19482537
Node List:
  Node 1: Service Tag ABCD123, IP 192.168.1.101
  Node 2: Service Tag EFGH456, IP 192.168.1.102
  Node 3: Service Tag IJKL789, IP 192.168.1.103
  Node 4: Service Tag MNOP012, IP 192.168.1.104
System Event Log (SEL) Records:
  1 | 10/15/2023 | 14:32:15 | Temperature | Upper Critical | CPU1 Temp 89C
  2 | 10/15/2023 | 14:28:42 | Voltage | Lower Warning | +12V Rail 11.8V
  3 | 10/15/2023 | 13:15:09 | Fan | Lower Critical | Fan1_SYS 2100 RPM
```

!!! warning "Common errors"
    **`ssh: connect to host <vxrail-manager-ip> port 22: Connection timed out`** — Verify the VxRail Manager IP address is correct and reachable on the network, and confirm SSH is enabled on the appliance.
    **`racadm: command not found`** — Install or load the Dell iDRAC tools package (typically `yum install dell-idrac-tools` or access iDRAC via HTTPS web interface instead).
    **`vxrail-system-info: command not found`** — Ensure you are running this command from the VxRail Manager appliance itself, not from a remote ESXi host.