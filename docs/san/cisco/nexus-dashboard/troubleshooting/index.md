---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
---
# Cisco Nexus Dashboard — Troubleshooting


<div class="kb-summary">
Diagnosing Nexus Dashboard site onboarding failures, fabric health alerts, flow collection gaps, and connectivity issues.

*Applies to: Cisco MDS · Nexus*
</div>

```text
┌─────────────────────────────── Cisco Nexus Dashboard — Troubleshooting ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         ND troubleshooting: app failures, cluster quorum loss, site onboarding errors         │   │
│   │         App not starting: check node resources (CPU/RAM), pod logs, app compatibility         │   │
│   │           Quorum loss: 2+ masters down → read-only mode; restore third node quickly           │   │
│   │       Site fail: verify Data VLAN reachability, APIC/switch credentials, firewall rules       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom → Admin UI events → kubectl pod logs → network test → resolve → verify                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          App Issues         │  │        Cluster Issues       │  │         Site Issues         │   │
│   │       App not starting      │  │        Node unhealthy       │  │         Onboard fail        │   │
│   │        App crash loop       │  │         Quorum loss         │  │        Cred rejected        │   │
│   │       Resource exhaust      │  │        Node isolated        │  │         Data NW fail        │   │
│   │         App UI down         │  │         Storage full        │  │        Firewall block       │   │
│   │        App compat err       │  │         Cert expired        │  │       Site stale data       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Use ND Admin > Events and kubectl logs for app pods; SSH to node for cluster-level diag            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │   First check    │    Key command    │    Resolution    │    Escalation    │   │
│   │     App down     │  Node resources  │    kubectl logs   │    Add worker    │    TAC + logs    │   │
│   │   Quorum loss    │   Node status    │    ND Admin UI    │   Restore node   │    TAC urgent    │   │
│   │    Site fails    │   Ping Data IP   │    curl APIC IP   │   Fix network    │    TAC + pcap    │   │
│   │   Cert expired   │    Admin>Sec.    │     Cert dates    │    Renew cert    │  TAC if locked   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ND VM compute (vCPU/RAM) · Data NIC connectivity · OOB switch port state                 │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    kubectl logs    = View pod container log; run from ND master node SSH session                      │
│    App crash loop  = Pod repeatedly starts then fails; check logs for OOM or config error             │
│    Quorum loss     = Fewer than 2 master nodes reachable; ND enters read-only protection              │
│    Node isolated   = Master node cannot reach peers; network partition or NIC failure                 │
│    Storage full    = ND etcd or PVC storage full; app pods fail; expand or clean up data              │
│    Cert expired    = ND TLS cert past expiry; browser blocks access; renew immediately                │
│    Site onboard fail = ND cannot reach APIC or switch via Data VLAN; check MTU, routing               │
│    Cred rejected   = Site credentials (APIC admin/password) wrong or account locked                   │
│    Resource exhaust = App pods OOMKilled due to insufficient RAM on cluster; add worker               │
│    App compat err  = Installed app version incompatible with ND release; upgrade ND first             │
│    Data NW fail    = ND Data VLAN cannot reach fabric; check VLAN tagging, routing, MTU               │
│    Stale site data = ND shows outdated fabric topology; re-trigger site discovery                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known problems, symptoms, and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to Cisco TAC with the right data.</span>
</a>

</div>

