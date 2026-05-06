# Superna Eyeglass Architecture

Superna Eyeglass is a DR orchestration platform purpose-built for NetApp PowerScale (Isilon). It is deployed as a virtual appliance pair — one at the primary site and one at the DR site — each running as an OVA on VMware or Hyper-V. Eyeglass continuously monitors SyncIQ replication policies and maintains a mirrored view of share, quota, and DNS configuration to enable orchestrated failover without manual reconfiguration steps.

During a failover event, Eyeglass executes share and quota reconfiguration on the DR cluster and performs DNS cutover automatically, reducing RTO to minutes for PowerScale-hosted file services.

| Component | Role | Location |
|---|---|---|
| Eyeglass Primary Appliance | Monitor SyncIQ, policy sync, orchestration control plane | Primary site |
| Eyeglass DR Appliance | Standby orchestration node; takes over during failover | DR site |
| PowerScale SyncIQ | Data replication engine (underlying replication) | Both sites |
| DNS Integration | Automated DNS zone cutover during failover | Primary / DR DNS servers |
| Eyeglass Admin UI | Web-based management, DR readiness dashboard, failover initiation | Accessed from management network |
