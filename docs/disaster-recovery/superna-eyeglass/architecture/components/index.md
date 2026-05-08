# Superna Eyeglass — Components

## Component Roles

| Component | Role | Location |
|---|---|---|
| Eyeglass Primary Appliance | Monitor SyncIQ policies; sync share/quota config; DR orchestration control plane | Primary site |
| Eyeglass DR Appliance | Standby orchestration node; activates when primary site is unavailable | DR site |
| PowerScale SyncIQ | Underlying data replication engine | Both sites |
| DNS Integration | Automated DNS zone cutover during failover | Primary / DR DNS servers |
| Eyeglass Admin UI | Web-based management (port 443) | Accessed from management network |
