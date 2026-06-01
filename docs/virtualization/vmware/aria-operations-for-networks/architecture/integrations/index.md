# Aria Operations for Networks — Integrations


<div class="kb-summary">
Integrations reference covering NSX-T Integration, Physical Switch Integration — NetFlow/IPFIX, vDS IPFIX (ESXi Distributed Switch), NSX-T Built-In IPFIX, Palo Alto Firewall Integration and 2 more sections.
</div>

## NSX-T Integration

AON connects to NSX-T Manager with a **read-only** service account. The Collector polls the NSX-T API on a 10-minute interval (default).

**Data pulled from NSX-T:**

| API Endpoint | Data |
|---|---|
| `/api/v1/logical-switches` | Overlay logical switches and their VNIs |
| `/api/v1/logical-ports` | Logical port to VM attachment mapping |
| `/api/v1/ns-groups` / `/policy/api/v1/infra/domains/default/groups` | Security group membership |
| `/api/v1/firewall/sections` / `/policy/api/v1/infra/domains/default/security-policies` | DFW rule sections and rules |
| `/api/v1/logical-routers` / `/policy/api/v1/infra/tier-0s` | T0/T1 router topology |
| `/api/v1/logical-router-ports` | Router interface IPs |
| `/api/v1/transport-nodes` | Host transport node registration |
| `/policy/api/v1/infra/tags` | NSX tag inventory |
| `/api/v1/cluster` | NSX Manager cluster health |

NSX-T 3.2+ uses the Policy API (`/policy/api/v1`). AON automatically detects the NSX-T version and switches between Manager API and Policy API where needed. NSX-T 4.x is fully supported via Policy API only.

**Adding NSX-T as a data source (UI):**

Settings → Accounts and Data Sources → Add Source → NSX-T Manager

Required fields:
- NSX-T Manager FQDN or IP
- Username / Password (dedicated read-only account)
- Nickname for display in AON UI

**Minimum NSX-T role required:** Assign the built-in `Auditor` role to the service account. This provides read-only access to DFW rules, security groups, segments, and transport nodes.

```bash
# Verify NSX-T API connectivity from Collector VM
curl -k -u 'svc-aon:PASSWORD' \
  https://nsxmgr.example.local/api/v1/cluster \
  -o /dev/null -w "HTTP %{http_code}\n"
# Expected: HTTP 200

# Verify Policy API access (NSX-T 3.2+)
curl -k -u 'svc-aon:PASSWORD' \
  https://nsxmgr.example.local/policy/api/v1/infra/tier-0s \
  -o /dev/null -w "HTTP %{http_code}\n"
```
```
┌────────────────────────────────────────── vRNI Integrations ──────────────────────────────────────────┐
│                                                                                                       │
│  NSX-T, vCenter, AWS/Azure, Splunk, and ServiceNow integrations for vRNI.                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             VMware Integrations              │  │              Cloud Integrations             │   │
│   │           NSX-T: IPFIX + DFW rules           │  │           AWS: VPC Flow Logs + IAM          │   │
│   │         vCenter: VM inventory + tags         │  │             Azure: NSG flow logs            │   │
│   │           vRNI API → vROps metrics           │  │            GCP: VPC flow support            │   │
│   │           vIDM: SSO authentication           │  │          Cloud: read-only IAM role          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  VMware and cloud sources feed flows; 3rd-party tools consume vRNI alerts and data.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           SIEM / ITSM Integration            │  │           Physical Network Sources          │   │
│   │          Splunk: syslog / REST push          │  │           Cisco: SNMP + NetFlow v9          │   │
│   │          ServiceNow: alert webhook           │  │             Arista: IPFIX + eAPI            │   │
│   │           Email: SMTP alert notify           │  │           Dell/Brocade: SNMP poll           │   │
│   │          REST API: external queries          │  │          Palo Alto: firewall flows          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform + collectors on vSphere; physical switches and firewalls as flow sources               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NSX-T Data Source   = vRNI connection using NSX API credentials for DFW rules + IPFIX                │
│  vCenter Data Source = vRNI connection using vCenter API for VM inventory and tags                    │
│  VPC Flow Logs       = AWS/Azure cloud flow records ingested via cloud data source type               │
│  SNMP                = Protocol used to poll physical switch interface stats and topology             │
│  NetFlow v9          = Cisco flow export protocol version; widely supported by switches               │
│  IPFIX               = RFC 7011 standard flow export; used by NSX-T and modern hardware               │
│  Splunk Integration  = vRNI pushes alerts via syslog or REST webhook to Splunk HEC                    │
│  ServiceNow Webhook  = HTTP POST from vRNI alert to ServiceNow event intake endpoint                  │
│  vIDM SSO            = VMware Identity Manager; federated login for vRNI web console                  │
│  REST API            = vRNI northbound API for external tools to query flows and entities             │
│  IAM Role            = Cloud read-only role allowing vRNI to fetch VPC/NSG flow logs                  │
│  eAPI                = Arista EOS API used by vRNI for topology and flow collection                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

## Physical Switch Integration — NetFlow/IPFIX

### Cisco IOS-XE — NetFlow v9

```ios
! Step 1: Define the exporter
flow exporter AON-EXPORTER
 destination 10.10.10.50
 source GigabitEthernet0/0/0
 transport udp 2055
 export-protocol netflow-v9
 template data timeout 60
 option interface-table timeout 60
 option application-table timeout 60
