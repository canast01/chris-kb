---
tags:
  - architecture
  - aria-lcm
  - vmware
---
# Aria Suite Lifecycle — Integrations

<div class="kb-summary">
Integrations reference covering vCenter Server, NSX-T Integration (Optional), SMTP Configuration, NFS Binary Repository, Proxy / Offline Depot and 2 more sections.

*Applies to: Aria Suite Lifecycle 8.x*
</div>
![Aria Suite Lifecycle — Integrations](../../../../assets/virtualization-vmware-aria-suite-lifecycle-architecture-inte.svg)

  LCM Integration Map

## NSX-T Integration (Optional)

If LCM-deployed products require new overlay segments:
1. LCM → Settings → NSX-T → Add NSX-T Manager
2. Provide NSX-T Manager FQDN and credentials
3. LCM can auto-provision overlay segments for Aria product deployment

## SMTP Configuration

Configure email notifications for upgrade alerts and certificate expiry warnings:
1. LCM → Settings → My VMware → SMTP Settings
2. Enter relay host, port (25/587), and credentials if required
3. Set a sender address and notification recipient list

Test SMTP: LCM → Settings → SMTP → Send Test Email.

## NFS Binary Repository

LCM stores downloaded product bundles on an NFS share:

```bash
# Verify NFS mount from LCM appliance
df -h /data
mount | grep /data
# Should show: <nfs-server>:/lcm-repo on /data type nfs

# Check available space (requires > 50 GB free per product version)
du -sh /data/*
```

If NFS becomes unavailable: LCM upgrades will fail. Ensure NFS server HA (or VMware datastore-backed NFS).

## Proxy / Offline Depot

For environments without direct internet access:

**Proxy**:
1. LCM → Settings → System Details → Proxy → configure HTTP proxy IP and port
2. Add proxy bypass for vCenter, NSX, and all Aria product FQDNs

**Offline Depot** (no internet):
1. Download product bundles from Broadcom Support Portal (*.pak files)
2. Upload to LCM: Lifecycle Operations → Settings → Binary Mapping → Upload Product Binaries
3. Map binaries before initiating upgrade

## Active Directory / LDAP

AD integration is handled through Workspace ONE Access, not LCM directly:
1. VIDM console → Connector → Active Directory → Add AD connector
2. Configure sync scope: OUs containing admin groups
3. Map AD groups to LCM roles in LCM → Settings → Access Control

## Aria Automation Integration

After LCM deploys Aria Automation:
1. LCM → My Services → Aria Automation → Connect to vCenter
2. Configure cloud accounts in Aria Automation for each vCenter under management

## See also

- [Aria Suite Lifecycle — How It Works](../how-it-works/)
- [Aria Suite Lifecycle — Deploy](../../deploy/)
