# Aria Ops for Logs — Integrations

```text
┌─────────────────────────────────────────────────────────────┐
│         Aria Ops for Logs Integration Map                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────┐  syslog UDP 514   ┌────────────────────┐     │
│  │  ESXi     │ ────────────────► │                    │     │
│  │  vCenter  │ ────────────────► │  Aria Ops for Logs │     │
│  │  NSX-T    │ ────────────────► │  (Master + Workers)│     │
│  │  Linux VMs│ ─cfapi TLS 9543─► │                    │     │
│  │  Win VMs  │ ─cfapi TLS 9543─► │                    │     │
│  │  Net devs │ ─SNMP trap 162──► │                    │     │
│  └───────────┘                   └──────────┬─────────┘     │
│                                             │               │
│            ┌────────────────────────────────┤               │
│            │                               │                │
│            ▼  bi-directional               ▼                │
│      Aria Operations              ServiceNow / Slack        │
│      (correlated alerts,          (webhook notifications)   │
│       "View Logs" deep link)                                │
└─────────────────────────────────────────────────────────────┘
```

## Integration with Aria Operations (vROps)

Aria Operations for Logs integrates bi-directionally with Aria Operations:

- **Log Insight → Aria Operations**: alerts triggered by log patterns can launch correlated views in Aria Operations, showing which objects are affected
- **Aria Operations → Log Insight**: clicking "View Logs" from an Aria Operations alert opens a pre-filtered Aria Ops for Logs search scoped to the affected object and time window

**Configure the integration:**

In Aria Operations for Logs UI:
```text
Administration → Integrations → Aria Operations → Add vRealize Operations Connection
```

Provide:
- Aria Operations primary node FQDN
- Admin credentials
- Accept the SSL certificate

In Aria Operations, the integration is reflected automatically — a "Logs" badge appears on vSphere object detail pages when correlated log data is available.

---

## vCenter Syslog Integration

Configure vCenter to forward its own syslog and ESXi host syslog to Aria Ops for Logs:

**Configure vCenter syslog via UI:**
```text
vCenter → Administration → Syslog → Add Syslog Target
```
- Protocol: UDP or TCP
- Host: `vrli-prod-01.example.local`
- Port: 514 (UDP syslog) or 1514 (TCP syslog via LI Agent protocol)

**Configure ESXi syslog via PowerCLI (bulk):**
```powershell
$target = "udp://vrli-prod-01.example.local:514"
Get-VMHost | ForEach-Object {
    $esxcli = Get-EsxCli -VMHost $_ -V2
    $esxcli.system.syslog.config.set.Invoke(@{loghost = $target})
    $esxcli.system.syslog.reload.Invoke()
    Write-Host "$($_.Name): syslog configured"
}

# Verify
Get-VMHost | ForEach-Object {
    $esxcli = Get-EsxCli -VMHost $_ -V2
    $cfg = $esxcli.system.syslog.config.get.Invoke()
    Write-Host "$($_.Name): $($cfg.RemoteHost)"
}
```

**Configure ESXi syslog via esxcli (single host):**
```bash
esxcli system syslog config set --loghost="udp://vrli-prod-01.example.local:514"
esxcli system syslog reload
esxcli system syslog config get
```

---

## NSX-T Syslog Integration

Forward NSX Manager and Edge node syslog to Aria Ops for Logs:

```bash
# Via NSX-T API — add syslog exporter on NSX Manager
curl -sk -u 'admin:<password>' -X POST \
  "https://nsx-mgr-01.example.local/api/v1/node/services/syslog/exporters" \
  -H "Content-Type: application/json" \
  -d '{
    "server": "vrli-prod-01.example.local",
    "port": 514,
    "protocol": "UDP",
    "exporter_name": "aria-ops-for-logs",
    "level": "INFO",
    "facility": "USER"
  }'
```

For NSX Edge nodes, apply the syslog configuration via a transport node profile or per-edge configuration in NSX-T Manager UI:
```text
NSX-T UI → Fabric → Nodes → Edge Transport Nodes → select node → Syslog → Add
```

---

## Linux Log Forwarding Agent

Install the Aria Operations for Logs Agent (formerly vRealize Log Insight Agent) on Linux VMs for structured log collection:

```bash
# Download agent from Aria Ops for Logs UI: Administration → Agents → Agent Downloads
# Transfer to target and install
chmod +x VMware-Log-Insight-Agent-*.bin
sudo ./VMware-Log-Insight-Agent-*.bin

# Configure agent — edit /var/lib/loginsight-agent/liagent.ini
[server]
hostname=vrli-prod-01.example.local
port=9543
proto=cfapi
ssl=yes

[storage]
max_disk_mb=200

# Restart agent service
sudo systemctl restart liagentd
sudo systemctl enable liagentd

# Verify connectivity
sudo /usr/lib/loginsight-agent/bin/liagent-binary verify
```

---

## Windows Log Forwarding Agent

```powershell
# Install the agent (MSI)
msiexec /i "VMware-Log-Insight-Agent-*.msi" /quiet SERVERHOST=vrli-prod-01.example.local `
  SERVERPORT=9543 SERVERPROTOCOL=cfapi

# Verify agent service is running
Get-Service -Name "VMware Log Insight Agent"

# Configuration file location on Windows
# C:\ProgramData\VMware\Log Insight Agent\liagent.ini
```

---

## SNMP Trap Receiver

Aria Ops for Logs can receive SNMP traps from network devices (switches, firewalls):

```text
Administration → General → SNMP Traps → Enable SNMP Trap Receiver
```

- Port: 162 (UDP)
- Version: SNMPv2c or SNMPv3
- Community string or credentials

Configure network devices to forward traps to `vrli-prod-01.example.local:162`.

---

## Generic Syslog (TCP/UDP)

Any RFC 5424 or RFC 3164 compliant syslog source can forward to Aria Ops for Logs:

| Protocol | Port | Use Case |
|---|---|---|
| UDP syslog | 514 | Legacy devices, ESXi hosts |
| TCP syslog | 1514 | Reliable delivery, Linux agents |
| cfapi (TLS) | 9543 | LI Agent protocol — encrypted and structured |
| cfapi (no TLS) | 9000 | LI Agent — unencrypted (lab only) |

Ensure firewall permits inbound traffic to Aria Ops for Logs on these ports from the syslog sources.

---

## Webhook / REST API for External Alerting

Aria Ops for Logs alert notifications can POST JSON payloads to external systems (ServiceNow, Slack, PagerDuty):

```text
Administration → Notification Channels → Add Channel → Webhook
```

Provide:
- Webhook URL (e.g., `https://hooks.slack.com/services/...`)
- Authentication headers if required
- Test with a sample payload

Alternatively, use the REST API to query recent alerts for external integration:

```bash
# Get recent critical alerts
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/alerts?severity=critical&limit=20" | \
  jq '.alerts[] | {name: .name, status: .status, timestamp: .timestamp}'
```
