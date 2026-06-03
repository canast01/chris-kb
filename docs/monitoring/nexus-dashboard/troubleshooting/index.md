# Nexus Dashboard: Troubleshooting Connectivity, Service Failures, and Upgrade Issues


<div class="kb-summary">
This page covers common Nexus Dashboard operational problems: node connectivity failures, service application crashes, and issues encountered during software upgrades.
</div>

## Checking Nexus Dashboard Cluster Health

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

Common upgrade failure points:

| Failure | Likely Cause | Fix |
|---|---|---|
| Pre-check fails: disk space | Less than 20 GB free | Clean logs, remove old app images |
| Pre-check fails: quorum lost | Node offline before upgrade | Bring node online before upgrading |
| Service app incompatible | App version not certified for new ND | Upgrade or downgrade app to compatible version first |
| Node stuck in "Upgrading" | Network interruption during image pull | Retry upgrade after verifying connectivity |
| Post-upgrade service offline | Service pod failed to restart | Check `kubectl get pods` and pod logs |

## Collecting a Support Bundle

```bash
# Generate a support bundle from the ND CLI
ssh rescue-user@nexus-dashboard.example.com
acs techsupport --node all

# Download the bundle (bundle saved to /data/techsupport/)
scp rescue-user@nexus-dashboard.example.com:/data/techsupport/nd-tech-support-*.tar.gz ./
```

## Common Troubleshooting Reference

| Problem | First Check | Second Check |
|---|---|---|
| ND UI not loading | `acs health` on node | Check load balancer VIP and port 443 |
| Fabric health score stuck | NDI service status | APIC API credentials valid |
| Alerts not generating | NDI telemetry receiving | Switch-level telemetry streaming enabled |
| NDO sync not completing | APIC version compatibility | Review NDO-APIC version compatibility matrix |
| Node offline after reboot | Management interface config | Verify CIMC/IPMI access and re-seat if physical |
