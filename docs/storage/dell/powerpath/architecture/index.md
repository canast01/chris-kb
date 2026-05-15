# PowerPath — Architecture

<div class="kb-summary">
Host-side multipath I/O driver for Dell/EMC arrays. Intercepts block I/O and distributes it across all available HBA paths with ALUA-aware load balancing (CLAROpt policy) and automatic sub-millisecond failover on path loss.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with PowerMax, Unity, and host OS multipath frameworks.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Path count requirements, CLAROpt policy standards, and installation best practices.</span></a>
</div>

## Load-Balancing Policies

| Policy | Code | Description |
|---|---|---|
| CLAROpt | `co` | ALUA-aware; prefers active-optimised paths — recommended for all Dell arrays |
| RoundRobin | `rr` | Even distribution across all paths regardless of ALUA state |
| BasicFailover | `bf` | Single active path; failover only — no load balancing |

## Host-Side MPIO Stack

```mermaid
graph LR
  HOST(["Host — Linux / Windows / VMware"]) --> PP["PowerPath\n(MPIO driver)"]
  PP --> P1["HBA0 → Fabric A → SP-A"]
  PP --> P2["HBA0 → Fabric A → SP-B"]
  PP --> P3["HBA1 → Fabric B → SP-A"]
  PP --> P4["HBA1 → Fabric B → SP-B"]
  P1 & P2 & P3 & P4 --> ARRAY["Storage Array\nPowerMax / Unity"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PP net
  class P1,P2,P3,P4 net
  class HOST host
  class ARRAY ctrl
```
