---
tags:
  - architecture
  - dell
---
# Dell VPLEX — Integrations

<div class="kb-summary">
Integration with back-end storage arrays, hypervisors, replication systems, and monitoring platforms.

*Applies to: VPLEX*
</div>
![Dell VPLEX — Integrations](../../../../assets/storage-dell-vplex-architecture-integrations.svg)

```mermaid
flowchart TB
    subgraph "Site A"
        hostA["ESXi / Linux Hosts\nSite A"]
        dirA["VPLEX Cluster-1\nDirectors"]
        arrA["PowerMax / Unity\nArray A"]
    end
    subgraph "Site B"
        hostB["ESXi / Linux Hosts\nSite B"]
        dirB["VPLEX Cluster-2\nDirectors"]
        arrB["PowerMax / Unity\nArray B"]
    end
    witness["Witness VM\n(3rd failure domain)"]
    vms["VMS\nUnisphere + vplexcli"]
    cloudiq["Dell CloudIQ\nAIOps / health telemetry"]
    siem["SIEM\nSyslog / SNMP traps"]

    hostA -->|"FC front-end\nSAN fabric A"| dirA
    dirA -->|"FC back-end\nzoning + masking"| arrA
    hostB -->|"FC front-end\nSAN fabric B"| dirB
    dirB -->|"FC back-end\nzoning + masking"| arrB
    dirA <-->|"ICL — 10/25GbE\nsynchronous Metro"| dirB
    witness -. "quorum" .- dirA
    witness -. "quorum" .- dirB
    vms -->|"management"| dirA
    vms -->|"management"| dirB
    vms -->|"telemetry"| cloudiq
    vms -->|"syslog"| siem
```

## Back-End Storage Arrays

VPLEX presents a virtualisation layer over heterogeneous back-end arrays. The back-end ports on each VPLEX director zone to the target ports on the back-end array, then VPLEX discovers and claims the LUNs exposed to those ports.

### Supported Back-End Arrays

| Array Platform | Notes |
|---|---|
| Dell PowerMax / VMAX | Primary production integration; PowerMax SRDF can coexist with VPLEX back-end masking |
| Dell Unity XT | Supported; verify per-version compatibility in the Dell VPLEX Compatibility Matrix |
| Dell PowerStore | Supported; confirm GeoSynchrony version compatibility |
| Dell XtremIO | Supported on compatible GeoSynchrony versions |
| Third-party arrays | EMC/Symmetrix legacy, NetApp, Hitachi VSP — check the compatibility matrix; not all models supported |

### Back-End Configuration Steps

1. **Zone**: Create SAN fabric zones between VPLEX back-end ports and array target ports. Use single-initiator (VPLEX BE port) to multiple-target (array ports) zoning.
2. **Mask**: On the back-end array, create a host/initiator group presenting the LUN to the VPLEX back-end port WWNs.
3. **Discover**: From vplexcli, rediscover the back-end array.
4. **Claim**: Claim the storage volume.

```bash
# List discovered back-end arrays
vplexcli -q -e "ls /storage-elements/storage-arrays"

# Show a specific array and its visible storage volumes
vplexcli -q -e "ll /storage-elements/storage-arrays/array-A/"
vplexcli -q -e "ls /storage-elements/storage-arrays/array-A/storage-volumes"

# Rediscover storage volumes on a back-end array (after adding new LUNs)
vplexcli -q -e "storage-volume rediscover \
  --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"

# Claim a discovered storage volume for use in VPLEX provisioning
vplexcli -q -e "storage-volume claim \
  --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"
```

### PowerMax Integration Notes

- PowerMax SRDF and VPLEX back-end masking can coexist on the same array; ensure SRDF R1/R2 pairs are not also claimed as VPLEX back-end volumes unless that is the intended Geo configuration.
- Use PowerMax Service Levels to assign appropriate performance tiers to LUNs before presenting them to VPLEX.
- When expanding a PowerMax LUN, expand on the array first, then rediscover and expand the extent and virtual volume in VPLEX.

