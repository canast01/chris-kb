# SRM — Integrations

## vCenter Integration

SRM Server registers with vCenter as a vCenter extension. This registration:

- Adds the **Site Recovery** plugin to the vSphere Client UI.
- Allows SRM to manage VM inventory, power operations, and guest customization.
- Uses a service account with **Site Recovery Administrator** privileges on the vCenter.

SRM is installed per site. Each SRM Server registers with its local vCenter. The **site pairing** then links the two SRM Servers together, establishing bi-directional awareness.

### Site Pairing

Pairing is initiated from one site (either) via SRM UI → Site Recovery → **New Site Pair**.

Steps:
1. Enter the remote vCenter FQDN/IP and credentials.
2. SRM retrieves the remote site's SSL certificate thumbprint.
3. Administrator reviews and accepts the thumbprint.
4. SRM registers the remote site's SRM extension and exchanges certificates.
5. Pairing appears as **Connected** in both sites.

```bash
# Verify site pairing via SRM REST API
curl -sk -X GET \
  "https://srm-server.example.com/api/sites" \
  -H "Authorization: Bearer $SRM_TOKEN" | python3 -m json.tool
```

Re-pairing is required if either SRM Server's certificate is rotated (thumbprint changes invalidate the trust).

---

## Storage Replication Adapter (SRA) Integration

SRAs are vendor-provided plugins that give SRM control over array-level replication. Each SRA implements a defined interface (XML-based API) that SRM calls to:

- **Discover** replicated devices (LUNs, volumes, datastores).
- **Test failover** — create writable snapshots of replicated volumes without breaking replication.
- **Failover** — promote replicated volumes to writable, break replication.
- **Reverse replication** — re-establish replication in the opposite direction for failback.
- **Query replication state** — check RPO compliance and replication health.

SRA binaries are installed on the SRM Server (Windows: `C:\Program Files\VMware\VMware vCenter Site Recovery Manager\storage\sra\<vendor>\`, appliance: `/opt/vmware/srm/storage/sra/<vendor>/`).

### SRA Registration and Testing

After installing an SRA:

1. In SRM UI → Array Managers → **Add Array Manager**.
2. Select the SRA type from the drop-down (populated from installed SRAs).
3. Enter array credentials (username, password, array management IP/hostname).
4. SRM calls the SRA's `discoverArrays` command to validate connectivity.
5. Assign array pair (protected site array ↔ recovery site array).
6. Scan for replicated devices.

```bash
# From SRM appliance: list installed SRAs
ls -la /opt/vmware/srm/storage/sra/

# Check SRA log for errors after an array scan
tail -f /var/log/vmware/srm/srm-sra.log
```

### SRA for Pure Storage

Pure Storage FlashArray SRA is available from Pure Storage support portal.

**Installation (SRM appliance):**

```bash
# Download SRA bundle from Pure Storage portal
# File: pure-sra-<version>-vmware.tar.gz

# Upload to SRM appliance and install
scp pure-sra-4.0.0-vmware.tar.gz root@srm-appliance:/tmp/

ssh root@srm-appliance
cd /tmp
tar xzf pure-sra-4.0.0-vmware.tar.gz
./install.sh
# Installs SRA to /opt/vmware/srm/storage/sra/Pure/

# Restart SRM service to detect new SRA
systemctl restart vmware-dr
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

```
Protected Site: dvPortGroup-App-VLAN100
      ↓ maps to ↓
Recovery Site:  dvPortGroup-App-VLAN200
```

Configure in SRM UI: Site Recovery → Inventory Mappings → Network → **Add Mapping**.

### NSX-T Logical Segment Mapping

When using NSX-T overlay segments, segments have logical names (not tied to physical VLANs):

```
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
