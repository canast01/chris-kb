# SRM — Integrations


<div class="kb-summary">
Integrations reference covering Storage Replication Adapter (SRA) Integration, vSphere Replication Integration, NSX-T Integration for Network Mapping, Active Directory / Identity Integration, Identity Federation with vIDM / Workspace ONE Access and 1 more sections.
</div>

  SRM Integration Points
        │                                    │
        └─────────────────┬──────────────────┘
                          ▼
                 ┌─────────────────┐
                 │  SRM Server     │
                 │  (site pair)    │
                 └─────────────────┘
```text
┌────────────────────────────────────── VMware SRM — Integrations ──────────────────────────────────────┐
│                                                                                                       │
│  SRM integrates with vCenter, vSphere Replication, storage arrays, NSX for network                    │
│  remapping, and Aria Operations for DR health monitoring.                                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             vCenter Integration              │  │           Replication Integration           │   │
│   │            Registered per vCenter            │  │         vSphere Replication: native         │   │
│   │        VM inventory: protection grps         │  │              SRA: array plug-in             │   │
│   │         vCenter events: failover log         │  │           Dell EMC: SRA available           │   │
│   │           Alarms: DR plan test due           │  │            NetApp: SnapMirror SRA           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SRA enables array-based replication; without it, only vSphere Replication is available.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Network Integration              │  │            Monitoring Integration           │   │
│   │             NSX: network mapping             │  │            Aria Ops: SRM adapter            │   │
│   │         IP customisation: re-IP VMs          │  │           Compliance: test alerts           │   │
│   │           vDS: port group mapping            │  │         Email: plan run notification        │   │
│   │            Stretched L2: no re-IP            │  │         CMDB: CI update on failover         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  WAN link between sites carries replication traffic; network mapping ensures VMs                      │
│  connect to correct networks after failover.                                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRA           = Storage Replication Adapter; array vendor plug-in for SRM                            │
│  vSphere Rep   = host-based replication; native SRM integration                                       │
│  SnapMirror SRA= NetApp SRA; uses SnapMirror for array replication                                    │
│  Network mapping= map protected-site portgroup to recovery-site portgroup                             │
│  IP customisation= script to re-IP VMs after failover to recovery site                                │
│  Stretched L2  = same subnet both sites; no IP change needed                                          │
│  vDS port group= vSphere Distributed Switch segment; mapped in SRM                                    │
│  NSX segment   = overlay network; SRM can map NSX segments                                            │
│  Aria Ops      = monitors SRM compliance and last test date                                           │
│  CMDB          = Configuration Management DB; update CI on failover                                   │
│  Protection group= set of VMs protected by same replication and plan                                  │
│  Test due alarm = SRM reminds when DR test is overdue                                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────────── VMware SRM — Integrations ──────────────────────────────────────┐
│                                                                                                       │
│  SRM integrates with vCenter, vSphere Replication, storage arrays, NSX for network                    │
│  remapping, and Aria Operations for DR health monitoring.                                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             vCenter Integration              │  │           Replication Integration           │   │
│   │            Registered per vCenter            │  │         vSphere Replication: native         │   │
│   │        VM inventory: protection grps         │  │              SRA: array plug-in             │   │
│   │         vCenter events: failover log         │  │           Dell EMC: SRA available           │   │
│   │           Alarms: DR plan test due           │  │            NetApp: SnapMirror SRA           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SRA enables array-based replication; without it, only vSphere Replication is available.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Network Integration              │  │            Monitoring Integration           │   │
│   │             NSX: network mapping             │  │            Aria Ops: SRM adapter            │   │
│   │         IP customisation: re-IP VMs          │  │           Compliance: test alerts           │   │
│   │           vDS: port group mapping            │  │         Email: plan run notification        │   │
│   │            Stretched L2: no re-IP            │  │         CMDB: CI update on failover         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  WAN link between sites carries replication traffic; network mapping ensures VMs                      │
│  connect to correct networks after failover.                                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRA           = Storage Replication Adapter; array vendor plug-in for SRM                            │
│  vSphere Rep   = host-based replication; native SRM integration                                       │
│  SnapMirror SRA= NetApp SRA; uses SnapMirror for array replication                                    │
│  Network mapping= map protected-site portgroup to recovery-site portgroup                             │
│  IP customisation= script to re-IP VMs after failover to recovery site                                │
│  Stretched L2  = same subnet both sites; no IP change needed                                          │
│  vDS port group= vSphere Distributed Switch segment; mapped in SRM                                    │
│  NSX segment   = overlay network; SRM can map NSX segments                                            │
│  Aria Ops      = monitors SRM compliance and last test date                                           │
│  CMDB          = Configuration Management DB; update CI on failover                                   │
│  Protection group= set of VMs protected by same replication and plan                                  │
│  Test due alarm = SRM reminds when DR test is overdue                                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Array Manager configuration for Pure:**

| Field | Value |
|---|---|
| SRA type | Pure Storage FlashArray SRA |
| Array Management IP | FlashArray management VIP |
| Username | `srmuser` (create dedicated account on array) |
| Password | Array account password |
| Protocol | HTTPS |

**Pure minimum permissions for SRA account:**

The SRA account on the Pure FlashArray requires `array_admin` role for replication operations (failover, reverse).

```bash
# On Pure FlashArray CLI
purecli user create srmuser --role array_admin
purecli user setpassword srmuser
```

### SRA for Dell PowerStore / EMC

Dell provides SRAs for multiple product lines.

**PowerStore SRA (appliance):**

```bash
scp Dell_SRA_for_PowerStore_<version>.tar.gz root@srm-appliance:/tmp/
ssh root@srm-appliance
cd /tmp
tar xzf Dell_SRA_for_PowerStore_<version>.tar.gz
./install.sh
systemctl restart vmware-dr
```

**PowerStore SRA credentials:**

| Field | Value |
|---|---|
| Array Management IP | PowerStore Manager IP |
| Username | Local admin user |
| Password | Admin password |
| Port | 443 |

Dell SRA writes logs to `/var/log/vmware/srm/` alongside SRM logs.

---

## vSphere Replication Integration

vSphere Replication requires:

1. **VR Appliance** deployed at each site (OVA from VMware download portal).
2. VR Appliance registered with local vCenter.
3. VR Appliances **paired** between sites.
4. SRM configured to use the VR Appliances.

### VR Appliance Deployment

```bash
# Deploy via govc
govc import.ova \
  --ds=vsanDatastore \
  --net="Management" \
  --name=vr-appliance-01 \
  vSphere_Replication_OVF10.ova
