---
tags:
  - architecture
  - aria-networks
  - vmware
---
# vRNI Integrations
![vRNI Integrations](../../../../assets/virtualization-vmware-aria-operations-for-networks-architect.svg)

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
```yaml
Name: AON-Syslog
Syslog Server IP: 10.10.10.50
Transport: UDP
Port: 514
Format: BSD
Facility: LOG_USER
```
```json
{
  "url": "https://hooks.slack.com/services/T000/B000/xxxx",
  "method": "POST",
  "headers": {"Content-Type": "application/json"},
  "body_template": "{\"text\": \"[AON] {{severity}}: {{alert_name}} — {{description}}\"}"
}
```

## See also

- [Aria Operations for Networks — How It Works](../how-it-works/)
- [Aria Operations for Networks — Deploy](../deploy/)
