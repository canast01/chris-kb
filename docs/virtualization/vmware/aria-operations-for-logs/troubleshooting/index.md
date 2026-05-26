# Aria Ops for Logs — Troubleshooting

┌───────────────────────────────────── Aria Logs — Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Agents not sending logs: check agent connectivity, firewall rules, and agent configuration  │   │
│   │    Missing log sources: verify syslog UDP/TCP port reachability and source IP configuration   │   │
│   │     Disk full blocking ingestion: expand disk or reduce retention; clear oldest partitions    │   │
│   │      Alert not firing: validate field extraction in content pack; check query match logic     │   │
│   │     vRLI support bundle collects cluster and agent logs; attach to GSS case for escalation    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues triage agent and source faults · diagnostics use logs and API                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │      Agent not sending      │  │       Admin UI sources      │  │      vRLI support bndl      │   │
│   │        Source missing       │  │       Agent log files       │  │        GSS case open        │   │
│   │          Disk full          │  │     /var/log/loginsight     │  │       Agent config exp      │   │
│   │        Alert not fire       │  │        REST API debug       │  │       Log sample coll       │   │
│   │         Query empty         │  │        Source status        │  │        TAM escalation       │   │
│   │        Forwarder err        │  │       Content pk test       │  │        Version matrix       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics use source admin and log paths                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │   Agent silent   │  Agent log file  │/var/log/loginsight│   vRLI bundle    │  Restart agent   │   │
│   │    Disk full     │  Source status   │ /var/log/li-server│   GSS P1 case    │   Expand disk    │   │
│   │  Alert not fire  │   REST API dbg   │   /var/log/agent  │   TAM escalate   │   Retune alert   │   │
│   │   Query empty    │ Content pk test  │  /var/log/server  │  Version matrix  │  Fix time range  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (cluster) · RAM DIMMs · Network NICs · Log storage · Syslog source hosts                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vRLI agent         = Host-based log forwarder; check agent service status and firewall on port 9000  │
│  Syslog source      = Network device or host sending UDP/TCP syslog; verify source IP is allowed      │
│  Disk retention     = Policy deleting oldest partitions at threshold; full disk blocks all ingestion  │
│  Alert pipeline     = Log-match rule; fails silently if field extraction is incorrect in content pack │
│  VLQL query         = Query returning empty if time range, field name, or syntax is incorrect         │
│  Content pack       = Field extractor and dashboard bundle; test via UI to validate regex patterns    │
│  Log forwarder      = SIEM stream; errors if destination unreachable or certificate mismatch          │
│  Ingestion rate     = Events-per-second; drop to zero indicates cluster issue or source problem       │
│  Cluster node health = Admin dashboard showing master and worker node status and disk usage           │
│  REST API debug     = Query the vRLI API directly to bypass UI and validate field extraction          │
│  Support bundle     = Full diagnostic archive: cluster logs, config, and event data for GSS review    │
│  Agent configuration = JSON config file on host specifying cluster address, port, and log paths       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌───────────────────────────────────── Aria Logs — Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Agents not sending logs: check agent connectivity, firewall rules, and agent configuration  │   │
│   │    Missing log sources: verify syslog UDP/TCP port reachability and source IP configuration   │   │
│   │     Disk full blocking ingestion: expand disk or reduce retention; clear oldest partitions    │   │
│   │      Alert not firing: validate field extraction in content pack; check query match logic     │   │
│   │     vRLI support bundle collects cluster and agent logs; attach to GSS case for escalation    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues triage agent and source faults · diagnostics use logs and API                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │      Agent not sending      │  │       Admin UI sources      │  │      vRLI support bndl      │   │
│   │        Source missing       │  │       Agent log files       │  │        GSS case open        │   │
│   │          Disk full          │  │     /var/log/loginsight     │  │       Agent config exp      │   │
│   │        Alert not fire       │  │        REST API debug       │  │       Log sample coll       │   │
│   │         Query empty         │  │        Source status        │  │        TAM escalation       │   │
│   │        Forwarder err        │  │       Content pk test       │  │        Version matrix       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics use source admin and log paths                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │   Agent silent   │  Agent log file  │/var/log/loginsight│   vRLI bundle    │  Restart agent   │   │
│   │    Disk full     │  Source status   │ /var/log/li-server│   GSS P1 case    │   Expand disk    │   │
│   │  Alert not fire  │   REST API dbg   │   /var/log/agent  │   TAM escalate   │   Retune alert   │   │
│   │   Query empty    │ Content pk test  │  /var/log/server  │  Version matrix  │  Fix time range  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (cluster) · RAM DIMMs · Network NICs · Log storage · Syslog source hosts                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vRLI agent         = Host-based log forwarder; check agent service status and firewall on port 9000  │
│  Syslog source      = Network device or host sending UDP/TCP syslog; verify source IP is allowed      │
│  Disk retention     = Policy deleting oldest partitions at threshold; full disk blocks all ingestion  │
│  Alert pipeline     = Log-match rule; fails silently if field extraction is incorrect in content pack │
│  VLQL query         = Query returning empty if time range, field name, or syntax is incorrect         │
│  Content pack       = Field extractor and dashboard bundle; test via UI to validate regex patterns    │
│  Log forwarder      = SIEM stream; errors if destination unreachable or certificate mismatch          │
│  Ingestion rate     = Events-per-second; drop to zero indicates cluster issue or source problem       │
│  Cluster node health = Admin dashboard showing master and worker node status and disk usage           │
│  REST API debug     = Query the vRLI API directly to bypass UI and validate field extraction          │
│  Support bundle     = Full diagnostic archive: cluster logs, config, and event data for GSS review    │
│  Agent configuration = JSON config file on host specifying cluster address, port, and log paths       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>