```

After deployment:
- Access VR Appliance VAMI at `https://<vr-ip>:5480`
- Configure: network, NTP, password
- Register with vCenter: VAMI → Configuration → vSphere Replication → **Register**

### VR Appliance Pairing

VR pairing is done from SRM UI: Site Recovery → Replication → Configure Replication, or from the VR VAMI: Configuration → vSphere Replication → Remote Sites → **Add Remote Site**. Enter remote VR appliance FQDN/IP and accept certificate.

Required firewall ports between VR appliances:

| Port | Protocol | Purpose |
|---|---|---|
| 80, 443 | TCP | VAMI and API |
| 44046 | TCP | Replication data (VR appliance → recovery ESXi) |
| 10000, 10001 | TCP | VR management channel |
| 31031 | TCP | HBR (host-based replication) control |

### VR Replication Configuration per VM

Configure replication per VM in vSphere Client → VM → **Configure** → **vSphere Replication**:

| Parameter | Description |
|---|---|
| RPO | 5 min – 24 hours |
| Target site | Recovery site VR appliance |
| Target datastore | Where to store replicated VMDK on recovery site |
| Enable quiescing | Quiesce guest OS before snapshot (requires VMware Tools) |
| Enable compression | Compress replication stream (reduces bandwidth, increases CPU) |
| Enable encryption | Encrypt replication stream in transit |

### VR Appliance Health Check

