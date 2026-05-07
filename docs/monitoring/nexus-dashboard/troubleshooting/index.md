# Nexus Dashboard: Troubleshooting Connectivity, Service Failures, and Upgrade Issues

This page covers common Nexus Dashboard operational problems: node connectivity failures, service application crashes, and issues encountered during software upgrades.

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
```

Node status reference:

| Status | Meaning | Action |
|---|---|---|
| Online | Node healthy and participating | None |
| Offline | Node unreachable | Check power, network, and reboot if needed |
| Decommissioned | Node removed from cluster | Expected if intentionally removed |
| Degraded | Node has service issues | Check `acs logs` on affected node |

## Diagnosing Service Application Failures

```bash
# List all services and their status
curl -sk -X GET \
  "https://nexus-dashboard.example.com/nexus/infra/api/v1/apps" \
  -H "Authorization: Bearer <token>" | jq '.data[] | {name, status, version}'

# Get detailed status for a specific service (e.g., NDI)
curl -sk -X GET \
  "https://nexus-dashboard.example.com/nexus/infra/api/v1/apps/ndi" \
  -H "Authorization: Bearer <token>" | jq '{status, healthStatus, errorMessage}'

# On the ND node: view service pod logs (Kubernetes-based)
# SSH to rescue-user, then check pods
kubectl get pods -n ndinsights
kubectl logs -n ndinsights <pod-name> --tail=100

# Restart a failing service pod
kubectl delete pod -n ndinsights <pod-name>
# Pod will be automatically recreated by the deployment controller
```

## Connectivity Issues Between ND and Fabrics

If NDI or NDO cannot reach the APIC/fabric:

```bash
# Test APIC reachability from ND node
ssh rescue-user@nexus-dashboard.example.com
curl -sk https://apic.example.com/api/aaaLogin.json \
  -d '{"aaaUser": {"attributes": {"name": "test", "pwd": "test"}}}' | jq '.imdata[0]'

# Check DNS resolution on ND node
nslookup apic.example.com

# Check NTP sync (critical for certificate validation and log timestamps)
timedatectl status
```

Network requirements for ND to fabric communication:

| Source | Destination | Port | Purpose |
|---|---|---|---|
| ND Management | APIC Management | 443 (HTTPS) | API communication |
| ND Data | Leaf switches | 5640 (UDP) | ERSPAN/telemetry |
| ND Management | NTP | 123 (UDP) | Time synchronisation |
| ND Management | DNS | 53 (UDP/TCP) | Name resolution |

## Upgrade Issues

Nexus Dashboard upgrades are managed via the Admin interface.

Navigation: **Admin > Software Management > Upgrade**

```bash
# Check current ND version
curl -sk -X GET \
  "https://nexus-dashboard.example.com/nexus/infra/api/v1/platform/version" \
  -H "Authorization: Bearer <token>" | jq '.version'

# Verify upgrade pre-checks pass before proceeding
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v1/platform/upgrade/precheck" \
  -H "Authorization: Bearer <token>" | jq '.checks[] | select(.status != "PASS")'
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
