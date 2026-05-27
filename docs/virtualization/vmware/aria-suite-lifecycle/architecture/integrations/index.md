# Aria Suite Lifecycle — Integrations

```text
  LCM Integration Map
┌─────────────────────────────────────────────────────────────────┐
│  Identity              Compute                  Storage          │
│  ┌─────────────────┐   ┌──────────────────┐    ┌─────────────┐  │
│  │ Workspace ONE   │   │ vCenter Server   │    │ NFS Repo    │  │
│  │ Access (VIDM)   │   │  deploy OVAs     │    │  /data      │  │
│  │  SSO for all    │   │  power mgmt      │    │  .pak files │  │
│  │  Aria products  │   │  VM snapshots    │    └─────────────┘  │
│  └────────┬────────┘   └────────┬─────────┘                     │
│           │                    │                                │
│           └────────────┬───────┘                                │
│                        ▼                                        │
│               LCM Appliance                                     │
│                        │                                        │
│           ┌────────────┼────────────────┐                       │
│           ▼            ▼                ▼                       │
│     ┌──────────┐ ┌──────────┐   ┌─────────────┐                 │
│     │ NSX-T    │ │  SMTP    │   │ Proxy /     │                 │
│     │(optional │ │  email   │   │ Offline     │                 │
│     │ segments)│ │  alerts  │   │ Depot       │                 │
│     └──────────┘ └──────────┘   └─────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────── Aria Suite LCM Integrations ─────────────────────────────────────┐
│                                                                                                       │
│  vIDM, vCenter, all Aria products, NFS/S3 content store integrations for LCM.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Core Platform Integrations          │  │                Content Store                │   │
│   │         vCenter: deploy product VMs          │  │            NFS: local PAK storage           │   │
│   │          vIDM: SSO for all products          │  │            S3: cloud depot option           │   │
│   │          DNS: FQDN resolution check          │  │           VMware online depot sync          │   │
│   │          NTP: time sync validation           │  │         SFTP: custom content source         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  vCenter and vIDM are mandatory; content store provides PAK files for all products.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Aria Product Integrations           │  │            Certificate Authority            │   │
│   │           vROps: deploy + upgrade            │  │            Import CA cert to LCM            │   │
│   │            vRLI: deploy + upgrade            │  │            LCM pushes to products           │   │
│   │            vRA: deploy + upgrade             │  │          Cert rotation orchestrated         │   │
│   │            vRNI: deploy + upgrade            │  │            Expired cert alerting            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM on vSphere; vCenter cluster; NFS/S3 for content; CA for cert signing                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vCenter Integration = LCM uses vCenter API to deploy product VMs and check resources                 │
│  vIDM Integration    = LCM registers all products with vIDM for unified SSO                           │
│  NFS Content Store   = Local file share holding PAK/OVA files for offline install                     │
│  S3 Depot            = Cloud object store as alternative content source for LCM                       │
│  SFTP Content Source = Custom SFTP server as content source for PAK delivery                          │
│  Online Depot        = VMware Customer Connect; LCM syncs PAK catalog from here                       │
│  CA Import           = Trusted CA cert uploaded to LCM for cert validation                            │
│  Cert Push           = LCM distributes assigned cert to all product nodes                             │
│  Cert Expiry Alert   = LCM tracks cert validity dates and warns on approach                           │
│  DNS Integration     = LCM validates FQDN resolution before deploying each product                    │
│  NTP Integration     = LCM checks time sync on LCM and target product VMs                             │
│  Product Version     = LCM tracks deployed version; drives upgrade PAK selection                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## vCenter Server

LCM requires vCenter to deploy and manage OVA-based product appliances:

1. LCM → Settings → vCenter Server → Add vCenter
2. Provide vCenter FQDN, username (`svc-lcm@vsphere.local` or domain account), password
3. Select target datacenter, cluster, and datastore during product deployment

Required vCenter permissions for the LCM service account:
```text
Virtual Machine Power User (or equivalent)
Datastore — AllocateSpace
Network — Assign
Host — CIM interaction
```

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
