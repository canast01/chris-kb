# Nexus Dashboard — Troubleshooting (Monitoring)

```bash
# SSH to the Nexus Dashboard primary node
ssh rescue-user@nexus-dashboard.example.com

# Check cluster node status
acs health

# Check all services status
acs status

# View active alerts on the cluster
acs logs --type alert

# Check ND cluster node connectivity
acs nodes
```
```text
┌────────────────────────────────── Nexus Dashboard — Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Fabric Not Collecting             │  │                Cluster Issues               │   │
│   │            Check APIC credential             │  │               acs health check              │   │
│   │             Verify TCP 443 reach             │  │              acs cluster status             │   │
│   │             Check MDT gRPC 9339              │  │               Check disk space              │   │
│   │              Re-onboard fabric               │  │              acs logs download              │   │
│   │             Check NDI app status             │  │                Cisco TAC case               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ND admin CLI via SSH · acs health · acs logs download · gRPC from switch to ND data IP               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  acs health = Shows ACTIVE/STANDBY/FAILURE state of each ND master node                               │
│  acs cluster status = Quorum state and leader node identification                                     │
│  acs logs download = Creates log bundle for all apps; attach to Cisco TAC case                        │
│  APIC credential = NDI uses Observer role; re-enter if expired                                        │
│  TCP 443 reach = curl -k https://<apic>/api/class/fvTenant.json from ND data IP                       │
│  MDT gRPC 9339 = telnet <nd-data-ip> 9339 from switch to test streaming path                          │
│  Re-onboard = Remove and re-add fabric in ND; resets collection state                                 │
│  NDI app status = acs app status; NDI should show RUNNING                                             │
│  Disk space = df -h on ND master; 80% triggers cleanup of old telemetry                               │
│  kubectl logs = kubectl logs <pod> -n ndinsights for NDI container logs                               │
│  Cisco TAC = Open case at cisco.com/support; attach acs logs bundle                                   │
│  Epoch gap = NDI shows missing epochs when telemetry interrupted                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Generate a support bundle from the ND CLI
ssh rescue-user@nexus-dashboard.example.com
acs techsupport --node all

# Download the bundle (bundle saved to /data/techsupport/)
scp rescue-user@nexus-dashboard.example.com:/data/techsupport/nd-tech-support-*.tar.gz ./
```