!
! Step 2: Define a flow record
flow record AON-RECORD
 match ipv4 source address
 match ipv4 destination address
 match transport source-port
 match transport destination-port
 match ip protocol
 match ip tos
 match interface input
 collect counter bytes long
 collect counter packets long
 collect timestamp sys-uptime first
 collect timestamp sys-uptime last
 collect transport tcp flags
!
! Step 3: Define the flow monitor
flow monitor AON-MONITOR
 exporter AON-EXPORTER
 cache timeout active 60
 cache timeout inactive 15
 record AON-RECORD
!
! Step 4: Apply to uplink/access interfaces
interface GigabitEthernet1/0/1
 ip flow monitor AON-MONITOR input
 ip flow monitor AON-MONITOR output
!
! Verification
show flow exporter AON-EXPORTER statistics
show flow monitor AON-MONITOR cache
show flow monitor AON-MONITOR statistics
```

### Cisco NX-OS — NetFlow v9

```nxos
feature netflow

flow exporter AON-EXPORTER
  destination 10.10.10.50 use-vrf management
  source mgmt0
  transport udp 2055
  version 9
    template data timeout 60
    option interface-table timeout 60

flow record AON-RECORD
  match ipv4 source address
  match ipv4 destination address
  match transport source-port
  match transport destination-port
  match ip protocol
  collect counter bytes long
  collect counter packets long
  collect timestamp sys-uptime first
  collect timestamp sys-uptime last

flow monitor AON-MONITOR
  record AON-RECORD
  exporter AON-EXPORTER
  cache timeout active 60
  cache timeout inactive 15

interface Ethernet1/1
  ip flow monitor AON-MONITOR input
  ip flow monitor AON-MONITOR output

show flow exporter AON-EXPORTER
show flow monitor AON-MONITOR statistics
```

### Arista EOS — IPFIX

```eos
flow tracking hardware
   tracker AON-TRACKER
      record export on inactive timeout 15
      record export on active timeout 60
      exporter AON
         collector 10.10.10.50
         local interface Management1
         transport udp 2055
         export-protocol ipfix
         template interval 60
   !
   interface Ethernet1 tracked
   interface Ethernet2 tracked
   interface Ethernet3 tracked
!
show flow tracking hardware tracker AON-TRACKER
show flow tracking hardware detail
```

### Juniper Junos — NetFlow v9

```junos
# Configure sampling
set forwarding-options sampling input rate 1
set forwarding-options sampling family inet output flow-server 10.10.10.50 port 2055
set forwarding-options sampling family inet output flow-server 10.10.10.50 version9 template ipv4
set forwarding-options sampling family inet output flow-inactive-timeout 15
set forwarding-options sampling family inet output flow-active-timeout 60
set forwarding-options sampling family inet output source-address 10.10.0.1

# Apply to interfaces
set interfaces ge-0/0/0 unit 0 family inet sampling input
set interfaces ge-0/0/0 unit 0 family inet sampling output
set interfaces ge-0/0/1 unit 0 family inet sampling input
set interfaces ge-0/0/1 unit 0 family inet sampling output

# Verify
show services flow-monitoring version9 template
show services flow-monitoring statistics
```

## vDS IPFIX (ESXi Distributed Switch)

Capturing east-west VM traffic within an ESXi cluster without physical switch changes requires IPFIX on the vDS.

**vCenter UI path:** Networking → Select vDS → Configure → NetFlow

| Field | Value |
|---|---|
| Collector IP | Collector VM IP |
| Collector Port | 2055 |
| Observation Domain ID | 0 (or any unique value per vDS) |
| Active Flow Timeout | 60 (seconds) |
| Idle Flow Timeout | 15 (seconds) |
| Sampling Rate | 0 (every packet) or higher (1000 = 1:1000) |
| Process internal flows only | Disabled (to see inter-host traffic) |

Via PowerCLI:

```powershell
$vds = Get-VDSwitch -Name "vDS-Production"
$configSpec = New-Object VMware.Vim.VMwareDVSConfigSpec
$configSpec.configVersion = $vds.ExtensionData.Config.ConfigVersion

$ipfix = New-Object VMware.Vim.VMwareIpfixConfig
$ipfix.collectorIpAddress = "10.10.10.50"
$ipfix.collectorPort       = 2055
$ipfix.observationDomainId = 0
$ipfix.activeFlowTimeout   = 60
$ipfix.idleFlowTimeout     = 15
$ipfix.samplingRate        = 0
$ipfix.internalFlowsOnly   = $false

