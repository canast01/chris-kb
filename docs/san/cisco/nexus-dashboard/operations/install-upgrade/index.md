```bash
# SSH to node 1 (the designated primary)
ssh ndadmin@nd-dc1-1.corp.example.com

# Initialize the cluster from node 1
acs cluster init \
  --name nd-dc1 \
  --primary-ip 10.10.5.21 \
  --node-ips 10.10.5.22,10.10.5.23 \
  --app-ips 192.168.100.1,192.168.100.2,192.168.100.3

# Monitor cluster formation (takes 10-20 minutes)
acs health
# Wait until all nodes show Healthy
```

```text
┌──────────────────────── Cisco Nexus Dashboard — Operations Install & Upgrade ─────────────────────────┐
│                                                                                                       │
│  ND cluster initial build and rolling upgrade process with pre/post validation steps.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Initial Install                │  │                Prerequisites                │   │
│   │          Deploy OVA/ISO: 3 node min          │  │          Hardware: 16 vCPU/64GB RAM         │   │
│   │         Bootstrap: node 1 as primary         │  │         Storage: 500GB min per node         │   │
│   │          Join: nodes 2+3 to cluster          │  │          Network: OOB + data VLANs          │   │
│   │           Configure: IP, NTP, DNS            │  │          NTP: synced before install         │   │
│   │          Install apps: NDFC/NDI/NDO          │  │          Cisco CCO: download images         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Bootstrap node 1 first; other nodes join via cluster join token; apps installed last                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Process                │  │           Post-Upgrade Validation           │   │
│   │            Backup: before upgrade            │  │         acs health: all nodes green         │   │
│   │           Upload image: UI or CLI            │  │             Apps: verify running            │   │
│   │         Rolling: one node at a time          │  │             Sites: all connected            │   │
│   │            Duration: ~45 min/node            │  │          Telemetry: flowing to NDI          │   │
│   │        Apps auto-upgrade post-cluster        │  │           Rollback: restore backup          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND nodes (UCS/VM) · management switch · NTP/DNS server · CCO download server                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA            = Open Virtualization Appliance; VMware VM image format for ND                        │
│  ISO            = Disk image for bare-metal ND node installation                                      │
│  Bootstrap      = First-node initialization creating the cluster with initial config                  │
│  Cluster join token= One-time secret additional nodes use to securely join cluster                    │
│  Rolling upgrade= ND upgrades one node at a time; cluster stays available throughout                  │
│  CCO            = Cisco Connection Online; software download portal                                   │
│  App auto-upgrade= After cluster upgrade, apps detect new platform and self-upgrade                   │
│  OOB VLAN       = Management VLAN on dedicated out-of-band network                                    │
│  Data VLAN      = In-band network VLAN used for site-to-ND app communication                          │
│  NTP pre-sync   = NTP must be configured and synced before cluster forms                              │
│  acs health     = Validates all nodes report green status after upgrade completes                     │
│  Rollback       = Only via backup restore; no in-place cluster downgrade supported                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Deploy two additional OVA nodes as per Step 1 above
# Configure their IPs but do not initialize them

# From the primary node, add the new nodes
acs cluster add-node --node-ip 10.10.5.24 --app-ip 192.168.100.4
acs cluster add-node --node-ip 10.10.5.25 --app-ip 192.168.100.5

# Monitor cluster expansion (takes 20-40 minutes)
acs health
acs nodes list
```