```bash
# After expanding a back-end LUN on PowerMax, rediscover and expand in VPLEX:
vplexcli -q -e "storage-volume rediscover \
  --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"
vplexcli -q -e "extent expand \
  --extent /clusters/cluster-1/storage-elements/extents/ext_app_001"
vplexcli -q -e "virtual-volume expand \
  --virtual-volume /virtual-volumes/my_app_vol_1"
```

## VMware vSphere

VPLEX is deeply integrated with VMware vSphere environments, particularly for Metro stretched-cluster configurations.

### ESXi Host Connectivity

- ESXi hosts connect to VPLEX front-end FC ports via the SAN fabric.
- Each ESXi host requires a storage view on each VPLEX cluster (for Metro); each view contains the front-end ports on that cluster and the distributed virtual volume(s) the host needs.
- ESXi multipathing: configure VMware NMP with the Round Robin policy or use the VPLEX-specific SATP rule. Verify that all expected paths are active in `esxcli storage nmp path list`.

```bash
# From ESXi host: list active paths to a VPLEX volume
esxcli storage nmp path list -d <naa_id>

# Rescan HBAs after storage view changes
esxcli storage core adapter rescan --adapter vmhba<n>
```

### VPLEX Metro + vSphere HA / vMotion

VPLEX Metro is the prerequisite for vSphere Metro Storage Cluster (vMSC) configurations:

| vSphere Feature | VPLEX Metro Behaviour |
|---|---|
| vSphere HA | VM restarts on the surviving site automatically after a site failure; Witness-arbitrated quorum allows surviving cluster to continue serving I/O |
| vMotion across sites | VM migrates between ESXi hosts at Site A and Site B using the same distributed virtual volume; I/O follows the VM transparently |
| Datastore accessibility | Both ESXi clusters see the same distributed volume from their respective VPLEX clusters; no storage path changes needed during vMotion |

**vMSC design requirements:**

- All VM datastore volumes must be distributed virtual volumes in a consistency group.
- Both vSphere clusters must be in separate failure domains corresponding to VPLEX Cluster-1 (Site A) and Cluster-2 (Site B).
- The vSphere Heartbeat Datastore (for HA) should be a VPLEX distributed volume accessible from both sites.
- Test planned site-switch failover before production go-live and document the procedure.

### VASA Provider

VPLEX supports VMware vSphere APIs for Storage Awareness (VASA) on compatible GeoSynchrony versions, enabling vVols and storage-policy-based management. Verify VASA provider support against the Dell VPLEX Compatibility Matrix before enabling.

## Dell RecoverPoint (VPLEX Geo)

VPLEX Geo uses RecoverPoint to extend the VPLEX federation beyond the ≤5ms Metro RTT limit with asynchronous replication.

### Architecture

```text
Site A (Active)
  VPLEX Cluster-1
  RecoverPoint Splitter (integrated with VPLEX directors)
  RecoverPoint Cluster A
      |
      | Async replication (WAN journal)
      |
Site B (DR)
  VPLEX Cluster-2
  RecoverPoint Cluster B (receives journal)
  Volumes active only after failover
```

The RecoverPoint splitter is embedded within VPLEX and intercepts writes to copy them asynchronously to the remote RecoverPoint cluster. RPO is configurable based on journal settings.

### Key Points

- Volumes in VPLEX Geo are active on one site at a time (not active-active like Metro).
- Failover is an orchestrated process through RecoverPoint (not automatic via Witness).
- RecoverPoint bookmarks enable point-in-time consistency for crash-consistent or application-consistent recovery.
- VPLEX Geo is typically used when Site A and Site B are separated by >5ms RTT (city-to-city, region-to-region).

