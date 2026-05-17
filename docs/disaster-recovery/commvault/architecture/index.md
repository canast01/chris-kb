# Commvault — Architecture

<div class="kb-summary">
Commvault architecture reference — CommServe topology, MediaAgent deduplication, storage library types, multi-site design, and port requirements.
</div>

![Commvault Architecture](../../../../assets/commvault-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>CommServe topology, MediaAgent dedup, storage library types, multi-site design, and port requirements.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware, cloud storage, NDMP, and third-party integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, retention schedule, DDB standards, and VMware backup settings.</span></a>
</div>

| Component | Role |
|---|---|
| CommServe | Command and control; SQL DB; HA pair for critical environments |
| MediaAgent | Data movement and deduplication (DDB); one DDB per storage pool |
| Client | Backup agent (Windows, Linux, VSA for VMware vSphere) |
| Command Center | Web UI (port 443); replaces legacy Java GUI in FR32+ |

```mermaid
graph TB
  CS["CommServe\n(command & control)"] --> WEBCON["Web Console\n& Command Center"]
  MA1["Media Agent 1\n(data mover)"] & MA2["Media Agent 2"] --> CS
  SRC(["Source — VMs / DBs / Files"]) --> MA1 & MA2
  MA1 & MA2 --> DISK[("Disk Library\nDDB dedup")]
  DISK -->|"aux copy"| TAPE[("Tape / Object\nlong-term retention")]
  ADMIN(["Backup Admin"]) --> WEBCON
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class CS,MA1,MA2 ctrl
  class DISK,TAPE store
  class SRC,ADMIN host
  class WEBCON mgmt
```
