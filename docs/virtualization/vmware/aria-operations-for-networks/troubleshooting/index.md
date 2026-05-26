# Aria Ops for Networks — Troubleshooting

┌─────────────────────────────────── Aria Networks — Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Collector offline and not collecting data; missing flow data gaps in platform analytics    │   │
│   │   Path trace errors for connectivity troubleshooting; NSX data source stale after credential  │   │
│   │     Physical switch collection gaps due to SNMP misconfiguration or firewall blocking SNMP    │   │
│   │    Alert not firing for topology changes; platform UI unresponsive or API returning errors    │   │
│   │  Escalation: support bundle export from Platform UI; GSS case with logs and API debug output  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate data source or platform layer           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │      Collector offline      │  │        Support bundle       │  │        Bundle export        │   │
│   │        Flow data gap        │  │        Collector logs       │  │        GSS case open        │   │
│   │        Path trace err       │  │       Data src status       │  │          Cred reset         │   │
│   │        NSX src stale        │  │        API debug mode       │  │        TAM escalation       │   │
│   │         Phys sw gap         │  │        Flow query dbg       │  │        Version matrix       │   │
│   │        Alert not fire       │  │          SNMP test          │  │         Log collect         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics isolate data source or network layer                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │  Collector down  │  Coll log file   │   /var/log/coll   │  Bundle export   │   Restart coll   │   │
│   │  Flow data gap   │ Data src status  │ /var/log/platform │   GSS P1 case    │   Re-auth src    │   │
│   │  Path trace err  │    API debug     │    /var/log/api   │   TAM escalate   │   Fix routing    │   │
│   │  NSX src stale   │    SNMP test     │  /var/log/nsx-ds  │  Cred rotation   │   Re-sync src    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · NSX/vCenter/switches                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Collector offline      = Collector VM not reachable or service stopped; no data flows to Platform VM │
│  Flow data gap         = Missing time range in flow analytics; caused by Collector outage or data     │
│  Path trace engine     = Aria Networks component that computes end-to-end path using topology and     │
│  NSX data source       = Configured NSX connection; becomes stale if credentials change without       │
│  SNMP collection       = Physical switch polling via SNMP; gaps caused by cred mismatch or firewall   │
│  Support bundle        = Diagnostic archive generated from Platform UI; contains logs and             │
│  API debug mode        = Verbose logging mode for REST API requests; helps diagnose query and auth    │
│  Data source re-authentication = Process of re-entering credentials for a stale NSX/vCenter data      │
│  Platform restart      = Service or VM restart of the Platform appliance to recover from unresponsive │
│  Credential rotation   = Update of service account passwords requiring re-auth of all affected data   │
│  Version compatibility  = Aria Networks to NSX/vCenter version matrix; mismatch can cause collection  │
│  Stale topology        = Outdated network map caused by data source not syncing; resolve by           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────── Aria Networks — Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Collector offline and not collecting data; missing flow data gaps in platform analytics    │   │
│   │   Path trace errors for connectivity troubleshooting; NSX data source stale after credential  │   │
│   │     Physical switch collection gaps due to SNMP misconfiguration or firewall blocking SNMP    │   │
│   │    Alert not firing for topology changes; platform UI unresponsive or API returning errors    │   │
│   │  Escalation: support bundle export from Platform UI; GSS case with logs and API debug output  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate data source or platform layer           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │      Collector offline      │  │        Support bundle       │  │        Bundle export        │   │
│   │        Flow data gap        │  │        Collector logs       │  │        GSS case open        │   │
│   │        Path trace err       │  │       Data src status       │  │          Cred reset         │   │
│   │        NSX src stale        │  │        API debug mode       │  │        TAM escalation       │   │
│   │         Phys sw gap         │  │        Flow query dbg       │  │        Version matrix       │   │
│   │        Alert not fire       │  │          SNMP test          │  │         Log collect         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics isolate data source or network layer                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │  Collector down  │  Coll log file   │   /var/log/coll   │  Bundle export   │   Restart coll   │   │
│   │  Flow data gap   │ Data src status  │ /var/log/platform │   GSS P1 case    │   Re-auth src    │   │
│   │  Path trace err  │    API debug     │    /var/log/api   │   TAM escalate   │   Fix routing    │   │
│   │  NSX src stale   │    SNMP test     │  /var/log/nsx-ds  │  Cred rotation   │   Re-sync src    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · NSX/vCenter/switches                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Collector offline      = Collector VM not reachable or service stopped; no data flows to Platform VM │
│  Flow data gap         = Missing time range in flow analytics; caused by Collector outage or data     │
│  Path trace engine     = Aria Networks component that computes end-to-end path using topology and     │
│  NSX data source       = Configured NSX connection; becomes stale if credentials change without       │
│  SNMP collection       = Physical switch polling via SNMP; gaps caused by cred mismatch or firewall   │
│  Support bundle        = Diagnostic archive generated from Platform UI; contains logs and             │
│  API debug mode        = Verbose logging mode for REST API requests; helps diagnose query and auth    │
│  Data source re-authentication = Process of re-entering credentials for a stale NSX/vCenter data      │
│  Platform restart      = Service or VM restart of the Platform appliance to recover from unresponsive │
│  Credential rotation   = Update of service account passwords requiring re-auth of all affected data   │
│  Version compatibility  = Aria Networks to NSX/vCenter version matrix; mismatch can cause collection  │
│  Stale topology        = Outdated network map caused by data source not syncing; resolve by           │
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
