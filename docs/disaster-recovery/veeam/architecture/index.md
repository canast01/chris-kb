# Veeam — Architecture

<div class="kb-summary">
Veeam Backup & Replication architecture — Backup Server manages scheduling, Proxies handle data movement via VADP or agent, and SOBR provides tiered storage with immutable object offload.
</div>

![Veeam Architecture](../../../assets/veeam-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Proxy transport modes, SOBR tiers, supported platforms, retention schedule, and sizing.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware vSphere, Hyper-V, physical agents, and cloud (AWS/Azure) integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Job naming, retention schedule, SOBR design, proxy placement, and immutability settings.</span></a>
</div>

| Component | Role |
|---|---|
| Backup Server | Management, scheduler, config DB; Windows Server + SQL |
| Backup Proxy | Data mover; reads VM data via VADP (hot-add, Direct NFS, NBD) or agent |
| Backup Repository | Target storage for .vbk/.vib backup files |
| Scale-Out Backup Repository (SOBR) | Tiered pool: performance extent (fast disk) + capacity tier (object storage) |
| Veeam ONE | Monitoring, alerting, and reporting; separate server |

```mermaid
graph TB
  ADMIN(["Backup Admin"]) -->|"console"| VBR["Veeam Backup & Replication Server"]
  VBR --> PROXY["Backup Proxy\n(data mover)"]
  VCTR(["VMware vCenter\nsource VMs"]) --> PROXY
  PROXY --> REPO[("SOBR\nperformance tier — fast disk")]
  REPO -->|"auto-offload"| OBJ[("Capacity Tier\nS3 / immutable object")]
  OBJ -->|"archive tier"| GLACIER[("Glacier / Archive\nyearly retention")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  class VBR,PROXY ctrl
  class REPO store
  class VCTR,ADMIN host
  class OBJ,GLACIER cloud
```