```mermaid
flowchart LR
    subgraph "Site A — Active"
        hostA["Hosts — Active I/O"]
        dirA["VPLEX Cluster-1"]
        rpSplitter["RecoverPoint Splitter\nembedded in VPLEX"]
        rpA["RecoverPoint\nCluster A"]
    end
    subgraph "Site B — DR Standby"
        rpB["RecoverPoint\nCluster B"]
        dirB["VPLEX Cluster-2"]
        hostB["Hosts\nInactive until failover"]
    end

    hostA -->|"FC I/O"| dirA
    dirA --> rpSplitter
    rpSplitter -->|"async journal\nWAN — any distance"| rpA
    rpA -->|"journal replication"| rpB
    rpB --> dirB
    dirB -.->|"volumes activated\nafter RP failover"| hostB
```

### Failover Procedure (Geo)

1. Initiate RecoverPoint failover for the target consistency group (from RecoverPoint management interface).
2. RecoverPoint applies the journal to bring Site B up to the latest consistent image.
3. VPLEX Cluster-2 at Site B activates the volumes for host access.
4. Update host storage views at Site B if required (for pre-staged DR configurations, views already exist).
5. Re-protect by reversing RecoverPoint replication direction once Site A is restored.

## Unisphere for VPLEX (Web GUI)

Unisphere for VPLEX is the browser-based management interface hosted on the VMS. It provides a graphical alternative to `vplexcli` for common operations.

| Capability | Location in Unisphere |
|---|---|
| Cluster and director health | Dashboard → System Health |
| Virtual volume provisioning | Storage → Virtual Volumes |
| Storage view management | Storage → Storage Views |
| Consistency group management | Storage → Consistency Groups |
| Distributed device status | Metro → Distributed Devices |
| Alert configuration (SMTP, SNMP) | Settings → Alerts |
| LDAP/AD authentication | Settings → Authentication |
| Support bundle collection | System → Support |

Access: `https://<VMS_IP>/` — authenticate with local VMS credentials or LDAP-integrated credentials if configured.

**Recommendation**: Use `vplexcli` for scripted operations and automation; use Unisphere for visual health checks and initial investigation. All configuration changes performed through Unisphere are executed as vplexcli commands internally and are logged identically.

## Dell CloudIQ / APEX AIOps

VPLEX can be integrated with Dell CloudIQ (now APEX AIOps) for proactive health monitoring, capacity analytics, and predictive failure detection.

### Enabling CloudIQ Integration

1. Log in to Unisphere for VPLEX.
2. Navigate to **Settings → CloudIQ** (or equivalent in the installed GeoSynchrony version).
3. Enter the CloudIQ connectivity token provided from the CloudIQ portal.
4. Confirm that VMS has outbound HTTPS connectivity to `cloudiq.dell.com`.
5. Verify telemetry upload status in CloudIQ within 24 hours.

CloudIQ provides:

- System health trending and anomaly detection
- Capacity forecasting per virtual volume and storage pool
- Proactive advisories when VPLEX components approach risk thresholds
- Integration with Dell support case creation from CloudIQ alerts

## SNMP and Syslog Alerting

VPLEX can send SNMP traps and forward syslog events to external monitoring platforms (Nagios, Zabbix, Splunk, Elastic, etc.).

### SNMP Configuration

Configure SNMP trap recipients in Unisphere → Settings → SNMP:

- VPLEX supports SNMP v2c and v3.
- Import the VPLEX MIB into your NMS (available from Dell Support portal under VPLEX downloads).
- Test trap delivery after configuration by forcing a minor health check warning.

### Syslog Forwarding

Forward VMS syslog to the centralised SIEM or log aggregator:

```bash
# On VMS (as root or admin), add a syslog forward rule:
# /etc/rsyslog.d/vplex-siem.conf  (example for rsyslog)
*.* @<SIEM_IP>:514

# Restart rsyslog to apply
systemctl restart rsyslog
```

Key log sources to forward:

| Log | Path on VMS | Content |
|---|---|---|
| vplexcli command history | `/var/log/VPlex/cli/vplexcli.log` | All CLI commands; critical for audit trail |
| Management events | `/var/log/VPlex/vplexmanagement.log` | Configuration changes, director events |
| Unisphere web UI | `/var/log/VPlex/` | Web authentication and API events |

---

## See also

- [Vplex — How It Works](../how-it-works/)
- [Vplex — Design Standards](../design-standards/)