```bash
# SSH to VR appliance
ssh admin@vr-appliance.example.com

# Check VR service status
systemctl status vmware-vcd-watchdog
systemctl status vmware-hbrsrv

# List active replication sessions
hbr-configure -l

# VR log location
ls -lh /var/log/vmware/
# hbrsrv.log      — main replication server log
# vmware-vcd-watchdog.log — VR daemon log
```

---

## NSX-T Integration for Network Mapping

When the protected and recovery sites use NSX-T, SRM uses **network mappings** to translate NSX-T logical segments between sites.

### Port Group Mapping (vDS-based)

Standard mapping for traditional vSphere networking:

```text
Protected Site: dvPortGroup-App-VLAN100
      ↓ maps to ↓
Recovery Site:  dvPortGroup-App-VLAN200
```

Configure in SRM UI: Site Recovery → Inventory Mappings → Network → **Add Mapping**.

### NSX-T Logical Segment Mapping

When using NSX-T overlay segments, segments have logical names (not tied to physical VLANs):

```text
Protected Site: overlay-segment-app-tier  (NSX-T logical segment)
      ↓ maps to ↓
Recovery Site:  overlay-segment-app-tier  (same name at recovery site, different segment ID)
```

SRM discovers NSX-T segments via the vSphere Client's NSX-T integration. Requirements:

- NSX-T Manager at recovery site must be registered with recovery-site vCenter.
- SRM service account requires NSX-T read permissions.

### Recovery Site Shadow Networks

In DR scenarios, recovery site VMs often need to come up on isolated networks until routing is established:

1. Create a dedicated **transit port group** at recovery site with controlled uplink access.
2. Map protected-site VLANs → recovery-site transit segments.
3. Adjust BGP/routing at recovery site to advertise protected-site subnets after failover completes.

For NSX-T stretched topologies (where segments span both sites), no network re-mapping is needed — VMs retain the same IP and the segment extends automatically.

---

## Active Directory / Identity Integration

SRM does **not** maintain its own user database. All authentication is delegated to vCenter SSO.

- Users are defined in the vCenter SSO identity source (Active Directory, local SSO domain, or LDAP).
- SRM roles are assigned via vCenter's **Roles and Permissions** system on the SRM extension object.
- AD group membership flows through vCenter SSO — assign SRM roles to AD groups, not individual users.

No AD configuration is required on the SRM Server directly. The SRM service runs as a local service account (Windows) or as root (appliance).

**Recommended AD groups for SRM:**

| AD Group | SRM Role |
|---|---|
| `grp-srm-admins` | Site Recovery Administrator |
| `grp-srm-recovery-ops` | Site Recovery Recovery Admin |
| `grp-srm-readonly` | Site Recovery User |

---

## Identity Federation with vIDM / Workspace ONE Access

For environments with multiple vCenters (e.g., management vCenter + workload vCenters), VMware Identity Manager (vIDM / Workspace ONE Access) federates SSO across vCenter instances.

With vIDM:
- Users authenticate once (IdP-initiated SSO) and access both vCenters and SRM without re-entering credentials.
- SRM follows vCenter SSO federation — no separate vIDM configuration needed on SRM.
- Useful in SRM deployments where operators need access to both protected-site vCenter and recovery-site vCenter simultaneously.

Configure vIDM integration on each vCenter: vCenter → Administration → Single Sign-On → Identity Providers → **Add Identity Provider**. SRM inherits the federation automatically.

---

## SRM and vSAN Integration

When datastores are vSAN:

- **vSAN stretched cluster** does not use SRM (built-in HA across sites).
- **Standard vSAN (non-stretched)** can be used with vSphere Replication — replicate VMs from vSAN at protected site to vSAN (or any datastore) at recovery site.
- ABR is not applicable to vSAN — vSAN does not expose block LUNs for SRA discovery. Use VR instead.

### vSAN and VR Considerations

| Factor | Impact |
|---|---|
| vSAN deduplication | Does not apply to VR staging area — replicated data is not deduplicated |
| vSAN encryption | VMs encrypted at source arrive encrypted at recovery site if same key is available; requires key server at recovery site |
| vSAN capacity at recovery site | Must accommodate all replicated VMDK data for all protected VMs |
