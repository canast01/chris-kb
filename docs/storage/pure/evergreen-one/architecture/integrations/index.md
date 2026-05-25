# Evergreen//One — Integrations

```text
  FlashArray / FlashBlade
  ┌────────────────────────────────────────────────┐
  │  Management plane                              │
  │  ├── Pure1 (phonehome) ──HTTPS 443──► Cloud   │
  │  │     capacity / SLA / firmware               │
  │  └── Syslog ──UDP/TLS──► SIEM                 │
  │                                                │
  │  Host data plane                               │
  │  ├── iSCSI / NVMe-TCP ──25GbE──► ESXi/Linux   │
  │  ├── FC / NVMe-FC ──16/32Gb──► HBAs           │
  │  └── NFS (FlashBlade) ──GbE──► Clients        │
  │                                                │
  │  VMware integrations                           │
  │  ├── VASA provider ──► vCenter (vVols/SPBM)   │
  │  └── VAAI ──► Hardware offload                │
  │                                                │
  │  Backup integrations                           │
  │  ├── Veeam VDAP ──► Snapshot transport        │
  │  └── Commvault / Rubrik ──► REST API           │
  │                                                │
  │  Replication                                   │
  │  └── ActiveCluster ──TCP 8081──► Peer array   │
  └────────────────────────────────────────────────┘
```

Evergreen//One uses the same FlashArray and FlashBlade hardware as standard Evergreen, so all host-side and management integrations are identical. The key difference is that Pure manages the hardware lifecycle — the management plane integration with Pure1 is mandatory and always active.

---

## Pure1 Management Plane

Pure1 is the cloud management and analytics portal that Pure uses to monitor all Evergreen//One installations. Phonehome telemetry is not optional — it is contractually required for SLA compliance.

| Integration | Protocol | Destination | Ports |
|---|---|---|---|
| Phonehome telemetry | HTTPS | api.pure1.purestorage.com | TCP 443 |
| Capacity reporting | HTTPS | api.pure1.purestorage.com | TCP 443 |
| Firmware updates | HTTPS | pure1-mds.pure1.purestorage.com | TCP 443 |
| Support case creation | HTTPS | support.purestorage.com | TCP 443 |

```bash
# Verify phonehome connectivity from the array (FlashArray CLI)
purecall list
# Should show recent successful uploads

# Check phonehome status
purearray list --connection
# Connectivity column should show "Connected"

# Test phonehome manually
puresupport call test
```

If phonehome is disconnected, Pure cannot monitor SLA compliance and cannot proactively manage the hardware. Treat phonehome connectivity as a critical dependency.

### Pure1 REST API Access

Customers can access Pure1 REST API to query their own Evergreen//One capacity and SLA data:

```bash
# Authenticate to Pure1 API (uses API client with private key)
# Create API client in Pure1 portal: Administration → API Clients

# Get subscription summary
curl -sX GET "https://api.pure1.purestorage.com/api/1.latest/subscriptions" \
  -H "Authorization: Bearer <api_token>"

# Get arrays enrolled in Evergreen//One
curl -sX GET "https://api.pure1.purestorage.com/api/1.latest/arrays" \
  -H "Authorization: Bearer <api_token>" | \
  python3 -m json.tool

# Get capacity metrics for a specific array
curl -sX GET "https://api.pure1.purestorage.com/api/1.latest/metrics/history?names=array_total_capacity,array_used_capacity" \
  -H "Authorization: Bearer <api_token>"
```

---

## vSphere / ESXi Host Connectivity

Evergreen//One FlashArray connects to ESXi hosts using the same protocols as a standard FlashArray. The customer is responsible for all host-side fabric and configuration.

### iSCSI

```bash
# On each ESXi host — discover the FlashArray iSCSI targets
esxcfg-swiscsi -s  # Enable software iSCSI if not already enabled

# Add FlashArray iSCSI target portals
esxcli iscsi adapter discovery sendtarget add \
  --adapter vmhba64 \
  --address 192.168.100.10

esxcli iscsi adapter discovery sendtarget add \
  --adapter vmhba64 \
  --address 192.168.100.11

# Rescan to discover LUNs
esxcli storage core adapter rescan --adapter vmhba64

# Set SATP and PSP rules for Pure FlashArray
esxcli storage nmp satp rule add \
  --satp VMW_SATP_ALUA \
  --psp VMW_PSP_RR \
  --vendor PURE \
  --model FlashArray

# Verify multipath is active
esxcli storage nmp device list | grep -i pure
```

### Fibre Channel

```bash
# Check FC HBA status on ESXi host
esxcli storage san fc list

# Verify FlashArray LUNs are visible after zoning
esxcli storage core device list | grep -i pure

# Confirm Round Robin path selection policy is set
esxcli storage nmp device list | grep -A3 "PURE"
```

### NVMe over Fibre Channel (NVMe/FC)

Supported on FlashArray //X and //C with NVMe-enabled controllers:

```bash
# List NVMe adapters on ESXi
esxcli nvme adapter list

# List NVMe namespaces visible from host
esxcli nvme namespace list

# Check NVMe path health
esxcli nvme path list
```

---

## VMware VASA Provider (vVols)

FlashArray integrates with vSphere as a VASA provider, enabling vVols (VMware Virtual Volumes) — per-VM storage policy enforcement directly on the array.

```bash
# Register FlashArray VASA provider in vCenter (run once)
# vCenter → Storage → Storage Providers → Add
# URL: https://<flasharray-management-ip>/vasa/version.xml
# Credentials: pureuser / <password>
```

After registration, storage policies can be created in vCenter that map to FlashArray QoS limits, replication, and protection groups.

---

## Veeam Backup & Replication

Veeam integrates with FlashArray as a storage array plugin (SAN snapshot transport) and as a Pure Storage snapshot provider.

```bash
# Add FlashArray as a Veeam storage infrastructure plugin
# Veeam Console → Storage Infrastructure → Add Storage → Pure Storage FlashArray
# Provide management IP and credentials

# Veeam creates storage snapshots on the FlashArray for application-consistent backups
# This uses the FlashArray REST API internally — ensure the Veeam service account
# has at least storage_admin role on the FlashArray
```

---

## ActiveCluster (Synchronous Replication)

ActiveCluster provides RPO=0 synchronous replication between two Evergreen//One sites. It requires a Mediator (lightweight VM) accessible from both arrays to resolve split-brain scenarios.

```bash
# Check ActiveCluster pod status (FlashArray CLI)
purepod list
# State should be "online"

# Check replication link health
purereplicationlink list

# Check Mediator connectivity
purepod list --connection
```

The two arrays must have network connectivity on the replication port (TCP 8081). Mediator VM can run on-premises or in a cloud VPC (GCP/Azure/AWS).

---

## SIEM / Syslog Integration

Forward FlashArray audit events to your SIEM for centralised security monitoring:

```bash
# Configure syslog on FlashArray (FlashArray CLI)
puresyslog add --name siem-server --address 192.168.10.100 --port 514 --protocol UDP

# Verify syslog configuration
puresyslog list

# Events forwarded include: admin logins, volume create/delete, policy changes, hardware alerts
```

Key events to alert on:
- Admin login from unexpected IP
- Volume deletion (especially pod volumes under ActiveCluster)
- Protection policy removed from a volume
- Array hardware component failure
