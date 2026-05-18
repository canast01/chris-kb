# Aria Operations for Networks

<div class="kb-summary">
Aria Operations for Networks knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
</div>

```
┌──────────── Aria Operations for Networks: Data Flow ───────────────────────────┐
│                                                                                 │
│  Data Sources                      Collector VM              Platform VM       │
│  ┌─────────────┐  API poll        ┌──────────────┐          ┌──────────────┐  │
│  │  vCenter    ├─────────────────►│              │   TLS    │              │  │
│  ├─────────────┤  API poll        │  Collector   ├─────────►│  Platform    │  │
│  │  NSX-T Mgr  ├─────────────────►│  VM          │  upload  │  VM          │  │
│  ├─────────────┤                  │              │          │              │  │
│  │  Phys Switch├─ NetFlow/IPFIX ─►│  UDP 2055    │          │  Cassandra   │  │
│  │  (Cisco/    │  UDP 2055        │  listener    │          │  Elastic     │  │
│  │  Arista/JNX)│                  │              │          │  PostgreSQL  │  │
│  ├─────────────┤                  └──────────────┘          │  Kafka       │  │
│  │  ESXi vDS   ├─ IPFIX ─────────►(same collector)          └──────┬───────┘  │
│  ├─────────────┤                                                    │          │
│  │  Palo Alto  ├─ syslog/API ────►(collector or direct)            │          │
│  └─────────────┘                                                    │          │
│                                                                      ▼          │
│  Admin/User ──── HTTPS 443 ────────────────────────────────►  UI / REST API   │
│                                       network map │ flow analysis │ microseg    │
└────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
