# Commvault — Architecture

<div class="kb-summary">
Commvault architecture reference — CommServe topology, MediaAgent deduplication, storage library types, multi-site design, and port requirements.
</div>

![Commvault Architecture](../../../assets/commvault-architecture-overview.svg)

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

