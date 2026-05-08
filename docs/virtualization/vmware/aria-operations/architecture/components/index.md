# Aria Operations — Components

## Sizing Guidelines

| Deployment Size | Nodes | VMs Monitored |
|----------------|-------|---------------|
| Small | Primary only | Up to ~1,500 VMs |
| Medium | Primary + Replica | Up to ~3,000 VMs |
| Large | Primary + Replica + 2 Data Nodes | Up to ~10,000 VMs |
| XL | Additional data nodes | 10,000+ VMs |

## Network Ports

| Port | Protocol | Direction | Purpose |
|------|----------|-----------|---------|
| 443 | TCP | Inbound | UI and API access |
| 443 | TCP | Outbound | vCenter adapter, cloud proxies |
| 4505/4506 | TCP | Inbound | Remote collector communication |
| 514 | UDP | Outbound | Syslog forwarding (optional) |