$configSpec.ipfixConfig = $ipfix
$vds.ExtensionData.ReconfigureDvs($configSpec)

# Enable IPFIX on specific portgroups
Get-VDPortgroup -VDSwitch $vds | Where-Object { $_.Name -match "^PG-(App|Web|DB)" } | ForEach-Object {
    $pgSpec = New-Object VMware.Vim.DVPortgroupConfigSpec
    $pgSpec.configVersion = $_.ExtensionData.Config.ConfigVersion
    $pgSpec.defaultPortConfig = New-Object VMware.Vim.VMwareDVSPortSetting
    $pgSpec.defaultPortConfig.ipfixEnabled = New-Object VMware.Vim.BoolPolicy
    $pgSpec.defaultPortConfig.ipfixEnabled.inherited = $false
    $pgSpec.defaultPortConfig.ipfixEnabled.value = $true
    $_.ExtensionData.ReconfigureDVPortgroup($pgSpec)
    Write-Host "Enabled IPFIX on $($_.Name)"
}
```

## NSX-T Built-In IPFIX

NSX-T can export IPFIX directly from the nsx-vswitch on each transport node, capturing overlay traffic without any changes to the physical fabric.

**NSX-T Policy UI:** System → Fabric → Settings → IPFIX Collector Profiles → Add

Or via NSX-T API:

```bash
curl -k -u 'admin:PASSWORD' -X POST \
  https://nsxmgr.example.local/policy/api/v1/infra/ipfix-l2-collector-profiles/AON-COLLECTOR \
  -H 'Content-Type: application/json' \
  -d '{
    "display_name": "AON-Collector",
    "ipfix_collector_profile_parameters": {
      "ipfix_collector": [
        {"ip_address": "10.10.10.50", "port": 2055}
      ]
    }
  }'

# Create IPFIX L2 profile
curl -k -u 'admin:PASSWORD' -X POST \
  https://nsxmgr.example.local/policy/api/v1/infra/ipfix-l2-profiles/AON-PROFILE \
  -H 'Content-Type: application/json' \
  -d '{
    "display_name": "AON-IPFIX-Profile",
    "ipfix_collector_profile_path": "/infra/ipfix-l2-collector-profiles/AON-COLLECTOR",
    "active_timeout": 60,
    "idle_timeout": 15,
    "packet_sample_probability": 1.0
  }'
```

Assign the IPFIX profile to a segment, binding to transport nodes.

## Palo Alto Firewall Integration

AON ingests Palo Alto traffic logs via two methods:

**Method 1: Syslog forwarding to Collector**

PAN-OS: Device → Server Profiles → Syslog → Add

```yaml
Name: AON-Syslog
Syslog Server IP: 10.10.10.50
Transport: UDP
Port: 514
Format: BSD
Facility: LOG_USER
```

Create a Log Forwarding Profile (Objects → Log Forwarding) referencing AON-Syslog for traffic logs, then attach to all Security policy rules.

**Method 2: Panorama API** — Add Panorama as a data source; AON queries traffic logs via the XML API. This avoids syslog and centralizes collection.

**Adding in AON UI:** Settings → Accounts and Data Sources → Add Source → Palo Alto Networks → Panorama or NGFW

Required credentials: admin-level API key or dedicated account with `Log Viewer` access.

## ServiceNow CMDB Integration

AON correlates discovered VMs and network devices with ServiceNow CMDB CI records to add business context to topology views.

**UI path:** Settings → Integrations → ServiceNow

| Field | Value |
|---|---|
| ServiceNow Instance URL | `https://yourinstance.service-now.com` |
| Username | ServiceNow user with `cmdb_read` role |
| Password | — |
| Sync Interval | 24 hours (default) |

Correlation logic: IP address and hostname matching between AON-discovered assets and ServiceNow CI records. Matched CIs surface in AON VM detail views with CMDB metadata (owner, environment, service, support group).

## Syslog and SIEM Forwarding

AON can forward alerts and events outbound to a syslog receiver or SIEM.

**UI path:** Settings → Notifications → Syslog → Add

| Field | Value |
|---|---|
| Server | SIEM IP or FQDN |
| Port | 514 (UDP default) or 6514 (TLS) |
| Protocol | UDP / TCP / TLS |
| Format | RFC 3164 or RFC 5424 |

Events forwarded: new problem detected, alert threshold crossed, data source sync failure, collector disconnected.

**Webhook integration:**

Settings → Notifications → Webhook → Add

```json
{
  "url": "https://hooks.slack.com/services/T000/B000/xxxx",
  "method": "POST",
  "headers": {"Content-Type": "application/json"},
  "body_template": "{\"text\": \"[AON] {{severity}}: {{alert_name}} — {{description}}\"}"
}
```

PagerDuty integration is available as a built-in notification type in AON 6.x+.
